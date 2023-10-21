from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name)

# Database configuration
db_config = {
    'dbname': 'your_db_name',
    'user': 'your_db_user',
    'password': 'your_db_password',
    'host': 'your_db_host',
    'port': 'your_db_port'
}

def authorize_access(user, key):
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()
    
    # Query the user_authorization table
    cursor.execute("SELECT authorization FROM user_authorization WHERE user = %s AND key = %s", (user, key))
    result = cursor.fetchone()
    
    if result:
        authorization = result[0]
        if authorization:
            # Log the access event
            cursor.execute("INSERT INTO access_log (user) VALUES (%s)", (user,))
            conn.commit()
            conn.close()
            return True

    conn.close()
    return False

@app.route('/authorize', methods=['GET'])
def authorize():
    user = request.args.get('user')
    key = request.args.get('key')
    
    if user and key:
        if authorize_access(user, key):
            return jsonify({'aut': 'approved', 'access_key': 'xxxxxxxx'})
        else:
            return jsonify({'aut': 'denied'})
    else:
        return jsonify({'error': 'Invalid request parameters'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)  # Change host and port as needed
