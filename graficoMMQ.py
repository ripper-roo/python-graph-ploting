### modules ###

import numpy as np 
import pandas as pd 
from matplotlib import pyplot as plt
from scipy import odr

### config ###

config = {
    'axes.spines.right': False,
    'axes.spines.top': False,
    'axes.edgecolor': '.4',
    'axes.labelcolor': '.0',
    'axes.titlesize': 'large',
    'axes.labelsize': 'medium',
    'figure.autolayout': True,
    'figure.figsize': (4.5, 3.5),
    'font.family': ['serif'],
    'font.size': 10.0,
    'grid.linestyle': '--',
    'legend.facecolor': '.9',
    'legend.frameon': True,
    'savefig.transparent': True,
    'text.color': '.0',
    'xtick.labelsize': 'small',
    'ytick.labelsize': 'small',
}

plt.style.use(['seaborn-v0_8-whitegrid', 'seaborn-v0_8-paper', 'seaborn-v0_8-muted', config])

### graphic data ###

# data for axes x and y, along with ther uncertainties dX and dY
d = {
        'y':    [],
        'dY':   [],
        'x':    [],
        'dX':   []
    }

data = pd.DataFrame(data=d)

### graphic plotting ###

x, dX = data['x'], data['dX']
y, dY = data['y'], data['dY']

# normal plotting
##plt.scatter(x, y, zorder=10, label='Dados Coletados')

# plotting with error bars
plt.errorbar(
    x, y, xerr=dX, yerr=dY,
    fmt='none', elinewidth=2/3, capsize=2, capthick=2/3, color='black',
    zorder=10, label='Dados Coletados'
)

# labels and titles
plt.title('Gráfico de tensão (V) por temperatura (T)')
plt.xlabel('T (ºC)')
plt.ylabel('V (mV)')

### linear regression ###

data = odr.RealData(x, y)
odreg = odr.ODR(data, odr.unilinear)
odreg.set_job(fit_type=2) # MMQ
ans = odreg.run()

a, b = ans.beta         # y = ax + b
da, db = ans.sd_beta    # a and b uncertainties
print("a = ", a, '\n', "b = ", b, '\n', "da = ", da, '\n', "db = ", db, sep='')

# define line graph limits
X = np.linspace(min(x), max(x), num=200)
Y = a * X + b

# and draw it through the points
formula = "y = " + str(round(a, 5)) + "x + " + str(round(b, 5))
plt.plot(X, Y, color='red', alpha=0.4, label=formula)

# show labels
plt.legend()

# save in an image
plt.savefig('grafico.png')