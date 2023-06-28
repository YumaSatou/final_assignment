import os, psycopg2, string, random, hashlib

# ランダムなソルトを生成
def get_salt():
    # 文字列の候補(英大小文字 + 数字)
    charset = string.ascii_letters + string.digits
    
    # charsetからランダムに30文字取り出して結合
    salt = ''.join(random.choices(charset, k=30))
    return salt

def get_hash(password, salt):
    b_pw = bytes(password, "utf-8")
    b_salt = bytes(password, "utf-8")
    hashed_password = hashlib.pbkdf2_hmac('sha256', b_pw, b_salt, 1000).hex()
    return hashed_password

def get_connection():
    url = os.environ['DATABASE_URL']
    connection = psycopg2.connect(url)
    return connection

def insert_user(user_name, password):
    sql = 'INSERT INTO admin_account VALUES (default, %s, %s, %s)'
    
    salt = get_salt()
    hashed_password = get_hash(password, salt)
    
    try: #例外処理
        connection = get_connection()
        cursor = connection.cursor()
        
        cursor.execute(sql, (user_name, hashed_password, password))
        count = cursor.rowcount # 更新件数を取得
        connection.commit()
        
    except psycopg2.DatabaseError:  # Javaでいうcatch 失敗した時の処理をここに書く
        count = 0 #例外が発生したら0をreturnする
        
    finally: # 成功しようが、失敗しようが、closeする
        cursor.close()
        connection.close()
        
    return count

def login(user_name,password):
    sql = "SELECT hashed_password, salt FROM admin_account WHERE name = %s"
    flg = False
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, (user_name,))
        user = cursor.fetchone()
        if user != None:
            #SQLの結果からソルトを取得
            salt = user[1]
            
            #DBから取得したソルト+y入力したパスワードからハッシュ値を取得
            hashed_password = get_hash(password,salt)
            
            #生成したハッシュ値とDBから取得したハッシュ値を比較する
            if hashed_password == user[0]:
                flg = True
    except psycopg2.DatabaseError:
        flg = False
    finally:
        cursor.close()
        connection.close()
    return flg

def select_all_books():
    connection = get_connection()
    cursor = connection.cursor()
    sql = "SELECT title, author, publisher FROM books_list"
    
    cursor.execute(sql)
    rows = cursor.fetchall()
    
    cursor.close()
    connection.close()
    return rows

def insert_book(title,author,publisher):
    connection = get_connection()
    cursor = connection.cursor()
    sql = "INSERT INTO books_list VALUES (default, %s, %s, %s)"
    
    cursor.execute(sql,(title,author,publisher))
    connection.commit()
    cursor.close()
    connection.close()
    