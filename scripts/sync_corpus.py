# -*- coding: utf-8 -*-
import csv
import json
import subprocess

# Load original corpus from git
raw = subprocess.check_output(["git", "show", "HEAD:data/parallel_corpus.json"], encoding="utf-8")
merged = json.loads(raw)
seen_spoken = {item["spoken"] for item in merged}

# Add Modalapada 2.0 items
with open("data/dataset.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row["dialect_text"] not in seen_spoken:
            reg_map = {
                "Hubballi-Dharwad": ("NK", "North Karnataka (Hubballi-Dharwad)", "ಉತ್ತರ ಕರ್ನಾಟಕ (ಹುಬ್ಬಳ್ಳಿ-ಧಾರವಾಡ)"),
                "Mangaluru": ("CO", "Coastal / Kundagannada (Mangaluru)", "ಕರಾವಳಿ / ಕುಂದಗನ್ನಡ (ಮಂಗಳೂರು)"),
                "Uttara Kannada": ("UK", "Uttara Kannada / Havyaka (Sirsi-Karwar)", "ಉತ್ತರ ಕನ್ನಡ / ಹವ್ಯಕ (ಶಿರಸಿ-ಕಾರವಾರ)")
            }
            code, name_en, name_kn = reg_map.get(row["dialect"], ("GEN", row["dialect"], row["dialect"]))
            merged.append({
                "id": row["id"],
                "region_code": code,
                "region_name_en": name_en,
                "region_name_kn": name_kn,
                "spoken": row["dialect_text"],
                "standard": row["standard_text"],
                "english": f"Topic: {row['topic']}, Town: {row['town']}",
                "context": f"{row['topic']} | {row['town']} ({row['age_band']})",
                "grammar_rule": f"Dialect transformation for {row['dialect']}",
                "vocabulary_changes": []
            })
            seen_spoken.add(row["dialect_text"])

with open("data/parallel_corpus.json", "w", encoding="utf-8") as f:
    json.dump(merged, f, ensure_ascii=False, indent=2)

print(f"Merged corpus total items: {len(merged)}")
