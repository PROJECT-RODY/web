import json
from pororoIG.Pororo_Generator import pororo_GAN
import torch

pororo_g = pororo_GAN()
# cap = "Pororo is on a land covered with snow. Pororo starts to sweep off the snow around it."

# cap = "Pororo is on the ground covered with snow. Pororo starts to sweep the eyes around him."

# cap = "Pororo is walking with his friends. Pororo is on the ground covered with snow. Pororo starts to sweep off the snow around it"

# Pororo starts walking with friends
# Pororo starts walking around with his friends.

cap = "Pororo is on the snow-covered ground. Pororo starts to walk around. Pororo looks around."
idx = '16'
pororo_g.generate(cap, idx)
