import s3fs
import zipfile
import os


import urllib.request
import zipfile
import os

def load_data_from_s3(project_dir, s3_path, endpoint_url="https://minio.lab.sspcloud.fr"):
    zip_path = os.path.join(project_dir, "data/history.zip")
    extract_path = os.path.join(project_dir, "data/historique/")
    
    os.makedirs(os.path.dirname(zip_path), exist_ok=True)
    os.makedirs(extract_path, exist_ok=True)
    
    url = f"{endpoint_url}/{s3_path}"
    urllib.request.urlretrieve(url, zip_path)
    
    with zipfile.ZipFile(zip_path, "r") as z:
        z.extractall(extract_path)
    
    print(os.listdir(extract_path))
    return extract_path