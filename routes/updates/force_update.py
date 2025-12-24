
from fastapi import APIRouter
from fastapi.responses import FileResponse, JSONResponse
import os

router = APIRouter(prefix="/api/force-update", tags=["Force Update"])

latest_apk_version = "1.0.8"
latest_apk_file = "app_ver_108.apk"


# GET /api/force-update - Return the latest APK file info (URL, version, filename)
@router.get('/')
def get_force_update():
    response = {
        "apk_url": "/api/force-update/download-apk/" + latest_apk_file,
        "version": latest_apk_version,
        "apk_file": latest_apk_file
    }
    return response


# GET /api/force-update/download-apk/{filename} - Serve a specific APK file from the apk-builds directory
@router.get('/download-apk/{filename}')
def download_apk(filename: str):
    apk_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'apk-builds')
    file_path = os.path.join(apk_dir, filename)
    if not os.path.isfile(file_path):
        return JSONResponse({"error": "File not found"}, status_code=404)
    return FileResponse(path=file_path, filename=filename, media_type='application/vnd.android.package-archive')


# GET /api/force-update/download-apk - Download the latest APK file as an attachment
@router.get('/download-apk')
def download_apk_latest():
    filename = latest_apk_file
    apk_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'apk-builds')
    file_path = os.path.join(apk_dir, filename)
    if not os.path.isfile(file_path):
        return JSONResponse({"error": "File not found"}, status_code=404)
    return FileResponse(path=file_path, filename=filename, media_type='application/vnd.android.package-archive')