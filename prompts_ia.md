Prompts de IA utilizados

Este projeto foi feito com o apoio de uma IA, um assistente de programação. Abaixo estão os principais pedidos que eu fiz, na ordem em que aconteceram. O professor pediu que o texto dos prompts fosse incluído no material entregue.

1. Entendimento e escolha do tema

"Preciso fazer um projeto da disciplina de Autômatos Celulares. A entrega é um código de autômato celular mais um artigo científico, de 2 a 6 páginas, no formato Nature Scientific Reports, explicando por que o código é relevante e para que serve. Me ajude a escolher um tema clássico, reconhecido na literatura, diferente de agricultura e degradação do solo, que já foi usado por outro aluno."

Resultado: escolhi o modelo de incêndio florestal, de Drossel e Schwabe, que liga os autômatos celulares à teoria de percolação e tem forte relevância ambiental, como as queimadas na Amazônia, no Cerrado e no Pantanal.

2. Implementação do modelo

"Implemente em Python, com numpy e matplotlib, um autômato celular de incêndio florestal numa grade N por N com quatro estados: vazio, árvore, fogo e queimado. As regras são: fogo vira queimado no passo seguinte; árvore pega fogo a partir de vizinhos em chamas com uma probabilidade p por vizinho; permita escolher a vizinhança de von Neumann, com 4 vizinhos, ou de Moore, com 8. Inclua uma animação da propagação do fogo."

3. Vento

"Adicione um parâmetro de vento que aumente a probabilidade de o fogo se propagar na direção do vento. O vento deve apenas reforçar a propagação a favor dele, sem reduzir a propagação contra o vento, que é o comportamento fisicamente mais coerente."

4. Experimentos e figuras do artigo

"Crie um script que gere as figuras do artigo rodando o modelo: a evolução espacial do incêndio em vários instantes; a série temporal da quantidade de células de cada estado; a transição de percolação, com a fração queimada e a probabilidade de o fogo atravessar a floresta em função da densidade inicial, com média de várias repetições e comparação com o limiar teórico; o efeito de um aceiro na contenção do fogo; e o efeito do vento na forma da mancha queimada."

5. Calibração

"O experimento de vento não estava mostrando efeito porque o fogo morria na densidade que escolhi. Faça uma busca de parâmetros de densidade, probabilidade e força do vento para achar uma configuração em que o efeito do vento fique visível e o resultado seja robusto."

Resultado: a figura do vento passou a mostrar o incêndio num instante fixo de tempo, comparando uma mancha compacta, sem vento, com uma mancha alongada, com vento.

6. Redação do artigo

"Escreva o artigo científico em português no formato Nature Scientific Reports, com resumo, introdução, metodologia, resultados, discussão, conclusão e referências, entre 2 e 6 páginas, explicando a relevância do modelo e discutindo os resultados, principalmente a transição de percolação e as implicações para o manejo do fogo."

Ferramenta usada: assistente de IA baseado em modelo de linguagem grande. Todo o código foi revisado e executado na minha máquina para gerar os resultados apresentados.
