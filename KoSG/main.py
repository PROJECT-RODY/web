import random
import json
import torch
from torch.utils.data import DataLoader # 데이터로더
from gluonnlp.data import SentencepieceTokenizer 
from transformers import GPT2LMHeadModel, PreTrainedTokenizerFast
import gluonnlp
from tqdm import tqdm
import torch, gc
from KoSG.model.torch_gpt2 import GPT2Config, GPT2LMHeadModel # model폴더의 torch_gpt2.py의
from KoSG.util.data import FairyDataset

class pororo_gtp2():
    def __init__(self, cfg):
        self.train_flg = cfg['train_flg']
        self.data_file_path = cfg['data_file_path']
        self.batch_size = cfg['batch_size']
        self.epochs=cfg['epochs'] 
        self.save_model_path = cfg['save_model_path']
        self.ctx = 'cuda'
        self.model, self.vocab_b_obj= self.model_load("pororo_2.tar", cfg['kogpt2_config']) # aesop_checkpoint_2_110_3

    def model_load(self, checkpoint_name, kogpt2_config):
        if self.save_model_path == '':
            # KoGPT-2 언어 모델 학습을 위한 GPT2LMHeadModel 선언
            kogpt2model = GPT2LMHeadModel(config=GPT2Config.from_dict(kogpt2_config))
            # model_path로부터 다운로드 받은 내용을 load_state_dict으로 업로드
            kogpt2model.from_pretrained("skt/kogpt2-base-v2")
            # 추가로 학습하기 위해 .train() 사용
            kogpt2model.train()
        else :
            from transformers import GPT2LMHeadModel, PreTrainedTokenizerFast
            # Device 설정
            device = torch.device(self.ctx)
            # 저장한 Checkpoint 불러오기
            checkpoint = torch.load(self.save_model_path+checkpoint_name, map_location=device)
            # KoGPT-2 언어 모델 학습을 위한 GPT2LMHeadModel 선언
            kogpt2model = GPT2LMHeadModel(config=GPT2Config.from_dict(kogpt2_config))
            kogpt2model.load_state_dict(checkpoint['model_state_dict'])
            kogpt2model.eval() # 예측

        vocab_b_obj = PreTrainedTokenizerFast.from_pretrained("./KoSG/data/tokenizer", bos_token='<s>', eos_token='</s>', unk_token='<unk>',  pad_token='<pad>', mask_token='<mask>')

        return kogpt2model, vocab_b_obj
        
    def main(self,):
        
        vocab, sentencepieceTokenizer = self.vocab_b_obj.get_vocab(), self.vocab_b_obj.tokenize

        if self.train_flg: # GTP2 파인튜닝
            self.model.train()

            ### 학습 데이터 로드
            if self.data_file_path == None:
                self.data_file_path = '/content/drive/MyDrive/textG/data/dataset.txt'
            dataset = FairyDataset(self.data_file_path, vocab, sentencepieceTokenizer)
            fairy_data_loader = DataLoader(dataset, batch_size=self.batch_size)

            ### 파라미터 설정
            learning_rates = [1e-4, 5e-5, 2.5e-5, 2e-5]# 데이터 양이 너무 적어서 학습 단계별 학습률을 다르게 적용했다.
            criterion = torch.nn.CrossEntropyLoss()
            

            ### 메모리 초과뜨면 한번씩 지워주기 위해서 사용
            # gc.collect()
            # torch.cuda.empty_cache()


            ### 학습시작
            self.model.cuda()
            print('KoGPT-2 Transfer Learning Start')
            for learning_rate in learning_rates:
                optimizer = torch.optim.Adam(self.model.parameters(), lr=learning_rate)
                for epoch in range(self.epochs):
                    count = 0
                    print(epoch)
                    for data in fairy_data_loader:
                        optimizer.zero_grad()
                        data = torch.stack(data) # list of Tensor로 구성되어 있기 때문에 list를 stack을 통해 변환해준다.
                        data= data.transpose(1,0)
                        
                        data= data.to(self.ctx)
                
                        outputs = self.model(data, labels=data)
                        loss, logits = outputs[:2]
                        loss.backward()
                        optimizer.step()
                        if count %10 ==0:
                            print('epoch no.{} train no.{}  loss = {}' . format(epoch, count+1, loss))
                            # torch.save(model,save_path+'checkpoint_{}_{}.tar'.format(epoch,count))
                            # 추론 및 학습 재개를 위한 일반 체크포인트 저장하기

                        count += 1
                print("save!") # learning_rate 바뀔때마다 저장
                save_path = './checkpoint/'       
                torch.save({
                        'epoch': epoch,
                        'train_no': count,
                        'model_state_dict': self.model.state_dict(),
                        'optimizer_state_dict': optimizer.state_dict(),
                        'loss':loss
                    }, save_path+'gt_checkpoint_'+str(learning_rate)+'1.tar')

        else : # 텍스트 생성
            self.model.eval()
            revers_vocab = {v:k for k,v in vocab.items()}
            text = text+' : '
            # text = '나뭇꾼'+' : '
            input_ids = vocab_b_obj.encode(text)
            gen_ids = self.model.generate(torch.tensor([input_ids]),
                                    max_length=128,
                                    repetition_penalty=2.0,
                                    pad_token_id=vocab_b_obj.pad_token_id,
                                    eos_token_id=vocab_b_obj.eos_token_id,
                                    bos_token_id=vocab_b_obj.bos_token_id,
                                    use_cache=True)
            generated = vocab_b_obj.decode(gen_ids[0,:].tolist())
            print(generated)

if __name__ == '__main__':
    with open('/content/drive/MyDrive/textG/cfg/config_json.json') as f:
        cfg = json.load(f)
    main(cfg)

