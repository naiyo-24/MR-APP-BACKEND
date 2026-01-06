
from fastapi import APIRouter
from fastapi.responses import FileResponse, JSONResponse
from pathlib import Path

router = APIRouter(prefix="/api/force-update", tags=["Force Update"])

latest_apk_version = "1.0.13"
latest_apk_file = "mr_app_113.apk"


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
    apk_dir = Path(__file__).resolve().parents[2] / 'apk-builds'
    file_path = apk_dir / filename
    if not file_path.is_file():
        return JSONResponse({"error": "File not found"}, status_code=404)
    return FileResponse(path=str(file_path), filename=filename, media_type='application/vnd.android.package-archive')


# GET /api/force-update/download-apk - Download the latest APK file as an attachment
@router.get('/download-apk')
def download_apk_latest():
    filename = latest_apk_file
    apk_dir = Path(__file__).resolve().parents[2] / 'apk-builds'
    file_path = apk_dir / filename
    if not file_path.is_file():
        return JSONResponse({"error": "File not found"}, status_code=404)
    return FileResponse(path=str(file_path), filename=filename, media_type='application/vnd.android.package-archive')