from flask import Flask, render_template, request, redirect, url_for, session
import db, string, random
from datetime import timedelta

app = Flask(__name__)
app.secret_key = ''.join(random.choices(string.ascii_letters, k=256))

@app.route('/', methods = ['GET'])
def index():
    msg = request.args.get('msg') # Redirectされた時のパラメータ受け取り
    
    if msg == None:
        #通常のアクセルの場合
        return render_template('index.html')
    else:
        # redister_exe()からredirectされた場合
        return render_template('index.html', msg=msg)

@app.route('/', methods = ['POST'])
def login():
    user_name = request.form.get('username')
    mail = request.form.get('mail')
    password = request.form.get('password')
    #ログイン判定
    if db.login(user_name,mail, password):
        session['user'] = True        #sessionにキー:'user', バリュー:Trueを追加
        session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes=1)
        return redirect(url_for('admin'))
    else:
        error = 'ユーザー名またはパスワードが違います。'
        input_data = {'user_name':user_name, 'password':password}
        return render_template('index.html', error=error, data = input_data)
    

@app.route('/admin', methods=['GET'])
def admin():
    # sessionにキー:'user'があるか判定
    if 'user' in session:
        return render_template('admin.html')  # sessionがあればmypage.htmlを表示 
    else:
        return redirect(url_for('index'))   #sessionがなければログイン画面にリダイレクト
    
@app.route('/register')
def register_form():
    return render_template('register.html')

@app.route('/register_exe', methods=['POST'])
def register_exe():
    user_name=request.form.get('username')
    mail=request.form.get('mail')
    password=request.form.get('password')
# バリデーションチェック
    if user_name=='':
        error='ユーザ名が未入力です'
        return render_template('register.html', error=error)
    if password=='':
        error='パスワードが未入力です'
        return render_template('register.html', error=error)
    
    count=db.insert_user(user_name, mail, password)
    if count == 1:
        msg='登録が完了しました。'
        return redirect(url_for('index', msg=msg)) # Redirect でindex()にGet アクセス
        # return render_template('index.html', msg=msg)
    else:
        error='登録に失敗しました。'
        return render_template('register.html', error=error)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)