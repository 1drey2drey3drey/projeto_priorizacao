# Guia para estudar e defender o projeto

## O projeto em uma frase

Comparamos maneiras de ordenar todos os testes para revelar defeitos cedo e verificamos se o tempo gasto para calcular essa ordem compensa.

## Por que o tema pertence a Análise e Projeto de Algoritmos?

O centro da comparação é a regra de escolha gulosa. Depois de formalizar entrada e saída, provamos que o algoritmo termina e devolve uma permutação, derivamos tempo e espaço, contamos operações e confrontamos essa análise com medições. Testes de software são o contexto de aplicação.

## Por que não é seleção de testes?

Cada algoritmo devolve todos os testes de sua entrada. Um orçamento limita apenas o prefixo avaliado. Os subconjuntos de 20 a 320 casos existem para estudar crescimento do custo, e são iguais para os métodos comparados.

## Como funciona o adicional/custo?

Para cada candidato, contamos as linhas ainda não vistas na rodada e dividimos pela duração. Escolhemos a maior razão, retiramos esse teste dos candidatos e atualizamos a cobertura. Se não há ganho restante, reiniciamos a rodada. O identificador resolve empates.

Em `demo.py`, B cobre duas linhas por uma unidade de custo. A cobre três por seis. Por isso B é escolhido antes de A pelo critério de custo. A regra é local; não prevê todas as consequências futuras da escolha.

## O guloso encontra a melhor ordem?

Não há essa garantia. A prova apresentada assegura uma permutação válida, sem perda ou repetição de testes. A garantia de Chvátal é para cobertura de conjuntos de custo mínimo. Não podemos transferi-la automaticamente para maximizar APFDc de uma permutação.

## De onde vem O(n²m)?

Na primeira escolha, até n candidatos são avaliados; depois n−1, n−2 e assim por diante. Cada avaliação pode percorrer até m linhas. A soma n+(n−1)+...+1 é n(n+1)/2. Um reinício faz no máximo uma segunda avaliação por rodada, mudando a constante, não a ordem. O caso m=0 é escrito como O(n²(m+1)). As operações de hash são consideradas de custo esperado constante.

## Por que cobertura total não custa O(nm) na tabela?

A matriz já está materializada em conjuntos e Python armazena o tamanho de cada conjunto. O estágio medido precisa ordenar n tamanhos, com O(n log n). Coletar ou construir a cobertura é anterior e custa tempo adicional. Análises que incluem a leitura da matriz têm outra fronteira de medição.

## APFD e APFDc significam a mesma coisa?

APFD usa posições na ordem, como se o passo de um teste tivesse o mesmo peso temporal. APFDc incorpora as durações e, nesta implementação, usa severidade uniforme e o ponto médio do teste detector. Por isso há ainda uma AUC em degraus que contabiliza o defeito apenas ao terminar o teste. Não confunda a convenção de uma métrica com a disponibilidade operacional do resultado.

## Por que os resultados não têm sempre 18 defeitos?

Os 18 são detectáveis pela suíte completa de 567 casos. Um subconjunto pode não conter um detector de todos eles. O denominador das métricas é o conjunto detectável daquela instância, igual para todos os métodos pareados. Ele está registrado no CSV.

## O que o resultado principal ensina?

Adicional/custo e menor duração tiveram APFDc próximo em n=320. Porém o guloso recalcula muitos ganhos, gastando dezenas de milissegundos. Como os testes são muito curtos, esse custo domina o tempo até o primeiro feedback. Isso responde ao recorte estudado e não invalida priorização em outros contextos.

## Os tempos apresentados são reais?

As durações individuais e o tempo dos algoritmos foram medidos. Os defeitos foram detectados em execuções reais. Depois, a duração de cada permutação foi modelada por soma das medianas. Não foi cronometrado um pipeline completo para cada ordem. Explique essa distinção sempre que apresentar APFDc e tempo de detecção.

## O ajuste quase quadrático prova a complexidade?

Não. A complexidade é derivada das operações do código. O ajuste em cinco tamanhos é uma verificação empírica limitada. Custos fixos, ruído e o tamanho do domínio podem gerar expoentes diferentes dos limites assintóticos. Além disso, m permaneceu pequeno.

## Como dividir a fala?

Para dois integrantes, a divisão sugerida na apresentação principal atual é: Andrey apresenta os slides 1–6 e Igor os slides 7–11. Confirmem a divisão em ensaio. Os dois devem dominar todo o método para responder perguntas, independentemente do bloco apresentado.

## O que ainda precisa ser feito pelos autores?

Confirmar nomes e contatos, validar pessoalmente as leituras, reproduzir os resultados, ajustar o texto após essa revisão, publicar o repositório e incluir sua URL. Se o professor exigir um sistema existente, substituir o MiniPedidos e repetir a avaliação, mantendo a distinção entre dado medido e simulado.
