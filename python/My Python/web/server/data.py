from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
    #templates파일에 있는 index.html 불러오기

@app.route('/second/')
def second():
    _id = request.args.get("id")
    _pass = request.args.get("pass")
    print(_id,_pass)
    return render_template("second.html", id = _id, _pass=_pass)
    #입력받은 id값을 html과 같이 보내주겠다~

@app.route('/third/', methods=["POST"])
def third():
    _id = request.form['id']
    _pass = request.form['pass']
    print(_id,_pass)
    return "Hello"
    #post 형식은 url 직접 쳐서 접속 불가능

app.run