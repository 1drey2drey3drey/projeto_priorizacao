# Priorização de testes automatizados sob restrição de tempo

Projeto didático de Análise e Projeto de Algoritmos (CESUPA), com eixo principal **E5 — algoritmos gulosos** e apoio de **E1 — complexidade**.

O pacote contém uma implementação executável, um experimento realizado, dados brutos, artigos em formato SBC, matriz bibliográfica, apresentação principal sem extras e guias de estudo. É uma **versão completa para revisão pelos autores**, não uma declaração de que todas as exigências pessoais e administrativas já foram cumpridas.

## Comece por aqui

1. Leia `docs/especificacao.md` para conhecer o pequeno sistema MiniPedidos.
2. Execute os testes e a demonstração didática. Use `python demo.py --passo-a-passo` quando quiser ver, rodada a rodada, as pontuações calculadas pelas heurísticas gulosas.
3. Leia o artigo completo e compare suas tabelas com `results/summary.csv`.
4. Consulte `docs/referencias_links.md`, abra as fontes e atualize os níveis de leitura da matriz segundo a leitura pessoal de cada autor.
5. Preencha autoria, contatos e endereço do repositório público antes da submissão.

## Arquivos de entrega

| Arquivo | Finalidade |
|---|---|
| `artigo/artigo_parcial.pdf` | Artigo parcial, metodologia proposta, 5 páginas |
| `artigo/artigo_completo.pdf` | Minuta do artigo com experimento e discussão, formato SBC |
| `artigo/*.tex` e `referencias.bib` | Texto editável em LaTeX e bibliografia |
| `docs/matriz_referencias.xlsx` | Modelo do professor preenchido, com fórmulas |
| `docs/matriz_referencias.pdf` | Anexo legível com os mesmos campos e cruzamento |
| `docs/referencias_links.md` | Todos os links consultados e alcance da leitura |
| `slides/apresentacao_projeto.pptx` | 11 slides editáveis para a fala principal, sem extras |
| `slides/apresentacao_projeto.pdf` | Cópia visual da apresentação |
| `slides/roteiro_apresentacao.md` | Roteiro oral simplificado de 11 slides, com falas naturais e uma demonstração curta |
| `docs/guia_defesa.md` | Explicações conceituais para estudar e responder perguntas |
| `docs/guia_execucao_codigo.md` | Comandos, leitura dos arquivos e demonstração passo a passo |
| `docs/conformidade.md` | Conferência das exigências e pendências reais |

## Executar no Windows

Instale Python 3.12 e abra um terminal na pasta deste README. Os testes e o experimento usam somente a biblioteca padrão. As dependências externas são necessárias apenas para os gráficos.

```powershell
py -3.12 -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python -m unittest discover -s tests -v
.venv\Scripts\python demo.py
.venv\Scripts\python demo.py --passo-a-passo
```

