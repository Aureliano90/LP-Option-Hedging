import time
import numpy as np
import matplotlib.pyplot as plt

mu = 0
n = 200
s = 100
sigma = 2
t = time.time()

x = np.arange(n+1)
f = np.zeros(s, dtype=int)
var = np.zeros(s)

fig = plt.figure(figsize=(16, 8))
ax = fig.add_subplot()
fig.subplots_adjust(top=0.85)

ax.set_title("Simulations of Brownian Motion", fontsize=14)
ax.set_xlabel('t')
ax.set_ylabel('x')
ax.set(xlim=(0, n + 1))

for i in range(s):
    np.random.seed()
    y = np.cumsum(np.concatenate(([0], sigma * (2 * (np.random.random(n) > 0.5 + 0.) - 1))))
    f[i] = y[-1]
    ax.scatter(x, y, s=4)

ax.text(10, 70, f"σ={sigma}, Avg={np.average(f):.2f}, Var={np.var(f):.2f}", fontsize=12)
plt.show()
