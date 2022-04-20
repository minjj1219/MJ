from flask import Flask

app = Flask(__name__)  #파일명 할당

@app.route('/')        #web -> 주소 -> 127.0.0.1:5000/, localhost:5000/    /하나는 기본주소
def index():
    return "Hello, World"   

#url을 추가해서 def 실행하려면?

@app.route('/second/')   #route: 다음에 나오는 함수 실행
# 뒤에 / 붙여주는 게 좋음
def second():
    return "Second Page"


app.run
