from decorators.base import PagamentoBase
from decorators.bonus_qualidade import BonusQualidadeDecorator
from decorators.bonus_volume import BonusVolumeDecorator


def test_composicao_de_decorators_aplica_bonuses_sobre_valor_base():
    base = PagamentoBase(100.0)

    com_volume = BonusVolumeDecorator(base, peso_kg=60.0)  # +10%
    com_qualidade = BonusQualidadeDecorator(base, limpo=True, triagem_correta=True)  # +10%

    com_todos = BonusQualidadeDecorator(
        BonusVolumeDecorator(base, peso_kg=60.0),
        limpo=True,
        triagem_correta=True,
    )

    assert base.calcular() == 100.0
    assert round(com_volume.calcular(), 2) == 110.0
    assert round(com_qualidade.calcular(), 2) == 110.0
    assert round(com_todos.calcular(), 2) > round(com_volume.calcular(), 2)
    assert round(com_todos.calcular(), 2) > round(com_qualidade.calcular(), 2)
