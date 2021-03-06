from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

import json
import torch
import re
import os

from KoSG import main
from pororoIG import Pororo_Generator

from send_email import email_sender
import papago_api
import save_pdf

pororo_g = Pororo_Generator.pororo_GAN()

# 이미지 생성기

# 이야기 생성기 모델 로드 시작.
with open('./KoSG/cfg/config_json.json') as f:
    cfg = json.load(f)

pororo_gpt2 = main.pororo_gtp2(cfg)
model, vocab_b_obj = pororo_gpt2.model, pororo_gpt2.vocab_b_obj
vocab, sentencepieceTokenizer = vocab_b_obj.get_vocab(), vocab_b_obj.tokenize
model.eval()
revers_vocab = {v:k for k,v in vocab.items()}
# 이야기 생성기 로드 끝

trans = papago_api.papago()# 파파고 번역기 로드


email_send = email_sender() # 이메일 발송

def story_generator(title, story, counter):
    if story != "":
        text = title + ' : ' + story
    else :
        text = title + ' : '

    input_ids = vocab_b_obj.encode(text)
    gen_ids = model.generate(torch.tensor([input_ids]),
                            max_length=30*counter,
                            repetition_penalty=2.0,
                            pad_token_id=vocab_b_obj.pad_token_id,
                            eos_token_id=vocab_b_obj.eos_token_id,
                            bos_token_id=vocab_b_obj.bos_token_id,
                            use_cache=True)
    generated = vocab_b_obj.decode(gen_ids[0,:].tolist())
    return generated[len(title)+3:]

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get('/create_pororo')
def form_post(request: Request):
    
    counter = 0
    if counter == 0:
        title_field = "제목을 입력하세요."
    result = 'Type a number' + str(counter)
    generate_img=""
    return templates.TemplateResponse('create_pororo.html', context={'request': request, 'title_field': title_field, 'counter' : counter, 'generate_img':generate_img})

@app.post('/create_pororo')
async def form_post(request: Request, pdf_path: str = Form(""), title_field: str = Form(""), story_field: str = Form(""), counter: int = Form(0), generate_img: str = Form(""), input_email: str = Form(""), situation_field_1: str = Form(""), situation_field_2: str = Form(""), situation_field_3: str = Form(""), error_m: str = Form("")):
    print(title_field, story_field, generate_img, pdf_path)

    if pdf_path != "":
        if input_email !="":
            
            if email_send.send_pdf([input_email], '"RODY로 작성한 이야기를 발송 하였습니다."', '완성된 이야기를 발송하였습니다.', pdf_path):
                return templates.TemplateResponse('create_pororo.html', context={'request': request, 'title_field': title_field, 'pdf_path': pdf_path, 'input_email' : input_email, 'error_m' : "이메일이 정상적으로 발송 되었습니다."})
            else :
                return templates.TemplateResponse('create_pororo.html', context={'request': request, 'title_field': title_field, 'pdf_path': pdf_path, 'input_email' : input_email, 'error_m' : "이메일 주소 오류 발생"})
        else :
            return templates.TemplateResponse('create_pororo.html', context={'request': request, 'title_field': title_field, 'pdf_path': pdf_path, 'input_email' : input_email, 'error_m' : "이메일을 입력하세요"})
    
    elif situation_field_1 != "" or situation_field_2 != "" or situation_field_3 != "":
        caps = [[situation_field_1],[situation_field_2],[situation_field_3]]
        situation = ''
        if situation_field_1 != '':
            situation += trans.get_translate(situation_field_1) + ' '

        if situation_field_2 != '':
            situation += trans.get_translate(situation_field_2) + ' '

        if situation_field_3 != '':
            situation += trans.get_translate(situation_field_3) + ' '
        
        img_name = 'text_2'

        generate_img = pororo_g.generate(situation[:-1], img_name) + ".png"
        return templates.TemplateResponse('create_pororo.html', context={'request': request, 'title_field': title_field, 'story_field': story_field, 'generate_img': generate_img})
        

    elif generate_img != "":
        pdf_path = save_pdf.create_pdf(title_field, story_field, generate_img)
        return templates.TemplateResponse('create_pororo.html', context={'request': request,'pdf_path': pdf_path, 'error_m' : "이메일을 입력하세요"})

    else :
        counter += 1
        story_field = story_generator(title_field, story_field, counter)
        story_field = re.sub(r'\<[^)]*\>', ' 이야기 끝!', story_field)
        return templates.TemplateResponse('create_pororo.html', context={'request': request, 'title_field': title_field, 'story_field': story_field, 'counter' : counter})



# @app.get('/create_pdf')
# async def form_post(request: Request):
#     return templates.TemplateResponse('create_pdf.html', context={'request': request,'pdf_path': pdf_path})


# @app.post('/create_pdf')
# async def form_post(request: Request, pdf_t: str = Form(""), pdf_s: str = Form(""), pdf_img: str = Form("")):
#     return templates.TemplateResponse('create_pdf.html', context={'request': request,'pdf_path': pdf_path})
 

@app.post('/create_story')
async def form_post(request: Request, user_title: str = Form(""), user_story: str = Form(""), user_counter: str = Form("")):
    print(user_title, user_story, user_counter)
    story_field = story_generator(user_title, user_story, int(user_counter))
    story_field = re.sub(r'\<[^)]*\>', ' 이야기 끝!', story_field)
    print(story_field)
    return story_field

@app.post('/create_image')
async def form_post(request: Request, situation_field_1: str = Form(""), situation_field_2: str = Form(""), situation_field_3: str = Form("")):
    print(situation_field_1, situation_field_2, situation_field_3)
    caps = [[situation_field_1],[situation_field_2],[situation_field_3]]
    situation = ''
    if situation_field_1 != '':
        situation += trans.get_translate(situation_field_1) + ' '

    if situation_field_2 != '':
        situation += trans.get_translate(situation_field_2) + ' '

    if situation_field_3 != '':
        situation += trans.get_translate(situation_field_3) + ' '
    
    img_name = 'text_5'

    generate_img = pororo_g.generate(situation[:-1], img_name) + ".png"

    return img_name

@app.post('/create_result')
async def form_post(request: Request, user_title: str = Form(""), user_story: str = Form(""), user_image: str = Form(""), user_email: str = Form("")):
    print(user_title, user_story, user_image, user_email)
    pdf_path = save_pdf.create_pdf_app(user_title, user_story, user_image)
    email_flg = email_send.send_pdf([user_email], '"RODY로 작성한 이야기를 발송 하였습니다."', '완성된 이야기를 발송하였습니다.', pdf_path)
    if email_flg:
        return "이메일이 정상적으로 발송 되었습니다."
    else:
        return "이메일 주소를 잘못 입력 하였습니다."

    