import s3fs
import zipfile
import os

# Connexion S3
fs = s3fs.S3FileSystem(client_kwargs={"endpoint_url": "https://minio.lab.sspcloud.fr"})

# Télécharger le zip depuis S3
fs.get("mathiskacer2/diffusion/projet_poker/history.zip", "history.zip")

# Dézipper
with zipfile.ZipFile("history.zip", "r") as z:
    z.extractall("historique/")

print(os.listdir("historique/"))