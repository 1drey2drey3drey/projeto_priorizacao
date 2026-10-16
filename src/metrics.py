"""Métricas sobre falhas detectáveis pela instância; severidade uniforme."""


def evaluate(order,records,kills,overhead_ns=0):
    detectable=set().union(*(kills[i] for i in order))
    total=sum(records[i]["cost_ns"] for i in order)
    if not order or not detectable:
        raise ValueError("APFD exige suíte e conjunto detectável não vazios")
    positions,completion,midpoints={},{},{}
    elapsed=0
    coverage=set()
    allcov=set().union(*(records[i]["coverage"] for i in order))
    checkpoints={f"faults_{int(b*100)}":0 for b in [.1,.25,.5,.75]}
    seen=set()
    for pos,i in enumerate(order,1):
        cost=records[i]["cost_ns"]
        for fault in kills[i]-seen:
            positions[fault]=pos
            completion[fault]=elapsed+cost
            midpoints[fault]=elapsed+cost/2
        elapsed += cost
        seen |= kills[i]
        for b in [.1,.25,.5,.75]:
            if elapsed <= total*b:
                checkpoints[f"faults_{int(b*100)}"]=len(seen)/len(detectable)
        if elapsed <= total*.25: coverage |= records[i]["coverage"]
    n,m=len(order),len(detectable)
    return {
        "detectable_faults":m,"suite_ns":total,
        "apfd":1-sum(positions.values())/(n*m)+1/(2*n),
        "apfdc":1-sum(midpoints.values())/(m*total),
        "auc_completion":1-sum(completion.values())/(m*total),
        "first_fault_ns":min(completion.values()),
        "first_fault_with_overhead_ns":overhead_ns+min(completion.values()),
        "coverage_25":len(coverage)/len(allcov) if allcov else 0,
        **checkpoints,
    }
