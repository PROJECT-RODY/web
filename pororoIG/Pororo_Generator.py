# -*- encoding: utf-8 -*-
from __future__ import print_function
import multiprocessing

import os
import io
import sys
import time
import random
import pprint
import datetime
import dateutil.tz
import argparse
import torch
import torch.optim as optim
import numpy as np
from PIL import Image
from pororoIG.miscc.config import cfg, cfg_from_file
from pororoIG.sync_batchnorm import DataParallelWithCallback
from pororoIG.DAMSM import RNN_ENCODER, CNN_ENCODER
from pororoIG.model import NetG
from nltk.tokenize import RegexpTokenizer # 추가
import pickle

class pororo_GAN():
    def __init__(self,):
        self.gpu_id = 0
        self.cfg_file = './pororoIG/cfg/pororo.yml'
        self.data_dir = './pororoIG/data/pororos'
        self.manualSeed = 100

        # self.args = parse_args()
        if self.cfg_file is not None:
            cfg_from_file(self.cfg_file)
        

        if self.gpu_id == -1:
            cfg.CUDA = False
        else:
            cfg.GPU_ID = self.gpu_id

        if self.data_dir != '':
            cfg.DATA_DIR = self.data_dir
        print('Using config:')
        pprint.pprint(cfg)

        if not cfg.TRAIN.FLAG:
            self.manualSeed = 100
        elif self.manualSeed is None:
            self.manualSeed = 100

        print("seed now is : ", self.manualSeed)
        random.seed(self.manualSeed)
        np.random.seed(self.manualSeed)
        torch.manual_seed(self.manualSeed)

        if cfg.CUDA:
            torch.cuda.manual_seed_all(self.manualSeed)

        ##########################################################################
        now = datetime.datetime.now(dateutil.tz.tzlocal())

        with open("./pororoIG/data/captions.pickle", 'rb') as f: # 수정
            x = pickle.load(f)
        self.word2idx = x[2]
        self.n_words = len(x[1])

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.netG = NetG(cfg.TRAIN.NF, 100).to(self.device)
        self.netG = DataParallelWithCallback(self.netG)
        
        self.text_encoder = RNN_ENCODER(self.n_words, nhidden=cfg.TEXT.EMBEDDING_DIM)
        state_dict = torch.load(cfg.TEXT.DAMSM_NAME, map_location=lambda storage, loc: storage)
        self.text_encoder.load_state_dict(state_dict)
        
        self.text_encoder.cuda()
        for p in self.text_encoder.parameters():
            p.requires_grad = False
        self.text_encoder.eval()

        optimizerG = torch.optim.Adam(self.netG.parameters(), lr=0.0001, betas=(0.0, 0.9))

        model_dir = cfg.TRAIN.NET_G
        istart = cfg.TRAIN.NET_G.rfind('_') + 1
        iend = cfg.TRAIN.NET_G.rfind('.')
        start_epoch = int(cfg.TRAIN.NET_G[istart:iend])
        num_epoch = 120
        model_dir = model_dir.replace(str(start_epoch), str(num_epoch))
        start_epoch = num_epoch
        
        # 학습된 netG불러오는 과정 끝
        self.netG.load_state_dict(torch.load(model_dir))
        self.netG.eval()
    
    def text2cap(self, s): # 추가
        tokenizer = RegexpTokenizer(r'\w+')
        s = s.replace("\ufffd\ufffd", " ")
        tokens = tokenizer.tokenize(s.lower())
        tokens_new = []
        for t in tokens:
            t = t.encode('ascii', 'ignore').decode('ascii')
            if len(t) > 0:
                tokens_new.append(t)

        rev=[]
        for w in tokens_new:
            if w in self.word2idx:
                rev.append(self.word2idx[w])
        # rev.append(0)  # do not need '<end>' token
        while len(rev) < 18:
            rev.append(0)
        
        return torch.tensor([rev]), torch.tensor([len(rev)])

    def generate(self, cap, img_name):
        captions, cap_lens = self.text2cap(cap)
        input_sen_size = 1
        
        hidden = self.text_encoder.init_hidden(input_sen_size)
        
        captions = captions.to(self.device)
        cap_lens = cap_lens.to(self.device)

        
        _, sent_emb = self.text_encoder(captions, cap_lens, hidden)
        
        sent_emb = sent_emb.detach()
        
        # idx = 0
        with torch.no_grad():
            noise = torch.randn(input_sen_size, 100)
            noise = noise.to(self.device)
            print(len(noise[0]), noise)
            fake_imgs, _ = self.netG(noise, sent_emb)
        
        #s_tmp = '%s/single/%s' % (save_dir, keys[j])
        s_tmp = './static/user_image/'

        im = fake_imgs[0].data.cpu().numpy()
        # [-1, 1] --> [0, 255]
        im = (im + 1.0) * 127.5
        im = im.astype(np.uint8)
        im = np.transpose(im, (1, 2, 0))
        im = Image.fromarray(im)
        # idx += 1
        #fullpath = '%s_%3d.png' % (s_tmp,i)
        fullpath = '%s%s.png' % (s_tmp, img_name)
        im.save(fullpath)
        print('%s에 이미지 생성' % (fullpath))
        return s_tmp+img_name

if __name__ == '__main__':
    pororo_g = pororo_GAN()
    cap = "Pororo is on a land covered with snow. Pororo starts to sweep off the snow around it."
    idx = '9'

    pororo_g.generate(cap, idx)