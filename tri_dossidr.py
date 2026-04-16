import os
import re
import shutil



dossier_source = "bdd"
dossier_mains = "mains"
dossier_resumes = "resumes"


def trier_fichiers():

    for nom_fichier in os.listdir(dossier_source):

        chemin_initial = os.path.join(dossier_source, nom_fichier)

        if not nom_fichier.endswith(".txt"):
            continue

        if "Expresso" in nom_fichier and "_summary" in nom_fichier:
            chemin_destination = os.path.join(dossier_resumes, nom_fichier)
            print(f"Déplacement du résumé : {nom_fichier}")

        elif "Expresso" in nom_fichier:
            chemin_destination = os.path.join(dossier_mains, nom_fichier)
            print(f"Déplacement de la main : {nom_fichier}")

        # 3. On déplace le fichier
        shutil.move(chemin_initial, chemin_destination)

# Exécution
trier_fichiers()
print("Terminé ! Tous les fichiers ont été classés.")
