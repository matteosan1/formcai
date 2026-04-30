import os

from datetime import datetime
from cloudinary.uploader import upload

def upload_file_cloudinary(file, numero_sentiero, i, prefix="foto"):
    _, estensione = os.path.splitext(file.name)
    file_name = f"{prefix}_{numero_sentiero}_{datetime.now().strftime('%Y%m%d_%H%M')}_{i}{estensione}"
    upload_result = upload(file, public_id=file_name, resource_type="auto", folder="form-manutenzione-sentieri", 
                            unique_filename=False, overwrite=True)
    file_url = upload_result.get("secure_url")
    return file_url
    