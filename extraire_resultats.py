import re
import pandas as pd
import os

def parse_resume(fichier):
    try:
        with open(fichier, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        return None

    tournament_id = re.search(r"Expresso\((\d+)\)", content)
    buy_in_raw = re.search(r"Buy-In : (\d+\.\d+)€ \+ (\d+\.\d+)€", content)
    duree = re.search(r"You played (\d+)min (\d+)s", content)
    rank = re.search(r"You finished in (\d+)(?:st|nd|rd|th) place", content)
    start_date = re.search(r"Tournament started (\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2} UTC)", content)
    prizepool = re.search(r"Prizepool : (\d+)€", content)

    summary_data = {
        "tournament_id": tournament_id.group(1) if tournament_id else None,
        "start_date": start_date.group(1) if start_date else None,
        "buy_in_price": float(buy_in_raw.group(1)) if buy_in_raw else 0.0,
        "buy_in_rake": float(buy_in_raw.group(2)) if buy_in_raw else 0.0,
        "prizepool": int(prizepool.group(1)) if prizepool else 0,
        "rank": int(rank.group(1)) if rank else None,
        "duree_seconds": (int(duree.group(1)) * 60 + int(duree.group(2))) if duree else 0
    }

    return summary_data


def parse_folder_resume(dossier):
    data = []
    for nom_fichier in os.listdir(dossier):
        chemin_fichier = os.path.join(dossier, nom_fichier)
        resume_data = parse_resume(chemin_fichier)
        if resume_data:
            data.append(resume_data)
    return pd.DataFrame(data)

df = parse_folder_resume("resumes")
print(df.head())
