import s3fs

fs = s3fs.S3FileSystem(client_kwargs={"endpoint_url": "https://minio.lab.sspcloud.fr"})

# Uploader tout un dossier
import os
for fichier in os.listdir("mon_dossier/"):
    fs.put(f"mon_dossier/{fichier}", f"mathiskacer2/diffusion/mon_dossier/{fichier}")