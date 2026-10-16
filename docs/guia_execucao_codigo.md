# Guia de estudo prático — execução e defesa do projeto

**Projeto:** Priorização de Testes Automatizados sob Restrição de Tempo  
**Autores:** Andrey Lourival Andrade Garcia e Igor Cecim Vilhena  
**Finalidade:** complementar o roteiro oral. Este material é para estudo e consulta; não deve ser lido integralmente na apresentação.

## 1. Como executar na hora

Abra o PowerShell na pasta que contém `demo.py`, `experiment.py`, `src/`, `tests/` e `requirements.txt`. Pelo terminal usado anteriormente, o ambiente virtual já está ativo, indicado pelo prefixo `(.venv)`.

### Primeiro: executar a demonstração didática

```powershell
python demo.py
```

O `demo.py` mostra quatro testes inventados e executa as seis estratégias. Por padrão, imprime as ordens e as métricas ilustrativas. Para acompanhar as escolhas internas das duas heurísticas gulosas, use `python demo.py --passo-a-passo`.

Se preferir não depender da ativação do ambiente virtual:

```powershell
.\.venv\Scripts\python.exe demo.py
.\.venv\Scripts\python.exe demo.py --passo-a-passo
```

### Segundo: executar os testes automatizados

```powershell
python -m unittest discover -s tests -v
```

Ou, sem ativar o ambiente:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

No pacote usado para esta versão do guia, os seis testes passaram. Ao executar na sua máquina, confira o resultado que aparecer no terminal; não apresente o teste como aprovado se a sua execução falhar.

### Terceiro: localizar os resultados existentes

Abra `results/summary.csv`, `results/report.json` e os gráficos de `figures/`. Esses arquivos já contêm os resultados registrados no pacote. Para consultar o código que gerou os resultados, leia `experiment.py` e `analyze.py`.

**Não rode `experiment.py` durante a fala.** Ele repete as medições e substitui arquivos de `data/` e `results/`. A execução também pode levar mais tempo que a demonstração e produzir números diferentes, porque tempos de execução variam conforme ambiente e ruído de medição.

## 2. A diferença entre os quatro comandos que você precisa conhecer

| Comando | O que faz | Quando usar |
|---|---|---|
| `python demo.py` | Executa as seis estratégias e mostra as ordens e métricas do exemplo. | Demonstração curta durante a apresentação. |
| `python demo.py --passo-a-passo` | Também mostra as pontuações calculadas em cada rodada das duas estratégias gulosas. | Quando quiser explicar uma escolha do algoritmo ao professor. |
| `python -m unittest discover -s tests -v` | Executa os testes automatizados que verificam propriedades e exemplos conhecidos. | Antes da apresentação, como validação rápida do pacote. |
| `python experiment.py` | Reexecuta o protocolo de medição, gera dados e substitui os arquivos experimentais. | Só para reproduzir o experimento, após fazer backup dos dados. |
| `python analyze.py` | Lê `results/raw_results.csv`, calcula resumos e ajustes e reconstrói gráficos. Não repete as medições do priorizador. | Quando os dados brutos já existem e você quer reconstruir as análises. |

**Regra prática:** o `demo.py` ensina; os testes automatizados verificam; `experiment.py` mede; `analyze.py` resume e gera gráficos.

## 3. O que cada arquivo do projeto faz

### `src/subject.py` — o sistema MiniPedidos

Contém o programa sob teste. Suas operações são:

- `discount`: calcula o desconto de associado e os cupons `PROMO10` e `FIXO500`.
- `freight`: calcula frete pela região, peso, frete expresso e regra de frete grátis.
- `reserve`: valida a quantidade pedida e calcula o saldo do estoque.
- `checkout`: combina itens, estoque, desconto e frete e retorna os valores finais.

O código usa centavos inteiros para os valores monetários. Isso evita depender de arredondamento binário de ponto flutuante para representar dinheiro neste protótipo.

### `src/cases.py` — geração e oráculo esperado

Gera os casos usados na avaliação e define resultados esperados. O oráculo é separado do sistema testado: ele calcula o que cada caso deveria produzir. A função `passes` compara o resultado real do programa com o resultado esperado.

