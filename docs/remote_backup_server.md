# Remote Backup Server

This simple Flask project exposes two REST endpoints used by Agent Zero to
synchronize settings and workspace files.

## Endpoints

- `GET /backup` – returns a ZIP archive with the latest backup.
- `POST /backup` – accepts a ZIP archive in the request body and stores it as the
  current backup.

## Example Implementation

```python
from flask import Flask, request, send_file
import os, io, zipfile

app = Flask(__name__)
BACKUP_FILE = 'data/backup.zip'

@app.route('/backup', methods=['GET'])
def download_backup():
    if not os.path.exists(BACKUP_FILE):
        return '', 404
    return send_file(BACKUP_FILE, mimetype='application/zip')

@app.route('/backup', methods=['POST'])
def upload_backup():
    os.makedirs('data', exist_ok=True)
    with open(BACKUP_FILE, 'wb') as f:
        f.write(request.get_data())
    return 'ok'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
```

Store the server separately and configure `backup_url` in Agent Zero to point to
its base URL (e.g. `http://your-vps:8000`).

## Docker Deployment

A ready-to-use `Dockerfile` is provided in `docker/backup_server/`.
To build and run the server:

```bash
# Build the image
cd docker/backup_server
docker build -t a0-backup-server .

# Start the server and persist backups in ./data
mkdir -p data
docker run -d -p 8000:8000 -v $(pwd)/data:/srv/data a0-backup-server
```

This container exposes the same `/backup` endpoints on port `8000`.
Configure `backup_url` in Agent Zero to point to your container's URL.
