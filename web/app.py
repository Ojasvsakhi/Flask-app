import os
from flask import Flask, jsonify

app = Flask(__name__)

def try_db_connect():
    try:
        import pymysql
    except Exception as e:
        return False, f"pymysql import error: {e}"

    host = os.environ.get('DB_HOST', 'db')
    user = os.environ.get('DB_USER', 'exampleuser')
    password = os.environ.get('DB_PASSWORD', 'examplepass')
    db = os.environ.get('DB_NAME', 'exampledb')

    try:
        conn = pymysql.connect(host=host, user=user, password=password, database=db, connect_timeout=5)
        with conn.cursor() as cur:
            cur.execute('SELECT NOW();')
            res = cur.fetchone()
        conn.close()
        return True, str(res)
    except Exception as e:
        return False, str(e)

@app.route('/')
def index():
    ok, info = try_db_connect()
    return jsonify({
        'message': 'Hello from Flask in Docker!',
        'db_connection': 'ok' if ok else 'failed',
        'db_info': info
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
