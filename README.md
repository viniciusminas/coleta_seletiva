# Coleta Seletiva – Design Patterns com OO

Trabalho 04 - Design Patterns  
Disciplina: Linguagem de Programação e Paradigmas  
Professor: Ademar Perfoll Junior  

Trabalho desenvolvido individualmente por:

- Vinícius Antonio Minas (@viniciusminas)

---

## 1. Problema / Domínio

O projeto modela uma cooperativa de coleta seletiva que recebe materiais recicláveis de cooperados e realiza o pagamento com base no peso entregue. Cada entrega informa:

- tipo de material (papel, vidro, metal, plástico);
- peso em quilogramas;
- condição do material (limpo ou não, triagem correta ou não).

A cooperativa:

- paga valores diferentes por quilograma conforme o material;
- aplica bonificações por qualidade da entrega e por volume;
- acompanha uma meta mensal de quilogramas por cooperado;
- notifica quando a meta é atingida.

O objetivo é representar esse cenário usando padrões de projeto clássicos (GoF), com código orientado a objetos, testes automatizados e um menu de console para simular o uso.

---

## 2. Linguagem utilizada e justificativa

A linguagem escolhida foi **Python 3**, pelos seguintes motivos:

- suporte adequado a orientação a objetos (classes, herança, composição);
- sintaxe concisa, que facilita focar na modelagem dos padrões sem excesso de código boilerplate;
- ecossistema de testes maduro, em especial o `pytest`, que torna simples criar e executar testes unitários;
- fácil execução em diferentes ambientes (Windows, Linux, WSL), o que colabora para correções e avaliação do trabalho.

---

## 3. Arquitetura e organização do projeto

A estrutura de pastas segue a orientação do enunciado:

```text
app/
  main.py           # CLI / menu principal
  README.md
  domain/
    models.py      # Entidades de domínio: Cooperado, Entrega, TipoMaterial
    events.py      # EventoColeta usado pelo Observer
  strategies/
    base.py        # PagamentoStrategy e CalculadoraPagamento (Context)
    materiais.py   # Implementações de Strategy por material
  decorators/
    base.py        # PagamentoComponent, PagamentoBase, PagamentoDecorator
    bonus_volume.py
    bonus_qualidade.py
  observers/
    base.py        # Observer e Subject
    subject.py     # Cooperativa (Subject concreto)
    notificadores.py
  factory/
    pagamento_factory.py  # Factory Method para criar Strategy
  infra/
    config.py      # Singleton com tabela de preços e meta
  tests/
    test_strategy.py
    test_decorator.py
    test_observer.py
    test_factory_singleton.py
```

As principais regras de negócio ficam em `domain/`, enquanto cada padrão tem sua própria pasta (`strategies/`, `decorators/`, `observers/`, `factory/`, `infra/`). O arquivo `main.py` expõe um menu simples para exercitar o domínio e os padrões.

---

## 4. Padrões de projeto implementados

Foram implementados cinco padrões:

1. Strategy  
2. Decorator  
3. Observer  
4. Singleton  
5. Factory Method  

A seguir, a justificativa de cada padrão, relacionando o problema do domínio, a escolha do padrão e como ele resolve o problema.

### 4.1 Strategy – cálculo de pagamento por material

**Localização no código**

- Interface e contexto:
  - `strategies/base.py` – `PagamentoStrategy`, `CalculadoraPagamento`
- Implementações concretas:
  - `strategies/materiais.py` – `PagamentoPorMaterial`, `PagamentoPapel`, `PagamentoVidro`, `PagamentoMetal`, `PagamentoPlastico`
- Criação das strategies:
  - `factory/pagamento_factory.py` – `PagamentoFactory.criar`

**Problema do domínio**

Cada material (papel, vidro, metal, plástico) tem um valor diferente por quilograma. A cooperativa pode, no futuro, alterar a política de preços ou adicionar novos materiais. Não é desejável espalhar `if`/`elif` de tipo por todo o código.

**Por que Strategy**

Strategy permite encapsular diferentes algoritmos de cálculo de pagamento por quilograma atrás de uma interface única (`PagamentoStrategy`). O contexto (`CalculadoraPagamento`) usa essa interface sem conhecer detalhes de cada cálculo.

**Como resolve**

- O menu cria uma `PagamentoStrategy` apropriada via `PagamentoFactory` com base no material da entrega.
- A `CalculadoraPagamento` delega o cálculo do valor base da entrega para a strategy atual.
- É possível trocar a strategy em tempo de execução (`trocar_strategy`), como demonstrado em `test_strategy.py`, onde a troca de `PAPEL` para `METAL` muda o valor calculado.

