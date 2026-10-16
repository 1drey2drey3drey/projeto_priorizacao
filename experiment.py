"""Executa coleta real e simulação de ordens: python experiment.py."""
import argparse
import csv
import gc
import hashlib
import json
import os
from pathlib import Path
import platform
import random
import statistics
import sys
import time
import tracemalloc
import types

from src import subject
from src.cases import generate,passes
from src.mutations import MUTATIONS
from src.prioritizers import prioritize,STRATEGIES
from src.metrics import evaluate

ROOT=Path(__file__).resolve().parent


def save_json(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding="utf-8")


def save_csv(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("w",newline="",encoding="utf-8") as stream:
        writer=csv.DictWriter(stream,fieldnames=list(rows[0]))
        writer.writeheader();writer.writerows(rows)


def collect(cases,repetitions=10,batch=50):
    records={};timings=[]
    filename=str(Path(subject.__file__).resolve())
    for case in cases:
        assert passes(subject,case),case["id"]
        lines=set()
        def trace(frame,event,arg):
            if frame.f_code.co_filename==filename:
                if event=="line": lines.add(frame.f_lineno)
                return trace
        sys.settrace(trace)
        try: assert passes(subject,case)
        finally: sys.settrace(None)
        records[case["id"]]={"coverage":lines,"cost_ns":0}
    # A ordem muda entre blocos de medição, sem tracing e com aquecimento.
    for case in cases:
        for _ in range(5): passes(subject,case)
    samples={c["id"]:[] for c in cases}
    for rep in range(repetitions):
        order=list(cases);random.Random(7000+rep).shuffle(order)
        for case in order:
            start=time.perf_counter_ns()
            for _ in range(batch): passes(subject,case)
            ns=(time.perf_counter_ns()-start)/batch
            samples[case["id"]].append(ns)
            timings.append({"test_id":case["id"],"rep":rep,"batch":batch,"ns_per_test":ns})
    for i,r in records.items(): r["cost_ns"]=statistics.median(samples[i])
    return records,timings


def fault_catalog(cases):
    source=Path(subject.__file__).read_text(encoding="utf-8")
    kills={c["id"]:set() for c in cases}
    catalog=[]
    for fid,description,old,new in MUTATIONS:
        assert source.count(old)==1,(fid,"patch não único")
        mutated=source.replace(old,new)
        module=types.ModuleType(fid)
        exec(compile(mutated,f"mutants/{fid}.py","exec"),module.__dict__)
        detected=[c["id"] for c in cases if not passes(module,c)]
        for i in detected: kills[i].add(fid)
        catalog.append({"id":fid,"description":description,"old":old,"new":new,
                        "detecting_tests":len(detected),"sha256":hashlib.sha256(mutated.encode()).hexdigest()})
        assert detected,(fid,"defeito não detectável; revisar catálogo")
    return kills,catalog


def execute(sizes=(20,40,80,160,320),repetitions=10,batch=50):
    started=time.perf_counter()
    cases=generate()
    records,timings=collect(cases,repetitions,batch)
    kills,catalog=fault_catalog(cases)
    results=[];orders=[]
    for rep in range(repetitions):
        shuffled=list(records);random.Random(8000+rep).shuffle(shuffled)
        for n in sizes:
            if n>len(cases): raise ValueError("tamanho excede suíte")
            selected=set(shuffled[:n])
            # Mantém a ordem de referência fixa no subconjunto.
            local={i:r for i,r in records.items() if i in selected}
            for strategy in STRATEGIES:
                elapsed=[]
                for _ in range(3):
                    start=time.perf_counter_ns()
                    order,ops=prioritize(local,strategy,9000+rep)
                    elapsed.append(time.perf_counter_ns()-start)
                assert sorted(order)==sorted(local)
                overhead=statistics.median(elapsed)
                tracemalloc.start()
                prioritize(local,strategy,9000+rep)
                _,peak=tracemalloc.get_traced_memory();tracemalloc.stop()
                metric=evaluate(order,local,kills,overhead)
                results.append({"n":n,"rep":rep,"seed_sample":8000+rep,"seed_order":9000+rep,
                                "strategy":strategy,"prioritization_ns":overhead,
                                "peak_aux_bytes":peak,**ops,**metric})
                orders.append({"n":n,"rep":rep,"strategy":strategy,"order":order})
    save_json(ROOT/"data/cases.json",cases)
    save_json(ROOT/"data/coverage_costs.json",{i:{**r,"coverage":sorted(r["coverage"])} for i,r in records.items()})
    save_json(ROOT/"data/fault_catalog.json",catalog)
    save_json(ROOT/"data/fault_matrix.json",{i:sorted(v) for i,v in kills.items()})
    save_csv(ROOT/"data/timing_samples.csv",timings)
    save_csv(ROOT/"results/raw_results.csv",results)
    save_json(ROOT/"results/orders.json",orders)
    cpu="não informado"
    if Path("/proc/cpuinfo").exists():
        lines=Path("/proc/cpuinfo").read_text().splitlines()
        cpu=next((s.split(":",1)[1].strip() for s in lines if s.startswith("model name")),cpu)
    env={"python":sys.version,"platform":platform.platform(),"cpu":cpu,"logical_cpus":os.cpu_count(),
         "clock":vars(time.get_clock_info("perf_counter")),"sizes":list(sizes),"repetitions":repetitions,
         "cost_batch":batch,"cost_repetitions":repetitions,"prioritizer_inner_repeats":3,
         "suite_cases":len(cases),"faults":len(catalog),"covered_lines":len(set().union(*(r["coverage"] for r in records.values()))),
         "date_utc":time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime()),
         "elapsed_seconds":time.perf_counter()-started,"source_sha256":hashlib.sha256(Path(subject.__file__).read_bytes()).hexdigest(),
         "semantics":"Baseline coverage and costs measured; fault matrix obtained by real executions; order metrics simulated with additive baseline median costs; no CI/process startup/I-O modeled."}
    save_json(ROOT/"results/environment.json",env)
    print(json.dumps({"rows":len(results),**env},ensure_ascii=False,indent=2))


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--repetitions",type=int,default=10)
    parser.add_argument("--batch",type=int,default=50)
    args=parser.parse_args()
    execute(repetitions=args.repetitions,batch=args.batch)
