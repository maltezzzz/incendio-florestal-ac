# -*- coding: utf-8 -*-
"""
Gera todas as figuras usadas no artigo, rodando o modelo de incendio florestal.
As imagens sao salvas na pasta 'figuras/'. Rode com:  python gerar_figuras.py
"""

import os
import numpy as np
import matplotlib
matplotlib.use("Agg")  # nao abre janela, so salva arquivos
import matplotlib.pyplot as plt

import incendio_florestal as fogo

PASTA = "figuras"
os.makedirs(PASTA, exist_ok=True)
plt.rcParams["figure.dpi"] = 150


def salvar(nome):
    caminho = os.path.join(PASTA, nome)
    plt.savefig(caminho, bbox_inches="tight")
    plt.close()
    print("  salvo:", caminho)


# ----------------------------------------------------------------------------
# FIGURA 1 - Evolucao espacial do incendio (varios instantes)
# ----------------------------------------------------------------------------
def figura_evolucao():
    print("Figura 1: evolucao espacial...")
    rng = np.random.default_rng(3)
    grade = fogo.criar_floresta(140, 0.65, rng)
    grade = fogo.acender_fogo(grade, "centro")
    offsets = fogo.montar_offsets("vonneumann", 1.0, None)

    _, _, historico = fogo.simular(grade, offsets, rng, guardar_historico=True)
    n = len(historico)
    indices = [0, n // 5, 2 * n // 5, 3 * n // 5, 4 * n // 5, n - 1]

    fig, eixos = plt.subplots(1, 6, figsize=(15, 2.8))
    for ax, k in zip(eixos, indices):
        ax.imshow(historico[k], cmap=fogo.MAPA_CORES, norm=fogo.NORMA)
        ax.set_title(f"t = {k}", fontsize=10)
        ax.set_xticks([]); ax.set_yticks([])
    fig.suptitle("Evolucao espacial do incendio (densidade = 0,65)", fontsize=12)
    salvar("fig1_evolucao.png")
    return historico


# ----------------------------------------------------------------------------
# FIGURA 2 - Serie temporal (quantidade de celulas de cada estado)
# ----------------------------------------------------------------------------
def figura_serie_temporal():
    print("Figura 2: serie temporal...")
    rng = np.random.default_rng(3)
    grade = fogo.criar_floresta(140, 0.65, rng)
    grade = fogo.acender_fogo(grade, "centro")
    offsets = fogo.montar_offsets("vonneumann", 1.0, None)

    _, serie, _ = fogo.simular(grade, offsets, rng)
    tempo = np.arange(len(serie))

    plt.figure(figsize=(7, 4.2))
    plt.plot(tempo, serie[:, fogo.ARVORE], label="Arvore", color=fogo.CORES[1])
    plt.plot(tempo, serie[:, fogo.FOGO], label="Fogo", color=fogo.CORES[2])
    plt.plot(tempo, serie[:, fogo.QUEIMADO], label="Queimado", color="black")
    plt.xlabel("Passo de tempo")
    plt.ylabel("Numero de celulas")
    plt.title("Evolucao temporal dos estados da floresta")
    plt.legend()
    plt.tight_layout()
    salvar("fig2_serie_temporal.png")


# ----------------------------------------------------------------------------
# FIGURA 3 - Transicao de percolacao (fracao queimada x densidade)
# ----------------------------------------------------------------------------
def figura_percolacao():
    print("Figura 3: transicao de percolacao (pode levar ~1 min)...")
    tamanho = 100
    repeticoes = 25
    densidades = np.linspace(0.05, 0.95, 19)

    media_queimada = []
    prob_atravessa = []
    for d in densidades:
        queimadas = []
        atravessou = []
        for r in range(repeticoes):
            rng = np.random.default_rng(1000 * int(d * 100) + r)
            grade = fogo.criar_floresta(tamanho, d, rng)
            grade = fogo.acender_fogo(grade, "esquerda")
            offsets = fogo.montar_offsets("vonneumann", 1.0, None)
            inicial = grade.copy()
            final, _, _ = fogo.simular(grade, offsets, rng)
            queimadas.append(fogo.fracao_queimada(inicial, final))
            atravessou.append(fogo.atravessou_floresta(final))
        media_queimada.append(np.mean(queimadas))
        prob_atravessa.append(np.mean(atravessou))
        print(f"    densidade={d:.2f}  queimada={np.mean(queimadas):.2f}  "
              f"atravessa={np.mean(atravessou):.2f}")

    media_queimada = np.array(media_queimada)
    prob_atravessa = np.array(prob_atravessa)
    p_c = 0.592746  # limiar de percolacao conhecido (rede quadrada, 4 vizinhos)

    # estimativa empirica do limiar: onde P(atravessar) cruza 0,5
    limiar_emp = np.interp(0.5, prob_atravessa, densidades)

    plt.figure(figsize=(7, 4.6))
    plt.plot(densidades, media_queimada, "o-", color="#B71C1C",
             label="Fracao da vegetacao queimada")
    plt.plot(densidades, prob_atravessa, "s--", color="#1565C0",
             label="Prob. de o fogo atravessar")
    plt.axvline(p_c, color="gray", linestyle=":",
                label=f"Limiar teorico $p_c$ = {p_c:.3f}")
    plt.xlabel("Densidade inicial da floresta")
    plt.ylabel("Fracao / Probabilidade")
    plt.title("Transicao de percolacao no incendio florestal")
    plt.legend()
    plt.tight_layout()
    salvar("fig3_percolacao.png")
    print(f"    -> limiar empirico estimado: {limiar_emp:.3f} "
          f"(teorico {p_c:.3f})")
    return limiar_emp


# ----------------------------------------------------------------------------
# FIGURA 4 - Efeito do aceiro (barreira que interrompe o fogo)
# ----------------------------------------------------------------------------
def figura_aceiro():
    print("Figura 4: efeito do aceiro...")
    tamanho = 120
    densidade = 0.75
    resultados = {}
    grades_finais = {}

    for cenario in ["sem", "com"]:
        rng = np.random.default_rng(5)
        grade = fogo.criar_floresta(tamanho, densidade, rng)
        if cenario == "com":
            # aceiro vertical: uma faixa de solo limpo no meio da floresta
            col = tamanho // 2
            grade[:, col - 1:col + 2] = fogo.VAZIO
        grade = fogo.acender_fogo(grade, "esquerda")
        offsets = fogo.montar_offsets("vonneumann", 1.0, None)
        inicial = grade.copy()
        final, _, _ = fogo.simular(grade, offsets, rng)
        resultados[cenario] = fogo.fracao_queimada(inicial, final)
        grades_finais[cenario] = final

    fig, eixos = plt.subplots(1, 2, figsize=(9, 4.6))
    titulos = {"sem": "Sem aceiro", "com": "Com aceiro"}
    for ax, cenario in zip(eixos, ["sem", "com"]):
        ax.imshow(grades_finais[cenario], cmap=fogo.MAPA_CORES, norm=fogo.NORMA)
        ax.set_title(f"{titulos[cenario]}\nvegetacao queimada = "
                     f"{resultados[cenario]*100:.0f}%", fontsize=11)
        ax.set_xticks([]); ax.set_yticks([])
    fig.suptitle("Efeito de um aceiro na contencao do incendio "
                 "(densidade = 0,75)", fontsize=12)
    salvar("fig4_aceiro.png")
    print(f"    -> queimada sem aceiro: {resultados['sem']*100:.0f}%  |  "
          f"com aceiro: {resultados['com']*100:.0f}%")
    return resultados


# ----------------------------------------------------------------------------
# FIGURA 5 - Efeito do vento
# ----------------------------------------------------------------------------
def figura_vento():
    print("Figura 5: efeito do vento...")
    tamanho = 180
    densidade = 0.65
    p_base = 0.55
    tempo_fixo = 60  # olhamos o incendio "no meio", ainda se espalhando
    cenarios = {"Sem vento": None,
                "Vento para leste": {"direcao": "leste", "forca": 0.40}}
    finais = {}
    fracoes = {}
    for nome, vento in cenarios.items():
        rng = np.random.default_rng(9)
        grade = fogo.criar_floresta(tamanho, densidade, rng)
        grade = fogo.acender_fogo(grade, "centro")
        offsets = fogo.montar_offsets("moore", p_base, vento)
        inicial = grade.copy()
        final, _, _ = fogo.simular(grade, offsets, rng, max_passos=tempo_fixo)
        finais[nome] = final
        fracoes[nome] = fogo.fracao_queimada(inicial, final)

    fig, eixos = plt.subplots(1, 2, figsize=(9, 4.8))
    for ax, nome in zip(eixos, cenarios.keys()):
        ax.imshow(finais[nome], cmap=fogo.MAPA_CORES, norm=fogo.NORMA)
        ax.set_title(f"{nome}\nqueimada em t={tempo_fixo}: "
                     f"{fracoes[nome]*100:.0f}%", fontsize=11)
        ax.set_xticks([]); ax.set_yticks([])
    fig.suptitle("Efeito do vento na propagacao do fogo "
                 "(mesmo instante de tempo, ignicao no centro)", fontsize=12)
    salvar("fig5_vento.png")
    print(f"    -> queimada sem vento: {fracoes['Sem vento']*100:.0f}%  |  "
          f"com vento: {fracoes['Vento para leste']*100:.0f}%")
    return fracoes


if __name__ == "__main__":
    print("Gerando figuras do artigo...\n")
    figura_evolucao()
    figura_serie_temporal()
    limiar = figura_percolacao()
    aceiro = figura_aceiro()
    vento = figura_vento()
    print("\nPronto! Todas as figuras estao na pasta 'figuras/'.")