---

### 4.2 Decorator – bônus por volume e qualidade

**Localização no código**

- Componente base e decorator:
  - `decorators/base.py` – `PagamentoComponent`, `PagamentoBase`, `PagamentoDecorator`
- Decorators concretos:
  - `decorators/bonus_volume.py` – `BonusVolumeDecorator`
  - `decorators/bonus_qualidade.py` – `BonusQualidadeDecorator`

**Problema do domínio**

Além do valor base por kg, a cooperativa concede bonificações:

- bônus progressivo para grandes volumes na mesma entrega (por exemplo, acima de 50 kg, acima de 100 kg);
- bônus por qualidade (material limpo e triagem correta).

Esses bônus podem ser combinados, e novas “camadas” de ajuste de valor podem surgir no futuro.

**Por que Decorator**

Decorator permite adicionar comportamentos extras a um objeto de forma flexível, empilhando decoradores em torno de um componente base, sem modificar sua classe. Isso encaixa bem na ideia de aplicar bônus em camadas sobre um mesmo valor base.

**Como resolve**

- A `PagamentoBase` guarda o valor base calculado pela Strategy.
- `BonusVolumeDecorator` aplica um multiplicador dependendo do peso da entrega.
- `BonusQualidadeDecorator` aplica um bônus percentual conforme o material esteja limpo e corretamente triado.
- Em `main.py`, o valor final é calculado encadeando os decorators:
  - `PagamentoBase` → `BonusVolumeDecorator` → `BonusQualidadeDecorator`.
- O teste `test_decorator.py` demonstra que:
  - o valor com apenas volume difere do valor com apenas qualidade;
  - a composição de ambos os decorators resulta em um valor ainda maior, mostrando o empilhamento típico do padrão.

---

### 4.3 Observer – notificação ao atingir a meta do cooperado

**Localização no código**

- Interfaces base:
  - `observers/base.py` – `Observer`, `Subject`
- Subject concreto:
  - `observers/subject.py` – `Cooperativa`
- Observers concretos:
  - `observers/notificadores.py` – `EmailNotifier`, `LogNotifier`
- Evento de domínio:
  - `domain/events.py` – `EventoColeta`

**Problema do domínio**

A cooperativa quer acompanhar o total de quilogramas entregues por cada cooperado e disparar notificações quando a meta mensal for atingida. Podem existir diferentes “interessados” nesse evento (por exemplo, um sistema de e-mail, um logger para auditoria, futuras integrações).

**Por que Observer**

Observer permite que múltiplos objetos observem eventos emitidos por um Subject sem acoplamento direto entre eles. O Subject não precisa saber quantos observers existem nem o que fazem com os dados.

**Como resolve**

- `Cooperativa` mantém um dicionário de `Cooperado` e acumula:
  - `total_kg`
  - `total_creditos`.
- Ao registrar um pagamento (`registrar_pagamento`), a cooperativa verifica se o cooperado atingiu a meta definida em `Config.meta_kg_mensal`.
- Quando a meta é atingida pela primeira vez, é criado um `EventoColeta` do tipo `"META_ATINGIDA"` e o método `notificar` do `Subject` chama todos os observers inscritos.
- `EmailNotifier` simula o envio de e-mail, guardando as mensagens em `enviados`.
- `LogNotifier` guarda registros em `registros` para simular um log.
- O arquivo `test_observer.py` comprova:
  - que múltiplos observers recebem o evento quando a meta é atingida;
  - que a meta não dispara múltiplas vezes para o mesmo cooperado.

---

### 4.4 Singleton – configuração de preços e meta

**Localização no código**

- `infra/config.py` – `Config`

**Problema do domínio**

A aplicação precisa de parâmetros globais de negócio:

- preços por quilograma de cada material;
- meta mensal de quilogramas por cooperado.

Essas informações devem ser consistentes em todo o sistema, com um ponto único de atualização.

**Por que Singleton**

Singleton garante que exista uma única instância de `Config` em todo o sistema, centralizando a leitura e atualização de parâmetros.

**Como resolve**

- `Config` define um atributo de classe `_instance` e controla a criação de instâncias no método `__new__`.
- O método de classe `Config.instance()` é a única forma de obter a instância.
- A tabela de preços e a meta são iniciadas em `_init_defaults`.
- `strategies/materiais.py` e `observers/subject.py` usam `Config.instance()` para acessar preços e meta.
- O teste `test_singleton_config_tem_unica_instancia` confirma que duas chamadas a `Config.instance()` retornam o mesmo objeto e compartilham o estado.

