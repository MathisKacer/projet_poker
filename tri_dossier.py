import os
import re
import shutil



dossier_source = "bdd"
dossier_mains = "mains"
dossier_resumes = "resumes"


def trier_fichiers():
    """
    Trie les fichiers de mains de poker en fonction de leur type (mains ou résumés)
    et les déplace dans les dossiers appropriés.
    """

    for nom_fichier in os.listdir(dossier_source):

        chemin_initial = os.path.join(dossier_source, nom_fichier)

        if not nom_fichier.endswith(".txt"):
            continue

        if "Expresso" in nom_fichier and "_summary" in nom_fichier:
            chemin_destination = os.path.join(dossier_resumes, nom_fichier)

        elif "Expresso" in nom_fichier:
            chemin_destination = os.path.join(dossier_mains, nom_fichier)

        # 3. On déplace le fichier
        shutil.move(chemin_initial, chemin_destination)
