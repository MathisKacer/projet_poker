import re
import pandas as pd
from pathlib import Path
from datetime import datetime

HERO = "Samponi"

def get_position(seat_num, button_seat):
    seats = [1, 2, 3]
    btn_idx = seats.index(button_seat)
    if seat_num == seats[btn_idx]:
        return "BTN"
    if seat_num == seats[(btn_idx + 1) % 3]:
        return "SB"
    if seat_num == seats[(btn_idx + 2) % 3]:
        return "BB"
    return "UNKNOWN"


def parse_hand(block):
    data = {}

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

    m = re.search(r"Seat #(\d+) is the button", block)
    if not m:
        return None
    button_seat = int(m.group(1))

    m = re.search(rf"Seat (\d+): {HERO} \((\d+)\)", block)
    if not m:
        return None
    data["hero_seat"]   = int(m.group(1))
    data["stack_start"] = int(m.group(2))
    data["position"]    = get_position(data["hero_seat"], button_seat)
    data["stack_bb"]    = round(data["stack_start"] / data["bb_amount"], 2)

    m = re.search(rf"Dealt to {HERO} \[(.+?)\]", block)
    data["hand_cards"] = m.group(1) if m else None

    pf = ""
    m = re.search(r"\*\*\* PRE-FLOP \*\*\*(.*?)(?=\*\*\*|\Z)", block, re.S)
    if m:
        pf = m.group(1)


    data["fold_preflop"]  = bool(re.search(rf"^{HERO} folds", pf, re.M))
    data["allin_preflop"] = bool(re.search(rf"^{HERO} .* and is all-in", pf, re.M))

    m = re.search(r"\*\*\* FLOP \*\*\* \[(.+?)\]", block)
    data["flop"] = m.group(1) if m else None
    m = re.search(r"\*\*\* TURN \*\*\* \[.+?\]\[(.+?)\]", block)
    data["turn"] = m.group(1) if m else None
    m = re.search(r"\*\*\* RIVER \*\*\* \[.+?\]\[(.+?)\]", block)
    data["river"] = m.group(1) if m else None

    data["saw_flop"]  = data["flop"]  is not None
    data["saw_turn"]  = data["turn"]  is not None
    data["saw_river"] = data["river"] is not None

    sd = re.search(r"\*\*\* SHOW DOWN \*\*\*(.*?)(?=\*\*\*|\Z)", block, re.S)
    data["went_to_showdown"] = sd is not None
    data["won_at_showdown"]  = bool(sd and re.search(rf"^{HERO} collected", sd.group(1), re.M))

    collected = sum(int(x) for x in re.findall(rf"{HERO} collected (\d+) from", block))
    invested  = sum(int(x) for x in re.findall(
        rf"^{HERO} (?:posts \S+ blind|calls|bets|raises \d+ to) (\d+)", block, re.M
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
