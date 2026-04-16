import re
import pandas as pd
import pandasgui

fichier = "fichier_test.txt"

def parse_winamax_history(file_content):
    # Séparer le fichier par main (chaque main commence par "Winamax Poker")
    hands_raw = file_content.split('Winamax Poker - ')
    hands_data = []

    for hand in hands_raw:
        if not hand.strip():
            continue

        # --- Extraction des métadonnées ---
        hand_id = re.search(r"HandId: #(\d+-\d+-\d+)", hand)
        level = re.search(r"level: (\d+)", hand)
        date = re.search(r"(\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2} UTC)", hand)

        # --- Extraction des joueurs et jetons ---
        # On cherche les lignes "Seat X: Nom (Chips)"
        players = re.findall(r"Seat (\d+): (.*?) \((\d+)\)", hand)

        # --- Cartes du Hero (Samponi dans votre exemple) ---
        hero_cards = re.search(r"Dealt to Samponi \[(.*?)\]", hand)

        # --- Board (Flop, Turn, River) ---
        board = re.search(r"Board: \[(.*?)\]", hand)

        # --- Résultat final (Vainqueur et Pot) ---
        winner_info = re.search(r"Total pot (\d+) \|", hand)

        # Organisation des données
        hand_info = {
            "hand_id": hand_id.group(1) if hand_id else None,
            "date": date.group(1) if date else None,
            "level": level.group(1) if level else None,
            "hero_cards": hero_cards.group(1) if hero_cards else None,
            "board": board.group(1) if board else None,
            "total_pot": int(winner_info.group(1)) if winner_info else 0,
            "players_count": len(players)
        }

        # On ajoute les détails des joueurs dynamiquement
        for i, p in enumerate(players):
            hand_info[f"p{i+1}_name"] = p[1]
            hand_info[f"p{i+1}_stack"] = p[2]

        hands_data.append(hand_info)

    return pd.DataFrame(hands_data)

# --- Simulation de l'exécution ---
# texte_complet = votre_variable_contenant_le_log
# df = parse_winamax_history(texte_complet)
# print(df.head())

tab = parse_winamax_history("fichier_test.txt")
pandasgui.show(tab)
