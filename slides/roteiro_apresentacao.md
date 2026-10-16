# Roteiro de fala — versão simples e demonstrativa

**Trabalho:** Priorização de Testes Automatizados sob Restrição de Tempo  
**Autores:** Andrey Lourival Andrade Garcia e Igor Cecim Vilhena  
**Tempo estimado:** cerca de 8 minutos, com demonstração curta do código.  
**Divisão sugerida:** Andrey apresenta os slides 1–6; Igor apresenta os slides 7–11. Ajustem a divisão caso seja necessário.

> A ideia não é decorar o texto. Usem as falas como guia e expliquem olhando para o slide. Os números do MiniPedidos são do protocolo planejado no artigo parcial, não devem ser apresentados como resultados concluídos.

## Antes de apresentar

Na pasta do projeto, abram um terminal com o ambiente virtual ativado.

Demonstração curta, que mostra as ordens e as métricas do exemplo:

```powershell
python demo.py
```

Demonstração passo a passo, que mostra as escolhas reais do algoritmo guloso:

```powershell
python demo.py --passo-a-passo
```

O exemplo usa apenas quatro testes inventados e custos abstratos. **Não é a execução do experimento do artigo e os valores da tela não são resultados do estudo.** Para caber no tempo, mostrem as ordens e expliquem uma rodada de cobertura adicional e uma de adicional por custo. Não precisam ler toda a tabela do terminal.

---

## Slide 1 — Título
**Tempo:** 25 segundos · **Quem:** Andrey

“Boa tarde. Nosso trabalho é sobre como organizar a ordem de execução dos testes automatizados. A ideia é simples: quando temos muitos testes, será que conseguimos encontrar defeitos mais cedo mudando a ordem? E será que vale a pena fazer essa mudança, considerando o tempo que o algoritmo demora para calcular a ordem?”

**Passagem:** “Primeiro, vamos ver por que a ordem faz diferença.”

## Slide 2 — O problema
**Tempo:** 40 segundos · **Quem:** Andrey

“Imaginem que temos quatro testes, mas só um deles revela um defeito. Se esse teste ficar no fim da fila, esperamos os anteriores terminarem antes de descobrir o problema. Se ele vier primeiro, recebemos o alerta bem antes. É isso que a priorização tenta fazer: mudar a ordem, sem tirar nenhum teste. Isso é diferente de selecionar testes ou eliminar testes repetidos.”

Aponte para as duas ordens no slide. Diga que os tempos mostrados são apenas um exemplo.

**Passagem:** “Com esse problema em mente, definimos o que queremos comparar.”

## Slide 3 — Objetivo e perguntas
**Tempo:** 35 segundos · **Quem:** Andrey

“Vamos comparar seis formas de ordenar os testes. Queremos olhar para três coisas: qual ordem ajuda a detectar defeitos mais cedo, quanto o custo de cada algoritmo cresce quando aumentamos a quantidade de testes, e se a vantagem continua existindo quando contamos o tempo gasto para calcular a ordem. Não estamos propondo um algoritmo totalmente novo; estamos comparando estratégias conhecidas de forma organizada.”

**Passagem:** “Para fazer essa comparação de forma justa, precisamos separar a entrada do algoritmo da avaliação.”

## Slide 4 — Entrada, saída e avaliação
**Tempo:** 45 segundos · **Quem:** Andrey

“Cada teste tem duas informações que interessam ao priorizador: quais linhas do programa ele cobre e quanto tempo leva. O algoritmo usa esses dados para montar uma nova ordem com todos os testes. Depois, nós avaliamos se essa ordem ajudou a encontrar defeitos. A informação de quais testes encontram quais defeitos fica fora do priorizador; ela só é usada na avaliação. Assim, o algoritmo não recebe a resposta antes de tomar a decisão.”

Se perguntarem sobre o orçamento: “O orçamento B serve para contar quantos defeitos aparecem dentro de uma parte do tempo disponível. Consideramos a sequência até o ponto em que o orçamento acaba; não pulamos um teste para escolher outro que vem depois.”

**Passagem:** “O programa que usamos para estudar isso é o MiniPedidos.”

## Slide 5 — MiniPedidos
**Tempo:** 45 segundos · **Quem:** Andrey

“O MiniPedidos é um programa pequeno em Python que simula partes de um sistema de pedidos: desconto, frete, estoque e fechamento do pedido. A proposta do experimento é gerar 567 casos de teste e 18 versões do programa, cada uma com um defeito artificial. Para cada teste, vamos medir cobertura e duração. Isso deixa o experimento controlado e repetível, mas tem uma limitação: é um sistema artificial, então não representa todos os problemas de um sistema real.”

**Importante:** como esta apresentação é do artigo parcial, diga “o protocolo prevê” ou “pretendemos gerar”, não “já geramos”, a menos que estejam apresentando explicitamente resultados posteriores do artigo completo.

**Passagem:** “Com os testes definidos, vamos comparar seis regras para ordenar.”

## Slide 6 — As seis estratégias
**Tempo:** 45 segundos · **Quem:** Andrey

“A primeira mantém a ordem original. A segunda embaralha os testes. A terceira coloca os mais rápidos primeiro. A quarta favorece testes que cobrem mais linhas no total. A quinta olha para as linhas que ainda não foram cobertas. E a sexta faz isso levando em conta também a duração do teste. As duas últimas são gulosas: escolhem o que parece melhor naquele momento e recalculam a escolha depois.”

**Demonstração curta:** execute `python demo.py`. Mostre que as ordens saem diferentes e que todos os testes continuam presentes.

**Passagem:** “A diferença entre cobertura total e cobertura adicional fica mais clara com um exemplo.”