A suíte completa tem 567 casos. Esse número é parte do protocolo do pacote, não uma quantidade que o `demo.py` usa: a demonstração usa somente quatro testes inventados.

### `src/mutations.py` — defeitos inseridos

Lista 18 alterações isoladas do programa, como mudar um limite, uma taxa ou uma condição. O experimento cria versões em memória com cada alteração e verifica quais casos passam a falhar. Isso permite formar a matriz teste × defeito.

Essas alterações são defeitos artificiais e controlados. Elas não são um conjunto de falhas históricas de um sistema de produção; essa diferença limita a generalização dos resultados.

### `src/prioritizers.py` — os seis algoritmos

A função principal é:

```python
order, counts = prioritize(records, strategy, seed=0)
```

- `records` contém os testes, as linhas cobertas e a duração de cada teste.
- `strategy` escolhe um dos seis métodos.
- `seed` torna o embaralhamento aleatório reproduzível.
- `order` é a lista ordenada de identificadores.
- `counts` contém contadores instrumentados, incluindo avaliações de candidatos, verificações de pertinência à cobertura e reinícios.

A função não recebe a matriz de defeitos. Essa separação é essencial: a estratégia ordena usando cobertura e custo, e a detecção é avaliada somente depois.

### `src/metrics.py` — avaliação das ordens

A função `evaluate(order, records, kills, overhead_ns=0)` recebe a ordem pronta e a matriz de defeitos. Ela calcula APFD, APFDc, métricas de detecção sob orçamento, tempo até concluir o primeiro teste detector e tempo de primeiro feedback acrescido do custo de priorização informado.

A matriz de defeitos entra nesta etapa de avaliação, e não dentro de `prioritize`. É assim que o projeto separa a informação usada para decidir a ordem daquela usada para julgar a ordem.

### `experiment.py` — coleta e experimento completo

O script:

1. gera os 567 casos;
2. verifica os casos no programa-base;
3. coleta cobertura de linhas no arquivo do MiniPedidos;
4. aquece a execução e mede durações em lotes, guardando medianas;
5. cria e executa as 18 versões com defeitos;
6. seleciona suítes com 20, 40, 80, 160 e 320 casos;
7. compara seis estratégias em dez repetições por tamanho;
8. mede custo de priorização e memória auxiliar;
9. grava os dados brutos, as ordens e o ambiente usado.

Há `5 × 10 × 6 = 300` configurações de tamanho, repetição/semente e estratégia. Isso não equivale a 300 sistemas independentes: o estudo usa um único MiniPedidos e diferentes amostras de testes.

O tempo de cada teste e o tempo do priorizador são medidos. Em seguida, as métricas temporais de uma ordem são calculadas somando os custos medidos dos testes na ordem. Portanto, o experimento não cronometria um pipeline de integração contínua completo para cada permutação.

### `analyze.py` — análise dos dados

Lê `results/raw_results.csv`, calcula médias, medianas e dispersões, ajusta curvas log-log e produz figuras. Ele não é o script que mede novamente cada teste. Seus arquivos de saída incluem `results/summary.csv`, `results/fits.json`, `results/report.json` e gráficos em `figures/`.

### `tests/test_methods.py` — verificações automatizadas

O arquivo contém seis testes:

1. `test_known_metrics`: verifica métricas em um caso com resposta conhecida.
2. `test_permutations_and_coverage_stagnation`: verifica que todas as estratégias devolvem os mesmos identificadores e que o método por custo funciona num exemplo de cobertura repetida.
3. `test_zero_gain_terminates`: verifica que métodos adicionais terminam quando os testes não cobrem nenhuma linha.
4. `test_metric_permutations_match_integral`: compara a métrica de conclusão com um cálculo independente ao percorrer as permutações possíveis de um exemplo pequeno.
5. `test_specification_anchors`: confere saídas de regras do MiniPedidos em casos escolhidos.
6. `test_all_generated_cases`: verifica os casos gerados no sistema-base.

Passar nesses testes aumenta a confiança nas propriedades verificadas, mas não prova que o programa esteja livre de todo defeito.

## 4. Como explicar o `demo.py` sem decorar a saída

O exemplo é curto para apoiar a demonstração oral. Ele **não usa os dados reais do experimento** e não grava dados em `data/` nem em `results/`. O modo `--passo-a-passo` recebe eventos emitidos pelo algoritmo real em `src/prioritizers.py`; não cria uma segunda implementação da heurística.

