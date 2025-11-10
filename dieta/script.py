
from pathlib import Path
import sys
import yaml
import pandas as pd
from matplotlib import rcParams
import matplotlib.pyplot as plt

BASE = Path(__file__).resolve().parent
yaml_file = BASE / "status.yaml"
if not yaml_file.exists():
    print(f"{yaml_file} non trovato")
    sys.exit(1)

with open(yaml_file, "r", encoding="utf-8") as f:
    raw = yaml.safe_load(f)

rows = []
# support various shapes: { "logbook": [ ... ] }, list of dicts, or simple dict date->peso
items = None
if isinstance(raw, dict):
    if "logbook" in raw and isinstance(raw["logbook"], list):
        items = raw["logbook"]
    else:
        # maybe simple mapping date->peso
        if all(not isinstance(v, (dict, list)) for v in raw.values()):
            for k, v in raw.items():
                rows.append({"date": k, "peso": v})
        else:
            # fallback: treat top-level as list-like dict values
            items = [raw]
elif isinstance(raw, list):
    items = raw
else:
    print("Formato YAML non riconosciuto")
    sys.exit(1)

if items:
    for item in items:
        if not isinstance(item, dict):
            continue
        date = item.get("date") or item.get("data")
        peso = item.get("peso") or item.get("peso_kg") or item.get("weight")
        waist = item.get("circonferenza_vita_cm") or item.get("waist_cm") or item.get("waist")
        note = item.get("commenti") or item.get("comment") or item.get("label") or item.get("notes")
        rows.append({"date": date, "peso": peso, "waist": waist, "note": note})

if not rows:
    print("Nessun dato leggibile nel file YAML")
    sys.exit(1)

df = pd.DataFrame(rows)
# try ISO 'YYYY-MM-DD' first to avoid pandas warning about dayfirst, then fallback to dayfirst parsing
df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d", errors="coerce")
mask = df["date"].isna()
if mask.any():
    df.loc[mask, "date"] = pd.to_datetime(df.loc[mask, "date"], dayfirst=True, errors="coerce")
df["peso"] = pd.to_numeric(df["peso"], errors="coerce")
if "waist" in df.columns:
    df["waist"] = pd.to_numeric(df["waist"], errors="coerce")
# keep rows with valid date and peso
df = df.dropna(subset=["date", "peso"]).sort_values("date")

if df.empty:
    print("Nessun dato valido dopo il parsing delle date/pesi")
    sys.exit(1)
# Use Palatino (falls back if not installed)
rcParams['font.family'] = 'serif'

plt.figure(figsize=(8, 6))
plt.plot(df["date"], df["peso"], marker="o", linestyle="-", label="Peso (kg)")
plt.ylabel("Peso (kg)", fontsize=10)
ax = plt.gca()
for x, y in zip(df["date"], df["peso"]):
    ax.annotate(f"{y:.1f}", xy=(x, y), xytext=(0, 6), textcoords="offset points",
                ha="center", va="bottom", fontsize=8,
                bbox=dict(boxstyle="round,pad=0.2", fc="white", alpha=0.6))
plt.xticks(rotation=45, ha="right", fontsize=8)
plt.grid(True)
plt.ylim(75, 88)
plt.axhline(y=76, color="r", linestyle="--", label="Obiettivo 76 kg")
plt.legend()
plt.tight_layout()

img_file = BASE / "status.png"
plt.savefig(img_file, dpi=150)
plt.close()

# Create status.md with embedded image and table
md_file = BASE / "status.md"
columns = ["date", "peso"]
if "waist" in df.columns and df["waist"].notna().any():
    columns.append("waist")
if "note" in df.columns and df["note"].notna().any():
    columns.append("note")

with open(md_file, "w", encoding="utf-8") as f:
    f.write("# Stato\n\n")
    f.write(f"![Peso vs Data]({img_file.name})\n\n")
    # header
    header = " | ".join([("Data" if c == "date" else ("Peso (kg)" if c == "peso" else ("Vita (cm)" if c == "waist" else "Note"))) for c in columns])
    f.write(f"| {header} |\n")
    f.write("|" + "|".join(["---"] * len(columns)) + "|\n")
    for _, row in df.iterrows():
        parts = []
        for c in columns:
            if c == "date":
                parts.append(row["date"].strftime("%Y-%m-%d"))
            elif c == "peso":
                parts.append(f"{row['peso']:.1f}")
            elif c == "waist":
                parts.append(str(int(row["waist"])) if not pd.isna(row["waist"]) else "")
            else:  # note
                parts.append(str(row.get("note") or ""))
        f.write("| " + " | ".join(parts) + " |\n")

print(f"Creati: {md_file.name} e {img_file.name}")