## Executar no Linux ou macOS

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python demo.py
.venv/bin/python demo.py --passo-a-passo
```

## Reproduzir o experimento

Faça uma cópia da pasta antes de executar, caso queira manter os resultados originais para comparação. Os comandos abaixo substituem `data/`, `results/` e os gráficos gerados.

```bash
python experiment.py
python analyze.py
```

Use o executável do ambiente virtual no lugar de `python` se o ambiente não estiver ativado. O `demo.py` é um exemplo didático com quatro testes e custos abstratos; ele não reproduz os resultados experimentais e não modifica `data/` nem `results/`. Por padrão, mostra entrada, seis ordens e métricas ilustrativas. Com `--passo-a-passo`, mostra as pontuações e as escolhas feitas dentro do código real das duas estratégias gulosas. A matriz de defeitos só é consultada depois de todas as ordens serem produzidas.

O protocolo completo usa cinco tamanhos (20, 40, 80, 160, 320), dez repetições, seis estratégias e três chamadas internas por medição do priorizador. O custo dos casos é a mediana de dez lotes de 50 chamadas. Há 300 linhas no CSV de resultados.

As sementes preservam geração, amostragem e embaralhamento. **Os tempos não serão idênticos** em outra execução. Como as estratégias de custo usam as durações medidas, suas ordens e métricas também podem mudar. As figuras são reconstruídas pelo CSV. Os números escritos nos artigos e slides não se atualizam automaticamente depois de uma nova medição.

Para reconstruir somente os gráficos e resumos dos dados fornecidos, execute apenas `python analyze.py`.

## O que foi medido e o que foi simulado

- Medidos por execução: cobertura de linhas, duração dos testes, detecção dos 18 defeitos inseridos, tempo e pico de alocação auxiliar dos priorizadores.
- Calculados por simulação: instantes de detecção de cada ordem, somando custos medianos medidos no programa-base. Não houve execução de um pipeline de integração contínua para cada permutação.
- Todos os testes de uma instância permanecem na ordem. Subamostras variam o tamanho experimental, não implementam seleção de testes.
- O catálogo artificial não é apresentado como defeitos naturais. O objeto é pequeno e sem E/S, banco de dados ou rede.

## Resultados de referência

Em 320 testes, APFDc médio foi 0,9850 para adicional/custo e 0,9844 para menor duração. O primeiro gastou cerca de 60,75 ms para ordenar, enquanto menor duração gastou cerca de 0,060 ms. Incluindo a priorização, a ordem de referência obteve o primeiro feedback mais cedo. Esses resultados descrevem o MiniPedidos e não estabelecem um vencedor universal.

O ambiente exato, as sementes e o hash do objeto estão em `results/environment.json`. Dados individuais estão em `data/timing_samples.csv` e `results/raw_results.csv`. `results/orders.json` permite auditar cada permutação.

## Compilar os artigos

Os arquivos usam `sbc-template.sty` e `sbc.bst` do modelo disponibilizado pela SBC. Em uma instalação LaTeX com os pacotes usados no preâmbulo:

```bash
cd artigo
pdflatex artigo_completo.tex
bibtex artigo_completo
pdflatex artigo_completo.tex
pdflatex artigo_completo.tex
```

Repita trocando `artigo_completo` por `artigo_parcial`. Ao usar Overleaf, envie a pasta `artigo/` e a pasta `figures/`, mantendo a estrutura relativa. Os rótulos estão em português; o estilo SBC original não foi alterado.

Modelo oficial: https://www.sbc.org.br/wp-content/uploads/2024/07/modelosparapublicaodeartigos.zip

## Apresentação

A versão destinada à fala principal contém 11 slides e foi organizada para aproximadamente 9 minutos e 20 segundos, dentro do limite de 5–10 minutos. Os slides extras permanecem no roteiro em Markdown como material de consulta, mas não estão no arquivo de entrega. A tabela de complexidade fica no slide 10. A divisão sugerida é Andrey nos slides 1–6 e Igor nos slides 7–11, a confirmar em ensaio. A apresentação foi renderizada e inspecionada, mas não foi testada em uma instalação do PowerPoint ou Google Slides.

## Publicar o repositório

A pasta está organizada para Git, mas nenhum repositório público foi criado. Depois da revisão, crie um repositório vazio na sua conta e use a URL real fornecida pelo serviço:

```bash
git init
git add .
git commit -m "Adiciona projeto de priorizacao de testes"
git branch -M main
git remote add origin URL_REAL_DO_SEU_REPOSITORIO
git push -u origin main
```

Não copie `URL_REAL_DO_SEU_REPOSITORIO` literalmente. Inclua o endereço confirmado no artigo. A disponibilidade de Git/conta e a publicação dependem dos autores. Não foram incluídos PDFs de terceiros no pacote.

## Uso de IA

Houve apoio de IA na pesquisa e conferência de fontes, preparação das minutas, implementação, depuração, execução, análise inicial e apresentação. Os autores devem conferir as fontes e os dados, compreender o código, repetir as medições e revisar a declaração de uso conforme as regras da disciplina. Os registros de leitura assistida não substituem a leitura pessoal exigida.
