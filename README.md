Projeto da disciplina optativa de Autômatos Celulares, UFRPE.

Autor: Victor Leite Malta da Silva

O projeto usa um autômato celular bidimensional para simular a propagação de
um incêndio numa floresta e estudar três perguntas de interesse ambiental:

1. Existe uma densidade crítica de floresta acima da qual o fogo atravessa toda a
   paisagem? (transição de percolação)
2. Um aceiro (faixa de vegetação removida) consegue conter o incêndio?
3. Como o vento muda a forma e a velocidade da propagação do fogo?

Funcionamento do Modelo

A floresta é uma grade N × N. Cada célula tem um dos quatro estados:

| Estado | Cor | Significado |
|--------|-----|-------------|
| `0` Vazio | cinza | solo sem vegetação (ou aceiro) |
| `1` Árvore | verde | vegetação intacta |
| `2` Fogo | laranja | célula queimando agora |
| `3` Queimado | preto | vegetação já consumida |

A cada passo de tempo, as regras são aplicadas a todas as células ao mesmo tempo:

- Fogo → Queimado, o fogo dura apenas um passo em cada célula.
- Árvore → Fogo, uma árvore pega fogo se tiver algum vizinho em chamas. A chance
  de pegar depende de quantos vizinhos estão queimando (probabilidade
  `p` por vizinho) e da direção do **vento**.
- Vazio e Queimado não mudam (nesta versão não há rebrota).

A vizinhança pode ser von Neumann (4 vizinhos) ou Moore (8 vizinhos).

Metodologia para rodar

Pré-requisitos: Python 3 com as bibliotecas `numpy` e `matplotlib`:

```bash
pip install numpy matplotlib
```

Ver a animação do incêndio:

```bash
python incendio_florestal.py
```

Mudança de parâmetros no topo do arquivo `incendio_florestal.py`
(`TAMANHO`, `DENSIDADE`, `PROB_PROPAGACAO`, `VIZINHANCA`, `IGNICAO`, `VENTO`).

Gerar todas as figuras do artigo (evolução, série temporal, percolação, aceiro e vento):

```bash
python gerar_figuras.py
```

As imagens são salvas na pasta `figuras/`.

Principais resultados:

- Transição de percolação: o fogo só atravessa a floresta acima de uma densidade
  crítica. O limiar medido na simulação (aproximadamente 0,58) coincide com o limiar teórico de
  percolação de sítios em rede quadrada (aproximadamente 0,593).
- Aceiro:uma faixa fina de solo limpo reduziu a área queimada de 99% para 50%.
- Vento: empurra o fogo na sua direção, deixando a mancha queimada alongada e
  aumentando a área atingida no mesmo intervalo de tempo (11% → 30%).

Arquivos:

- `incendio_florestal.py` — o modelo do autômato celular + animação.
- `gerar_figuras.py` — roda os experimentos e gera as figuras do artigo.
- `figuras/` — imagens geradas.
- `artigo/` — o texto científico (formato Nature *Scientific Reports*).
- `prompts_ia.md` — os prompts de IA usados na construção do projeto.

Referências principais:

- Drossel, B. & Schwabe, F. Self-organized critical forest-fire model. Phys. Rev. Lett. **69**, 1629 (1992).
- Stauffer, D. & Aharony, A. Introduction to Percolation Theory. Taylor & Francis (1994).
- Wolfram, S. A New Kind of Science. Wolfram Media (2002).
