import asyncio
import os
import io
import zipfile
from urllib import request, parse
from python.helpers import files
from python.helpers.print_style import PrintStyle

WATCH_FOLDERS = ["tmp", "memory", "knowledge"]


def _collect_files() -> dict[str, float]:
    base = files.get_base_dir()
    mapping: dict[str, float] = {}
    for folder in WATCH_FOLDERS:
        path = files.get_abs_path(folder)
        if not os.path.exists(path):
            continue
        for root, _dirs, file_names in os.walk(path):
            for name in file_names:
                full = os.path.join(root, name)
                try:
                    mapping[os.path.relpath(full, base)] = os.path.getmtime(full)
                except FileNotFoundError:
                    pass
    return mapping


def _create_zip() -> bytes:
    base = files.get_base_dir()
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for rel, _ in _collect_files().items():
            abs_path = os.path.join(base, rel)
            if os.path.isfile(abs_path):
                zf.write(abs_path, rel)
    return buf.getvalue()


def _extract_zip(data: bytes):
    base = files.get_base_dir()
    buf = io.BytesIO(data)
    with zipfile.ZipFile(buf) as zf:
        zf.extractall(base)


def download_backup(url: str) -> bool:
    try:
        with request.urlopen(f"{url.rstrip('/')}/backup") as resp:
            if resp.status != 200:
                PrintStyle.error(f"Backup server error: {resp.status}")
                return False
            data = resp.read()
            _extract_zip(data)
            PrintStyle.debug("Backup downloaded")
            return True
    except Exception as e:
        PrintStyle.error(f"Download failed: {e}")
        return False


def upload_backup(url: str) -> bool:
    data = _create_zip()
    req = request.Request(
        f"{url.rstrip('/')}/backup",
        method="POST",
        data=data,
        headers={"Content-Type": "application/zip"},
    )
    try:
        with request.urlopen(req) as resp:
            if resp.status != 200:
                PrintStyle.error(f"Upload failed: {resp.status}")
                return False
            PrintStyle.debug("Backup uploaded")
            return True
    except Exception as e:
        PrintStyle.error(f"Upload error: {e}")
        return False


async def start(url: str):
    download_backup(url)
    previous = _collect_files()
    while True:
        await asyncio.sleep(30)
        current = _collect_files()
        if current != previous:
            upload_backup(url)
            previous = current
