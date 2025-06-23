from flask import Flask, request, send_file
import os

app = Flask(__name__)
BASE_DIR = '/srv/data'
BACKUP_FILE = os.path.join(BASE_DIR, 'backup.zip')

@app.route('/backup', methods=['GET'])
def download_backup():
    if not os.path.exists(BACKUP_FILE):
        return '', 404
    return send_file(BACKUP_FILE, mimetype='application/zip')

@app.route('/backup', methods=['POST'])
def upload_backup():
    os.makedirs(BASE_DIR, exist_ok=True)
    with open(BACKUP_FILE, 'wb') as f:
        f.write(request.get_data())
    return 'ok'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
