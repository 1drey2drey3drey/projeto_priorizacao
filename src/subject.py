"""MiniPedidos: componente experimental. Valores monetários em centavos."""


def discount(subtotal, member=False, coupon=""):
    if subtotal < 0:
        raise ValueError("subtotal negativo")
    if coupon not in ("", "PROMO10", "FIXO500"):
        raise ValueError("cupom inválido")
    member_discount = subtotal * 5 // 100 if member else 0
    base = subtotal - member_discount
    if coupon == "PROMO10" and base >= 10000:
        coupon_discount = base * 10 // 100
    elif coupon == "FIXO500":
        coupon_discount = min(base, 500)
    else:
        coupon_discount = 0
    return base - coupon_discount


def freight(subtotal, region, weight_kg, express=False):
    if region not in ("local", "regional", "remota") or weight_kg < 1:
        raise ValueError("entrega inválida")
    if subtotal >= 20000 and region == "local" and not express:
        return 0
    rates = {"local": 800, "regional": 1500, "remota": 3000}
    cost = rates[region] + max(0, weight_kg - 2) * 500
    if express:
        cost += 1200
    return cost


def reserve(quantity, stock):
    if quantity <= 0 or stock < 0:
        raise ValueError("quantidade inválida")
    if quantity > stock:
        raise ValueError("estoque insuficiente")
    return stock - quantity


def checkout(items, member=False, coupon="", region="local", express=False):
    if not items:
        raise ValueError("pedido vazio")
    subtotal = 0
    grams = 0
    remaining = 0
    for price, quantity, stock, weight in items:
        if price < 0 or weight <= 0:
            raise ValueError("item inválido")
        remaining += reserve(quantity, stock)
        subtotal += price * quantity
        grams += weight * quantity
    net = discount(subtotal, member, coupon)
    shipping = freight(net, region, (grams + 999) // 1000, express)
    return net + shipping, subtotal, subtotal - net, shipping, remaining
