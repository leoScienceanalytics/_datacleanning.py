import pandas as pd
import numpy as np


s = pd.Series(list('abca'))
s = pd.get_dummies(s)
print(s)

f =pd.Series(list('abca'))
f = pd.get_dummies(f, dtype=int)
print(f)

print(pd.__version__)