### 4.1 A entrada

| Teste | Linhas cobertas | Custo ilustrativo |
|---|---|---:|
| A | `{1, 2, 3}` | 6 |
| B | `{1, 2}` | 1 |
| C | `{3, 4}` | 2 |
| D | `{4}` | 1 |

Os números de custo são unidades abstratas, não milissegundos ou nanossegundos. O conjunto de cobertura representa as linhas que cada teste executa.

Depois de gerar as ordens, o demo revela uma matriz didática: A detecta F1, C detecta F2, D detecta F3 e B não detecta nenhum desses três defeitos. A matriz só é usada para avaliar as ordens; não é passada ao priorizador.

### 4.2 Por que as seis ordens diferem

- **Referência:** mantém a ordem de entrada, `A → B → C → D`.
- **Aleatória:** embaralha com semente 42; neste exemplo resulta em `C → B → D → A`.
- **Menor duração:** põe os custos 1 antes de 2 e 6; os empates são resolvidos pelo identificador, resultando em `B → D → C → A`.
- **Cobertura total:** ordena pelo número total de linhas cobertas. A tem 3, B e C têm 2, D tem 1; o desempate por identificador produz `A → B → C → D`.
- **Cobertura adicional:** recalcula quantas linhas novas cada teste pode acrescentar, dado o que já foi selecionado.
- **Adicional por custo:** divide esse ganho novo pela duração, escolhendo a maior razão em cada rodada.

Os contadores `score_evaluations` e `membership_checks` são instrumentos para analisar o trabalho das heurísticas gulosas. Nos métodos de referência, aleatório e ordenações estáticas, esses contadores ficam em zero porque essas operações não são contabilizadas por esses dois contadores; isso **não** significa que esses métodos não executem trabalho computacional.

### 4.3 Cobertura adicional, rodada a rodada

No início, as linhas ainda não vistas são `{1, 2, 3, 4}`.

1. A acrescenta 3 linhas; B acrescenta 2; C acrescenta 2; D acrescenta 1. A é escolhido.
2. Depois de A, só a linha 4 ainda é nova. B acrescenta 0, C acrescenta 1 e D acrescenta 1. C e D empatam; o identificador C vem primeiro.
3. Depois de C, as quatro linhas já foram cobertas nesta rodada. B e D não acrescentam novas linhas. O algoritmo reinicia a referência de cobertura para ordenar os testes restantes, não remove nenhum teste.
4. Na nova rodada, B acrescenta 2 linhas, contra 1 de D; escolhe B e depois D.

Resultado: `A → C → B → D`.

**Por que há reinício?** O objetivo é produzir uma permutação completa, não parar assim que toda a cobertura tiver sido alcançada. Depois de esgotar o ganho de cobertura novo, o código restaura o universo de linhas para escolher entre os testes ainda restantes. É uma regra específica desta implementação; não é uma garantia de otimalidade.

### 4.4 Cobertura adicional por custo, rodada a rodada

Na primeira rodada, o escore é `ganho novo / custo`:

| Teste | Ganho novo | Custo | Escore |
|---|---:|---:|---:|
| A | 3 | 6 | 0,5 |
| B | 2 | 1 | 2,0 |
| C | 2 | 2 | 1,0 |
| D | 1 | 1 | 1,0 |

B vence porque cobre duas linhas novas por unidade de custo. Depois dele, faltam as linhas 3 e 4: C obtém `2/2 = 1`, D obtém `1/1 = 1`, e o identificador C desempata. Quando a cobertura fica esgotada, resta A e D. Após o reinício, D obtém `1/1 = 1` e A `3/6 = 0,5`, então D vem antes de A.

Resultado: `B → C → D → A`.

A diferença em relação à cobertura adicional é o denominador: a primeira estratégia maximiza a quantidade de linhas novas; a segunda maximiza a quantidade de linhas novas por unidade de duração. Nenhuma delas vê a matriz de defeitos.

### 4.5 Como interpretar a tabela de métricas do demo

