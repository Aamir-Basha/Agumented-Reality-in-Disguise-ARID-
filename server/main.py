from flask import Flask, request, jsonify, render_template
import psycopg2
from psycopg2 import sql, OperationalError

app = Flask(__name__)

db_config = {
    'host': 'localhost',
    'user': 'amerbasha',
    'password': '998',
    'database': 'mydatabase'
}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/search', methods=['POST'])
def search():
    plaintext = request.form.get('search_text')
    add_to_db = request.form.get('add_to_db')

    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        sql_select = sql.SQL("SELECT hidden_text, mon_id FROM mono3 WHERE plain_text = %s")
        cursor.execute(sql_select, (plaintext,))
        result_select = cursor.fetchall()

        if result_select:
            row = result_select[0]
            hidden_text = row[0]
            mon_id = row[1]
            
            response = {
                'encrypted_msg': hidden_text,
                'mon_id': mon_id
            }
            return jsonify(response)
        else:
            if add_to_db == 'yes':
                hidden_text = request.form.get('hidden_text')
                mon_id = request.form.get('mon_id')
    
                sql_insert = sql.SQL("INSERT INTO mono3 (mon_id, plain_text, hidden_text) VALUES (%s, %s, %s)")
                cursor.execute(sql_insert, (mon_id, plaintext, hidden_text))
                conn.commit()
                return "Successfully added the data."
            else:
                return f"No hidden text found for plaintext: {plaintext}"
    except OperationalError as e:
        return f"Error: {e}"
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, debug=True)
