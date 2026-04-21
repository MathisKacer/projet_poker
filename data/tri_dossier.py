import os
import shutil


def trier_fichiers(dossier_source, dossier_mains, dossier_resumes):
    """
    Trie les fichiers de mains de poker en fonction de leur type (mains ou résumés)
    et les déplace dans les dossiers appropriés.
    """
    os.makedirs(dossier_mains, exist_ok=True)
    os.makedirs(dossier_resumes, exist_ok=True)

    for nom_fichier in os.listdir(dossier_source):
        chemin_initial = os.path.join(dossier_source, nom_fichier)

        if not nom_fichier.endswith(".txt"):
            continue

        if "Expresso" in nom_fichier and "_summary" in nom_fichier:
            chemin_destination = os.path.join(dossier_resumes, nom_fichier)
        elif "Expresso" in nom_fichier:
            chemin_destination = os.path.join(dossier_mains, nom_fichier)
        else:
            continue

        shutil.move(chemin_initial, chemin_destination)