## Slide 7 — Cobertura total versus adicional
**Tempo:** 45 segundos · **Quem:** Igor

“Na cobertura total, um teste pode ficar bem colocado só porque cobre muitas linhas. O problema é que essas linhas podem ser quase todas as mesmas que outro teste já cobriu. A cobertura adicional tenta evitar isso: depois de escolher um teste, olha de novo para o que ainda falta cobrir. Por isso, pode escolher um teste que cobre menos linhas no total, mas acrescenta algo novo.”

Aponte para a comparação visual e diga: “Isso melhora a cobertura de código, mas não garante que o teste encontre defeitos. Cobrir uma linha não é a mesma coisa que revelar um erro.”

Se houver tempo ou o professor pedir, execute `python demo.py --passo-a-passo` e mostre a pontuação dos candidatos em uma rodada de cada estratégia gulosa.

**Passagem:** “Essas ideias vêm de trabalhos anteriores, que também mostram os cuidados que precisamos ter.”

## Slide 8 — Referências
**Tempo:** 40 segundos · **Quem:** Igor

“Usamos a literatura para apoiar partes diferentes do projeto. Rothermel e colegas ajudam a fundamentar a priorização de testes. Chvátal estuda uma estratégia gulosa para cobertura de conjuntos. Outros trabalhos analisam custo de execução e a relação entre cobertura e eficácia. Esse último ponto é importante: não podemos supor que um teste mais abrangente necessariamente encontre mais defeitos. A garantia teórica do problema de cobertura também não pode ser aplicada automaticamente às nossas métricas de priorização.”

Não leia a lista de autores inteira. Explique as contribuições principais e deixe os detalhes para os slides extras, caso haja perguntas.

**Passagem:** “Agora, como vamos comparar as seis estratégias?”

## Slide 9 — Plano de avaliação
**Tempo:** 50 segundos · **Quem:** Igor

“O plano é aumentar o tamanho das suítes de 20 até 320 testes e usar dez sementes para cada tamanho. Para cada instância, aplicamos as seis estratégias. Vamos medir APFD, APFDc, quantos defeitos são encontrados dentro de um orçamento, quanto demora para calcular a ordem e quanto tempo passa até o primeiro defeito, incluindo esse custo. Esse slide descreve o protocolo previsto no artigo parcial, não deve ser apresentado como resultado.”

Se perguntarem como os tempos são obtidos: “A proposta mede separadamente a duração dos testes e o custo de priorização. A avaliação temporal de cada ordem é calculada a partir dos custos medidos; não estamos dizendo que executamos um pipeline industrial completo para cada ordem.”

**Passagem:** “Isso leva à outra parte do trabalho: quanto custa cada estratégia do ponto de vista computacional?”

## Slide 10 — Complexidade
**Tempo:** 55 segundos · **Quem:** Igor

“As duas estratégias mais simples, referência e aleatória, fazem trabalho proporcional à quantidade de testes, então são lineares. Menor duração e cobertura total precisam ordenar os testes, por isso ficam em O de n log n. As estratégias de cobertura adicional são mais caras porque, a cada escolha, avaliam os testes que ainda sobraram e calculam a cobertura nova. Esse processo repetido leva a um custo quadrático em relação ao número de testes, multiplicado pelo trabalho de analisar a cobertura. Por isso vamos olhar tanto para o limite teórico quanto para o tempo medido.”

Aponte para a tabela. Não precisa ler cada célula em voz alta. Explique apenas a diferença entre ordenar uma vez e recalcular candidatos a cada rodada.

**Passagem:** “Por fim, precisamos deixar claro o que o estudo pode e não pode concluir.”

## Slide 11 — Limitações e conclusão
**Tempo:** 40 segundos · **Quem:** Igor

“O estudo tem limitações: usamos um sistema pequeno, defeitos artificiais e testes curtos, então os resultados não podem ser generalizados automaticamente. Também não vamos tratar um ajuste dos tempos como prova matemática de complexidade, nem confundir cobertura com detecção. A contribuição esperada é uma comparação clara e repetível das seis estratégias, mostrando não só a qualidade da ordem, mas também o custo de produzi-la. Obrigado.”

---

## Se o professor perguntar sobre o código

**Como executar:**

```powershell
python demo.py --passo-a-passo
```

**O que mostrar:**

1. A entrada contém o identificador do teste, linhas cobertas e duração abstrata.
2. `src/prioritizers.py` calcula as ordens usando as seis estratégias.
3. No modo passo a passo, o programa mostra as pontuações calculadas dentro do algoritmo guloso e qual teste ele escolheu.
4. Só depois da priorização, `src/metrics.py` consulta a matriz fictícia de defeitos para calcular as métricas.

**Frase importante:** “Esse é um exemplo didático pequeno para mostrar como o código funciona. Não são os resultados do experimento completo.”

## Três perguntas para ensaiar

**Por que cobertura não garante detecção?**  
Porque o teste pode executar uma linha sem exercitar a condição errada que revela o defeito.

**Por que a cobertura adicional custa mais?**  
Porque a cada passo precisa avaliar os testes restantes e recalcular quantas linhas novas cada um acrescenta.

**Por que medir o tempo de priorização?**  
Porque uma ordem pode ser melhor, mas demorar tanto para ser calculada que o ganho de feedback deixa de compensar.

## Dicas finais

- Não leiam o texto do slide; usem as falas como guia.
- Não leiam todos os números da tela durante a demo. Mostrem uma escolha e expliquem o motivo.
- Digam “o protocolo prevê” quando estiverem falando do artigo parcial.
- Guardem as fórmulas completas de APFD/APFDc e o artigo completo para perguntas, sem colocá-los no tempo da exposição principal.
