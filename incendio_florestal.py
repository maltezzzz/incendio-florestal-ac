# -*- coding: utf-8 -*-
"""
Modelo de Incendio Florestal baseado em Automato Celular.

A floresta e uma grade quadrada (TAMANHO x TAMANHO). Cada celula tem um estado:
    0 = VAZIO     -> solo sem vegetacao (ou aceiro/barreira)
    1 = ARVORE    -> vegetacao intacta
    2 = FOGO      -> celula queimando neste instante
    3 = QUEIMADO  -> vegetacao ja consumida pelo fogo (cinzas)

Regras de transicao (aplicadas a todas as celulas ao mesmo tempo, a cada passo):
    - FOGO      -> QUEIMADO       (o fogo dura so um passo em cada celula)
    - ARVORE    -> FOGO           se pega fogo de algum vizinho em chamas
    - VAZIO     -> VAZIO          (nada acontece)
    - QUEIMADO  -> QUEIMADO       (nao volta a crescer nesta versao)

A chance de uma arvore pegar fogo depende de quantos vizinhos estao queimando
e da direcao do vento. Rodar este arquivo mostra a animacao do incendio.

Autor: (colocar seu nome)
Disciplina optativa de Automatos Celulares - UFRPE
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.animation import FuncAnimation

# ------------------------- Parametros que voce pode mudar -------------------------
TAMANHO = 120            # a grade tem TAMANHO x TAMANHO celulas
DENSIDADE = 0.62         # fracao da floresta que comeca com arvore (0 a 1)
PROB_PROPAGACAO = 1.0    # chance de uma arvore pegar fogo de UM vizinho em chamas
VIZINHANCA = "vonneumann"  # "vonneumann" (4 vizinhos) ou "moore" (8 vizinhos)
IGNICAO = "centro"       # onde o fogo comeca: "centro" ou "esquerda"
VENTO = None             # None, ou ex.: {"direcao": "leste", "forca": 0.3}
SEMENTE = 7              # semente aleatoria (mesma semente = mesmo resultado)

# ------------------------- Estados das celulas -------------------------
VAZIO, ARVORE, FOGO, QUEIMADO = 0, 1, 2, 3

# Vetores de direcao usados pelo vento (linha, coluna)
VETORES = {"norte": (-1, 0), "sul": (1, 0), "leste": (0, 1), "oeste": (0, -1)}

# Cores para desenhar: vazio, arvore, fogo, queimado
CORES = ["#E4E4E4", "#2E7D32", "#FF3B00", "#2B2B2B"]
MAPA_CORES = mcolors.ListedColormap(CORES)
NORMA = mcolors.BoundaryNorm([0, 1, 2, 3, 4], MAPA_CORES.N)


def criar_floresta(tamanho, densidade, rng):
    """Cria a grade inicial: cada celula vira ARVORE com probabilidade 'densidade'."""
    sorteio = rng.random((tamanho, tamanho))
    grade = np.where(sorteio < densidade, ARVORE, VAZIO)
    return grade


def acender_fogo(grade, modo):
    """Coloca o fogo inicial na floresta (so acende onde ja existe arvore)."""
    if modo == "centro":
        meio = grade.shape[0] // 2
        if grade[meio, meio] == ARVORE:
            grade[meio, meio] = FOGO
        else:
            # se o centro estiver vazio, acende a arvore mais proxima do centro
            arvores = np.argwhere(grade == ARVORE)
            if len(arvores) > 0:
                dist = np.abs(arvores[:, 0] - meio) + np.abs(arvores[:, 1] - meio)
                linha, coluna = arvores[np.argmin(dist)]
                grade[linha, coluna] = FOGO
    elif modo == "esquerda":
        # acende todas as arvores da primeira coluna (uma frente de fogo)
        coluna0 = grade[:, 0]
        coluna0[coluna0 == ARVORE] = FOGO
    return grade


def montar_offsets(vizinhanca, prob_base, vento):
    """
    Monta a lista de vizinhos considerados e a probabilidade de o fogo passar
    por cada um deles. Se houver vento, a chance aumenta na direcao do vento.
    Retorna uma lista de pares ((dy, dx), probabilidade).
    """
    if vizinhanca == "vonneumann":
        base = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    else:  # moore
        base = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
                (0, 1), (1, -1), (1, 0), (1, 1)]

    offsets = []
    for (dy, dx) in base:
        p = prob_base
        if vento is not None:
            # o fogo vai do vizinho (dy, dx) para a celula, ou seja na direcao (-dy, -dx)
            direcao_prop = (-dy, -dx)
            v = VETORES[vento["direcao"]]
            alinhamento = direcao_prop[0] * v[0] + direcao_prop[1] * v[1]
            # o vento so REFORCA a propagacao a favor dele (nunca reduz a contra-vento)
            p = prob_base + vento["forca"] * max(0.0, alinhamento)
            p = min(p, 1.0)
        offsets.append(((dy, dx), p))
    return offsets


def _desloca(mascara, dy, dx):
    """Retorna a mascara deslocada: resultado[i, j] = mascara[i+dy, j+dx].
    As celulas que sairiam da grade viram False (o fogo nao atravessa a borda)."""
    com_borda = np.pad(mascara, 1, mode="constant", constant_values=False)
    h, w = mascara.shape
    return com_borda[1 + dy:1 + dy + h, 1 + dx:1 + dx + w]


def passo(grade, offsets, rng):
    """Calcula uma geracao (um passo de tempo) do automato."""
    nova = grade.copy()
    em_chamas = (grade == FOGO)
    arvores = (grade == ARVORE)

    # Chance de a arvore NAO pegar fogo, juntando a contribuicao de cada vizinho.
    # Se um vizinho na direcao (dy, dx) esta queimando, ele "ataca" com prob. p.
    log_sobrevive = np.zeros(grade.shape)
    for (dy, dx), p in offsets:
        if p <= 0:
            continue
        p_ef = min(p, 1 - 1e-9)  # evita log(0) quando p = 1
        vizinho_em_chamas = _desloca(em_chamas, dy, dx)
        log_sobrevive += vizinho_em_chamas * np.log(1 - p_ef)

    prob_pegar = 1 - np.exp(log_sobrevive)
    pegou_fogo = arvores & (rng.random(grade.shape) < prob_pegar)

    nova[pegou_fogo] = FOGO      # arvores atingidas comecam a queimar
    nova[em_chamas] = QUEIMADO   # quem estava queimando vira cinza
    return nova


def contar(grade):
    """Conta quantas celulas de cada estado existem na grade."""
    return (int(np.sum(grade == VAZIO)),
            int(np.sum(grade == ARVORE)),
            int(np.sum(grade == FOGO)),
            int(np.sum(grade == QUEIMADO)))


def simular(grade, offsets, rng, max_passos=5000, guardar_historico=False):
    """Roda o incendio ate o fogo se apagar. Retorna a grade final, a serie
    temporal das contagens e (opcionalmente) o historico das grades."""
    historico = [grade.copy()] if guardar_historico else None
    serie = []
    passos = 0
    while True:
        serie.append(contar(grade))
        if not np.any(grade == FOGO) or passos >= max_passos:
            break
        grade = passo(grade, offsets, rng)
        passos += 1
        if guardar_historico:
            historico.append(grade.copy())
    return grade, np.array(serie), historico


def fracao_queimada(grade_inicial, grade_final):
    """Fracao da vegetacao inicial que terminou queimada (0 a 1)."""
    vegetacao_inicial = np.sum((grade_inicial == ARVORE) | (grade_inicial == FOGO))
    if vegetacao_inicial == 0:
        return 0.0
    return np.sum(grade_final == QUEIMADO) / vegetacao_inicial


def atravessou_floresta(grade_final):
    """Diz se o fogo chegou ate a coluna oposta (percolou pela paisagem)."""
    return bool(np.any(grade_final[:, -1] == QUEIMADO))


def rodar_animacao():
    """Mostra a animacao do incendio usando os parametros do topo do arquivo."""
    rng = np.random.default_rng(SEMENTE)
    grade = criar_floresta(TAMANHO, DENSIDADE, rng)
    grade = acender_fogo(grade, IGNICAO)
    offsets = montar_offsets(VIZINHANCA, PROB_PROPAGACAO, VENTO)

    fig, ax = plt.subplots()
    ax.set_title("Incendio Florestal - Automato Celular")
    ax.set_xticks([])
    ax.set_yticks([])
    imagem = ax.imshow(grade, cmap=MAPA_CORES, norm=NORMA, animated=True)

    rotulos = ["Vazio", "Arvore", "Fogo", "Queimado"]
    caixas = [plt.Rectangle((0, 0), 1, 1, fc=c) for c in CORES]
    ax.legend(caixas, rotulos, loc="upper left",
              bbox_to_anchor=(1.02, 1.0), borderaxespad=0)
    texto = ax.text(1.02, 0.05, "", transform=ax.transAxes, fontsize=9)

    estado = {"grade": grade, "passo": 0}

    def atualizar(_frame):
        if np.any(estado["grade"] == FOGO):
            estado["grade"] = passo(estado["grade"], offsets, rng)
            estado["passo"] += 1
        imagem.set_array(estado["grade"])
        texto.set_text(f"Passo: {estado['passo']}")
        return imagem, texto

    _ = FuncAnimation(fig, atualizar, frames=400, interval=60,
                      blit=False, repeat=False)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    rodar_animacao()
