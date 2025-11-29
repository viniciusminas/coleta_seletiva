from domain.models import TipoMaterial
from factory.pagamento_factory import PagamentoFactory
from strategies.base import CalculadoraPagamento


def test_troca_de_strategy_muda_resultado():
    factory = PagamentoFactory()

    calculadora = CalculadoraPagamento(factory.criar(TipoMaterial.PAPEL))
    valor_papel = calculadora.calcular_pagamento(10.0)

    calculadora.trocar_strategy(factory.criar(TipoMaterial.METAL))
    valor_metal = calculadora.calcular_pagamento(10.0)

    assert valor_papel != valor_metal
    assert valor_metal > valor_papel  # metal vale mais que papel
