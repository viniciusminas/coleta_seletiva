from domain.models import TipoMaterial
from factory.pagamento_factory import PagamentoFactory
from infra.config import Config
from strategies.materiais import PagamentoPapel


def test_singleton_config_tem_unica_instancia():
    c1 = Config.instance()
    c2 = Config.instance()

    assert c1 is c2

    c1.meta_kg_mensal = 200.0
    assert c2.meta_kg_mensal == 200.0


def test_factory_cria_strategy_adequada_para_material():
    factory = PagamentoFactory()
    strategy = factory.criar(TipoMaterial.PAPEL)

    assert isinstance(strategy, PagamentoPapel)
