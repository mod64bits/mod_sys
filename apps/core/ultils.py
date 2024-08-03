from datetime import datetime as data_key
import datetime
import string
import random


def gerador_protocolo(ticket_id):
    _data = data_key.now()
    data = _data.strftime('%m%d%Y%H%M%S')
    id_t = ticket_id.hex
    protocolo = f"#{id_t[:5]}-{data}"

    return protocolo

class GeradorKeys:
    def __init__(self, user_id, cliente_id):
        self.user_id = user_id
        self.cliente_id = cliente_id
        self.data = data_key.now()

    def __key_ano_gerador(self):
        key = f"{self.data.strftime('%m%d%Y%H%M%S')}#{self.user_id}-{self.cliente_id}"

        return key

    def key(self):
        return self.__key_ano_gerador()



def gerar_protocolo():
    _data = data_key.now()
    chars = string.ascii_uppercase + string.digits
    protocolo = f"#{''.join(random.choice(chars) for _ in range(3))}-{_data.strftime('%Y-%m-%d-%H-%M:%S')}"
    return protocolo



class Datas:
    def __init__(self, data_inicial=datetime.date.today(), quantidade_dias=15):
        self.data_inicial = data_inicial
        self.quantidade_dias = quantidade_dias

    def vencimento(self):
        data = self.data_inicial + datetime.timedelta(days=self.quantidade_dias)
        print(f"Data:{data}")
        return self.verificar_fim_de_semana(data)

    def verificar_fim_de_semana(self, data_vencimento):
        dia = data_vencimento.weekday()
        if dia == 5:
            return data_vencimento + datetime.timedelta(days=2)
        if dia == 6:
            return data_vencimento + datetime.timedelta(days=1)
        return data_vencimento


def gerador_de_codigo(cliente):
    _cli = cliente.split()
    cli = [i[0].upper() for i in _cli]
    _codigo = ''.join([i[0].upper() for i in cli])
    codigo = _codigo + str(datetime.datetime.now())

    return codigo