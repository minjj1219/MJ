from flask import Flask, render_template, request, redirect, url_for
from modules import mod_sql
import pandas as pd

#플라스크라는 class에 
#__name__은 파일 이름
app = Flask(__name__)

#localhost로 접속, 밑에 함수 실행시켜서 응답
@app.route("/")
def index():
    return render_template("index.html")

#localhost/signup로 접속했을 때
#get은 데이터를 url을 통해 보냄
#post는 url에 보내지 않고 메세지 안에 숨겨서 보냄. 외부 유출x but 속도 상대적으로 느림
@app.route("/signup/", methods=["GET"])
def signup():
    return render_template("signup.html")
# render_template은 html파일을 답변으로 주는 역할

@app.route("/signup/", methods=["POST"])
def signup_2():
    #sql 쿼리문 실행 위해 cursor 이용
    _id = request.form["_id"]
    _password = request.form["_password"]
    _name = request.form["_name"]
    _phone = request.form["_phone"]
    _gender = request.form["_gender"]
    _age = request.form["_age"]
    _ads = request.form["_ads"]
    _regitdate = request.form["_regitdate"]
    sql = """
            INSERT INTO user_info VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s)
          """
    _values = [_id, _password, _name, _phone, _ads, _gender, _age, _regitdate]
    _db = mod_sql.Database()
    # 변수: 값 저장해주는 공간
    # class: 여러 함수, method 저장해놓는 공간
    # but 변수 지정안해주면 새로운 곳에 계속 다른 class 만들어냄
    # 그래서 특정 주소를 지정하기 위해 변수 만드는 것임
    _db.execute(sql, _values)
    # self부분은 _db에 저장되기 때문에 따로 쓰지 않아도 됨
    _db.commit()
    # 데이터베이스에 commit
    return redirect(url_for('index'))
    # index 함수 요청, 빈 url로 다시 돌아감

@app.route("/login", methods=["POST"])
# "/login"이라는 질문을 POST형식으로 던짐
def login():
    _id = request.form["_id"]
    _password = request.form["_password"]

    sql = """
          SELECT * FROM user_info WHERE ID=%s AND password=%s
          """
    _values = [_id,_password]
    # sql문의 변수와 순서 같아야함
    _db = mod_sql.Database()
    result = _db.executeAll(sql,_values)
    # 결과값을 받아올 변수 지정
    
    #fetchall: 결과값 받아오는 역할
    # db 변경사항 없으면 commit x
    print(result)
    
    #if len(result)==1 튜플 안 튜플이라 한개
    #존재하면 True
    if result:
        return render_template("welcome.html", 
                                name = result[0]["name"], 
                                id = result[0]["ID"])
    else:
        return redirect(url_for("index"))

@app.route("/update", methods=['GET'])
def update():
    id = request.args["_id"]
    print(id)
    sql = """
            SELECT * FROM user_info WHERE ID = %s        
        """
    # 기존 회원정보를 확인시켜주기 위해 전체 테이블 조회
    values = [id]
    _db = mod_sql.Database()
    result = _db.executeAll(sql,values)
    return render_template("update.html", info = result[0])
    # info라는 키값으로 dict형태 데이터 보내준다

@app.route("/update", methods=['POST'])
def update_2():
    _id = request.form["_id"]
    _password = request.form["_password"]
    _name = request.form["_name"]
    _phone = request.form["_phone"]
    _gender = request.form["_gender"]
    _age = request.form["_age"]
    _ads = request.form["_ads"]
    sql = """
            UPDATE user_info SET password = %s,
            name = %s,
            phone = %s,
            gender = %s,
            age = %s,
            ads = %s
            WHERE ID = %s
          """

    values = [_password, _name, _phone, _gender, _age, _ads, _id]
    # 순서 정확하게 맞추기!
    _db = mod_sql.Database()
    _db.execute(sql,values)
    _db.commit()
    
    return redirect(url_for('index'))
    # redirect: 주소를 불러오는 작업
    # url_for: 지정된 함수를 불러오는 역할
    # render_template: html을 불러오는 작업

@app.route("/delete", methods=['GET'])
def delete():
    _id = request.args["_id"]
    return render_template("delete.html", id=_id)
    # key = value

@app.route("/delete", methods=['POST'])
def delete_2():
    _id = request.form["_id"]
    _password = request.form["_password"]
    _db = mod_sql.Database()
    s_sql = """
            SELECT * FROM user_info WHERE ID = %s AND password = %s
            """
    d_sql = """
            DELETE FROM user_info WHERE ID=%s AND password=%s
            """
    _values = [_id, _password]
    result = _db.executeAll(s_sql,_values)
    if result:
        _db.execute(d_sql, _values)
        _db.commit()
        return redirect(url_for('index'))
    else:
        return "패스워드가 일치하지 않습니다"

@app.route("/view", methods=['GET'])
def _view():
    sql = """
          SELECT 
          user_info.name, 
          user_info.ads, 
          user_info.age, 
          ads_info.register_count
          FROM 
          user_info 
          LEFT JOIN 
          ads_info 
          ON 
          user_info.ads = ads_info.ads
          """
    _db = mod_sql.Database()
    result = _db.executeAll(sql)
    key = list(result[0].keys())
    return render_template("view.html", result=result, keys=key)




        
    # user_info left join ads_info -> 
    # columns -> user_info : name, ads, age / ads_info : register_count 쿼리문 작성
    # view.html을 render 쿼리문의 결과값을 데이터로 같이 보내주는 코드를 작성



    #DB 접속 select문을 사용 -> index page input ID, PASSWORD 받아와서
    #SELECT문으로 조회
    #결과 값이 존재하면 return "login" 존재x return "fail"
    #index.html 수정 main.py 수정

    #회원탈퇴
    #welcome.html -> /delete url로 접속 -> 로그인한 ID값을 같이 전송
    #delete -> password를 확인(delete.html 페이지 생성) -> id password가 db에 존재하면 delete
    #존재하지 않으면 패스워드가 맞지 않습니다. 메세지 페이지에 띄워주는 형식




app.run(port=80, debug=True)

