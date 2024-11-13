# TORMENTCHÊ BOT

Um bot para discord que implementa algumas funcionalidades relacionadas ao RPG **Tormenta 20**, para auxiliar os grupos em suas mesas.

## Observações

Esse projeto utiliza módulos que podem ser instalados através do seguinte comando:

```bash
$ pip install -r requirements.txt
```

## Funcionalidades

- Busca de informações como magias, condições, manobras de combate e parceiros do RPG Tormenta 20.

- Rolagem de dados, permitindo a utilização de expressões matemáticas em sua composição.

## Comandos

Tormentche utiliza comandos Slash como padrão, para implementação de algumas funcionalidades suportadas apenas por esses comandos, como _auto complete_.

Atualmente os seguintes comandos estão disponíveis para uso.

- Comandos gerais

  - Nome: _/ajuda_
  - Descrição: Retorna todos os comandos em conjunto com uma explicação de sua utilização

- Comandos de busca

  - Nome: _/magias ${nome_da_magia}_
  - Descrição: Procura e exibe a descrição detalhada da magia especificada. Informe o nome da magia que deseja consultar.

  - Nome: _/condicoes ${nome_do_condicao}_
  - Descrição: Procura e exibe a descrição da condição informada. Digite o nome da condição para obter suas informações. Caso a condição procurada tenha relação com outras condições em seu texto, as retorná em botões que exibirão suas descrições ao clique.

  - Nome: _/manobras ${nome_da_manobra}_
  - Descrição: Procura e exibe a descrição da manobra de combate indicada. Informe o nome da manobra para ver os detalhes.

  - Nome: _/parceiros ${nome_do_parceiro}_
  - Descrição: Procura e exibe a descrição do parceiro mencionado. Digite o nome do parceiro para obter a descrição correspondente.

- Comandos de rolagem de dados

  - Nome: _/rolar ${expressão}_
  - Descrição: Rola dados e calcula o resultado de expressões matemáticas. Use a sintaxe 'XdY', onde 'X' é o número de dados e 'Y' o número de faces. Você pode combinar múltiplos lançamentos e operações matemáticas.

- Comandos de rolagem de itens

  - Nome: _/pocoes ${numero_de_pocoes}_
  - Descrição: Rola um número X de poções utilizando a tabela de poções. Por padrão, caso o numero desejado de poções passado seja menor que 1, 1 poção é rolada.

## O que está faltando?

O bot Tormentche é um trabalho em progresso e por isso ainda não conta com algumas funcionalidades desejadas.

- Rolagem de tesouros da aba de recompensas do livro.

- Rolagem de tabelas de itens, como acessórios, armaduras, armas entre outros.

- Suporte a rolagem do Baralho do Caos.

- Suporte as buscas de poderes e habilidades.
