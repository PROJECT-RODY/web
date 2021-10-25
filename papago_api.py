import requests
import json

class papago():
    def __init__(self,):
        with open('./papago_info.json') as f:
            SETTING = json.load(f)

        self.client_id = SETTING['client_id'] # <-- client_id 기입
        self.client_secret = SETTING['client_secret'] # <-- client_secret 기입

    def get_translate(self, text):
        data = {'text' : text,
                'source' : 'ko',
                'target': 'en'}

        url = "https://openapi.naver.com/v1/papago/n2mt"

        header = {"X-Naver-Client-Id":self.client_id,
                "X-Naver-Client-Secret":self.client_secret}

        response = requests.post(url, headers=header, data=data)
        rescode = response.status_code

        if(rescode==200):
            send_data = response.json()
            trans_data = (send_data['message']['result']['translatedText'])
            return trans_data
        else:
            print("Error Code:" , rescode)


if __name__ == '__main__':
    t_papa = papago()
    
    cap_3 = "뽀로로는 눈으로 덮인 땅 위에 있습니다."
    trans = t_papa.get_translate(cap_3)
    print(trans)
    # 뽀로로는 입을 벌리고 팔을 빠르게 움직입니다., 뽀로로는 입을 벌리고 있습니다.    

    cap_4 = "뽀로로가 걸어 다니기 시작합니다."
    trans = t_papa.get_translate(cap_4)
    print(trans)

    cap_5 = "" # Pororo starts to walk around.
    cap_5 = "뽀로로가 주변을 둘러본다."
    trans = t_papa.get_translate(cap_5)
    print(trans)

    # Pororo is on the snow-covered ground. 뽀로로는 눈으로 덮인 땅 위에 있습니다.
    # Pororo is sliding down the snowy hill. 뽀로로가 눈 덮인 언덕을 미끄러져 내려가고 있습니다.
    # Pororo opens his mouth and moves his arms quickly. 뽀로로는 입을 벌리고 팔을 빠르게 움직입니다.
    
    # Pororo is on the snowy ground. Pororo is sliding down the snowy hill. Pororo opens his mouth and moves his arms quickly.