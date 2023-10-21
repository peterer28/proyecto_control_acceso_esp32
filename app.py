from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name)

# Database configuration (replace with your actual database details)
db_config = {
    'dbname': 'mydatabase',
    'user': 'fl0user',
    'password': 'RXbdasv36qrt',
    'host': 'ep-shy-thunder-24509743.us-east-2.aws.neon.fl0.io',
    'port': '5432'
}

def authorize_access(user_name, access_key):
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()
    
    # Query the user_authorization table
    cursor.execute("SELECT auth FROM user_authorization WHERE user_name = %s AND acces_key = %s", (user_name, access_key))
    result = cursor.fetchone()
    
    if result:
        auth = result[0]
        if auth:
            # Log the access event
            cursor.execute("INSERT INTO access_log (user_name) VALUES (%s)", (user_name,))
            conn.commit()
            conn.close()
            return True

    conn.close()
    return False

@app.route('/authorize', methods=['GET'])
def authorize():
    user_name = request.args.get('user_name')
    access_key = request.args.get('access_key')
    
    if user_name and access_key:
        if authorize_access(user_name, access_key):
            return jsonify({'aut': 'approved', 'access_key': 'xxxxxxxx'})
        else:
            return jsonify({'aut': 'denied'})
    else:
        return jsonify({'error': 'Invalid request parameters'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)  # Change host and port as needed
