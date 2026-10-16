"""Demonstração prática das seis estratégias.

Este exemplo usa quatro testes inventados e custos abstratos. Ele não reproduz
os resultados do artigo nem executa o experimento completo.

O código importante está em src/prioritizers.py e src/metrics.py. Execute este
arquivo para ver esses módulos trabalhando com uma entrada pequena.
Use --passo-a-passo para acompanhar as escolhas reais das duas heurísticas gulosas.
"""

import argparse

from src.metrics import evaluate
from src.prioritizers import STRATEGIES, prioritize

# Dados que o priorizador pode conhecer: linhas cobertas e duração.
# Os custos são unidades didáticas, não tempos medidos.
RECORDS = {
    "A": {"coverage": {1, 2, 3}, "cost_ns": 6},
    "B": {"coverage": {1, 2}, "cost_ns": 1},
    "C": {"coverage": {3, 4}, "cost_ns": 2},
    "D": {"coverage": {4}, "cost_ns": 1},
}

# A matriz de defeitos é usada SÓ DEPOIS de calcular todas as ordens.
DEMO_FAULTS = {
    "A": {"F1"},
    "B": set(),
    "C": {"F2"},
    "D": {"F3"},
}

NAMES = {
    "original": "Referência",
    "random": "Aleatória",
    "fastest": "Menor duração",
    "total": "Cobertura total",
    "additional": "Cobertura adicional",
    "cost_aware": "Adicional / custo",
}


def show_trace(event):
    """Mostra dados emitidos pelo algoritmo enquanto ele realmente executa."""
    kind = event["event"]

    if kind == "scores":
        stage = " (após reinício)" if event["stage"] == "after_reset" else ""
        unseen = ",".join(map(str, event["unseen"])) or "nenhuma"
        print(f"  Rodada {event['round']}{stage} | linhas ainda não vistas: {unseen}")
        for candidate in event["candidates"]:
            score = candidate["score"]
            score_text = f"{score:.2f}" if candidate["cost"] != 1 or score % 1 else f"{score:.0f}"
            print(
                f"    {candidate['test']}: ganho={candidate['gain']}, "
                f"custo={candidate['cost']}, pontuação={score_text}"
            )
    elif kind == "reset":
        print("  Sem ganho entre os testes restantes; o algoritmo reinicia a cobertura.")
    elif kind == "chosen":
        new_lines = ",".join(map(str, event["new_lines"])) or "nenhuma"
        print(f"  Escolhe {event['test']} | ganho={event['gain']} | linhas novas: {new_lines}")


def main():
    parser = argparse.ArgumentParser(description="Executa uma demonstração pequena de priorização.")
    parser.add_argument(
        "--passo-a-passo",
        action="store_true",
        help="exibe as pontuações calculadas em cada rodada das duas estratégias gulosas",
    )
    args = parser.parse_args()

    print("ENTRADA: teste | linhas cobertas | custo")
    for test_id, record in RECORDS.items():
        lines = ",".join(map(str, sorted(record["coverage"]))) or "—"
        print(f"  {test_id} | {{{lines}}} | {record['cost_ns']}")

    # Cada chamada abaixo executa o algoritmo real em src/prioritizers.py.
    orders = {}
    print("\nORDENS PRODUZIDAS")
    for strategy in STRATEGIES:
        order, _ = prioritize(RECORDS, strategy, seed=42)
        orders[strategy] = order
        print(f"  {NAMES[strategy]:20} {' -> '.join(order)}")

    # A demonstração detalhada chama o MESMO algoritmo com um callback de rastreamento.
    if args.passo_a_passo:
        for strategy in ("additional", "cost_aware"):
            title = NAMES[strategy].upper()
            print(f"\nPASSO A PASSO — {title}")
            traced_order, _ = prioritize(RECORDS, strategy, seed=42, trace=show_trace)
            assert traced_order == orders[strategy], "A ordem rastreada divergiu da execução normal."
            print(f"  Ordem final: {' -> '.join(traced_order)}")

    # Só aqui a demonstração consulta quais testes revelam quais defeitos.
    print("\nAVALIAÇÃO POSTERIOR (custos abstratos; não são resultados do artigo)")
    print(f"  {'Estratégia':20} {'APFD':>6} {'APFDc':>7} {'1º defeito':>12} {'Defeitos em 50%':>16}")
    for strategy in STRATEGIES:
        metrics = evaluate(orders[strategy], RECORDS, DEMO_FAULTS)
        print(
            f"  {NAMES[strategy]:20} {metrics['apfd']:6.3f} {metrics['apfdc']:7.3f} "
            f"{metrics['first_fault_ns']:12.1f} {metrics['faults_50']:15.2f}"
        )


if __name__ == "__main__":
    main()
