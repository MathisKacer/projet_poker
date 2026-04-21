import s3fs
import zipfile
import os


def load_data_from_s3(project_dir, s3_path, endpoint_url="https://minio.lab.sspcloud.fr"):
    zip_path = os.path.join(project_dir, "data/history.zip")
    extract_path = os.path.join(project_dir, "data/historique/")
    
    os.makedirs(extract_path, exist_ok=True)
    
    fs = s3fs.S3FileSystem(client_kwargs={"endpoint_url": endpoint_url})
    fs.get(s3_path, zip_path)
    
    with zipfile.ZipFile(zip_path, "r") as z:
        z.extractall(extract_path)
    
    print(os.listdir(extract_path))
    return extract_path