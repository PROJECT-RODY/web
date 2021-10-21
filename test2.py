import json
from pororoIG.Pororo_Generator import pororo_GAN
import torch

pororo_g = pororo_GAN()
# cap = "Pororo is on a land covered with snow. Pororo starts to sweep off the snow around it."

# cap = "Pororo is on the ground covered with snow. Pororo starts to sweep the eyes around him."

# cap = "Pororo is walking with his friends. Pororo is on the ground covered with snow. Pororo starts to sweep off the snow around it"

# Pororo starts walking with friends
# Pororo starts walking around with his friends.

# cap = "Pororo is on the snow-covered ground. Pororo starts to walk around. Pororo looks around."
# cap = "Pororo is on the snow-covered ground. Pororo opens his mouth and moves his arms fast."
# cap = "Pororo is on the snow-covered ground. Pororo is blocking his ears and opening his mouth."
cap=''
idx = '16'
# pororo_g.generate(cap, idx)

while True:
    try:
        cap = input("입력\n")
        pororo_g.generate(cap, idx)
    except :
        break