---

### 4.5 Factory Method – criação de estratégias de pagamento

**Localização no código**

- `factory/pagamento_factory.py` – `PagamentoFactory`

**Problema do domínio**

O menu da aplicação não deve conhecer a lógica de instanciar cada Strategy concreta. Além disso, a inclusão de novos materiais no futuro não deveria exigir modificações espalhadas no código.

**Por que Factory Method**

Factory Method encapsula a criação de objetos em uma classe dedicada, devolvendo a interface (`PagamentoStrategy`) apropriada conforme o tipo solicitado.

**Como resolve**

- `PagamentoFactory.criar(material: TipoMaterial)` retorna uma instância da Strategy concreta correta:
  - `PagamentoPapel`
  - `PagamentoVidro`
  - `PagamentoMetal`
  - `PagamentoPlastico`
- `main.py` delega para a factory a criação da strategy, evitando condicionais repetidas no código da interface.
- O teste `test_factory_cria_strategy_adequada_para_material` garante que, ao pedir uma strategy para `TipoMaterial.PAPEL`, a factory devolve um `PagamentoPapel`.

---

## 6. Como executar a aplicação

Pré-requisitos:

- Python 3.12 ou versão compatível instalada;
- opcionalmente, um ambiente virtual (`venv`).

Passos sugeridos:

1. Clonar ou baixar o repositório.
2. Abrir o terminal na pasta `coleta-seletiva/app`.
3. Executar o menu:

   ```bash
   python main.py
   ```

O menu permite:

- registrar entregas para o cooperado de demonstração;
- visualizar totais de quilogramas e créditos do cooperado;
- visualizar notificações simuladas de meta atingida;
- sair da aplicação.

Ao escolher a opção “0 - Sair”, o sistema exibe o rodapé:

```text
Desenvolvido por: Vinícius Antonio Minas (@viniciusminas)
```

---

## 7. Como executar os testes automatizados

Na pasta `coleta-seletiva/app`, executar:

```bash
python -m pytest
```

Os testes cobrem:

- `test_strategy.py`: troca dinâmica de Strategy altera o resultado, principalmente quando se muda de papel para metal.
- `test_decorator.py`: composição de decorators (volume e qualidade) aplicando bônus sobre o mesmo valor base.
- `test_observer.py`: notificação de múltiplos observers quando a meta é atingida e garantia de que o evento dispara apenas uma vez por cooperado.
- `test_factory_singleton.py`: unicidade da instância de `Config` (Singleton) e criação correta de Strategies pela `PagamentoFactory`.

---

## 8. Decisões de design

- Centralização de parâmetros em `Config` (Singleton): preços por kg e meta mensal são lidos de um único ponto, facilitando ajustes e testes.
- Uso combinado de Factory Method e Strategy: o cálculo de pagamento é parametrizado por Strategy, e a factory encapsula a forma de construir a estratégia correta com base no material.
- Aplicação de Decorator apenas sobre o valor base: o valor calculado pela Strategy é a base sobre a qual os decorators aplicam bonificações, evitando misturar regras de valor com regras de bônus.
- Subject voltado ao cooperado (`Cooperativa`): a classe `Cooperativa` é responsável por acumular o estado do cooperado e disparar o evento de meta atingida, mantendo o Observer focado em notificações.
- Dados em memória: todas as entidades são mantidas em memória e criadas a partir da interface de console, simplificando o escopo do trabalho.
- Comentários no código: foram adicionadas docstrings e comentários pontuais explicando o papel de cada classe e os comportamentos principais, para facilitar leitura e correção.

---

## 9. Limitações e próximos passos

Limitações conhecidas:

- não há persistência em banco de dados; ao encerrar o programa, os dados são perdidos;
- o cooperado de demonstração é fixo (id 1); não há cadastro de múltiplos cooperados via interface;
- a meta mensal é global para todos os cooperados (e não individual);
- a simulação de envio de e-mail é apenas em memória, sem integração com serviços externos.

Possíveis extensões futuras:

- permitir o cadastro de múltiplos cooperados e seleção de cooperado no menu;
- persistir dados em arquivo ou banco de dados;
- separar menu e regras de negócio usando camadas adicionais (por exemplo, uma camada de serviço ou aplicação);
- diferenciar metas por cooperado;
- adicionar novos padrões, como Command (para histórico de operações) ou Template Method (para relatórios de fechamento mensal).

---

## 10. Autor

- Vinícius Antonio Minas (@viniciusminas)
