from flask import Flask, render_template, send_file
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def index():
    return  render_template('index.html')

@app.route('/corona/')
def corona():
    corona_df = pd.read_csv('corona.csv')
    corona_df.columns = ["인덱스", "등록일시", "사망자", 
                         "확진자", "게시글번호", "기준일",
                         "기준시간","수정일시", "누적 의심자", "누적확진률"]
    corona_df.sort_values("등록일시", inplace=True)
    corona_df["일일 확진자"] = (corona_df["확진자"] - corona_df["확진자"].shift()).fillna(0)
    corona_df["일일 사망자"] = corona_df["사망자"].diff().fillna(0)
    corona_df.drop(['인덱스', '기준일', '게시글번호', '기준시간', '수정일시'], axis=1, inplace=True)
    corona_df.reset_index(drop=True, inplace=True)
    corona_dict = corona_df.head(10).to_dict()
    cnt = len(corona_dict["등록일시"].keys())
    #cnt = len(corona_df.head(10))

    return render_template('corona.html', result = corona_dict, cnt = cnt)
    #corona.html에서 corona_dict 데이터를 사용할 것임
    #<주의> html에서는 result 변수 이름을 써야함

@app.route("/img/")
def img():
    corona_df = pd.read_csv('corona.csv')
    corona_df.columns = ["인덱스", "등록일시", "사망자", 
                         "확진자", "게시글번호", "기준일",
                         "기준시간","수정일시", "누적 의심자", "누적확진률"]
    corona_df.sort_values("등록일시", inplace=True)
    corona_df["일일 사망자"] = corona_df["사망자"].diff().fillna(0)
    decide_cnt = corona_df.head(10)["일일 사망자"].values.tolist()
    state_dt = corona_df.head(10)["등록일시"].values.tolist()
    print(decide_cnt)
    plt.plot(state_dt, decide_cnt)
    img_1 = BytesIO()
    plt.savefig(img_1, format='png', dpi=200)
    img_1.seek(0)
    # dpi 그림에 대한 질

    return send_file(img_1, mimetype ='image/png')

    #웹은 return 값을 보여줌, show로만 하면 새 창


app.run