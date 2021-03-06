#### WEB
[APP 시연](https://youtu.be/sV3KIN0TWTY)
---
- 훈련된 모델은 [링크](https://drive.google.com/drive/folders/1xPkj4Xd5DrvpeoA0xjXK1k7Fm57E6zZF?usp=sharing)의 Image-Generator 또는 Korean-Story-Generator압축파일을 내려받아 사용할 수 있다.
---
> 텍스트 생성 모델, 이미지 생성 모델을 사용하는 웹.
>
> pdf, docx 파일 생성 코드 모듈화
> 
> 이메일 발송 코드 모듈화
> 
> 이미지 생성 기능 모듈화
> 
> 텍스트 생성 기능 모듈화
>
> fast API이용 웹 서비스 구현중
> - 모듈화한 기능들 순서에 맞게 배치하여 서비스 제공하도록 구현중
> 
> - 현재는 이미지 생성기능 부분을 제외한 모든부분의 기능을 연결 시킴
> 
> 이미지 생성기 연결 완료
> - 학습 데이터의 디스크립션이 전부 영어여서 사용자 입력 문장또한 영어로 해야한다는 문제점 해결
> 
> - 파파고 api이용 한국어 -> 영어 번역
> 
> 모든과정 정상적으로 수행되는것 확인
> 
---
> 이미지 생성 모델과 이야기 생성 모델의 훈련관련 사항은 각각 아래 링크를 참고하여 응용하면 된다.
> - [이미지 생성 모델 링크](https://github.com/PROJECT-RODY/Image-Generator)
> 
> - [이야기 생성 모델 링크](https://github.com/PROJECT-RODY/Korean-Story-Generator)
> 
> 현재 web와 app를 같은 fastAPI프레임워크로 처리하며 요청을 보내는 링크(주소)만 다르다.
> 
> app의 경우는 입력값을 전송, 서버에서 처리한 결과값을 화면에 표시하는 역할만 한다.
> 
> ### requirements.yaml 을 이용해 동일한 환경의 가상환경을 셋팅할 수 있다.
