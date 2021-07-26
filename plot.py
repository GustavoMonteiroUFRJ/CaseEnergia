import matplotlib.pyplot as plt
import json
import sys
from dotmap import DotMap
import numpy as np

CONST_INPUT_MERCADO = 12 # quantidade de meses que o mercado tem preço;
CONST_INPUT_CENARIOS = 12 # quantidade de meses que foi projetado preço.

update_data = True


if update_data:
    # ATUALIZANDO OS DADOS DE INPUT #

    d = { # essa variavel existe apenas para ser um modelo. 
        "jan": 0,
        "feb": 0,
        "mar": 0,
        "abr": 0,
        "mai": 0,
        "jun": 0,
        "jul": 0,
        "ago": 0,
        "set": 0,
        "out": 0,
        "nov": 0,
        "dez": 0
    }

    cenarios = {'mu': {}, 'u': {}, 'n': {}, 's': {}, 'ms': {}} # De mu (Muito Umido) até ms (Muito Seco)
    mercado = {}

    with open('auxiliar.txt', 'r') as f:

        # Pega os valrores do mercado.
        num = np.fromfile(f, dtype=int, count=CONST_INPUT_MERCADO, sep=" ") 
        for mes, valor in zip(d, num):
            mercado[mes] = int(valor)

        # Pega os valrores previstos para cada cenario.
        for cenario in cenarios:
            num = np.fromfile(f, dtype=int, count=CONST_INPUT_CENARIOS, sep=" ")
            for mes, valor in zip(d, num):
                cenarios[cenario][mes] = int(valor)


    with open('input.json', 'r') as f:
        my_input = DotMap(json.load(f))

    my_input.mercado = mercado
    my_input.cenarios = cenarios

    with open('input.json', 'w') as f:
        json.dump(my_input, f, indent=4)


with open('input.json', 'r') as f:
    my_input = json.load(f)

my_input_dot = DotMap(my_input)

mes_corrente = my_input_dot.mes_corrent
plot_percent  = bool( my_input_dot.plot_percent)
precent_especifc = bool(my_input_dot.precent_especifc)
cenario_especifico = my_input_dot.cenrio_previsto
plot_legend = bool(my_input_dot.plot_legend)

CONST_LIMIT_SUPERIOR = 600
CONST_LIMIT_INFERIOR = 50

## PLOTANDO O GRAFICO ##


# Config plot #
map_cor = {'mu': '#7F71FD',
           'u': '#6EECEC',
           'n': '#85EF9E',
           's': '#E0E47D',
           'ms': '#FF9D3A',
           'default': '#FF8383'
           }
labels = list(my_input['mercado'].keys())
x = [i for i in range(len(labels))]
plt.xticks(x, labels)
plt.ylabel('PLD Futuro')
plt.ylabel('Meses')
plt.ylim([CONST_LIMIT_INFERIOR-5, CONST_LIMIT_SUPERIOR+5])
plt.xlim([0, 11])
plt.fill_between(x, CONST_LIMIT_SUPERIOR, y2=0, color=map_cor['default'])


# Plot mes corrente #
plt.vlines(labels.index(mes_corrente), CONST_LIMIT_INFERIOR, CONST_LIMIT_SUPERIOR)

# Plot cenarios #
cenarios = ['ms', 's', 'n', 'u', 'mu'] # Variavel para definidr ordem para o print fill_btween
for cenario in cenarios:
    y = list(my_input['cenarios'][cenario].values())
    plt.fill_between(x, y, y2=0, color=map_cor[cenario], label=cenario)


# Plot espectativa mercado #
plt.plot(list(my_input['mercado'].values()),
         color='black', linewidth=2, label='mercado')



if plot_percent:
    # plot percentage #
    mercado = list(my_input['mercado'].values())
    for cenario in cenarios:
        if not precent_especifc or  cenario == cenario_especifico:
            y = list(my_input['cenarios'][cenario].values())
            plt.scatter(x, y, c='black', s=2 )
            for i, valor in enumerate(y):
                note = ''.join((str(int(valor*100/mercado[i] -100)), '%'))
                plt.annotate(note, (x[i], y[i]))


if plot_legend:
    plt.legend()

plt.show()