- **APFD:** considera a posição do primeiro teste que revela cada defeito.
- **APFDc:** considera também os custos/durações dos testes, usando os pontos médios dos testes detectores nesta implementação.
- **1º defeito:** tempo acumulado até o término do primeiro teste que revela algum defeito, em unidades abstratas do exemplo.
- **B25/B50:** fração de defeitos detectada dentro de 25% ou 50% do custo total da suíte.

Esses valores servem apenas para demonstrar que métricas distintas podem classificar as ordens de maneiras diferentes. **Não use os valores do demo como resultados do artigo ou como prova de que uma estratégia vence.** No experimento completo, durações medidas em unidades temporais são usadas para avaliar as ordens, e os resultados devem ser citados a partir de `results/summary.csv`.

## 5. O caminho da execução — do terminal ao resultado

Use a seguinte narrativa caso o professor peça para explicar a arquitetura do código:

1. `demo.py` monta um pequeno dicionário de testes e chama `prioritize` para cada estratégia.
2. `prioritize` retorna a permutação e contadores da estratégia; não sabe quais testes detectam falhas.
3. No modo `--passo-a-passo`, `prioritize` envia eventos de rastreamento com os candidatos, os escores e a escolha feita em cada rodada.
4. Só depois o demo fornece `DEMO_FAULTS` à função `evaluate`.
5. `evaluate` percorre a ordem, calcula as posições e os tempos de detecção, e retorna as métricas.
6. O código de demonstração termina sem regravar os dados de pesquisa.

O experimento real segue a mesma separação conceitual, mas usa testes gerados, cobertura coletada no MiniPedidos e versões com defeitos. `experiment.py` coleta os dados e `analyze.py` os sumariza.

## 6. Complexidade: explicar a partir das operações do código

Use `n` para número de testes e `m` para número de linhas/elementos distintos de cobertura.

| Estratégia | Tempo teórico declarado | Intuição |
|---|---|---|
| Referência | `O(n)` | Percorre/manipula a lista inicial. |
| Aleatória | `O(n)` esperado | Embaralha a lista. |
| Menor duração | `O(n log n)` | Ordena os testes por duração. |
| Cobertura total | `O(n log n)` | Ordena pelo tamanho já materializado de cada conjunto de cobertura. |
| Cobertura adicional | `O(n²(m+1))` | Avalia os candidatos restantes a cada escolha e calcula ganho de cobertura. |
| Adicional por custo | `O(n²(m+1))` | Faz as mesmas avaliações adicionais e divide o ganho pela duração. |

Na abordagem gulosa, o número de candidatos avaliados é `n + (n - 1) + ... + 1 = n(n+1)/2`, que é quadrático em `n`. Uma avaliação pode percorrer até `m` elementos de cobertura. O reinício previsto pela implementação adiciona outra avaliação em certas rodadas, mas não muda essa ordem assintótica.

O espaço auxiliar é `O(n)` para os quatro primeiros métodos e `O(n+m)` para os dois adicionais, sem contar a memória necessária para armazenar a entrada.

Há três coisas diferentes: (1) complexidade derivada do código, (2) tempo medido numa máquina e (3) expoente de um ajuste empírico. O ajuste em cinco tamanhos não prova uma complexidade. Em particular, `m` ficou limitado no experimento, e custos fixos/ruído podem alterar o comportamento observado.

## 7. APFD e APFDc: explicação rápida para perguntas

Na convenção de APFD usada pelo projeto:

`APFD = 1 - (Σ TFᵢ) / (n · m) + 1 / (2n)`

- `n`: número de testes na ordem;
- `m`: número de defeitos detectáveis pela instância;
- `TFᵢ`: posição do primeiro teste que detecta o defeito `i`.

Quanto mais cedo forem as primeiras detecções, menor tende a ser a soma das posições e maior a pontuação. APFD atribui o mesmo peso a cada posição e não modela duração diferente entre testes.

Na implementação de APFDc usada neste projeto:

`APFDc = 1 - (Σ pmᵢ) / (m · T)`

`pmᵢ = tempo acumulado antes do teste detector + duração desse teste / 2`

- `T`: soma das durações de todos os testes da ordem;
- `pmᵢ`: ponto médio temporal do teste que detecta o defeito.

