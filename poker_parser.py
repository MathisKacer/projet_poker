import re
import pandas as pd
from pathlib import Path
from datetime import datetime


def get_position(hero_seat, button_seat, seat_list):
    seats = sorted(seat_list)
    n = len(seats)
    btn_idx = seats.index(button_seat)
    if n == 2:
        if hero_seat == seats[btn_idx]:
            return "BTN"
        return "BB"
    if n == 3:
        if hero_seat == seats[btn_idx]:
            return "BTN"
        if hero_seat == seats[(btn_idx + 1) % 3]:
            return "SB"
        return "BB"
    return "UNKNOWN"


def parse_hand(block):
    data = {}

    # Header
    m = re.search(
        r'Tournament "(.+?)" buyIn: ([\d.]+).*?level: (\d+)'
        r'.*?HandId: #(\S+).*?\((\d+)/(\d+)\)'
        r'.*?(\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2})',
        block
    )
    if not m:
        return None

    data["tournament"] = m.group(1)
    data["buy_in"]     = float(m.group(2))
    data["level"]      = int(m.group(3))
    data["hand_id"]    = m.group(4)
    data["sb_amount"]  = int(m.group(5))
    data["bb_amount"]  = int(m.group(6))
    data["datetime"]   = datetime.strptime(m.group(7), "%Y/%m/%d %H:%M:%S")

    # Bouton
    m = re.search(r"Seat #(\d+) is the button", block)
    if not m:
        return None
    button_seat = int(m.group(1))

    # Sièges
    seats_found = {
        m.group(2): {"seat": int(m.group(1)), "stack": int(m.group(3))}
        for m in re.finditer(r"Seat (\d+): (.+?) \((\d+)\)", block)
    }

    # Détection automatique du héros
    m = re.search(r"Dealt to (.+?) \[", block)
    if not m:
        return None
    hero = m.group(1)

    if hero not in seats_found:
        return None

    seat_list = [v["seat"] for v in seats_found.values()]
    data["hero"]          = hero
    data["hero_seat"]     = seats_found[hero]["seat"]
    data["stack_start"]   = seats_found[hero]["stack"]
    data["total_players"] = len(seat_list)
    data["position"]      = get_position(data["hero_seat"], button_seat, seat_list)
    data["stack_bb"]      = round(data["stack_start"] / data["bb_amount"], 2)

    # Cartes
    m = re.search(rf"Dealt to {re.escape(hero)} \[(.+?)\]", block)
    data["hand_cards"] = m.group(1) if m else None

    # Section préflop
    pf = ""
    m = re.search(r"\*\*\* PRE-FLOP \*\*\*(.*?)(?=\*\*\*|\Z)", block, re.S)
    if m:
        pf = m.group(1)

    hero_re = re.escape(hero)
    data["fold_preflop"]  = bool(re.search(rf"^{hero_re} folds", pf, re.M))
    data["allin_preflop"] = bool(re.search(rf"^{hero_re} .* and is all-in", pf, re.M))

    # Board
    m = re.search(r"\*\*\* FLOP \*\*\* \[(.+?)\]", block)
    data["flop"] = m.group(1) if m else None
    m = re.search(r"\*\*\* TURN \*\*\* \[.+?\]\[(.+?)\]", block)
    data["turn"] = m.group(1) if m else None
    m = re.search(r"\*\*\* RIVER \*\*\* \[.+?\]\[(.+?)\]", block)
    data["river"] = m.group(1) if m else None

    data["saw_flop"]  = data["flop"]  is not None
    data["saw_turn"]  = data["turn"]  is not None
    data["saw_river"] = data["river"] is not None

    # Showdown
    sd = re.search(r"\*\*\* SHOW DOWN \*\*\*(.*?)(?=\*\*\*|\Z)", block, re.S)
    data["went_to_showdown"] = sd is not None
    data["won_at_showdown"]  = bool(
        sd and re.search(rf"^{hero_re} collected", sd.group(1), re.M)
    )

    # Résultat net
    collected = sum(int(x) for x in re.findall(rf"{hero_re} collected (\d+) from", block))
    invested  = sum(int(x) for x in re.findall(
        rf"^{hero_re} (?:posts \S+ blind|calls|bets|raises \d+ to) (\d+)", block, re.M
    ))
    m = re.search(r"Total pot (\d+)", block)
    data["total_pot"] = int(m.group(1)) if m else None
    data["net_chips"] = collected - invested
    data["net_bb"]    = round(data["net_chips"] / data["bb_amount"], 2)

    return data


def parse_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    blocks = [b.strip() for b in re.split(r"(?=Winamax Poker - Tournament)", content) if b.strip()]
    hands = []
    for block in blocks:
        result = parse_hand(block)
        if result:
            result["source_file"] = Path(filepath).name
            hands.append(result)
    return pd.DataFrame(hands)


def parse_folder(folder_path):
    dfs = []
    files = list(Path(folder_path).rglob("*.txt"))
    print(f"{len(files)} fichier(s) trouve(s)")
    for f in files:
        df = parse_file(str(f))
        print(f"  {f.name} -> {len(df)} mains")
        dfs.append(df)
    if not dfs:
        return pd.DataFrame()
    df = pd.concat(dfs, ignore_index=True)
    df["datetime"] = pd.to_datetime(df["datetime"])
    df = df.sort_values("datetime").reset_index(drop=True)
    print(f"\nTotal : {len(df)} mains")
    return df
