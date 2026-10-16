"""Resumo e gráficos a partir dos CSV existentes; não refaz medições."""
import csv
import json
import statistics
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parent
NAMES={"original":"Original","random":"Aleatória","fastest":"Menor duração",
       "total":"Cobertura total","additional":"Adicional","cost_aware":"Adicional/custo"}
COLORS=["#6b7280","#c084fc","#d97706","#0284c7","#15803d","#b91c1c"]


def main():
    with (ROOT/"results/raw_results.csv").open() as f:
        rows=[{k:(v if k=="strategy" else float(v)) for k,v in row.items()} for row in csv.DictReader(f)]
    sizes=sorted({int(r["n"]) for r in rows})
    summaries=[]
    for n in sizes:
        for strategy in NAMES:
            group=[r for r in rows if r["n"]==n and r["strategy"]==strategy]
            out={"n":n,"strategy":strategy,"count":len(group)}
            for metric in ["apfd","apfdc","auc_completion","prioritization_ns","peak_aux_bytes",
                           "first_fault_ns","first_fault_with_overhead_ns","faults_25","faults_50",
                           "coverage_25","score_evaluations","membership_checks","detectable_faults","suite_ns"]:
                values=[r[metric] for r in group]
                out[metric+"_mean"]=statistics.mean(values)
                out[metric+"_median"]=statistics.median(values)
                out[metric+"_sd"]=statistics.stdev(values)
            summaries.append(out)
    with (ROOT/"results/summary.csv").open("w",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=list(summaries[0]));writer.writeheader();writer.writerows(summaries)
    fits=[]
    for strategy in NAMES:
        data=[r for r in summaries if r["strategy"]==strategy]
        x=np.log([r["n"] for r in data]);y=np.log([r["prioritization_ns_median"] for r in data])
        slope,intercept=np.polyfit(x,y,1);pred=slope*x+intercept
        denom=np.sum((y-y.mean())**2)
        fits.append({"strategy":strategy,"loglog_exponent":float(slope),
                     "r2_loglog":float(1-np.sum((y-pred)**2)/denom) if denom else None})
    (ROOT/"results/fits.json").write_text(json.dumps(fits,indent=2),encoding="utf-8")
    plt.rcParams.update({"font.family":"DejaVu Sans","font.size":10,"axes.spines.top":False,"axes.spines.right":False})
    for metric,label,file,scale in [
        ("prioritization_ns","Tempo de priorização (ms)","tempo_priorizacao",1e6),
        ("membership_checks","Verificações de pertinência","operacoes",1),
        ("apfdc","APFDc (maior é melhor)","apfdc",1),
        ("first_fault_with_overhead_ns","Primeira falha + priorização (ms)","feedback_total",1e6)]:
        fig,ax=plt.subplots(figsize=(7.4,4.0))
        for (strategy,name),color in zip(NAMES.items(),COLORS):
            data=[r for r in summaries if r["strategy"]==strategy]
            if metric=="membership_checks" and strategy not in ["additional","cost_aware"]:continue
            if metric == "apfdc":
                ax.errorbar(sizes,[r[metric+"_mean"] for r in data],
                            yerr=[r[metric+"_sd"] for r in data],
                            marker="o",capsize=3,label=name,color=color)
            else:
                ax.plot(sizes,[r[metric+"_median"]/scale for r in data],marker="o",label=name,color=color)
        if metric == "membership_checks":
            start=next(r["membership_checks_median"] for r in summaries if r["n"]==sizes[0] and r["strategy"]=="additional")
            ax.plot(sizes,[start*(n/sizes[0])**2 for n in sizes],linestyle="--",color="#333333",label="Referência n²")
        if metric in ["prioritization_ns","first_fault_with_overhead_ns"]:
            ax.set_yscale("log")
        ax.set_xlabel("Número de testes n");ax.set_ylabel(label);ax.grid(alpha=.2)
        ax.legend(ncols=3,fontsize=8,loc="upper center",bbox_to_anchor=(.5,1.25),frameon=False)
        fig.tight_layout();fig.savefig(ROOT/f"figures/{file}.png",dpi=180);fig.savefig(ROOT/f"figures/{file}.pdf");plt.close(fig)
    selected=[r for r in summaries if r["n"]==max(sizes)]
    fig,ax=plt.subplots(figsize=(7.4,4.2))
    x=np.arange(len(selected));ax.bar(x,[r["faults_25_mean"] for r in selected],color=COLORS)
    ax.set_xticks(x,[NAMES[r["strategy"]] for r in selected],rotation=15,ha="right")
    ax.set_ylabel("Fração das falhas detectáveis revelada");ax.set_ylim(0,1.05)
    ax.set_title("Falhas até 25% do tempo da suíte (n = 320)",fontsize=11)
    fig.tight_layout();fig.savefig(ROOT/"figures/falhas_orcamento.png",dpi=180);plt.close(fig)
    report={"n_max":max(sizes),"summary_max":selected,"fits":fits}
    (ROOT/"results/report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
    for r in selected:
        print(r["strategy"],"APFDc",round(r["apfdc_mean"],4),"prior_ms",round(r["prioritization_ns_median"]/1e6,4),
              "first_us",round(r["first_fault_ns_median"]/1000,2),"net_ms",round(r["first_fault_with_overhead_ns_median"]/1e6,4))


if __name__=="__main__":main()
