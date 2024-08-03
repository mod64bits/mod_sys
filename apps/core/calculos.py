import decimal

def valor_porcentagem(percentual, valor):
    _percentual = percentual / decimal.Decimal(100)
    aumento = decimal.Decimal(_percentual) * valor
    total = decimal.Decimal(valor + aumento)

    return {
        "aumento": aumento,
        "total": total,
    }