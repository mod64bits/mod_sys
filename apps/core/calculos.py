import decimal

def valor_porcentagem(percentual, valor):
    _percentual = percentual / decimal.Decimal(100)
    aumento = decimal.Decimal(_percentual) * valor
    total = decimal.Decimal(valor + aumento)

    return {
        "aumento": aumento,
        "total": total,
    }

def desconto_avista(valor_bruto, desconto):
    valor_desconto = valor_bruto * desconto / 100
    valor_final = valor_bruto - valor_desconto

    return {
        "desconto": valor_desconto,
        "valor_final": valor_final,
    }