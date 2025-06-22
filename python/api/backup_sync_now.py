from python.helpers.api import ApiHandler
from flask import Request, Response
from python.helpers import settings, backup_sync

class BackupSyncNow(ApiHandler):
    async def process(self, input: dict, request: Request) -> dict | Response:
        set = settings.get_settings()
        if not set["backup_enabled"] or not set["backup_url"]:
            return {"status": "disabled"}
        ok = backup_sync.upload_backup(set["backup_url"])
        return {"status": "ok" if ok else "error"}
