# Importation des modules
import matplotlib.pyplot as plt
import numpy as np
import pytest
try:
    from algorithmie_fct import *
except:
    pass

import algorithmie_corr

# Série harmonique

x_axis = np.linspace(50, 100, 51, dtype=int)
y_axis = np.empty(x_axis.shape)

for i in range(x_axis.size):
    y_axis[i] = serie_harmonique(x_axis[i])

plt.plot(x_axis, y_axis)
plt.legend(['Harmonique'])
plt.show()

# Factoriel

#print(np.math.factorial(50))

# Correction
#pytest.main(['-q', '--tb=long', 'algorithmie_corr.py'])