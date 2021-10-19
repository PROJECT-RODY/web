import json
from KoSG import main
import torch
import json
from pororoIG.Pororo_Generator import pororo_GAN


with open('./KoSG/cfg/config_json.json') as f:
    cfg = json.load(f)
print(cfg)

pororo_gpt2 = main.pororo_gtp2(cfg)
model, vocab_b_obj = pororo_gpt2.model, pororo_gpt2.vocab_b_obj
vocab, sentencepieceTokenizer = vocab_b_obj.get_vocab(), vocab_b_obj.tokenize

text = input("문장 입력")

model.eval()
revers_vocab = {v:k for k,v in vocab.items()}
text = text+' : '
# text = '나뭇꾼'+' : '
input_ids = vocab_b_obj.encode(text)
gen_ids = model.generate(torch.tensor([input_ids]),
                        max_length=128,
                        repetition_penalty=2.0,
                        pad_token_id=vocab_b_obj.pad_token_id,
                        eos_token_id=vocab_b_obj.eos_token_id,
                        bos_token_id=vocab_b_obj.bos_token_id,
                        use_cache=True)
generated = vocab_b_obj.decode(gen_ids[0,:].tolist())
print(generated)



pororo_g = pororo_GAN()
cap = "Pororo is on a land covered with snow. Pororo starts to sweep off the snow around it."
idx = 9

pororo_g.generate(cap, idx)