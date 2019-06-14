from flask import *
from flaskext.mysql import MySQL
import requests
from flask_basicauth import BasicAuth
import time

app = Flask(__name__)

app.config['BASIC_AUTH_USERNAME'] = 'root'
app.config['BASIC_AUTH_PASSWORD'] = '12345678'

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '12345678'
app.config['MYSQL_DATABASE_DB'] = 'test_database'
app.config['MYSQL_DATABASE_HOST'] = '203.154.83.124'
app.config['MYSQL_DATABASE_PORT'] = 3306

mysql = MySQL()
mysql.init_app(app)
secure_my_api = BasicAuth(app)

conn = mysql.connect()

def toJson(data, columns):
    results = []
    for row in data:
        results.append(dict(zip(columns, row)))
    return results

@app.route('/users', methods=['POST'])
@secure_my_api.required
def create_table_user():
    try:
        receiver = request.get_json()
        cursor = conn.cursor()
        now = int(time.time())
        insert = """INSERT INTO  users(username, password, create_time)
                    values (%s, %s, %s)"""
        values = (receiver['username'], receiver['password'], now)
        cursor.execute(insert, values)

        query = """SELECT * FROM users where username = %s;"""
        query_word = (receiver['username'])
        cursor.execute(query, query_word)
        data = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        result_pool = toJson(data, columns)
        conn.commit()
        conn.close()
        Show_message(receiver['username'])
        return jsonify(result_pool)

    except Exception as e:
        print e
        conn.rollback()
        conn.close()
        return e

def Show_message(message):
    url = 'https://notify-api.line.me/api/notify'
    token = 'm1Ic52ow8sNaTV1utQiePqGnZp0CIVxWpVRSC6IQXzc'
    headers = {'content-type': 'application/x-www-form-urlencoded', 'Authorization': 'Bearer ' + token}
    r = requests.post(url, headers=headers, data={'message': message})
    print r.text
    return r.text

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000, threaded=True)