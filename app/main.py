from decorators.base import PagamentoBase, PagamentoComponent
from decorators.bonus_qualidade import BonusQualidadeDecorator
from decorators.bonus_volume import BonusVolumeDecorator
from domain.models import Cooperado, Entrega, TipoMaterial
from factory.pagamento_factory import PagamentoFactory
from observers.notificadores import EmailNotifier, LogNotifier
from observers.subject import Cooperativa
from strategies.base import CalculadoraPagamento

def escolher_material() -> TipoMaterial:
    while True:
        print("Escolha o material:")
        print("1 - Papel")
        print("2 - Vidro")
        print("3 - Metal")
        print("4 - Plástico")
        opcao = input("Opção: ").strip()
        mapping = {
            "1": TipoMaterial.PAPEL,
            "2": TipoMaterial.VIDRO,
            "3": TipoMaterial.METAL,
            "4": TipoMaterial.PLASTICO,
        }
        if opcao in mapping:
            return mapping[opcao]
        print("Opção inválida, tente novamente.\n")

def main() -> None:
    cooperativa = Cooperativa()
    factory = PagamentoFactory()

    email_notifier = EmailNotifier()
    log_notifier = LogNotifier()
    cooperativa.adicionar_observer(email_notifier)
    cooperativa.adicionar_observer(log_notifier)

    # Para simplificar, 1 cooperado de demonstração
    cooperado = Cooperado(id=1, nome="Cooperado Demo", email="demo@coop.br")
    cooperativa.registrar_cooperado(cooperado)

    print("=== Sistema de Coleta Seletiva ===")

    while True:
        print("\nMenu:")
        print("1 - Registrar entrega")
        print("2 - Ver totais do cooperado")
        print("3 - Ver notificações de meta")
        print("0 - Sair")
        opcao = input("Opção: ").strip()

        if opcao == "1":
            material = escolher_material()
            peso = float(input("Peso em kg: ").replace(",", "."))
            limpo = input("Material limpo? (s/n): ").strip().lower().startswith("s")
            triagem = (
                input("Triagem correta? (s/n): ")
                .strip()
                .lower()
                .startswith("s")
            )

            entrega = Entrega(
                cooperado_id=cooperado.id,
                material=material,
                peso_kg=peso,
                limpo=limpo,
                triagem_correta=triagem,
            )

            strategy = factory.criar(entrega.material)
            calculadora = CalculadoraPagamento(strategy)
            valor_base = calculadora.calcular_pagamento(entrega.peso_kg)

            componente: PagamentoComponent = PagamentoBase(valor_base)
            componente = BonusVolumeDecorator(componente, peso_kg=entrega.peso_kg)
            componente = BonusQualidadeDecorator(
                componente,
                limpo=entrega.limpo,
                triagem_correta=entrega.triagem_correta,
            )
            valor_final = componente.calcular()

            cooperativa.registrar_pagamento(
                cooperado_id=entrega.cooperado_id,
                peso_kg=entrega.peso_kg,
                valor_pago=valor_final,
            )

            print(f"\nValor base........: R$ {valor_base:.2f}")
            print(f"Valor com bônus...: R$ {valor_final:.2f}")

        elif opcao == "2":
            coop = cooperativa.buscar_cooperado(cooperado.id)
            print(f"\nCooperado: {coop.nome}")
            print(f"Total de kg.......: {coop.total_kg:.2f}")
            print(f"Total de créditos.: R$ {coop.total_creditos:.2f}")
            print(f"Meta atingida?....: {'Sim' if coop.meta_atingida else 'Não'}")

        elif opcao == "3":
            print("\nNotificações simuladas (e-mail):")
            if not email_notifier.enviados:
                print("Nenhuma notificação ainda.")
            else:
                for msg in email_notifier.enviados:
                    print("-", msg)

        elif opcao == "0":
            print("\nDesenvolvido por: Vinícius Antonio Minas (@viniciusminas)")
            break
        else:
            print("Opção inválida, tente novamente.")


if __name__ == "__main__":
    main()
