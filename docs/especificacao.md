# MiniPedidos: especificação e limites

Este é um programa artificial criado para o estudo. Não representa um sistema de uma empresa.

Valores monetários são inteiros em centavos. Os testes comparam valores retornados ou o tipo da exceção. O código não executa banco de dados, rede nem espera artificial.

- **Desconto:** subtotal não negativo. Membro recebe 5%, com divisão inteira. O cupom PROMO10 desconta 10% sobre a base após o desconto de membro quando essa base é pelo menos 10.000. FIXO500 desconta até 500, limitado à base. Cupom desconhecido gera `ValueError`.
- **Frete:** peso inteiro de pelo menos 1 kg. Tarifas local, regional e remota: 800, 1.500 e 3.000. Cada kg acima de 2 acrescenta 500. Expresso acrescenta 1.200. Subtotal de pelo menos 20.000 tem frete gratuito somente na região local e sem expresso. Região inválida ou peso menor que 1 gera `ValueError`.
- **Estoque:** quantidade positiva, estoque não negativo, quantidade não superior ao estoque. O retorno é o estoque restante; violação gera `ValueError`.
- **Fechamento:** lista não vazia de `(preço, quantidade, estoque, gramas por unidade)`. Preço não negativo e peso positivo. Calcula subtotal e peso por quantidade; valida o estoque de cada linha; aplica desconto; arredonda o peso total para kg para cima; cobra frete sobre o subtotal líquido. Retorna total, subtotal bruto, desconto, frete e soma dos estoques restantes.

O oráculo em `src/cases.py` é implementado separadamente. Essa separação reduz dependência direta do objeto, mas não elimina erros compartilhados de interpretação da especificação. Os defeitos são alterações isoladas documentadas em `data/fault_catalog.json`.

Os priorizadores recebem somente cobertura, duração e identificador. A matriz de defeitos é utilizada exclusivamente na avaliação. Nenhum priorizador remove testes. A amostragem de tamanhos é parte do desenho experimental.
