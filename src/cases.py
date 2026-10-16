"""Casos determinísticos e oráculos derivados da especificação, sem executar o SUT."""
import itertools
import random


def expected_discount(s, member, coupon):
    if s < 0 or coupon not in {"", "PROMO10", "FIXO500"}:
        return {"error": "ValueError"}
    base = s - (s // 20 if member else 0)
    deductions = {"": 0, "FIXO500": min(base, 500),
                  "PROMO10": (base // 10) * int(base >= 10000)}
    return base - deductions[coupon]


def expected_freight(s, region, weight, express):
    if region not in {"local", "regional", "remota"} or weight < 1:
        return {"error": "ValueError"}
    base = dict(zip(("local", "regional", "remota"), (800, 1500, 3000)))[region]
    full = base + 500 * max(weight - 2, 0) + 1200 * int(express)
    return full * (1 - int(s >= 20000 and region == "local" and not express))


def expected_reserve(q, stock):
    return stock - q if 0 < q <= stock else {"error": "ValueError"}


def expected_checkout(items, member, coupon, region, express):
    if not items or any(p < 0 or w <= 0 or q <= 0 or q > s for p,q,s,w in items):
        return {"error": "ValueError"}
    gross = sum(p*q for p,q,s,w in items)
    net = expected_discount(gross, member, coupon)
    if isinstance(net, dict):
        return net
    weight = -(-sum(q*w for p,q,s,w in items) // 1000)
    ship = expected_freight(net, region, weight, express)
    if isinstance(ship, dict):
        return {"error": "ValueError"}
    return [net+ship, gross, gross-net, ship, sum(s-q for p,q,s,w in items)]


def generate(seed=20261015):
    cases = []
    def add(fn,args,expected):
        cases.append({"id":f"T{len(cases)+1:04d}","function":fn,
                      "args":args,"expected":expected})
    for s,member,coupon in itertools.product(
            [-1,0,1,499,500,501,9999,10000,10001,10526,10527,19999,20000,20001,50000],
            [False,True],["","PROMO10","FIXO500","INVALIDO"]):
        add("discount",[s,member,coupon],expected_discount(s,member,coupon))
    for s,region,w,express in itertools.product(
            [0,19999,20000,20001],["local","regional","remota","invalida"],
            [0,1,2,3,20],[False,True]):
        add("freight",[s,region,w,express],expected_freight(s,region,w,express))
    for q,stock in itertools.product([-1,0,1,2,10,11,50],[-1,0,1,2,10,50]):
        add("reserve",[q,stock],expected_reserve(q,stock))
    rng = random.Random(seed)
    for k in range(240):
        length = [1,4,16,64,256][k % 5]
        items = [[rng.choice([0,199,500,1000,9999,20000]),rng.randint(1,4),10,
                  rng.choice([1,200,500,1000,1001])] for _ in range(length)]
        member,coupon,region,express = (bool(k%2),["","PROMO10","FIXO500"][k%3],
                                      ["local","regional","remota"][(k//3)%3],bool((k//9)%2))
        args=[items,member,coupon,region,express]
        add("checkout",args,expected_checkout(*args))
    for items in [[], [[-1,1,1,1]], [[1,1,1,0]], [[1,0,1,1]], [[1,2,1,1]]]:
        args=[items,False,"","local",False]
        add("checkout",args,expected_checkout(*args))
    # Ordem de referência arbitrária, fixada antes dos experimentos.
    rng.shuffle(cases)
    return cases


def outcome(module, case):
    try:
        result = getattr(module,case["function"])(*case["args"])
        return list(result) if isinstance(result,tuple) else result
    except Exception as exc:
        return {"error":type(exc).__name__}


def passes(module,case):
    return outcome(module,case) == case["expected"]
