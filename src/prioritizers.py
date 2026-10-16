"""Ordenação completa dos testes; nenhuma estratégia recebe dados de defeitos."""

import random

STRATEGIES = ("original", "random", "fastest", "total", "additional", "cost_aware")


def prioritize(records, strategy, seed=0, trace=None):
    """Retorna (ordem, contadores).

    Se ``trace`` for uma função, ela recebe eventos gerados DURANTE a execução
    real do algoritmo. Isso permite demonstrar as escolhas sem reimplementar o
    algoritmo em demo.py. Sem callback, o comportamento é o mesmo de antes.
    """
    if strategy not in STRATEGIES:
        raise ValueError("estratégia desconhecida")

    ids = list(records)
    counts = {"score_evaluations": 0, "membership_checks": 0, "resets": 0}

    if strategy == "original":
        return ids, counts
    if strategy == "random":
        random.Random(seed).shuffle(ids)
        return ids, counts
    if strategy == "fastest":
        return sorted(ids, key=lambda i: (records[i]["cost_ns"], i)), counts
    if strategy == "total":
        return sorted(ids, key=lambda i: (-len(records[i]["coverage"]), i)), counts

    # As duas estratégias gulosas constroem a ordem uma escolha por vez.
    remaining = set(ids)
    universe = set().union(*(record["coverage"] for record in records.values()))
    unseen = universe.copy()
    order = []
    round_number = 0

    while remaining:
        round_number += 1

        def best(stage="normal"):
            scored = []
            candidates_for_trace = []

            # Não ordenamos remaining antes de pontuar: isso acrescentaria custo
            # desnecessário ao algoritmo. O identificador já desempata em min().
            for test_id in remaining:
                coverage = records[test_id]["coverage"]
                gain = sum(element in unseen for element in coverage)
                cost = records[test_id]["cost_ns"]
                score = gain / cost if strategy == "cost_aware" else gain

                counts["membership_checks"] += len(coverage)
                counts["score_evaluations"] += 1
                scored.append((-score, test_id, gain))
                candidates_for_trace.append({
                    "test": test_id,
                    "gain": gain,
                    "cost": cost,
                    "score": score,
                })

            if trace is not None:
                # A ordenação é apenas para apresentar a trilha em ordem legível;
                # só acontece quando a demonstração solicita rastreamento.
                candidates_for_trace.sort(key=lambda row: row["test"])
                trace({
                    "event": "scores",
                    "round": round_number,
                    "stage": stage,
                    "unseen": sorted(unseen),
                    "candidates": candidates_for_trace,
                })
            return min(scored)

        _, chosen, gain = best()

        # Se nenhum teste restante acrescenta cobertura, reiniciamos a referência
        # de cobertura para que os testes restantes também recebam uma ordem.
        if gain == 0 and unseen != universe:
            if trace is not None:
                trace({"event": "reset", "round": round_number})
            unseen = universe.copy()
            counts["resets"] += 1
            _, chosen, gain = best("after_reset")

        new_lines = records[chosen]["coverage"] & unseen
        order.append(chosen)
        remaining.remove(chosen)
        unseen.difference_update(records[chosen]["coverage"])

        if trace is not None:
            trace({
                "event": "chosen",
                "round": round_number,
                "test": chosen,
                "gain": gain,
                "new_lines": sorted(new_lines),
            })

    return order, counts
