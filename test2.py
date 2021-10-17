import json
from pororoIG.Pororo_Generator import pororo_GAN
import torch

pororo_g = pororo_GAN()
cap = "Pororo is on a land covered with snow. Pororo starts to sweep off the snow around it."
idx = 9

pororo_g.generate(cap, idx)