APFDc considera custo de execução, mas **não inclui automaticamente o custo computacional de calcular a ordem**. O projeto mede esse custo separadamente e também calcula o primeiro feedback acrescido do overhead. Essa separação corresponde à pergunta sobre se o benefício compensa o tempo gasto em priorizar.

Uma pontuação APFDc de `0,985` não significa literalmente “98,5% dos defeitos encontrados”. É uma pontuação normalizada de antecipação no tempo segundo a fórmula implementada.

## 8. Perguntas práticas que você deve conseguir responder

**Por que `demo.py` não é o experimento?**  
Porque usa quatro testes inventados, custos abstratos e três defeitos didáticos. Ele existe para explicar as regras; o experimento utiliza os 567 casos, as 18 versões com defeitos e as amostras descritas no protocolo.

**A matriz de defeitos está disponível ao algoritmo?**  
Não. `prioritize` recebe cobertura, duração e identificadores. A matriz entra depois na avaliação.

**O que prova que todos os testes foram preservados?**  
Cada estratégia devolve uma lista com todos os identificadores uma vez. Os testes automatizados verificam essa propriedade em exemplos e o experimento confere que a ordem produzida é uma permutação do subconjunto de entrada.

**Por que cobertura adicional escolheu C em vez de D?**  
Depois de escolher A, ambos acrescentam apenas a linha 4; o ganho é igual. O desempate por identificador escolhe C. A regra de cobertura adicional não divide pelo custo.

**Por que adicional por custo escolheu B primeiro?**  
B acrescenta duas linhas com custo 1, escore 2. A acrescenta três com custo 6, escore 0,5. Apesar de A ter maior cobertura total, o ganho por custo de B é superior.

**Cobertura maior implica detecção maior?**  
Não. Cobertura informa quais linhas são executadas; a detecção depende de o teste expor um comportamento incorreto. Por isso o projeto mantém cobertura e matriz de defeitos separadas.

**O código mede o pipeline completo para cada ordem?**  
Não. Ele mede os custos individuais e os custos dos priorizadores. As métricas temporais de cada ordem são calculadas a partir da soma dos custos medidos. Não inclui inicialização e todas as despesas de uma pipeline industrial.

**O projeto provou que uma estratégia é universalmente melhor?**  
Não. O estudo é limitado a um protótipo, defeitos artificiais e testes curtos. A contribuição é a comparação controlada e a análise do compromisso entre eficácia e custo de priorização.

## 9. Plano de ensaio em 30 minutos

1. **5 min — executar:** rodar `python demo.py` sem interrupções e localizar o trecho da saída que explica a escolha de A e B.
2. **5 min — testes:** rodar `python -m unittest discover -s tests -v` e explicar brevemente o que verifica cada teste.
3. **7 min — código:** abrir `src/prioritizers.py`, localizar `fastest`, `total`, `additional` e `cost_aware`; explicar em voz alta como cada um escolhe o próximo teste.
4. **5 min — métricas:** abrir `src/metrics.py`, apontar `positions`, `midpoints`, `apfd` e `apfdc`.
5. **5 min — limites:** explicar defeitos artificiais, um único sistema, custos simulados por soma e ajuste empírico não ser prova.
6. **3 min — cronômetro:** ensaiar o começo e o fechamento da fala principal. Não incluir os slides extras no tempo oral.

## 10. Sequência recomendada para a apresentação prática

Se o professor pedir uma demonstração do código, evite percorrer todos os arquivos em sequência. Faça o seguinte:

1. Mostre `src/prioritizers.py` por 15–20 segundos e a assinatura `prioritize(records, strategy, seed=0)`.
2. Rode `python demo.py`.
3. Explique a rodada 1 de cobertura adicional: A ganha 3 linhas; B e C ganham 2; D ganha 1.
4. Explique o primeiro cálculo de adicional/custo: B tem escore 2, maior que os demais.
5. Mostre a seção final de APFD/APFDc e ressalte que a matriz de defeitos só é usada após a geração das ordens.
6. Se perguntarem sobre os resultados do artigo, abra `results/summary.csv` ou o gráfico correspondente, não use as pontuações didáticas de `demo.py`.

A demonstração deve levar aproximadamente 2–4 minutos se os arquivos estiverem abertos e o ambiente pronto. O experimento completo não deve ser iniciado durante a fala.
