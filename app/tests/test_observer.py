from domain.models import Cooperado
from infra.config import Config
from observers.notificadores import EmailNotifier, LogNotifier
from observers.subject import Cooperativa

def test_multiplos_observers_notificados_quando_meta_atingida():
    # garante meta conhecida para este teste
    Config.instance().meta_kg_mensal = 100.0

    cooperativa = Cooperativa()
    email = EmailNotifier()
    log = LogNotifier()
    cooperativa.adicionar_observer(email)
    cooperativa.adicionar_observer(log)

    cooperado = Cooperado(id=1, nome="Maria")
    cooperativa.registrar_cooperado(cooperado)

    cooperativa.registrar_pagamento(cooperado.id, peso_kg=120.0, valor_pago=100.0)

    assert len(email.enviados) == 1
    assert len(log.registros) == 1
    assert cooperado.meta_atingida


def test_meta_notificada_apenas_uma_vez():
    # garante meta conhecida para este teste
    Config.instance().meta_kg_mensal = 100.0

    cooperativa = Cooperativa()
    email = EmailNotifier()
    cooperativa.adicionar_observer(email)

    cooperado = Cooperado(id=1, nome="João")
    cooperativa.registrar_cooperado(cooperado)

    cooperativa.registrar_pagamento(cooperado.id, peso_kg=80.0, valor_pago=50.0)
    cooperativa.registrar_pagamento(cooperado.id, peso_kg=30.0, valor_pago=40.0)

    assert len(email.enviados) == 1
