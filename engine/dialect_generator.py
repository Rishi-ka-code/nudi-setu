# -*- coding: utf-8 -*-
"""
Cross-Dialect Generator:
Transforms standard textbook Kannada sentences into all 5 major Karnataka dialects:
1. North Karnataka (ಧಾರವಾಡ, ಹುಬ್ಬಳ್ಳಿ, ಬೆಳಗಾವಿ)
2. Kalyana Karnataka (ಕಲಬುರಗಿ, ಬೀದರ್, ರಾಯಚೂರು)
3. Coastal / Kundagannada (ಮಂಗಳೂರು, ಉಡುಪಿ, ಕುಂದಾಪುರ)
4. Uttara Kannada / Havyaka (ಶಿರಸಿ, ಕಾರವಾರ, ಗೋಕರ್ಣ)
5. Mysuru-Mandya (ದಕ್ಷಿಣ ಕರ್ನಾಟಕ)
"""

import re
from typing import Dict, Any

class DialectGenerator:
    def __init__(self):
        import os, csv
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        glossary_path = os.path.join(base_dir, "data", "glossary.csv")

        # 1. Base curated vocabulary
        self.nk_phrases = [
            ("ಊಟ ಆಯಿತೇ", "ಊಟ ಆತೇನ್ರಿ"), ("ಕುಳಿತರೂ ನಿಂತರೂ", "ಕುಂತ್ರೇನ್ ನಿಂತ್ರೇನ್"),
            ("ನಿಜ ಹೇಳಬೇಕೆಂದರೆ", "ಖರೇ ಹೇಳ್ಬೇಕಂದ್ರ"), ("ತುಂಬಾ ಒಳ್ಳೆಯ", "ಬಹಳ ಚೊಲೋ"),
            ("ಬರುತ್ತಿದ್ದಾನೆ", "ಬರಾಕತ್ತಾನ"), ("ಮಾಡುತ್ತಿದ್ದಾಳೆ", "ಮಾಡಾಕತ್ತಾಳ"),
            ("ಮಾಡುತ್ತಿದ್ದಾರೆ", "ಮಾಡಾಕತ್ತಾರ"), ("ಬರುತ್ತಿದ್ದಾರೆ", "ಬರಾಕತ್ತಾರ"),
            ("ಮಾಡುತ್ತಿದ್ದೀರಿ", "ಮಾಡಾಕತ್ತೀರಿ"), ("ಕುಡಿಯೋಣ", "ಕುಡೀರಿ"),
            ("ಕುಳಿತುಕೊಳ್ಳಿ", "ಕುಡೀರಿ"), ("ಕುಳಿತುಕೋ", "ಕುಂದ್ರು")
        ]
        self.nk_vocab = {
            "ಬರುತ್ತಿದ್ದಾನೆ": "ಬರಾಕತ್ತಾನ", "ಹೋಗುತ್ತಿದ್ದಾನೆ": "ಹೋಗಾಕತ್ತಾನ", "ಮಾಡುತ್ತಿದ್ದಾನೆ": "ಮಾಡಾಕತ್ತಾನ",
            "ಬರುತ್ತಾಳೆ": "ಬರಾಕತ್ತಾಳ", "ಹೋಗುತ್ತಾಳೆ": "ಹೋಗಾಕತ್ತಾಳ", "ಬರುತ್ತಾರೆ": "ಬರಾಕತ್ತಾರ",
            "ಬರುತ್ತಾನೆ": "ಬರ್ತಾನ", "ಹೋಗುತ್ತಾನೆ": "ಹೋಗ್ತಾನ", "ಮಾಡುತ್ತಾನೆ": "ಮಾಡ್ತಾನ",
            "ಬರುವುದಿಲ್ಲ": "ಬರಲ್ಲ", "ಹೋಗುವುದಿಲ್ಲ": "ಹೋಗಲ್ಲ", "ಮಾಡುವುದಿಲ್ಲ": "ಮಾಡಲ್ಲ",
            "ಮಾಡಬೇಕು": "ಮಾಡ್ಬೇಕು", "ಹೋಗಬೇಕು": "ಹೋಗ್ಬೇಕು", "ಮಾಡಬಾರದು": "ಮಾಡ್ಬಾರ್ದು",
            "ಬರುತ್ತಿದ್ದೇನೆ": "ಬರಾಕತ್ತೀನಿ", "ಹೋಗುತ್ತಿದ್ದೇನೆ": "ಹೋಗಾಕತ್ತೀನಿ",
            "ಇಂದು": "ಇವ್ವತ್", "ಶಾಲೆಗೆ": "ಸಾಲಿಗಿ", "ಶಾಲೆ": "ಸಾಲಿ", "ಹಣ": "ರೊಕ್ಕ", "ಗೆಳೆಯ": "ದೋಸ್ತ್",
            "ಗೆಳೆಯರೇ": "ದೋಸ್ತ್ರ", "ತಾಯಿ": "ಅವ್ವ", "ತಂದೆ": "ಅಪ್ಪಾ", "ಮನೆಯಲ್ಲಿ": "ಮನ್ಯಾಗ", "ಮನೆಗೆ": "ಮನಿಗೆ",
            "ಮನೆ": "ಮನಿ", "ಏಕೆ": "ಯಾಕ", "ಹೇಗೆ": "ಹ್ಯಾಂಗ", "ಹೀಗೆ": "ಹಿಂಗ", "ತುಂಬಾ": "ಬಹಳ",
            "ಒಳ್ಳೆಯ": "ಚೊಲೋ", "ಚೆನ್ನಾಗಿ": "ಚೊಲೋ", "ಇದೆ": "ಐತಿ", "ಇವೆ": "ಅದಾವ", "ಬೇಡ": "ಬ್ಯಾಡ",
            "ಬೇಡಿ": "ಬ್ಯಾಡ್ರಿ", "ಚಹಾ": "ಚಾ", "ನಾಳೆ": "ನಾಳಿಕಿ"
        }

        self.kk_phrases = [
            ("ಬರುತ್ತಿದ್ದಾನೆ", "ಬರಲಿಕ್ಕತ್ತಾನ"), ("ಹೋಗುತ್ತಿದ್ದಾನೆ", "ಹೋಗಲಿಕ್ಕತ್ತಾನ"),
            ("ಮಾಡುತ್ತಿದ್ದಾನೆ", "ಮಾಡಲಿಕ್ಕತ್ತಾನ"), ("ಮಾಡುತ್ತಿದ್ದಾರೆ", "ಮಾಡಲಿಕ್ಕತ್ತಾರ")
        ]
        self.kk_vocab = {
            "ಬರುತ್ತಾನೆ": "ಬರ್ತಾನ", "ಹೋಗುತ್ತಾನೆ": "ಹೋಗ್ತಾನ", "ಬರುವುದಿಲ್ಲ": "ಬರೂದಿಲ್ಲ",
            "ಗೆಳೆಯ": "ದೋಸ್ತ್", "ಗೆಳೆಯರೇ": "ದೋಸ್ತ್ರ", "ಹಣ": "ರೊಕ್ಕ", "ಶಾಲೆಗೆ": "ಸಾಲಿಗೆ",
            "ಶಾಲೆ": "ಸಾಲಿ", "ತುಂಬಾ": "ಬಾಳಾ", "ಮನೆಗೆ": "ಮನಿಗೆ", "ಮನೆ": "ಮನಿ", "ಬೇಗ": "ಜಲ್ದಿ",
            "ತೊಂದರೆ": "ತಕ್ಲಿಫ್", "ಇದೆ": "ಐತಿ"
        }

        self.co_phrases = [
            ("ಹೋಗಿ ಬರುತ್ತೇನೆ", "ಪೋಯಿ ಬರ್ಪೆ"), ("ಏನು ಮಾಡುತ್ತಿದ್ದೀರಿ", "ಎಂತ ಮಾಡ್ತಾ ಇದ್ದೀರಿ"),
            ("ಚೆನ್ನಾಗಿದೆ", "ಲಯಿಕ್ ಉಂಡು"), ("ಬರುತ್ತಿದೆ", "ಬರ್ತಾ ಉಂಡು"),
            ("ರಜೆಯೇ", "ರಜಾನಾ"), ("ರಜೆಯೇ?", "ರಜಾನಾ?"), ("ಬರುತ್ತಿದ್ದಾನೆ", "ಬರ್ಪ"),
            ("ಹೋಗುತ್ತಿದ್ದಾನೆ", "ಪೋಪ"), ("ಕುಡಿಯೋಣ", "ಕುಡಿಯುವಾ"), ("ಕುಳಿತುಕೊಳ್ಳಿ", "ಕುತ್ಕೊಳಿ"),
            ("ಮಾತನಾಡಿದೆವು", "ಮಾತಾಡಿದ್ವಿ"), ("ಹೋದೆವು", "ಹೋದ್ವಿ"), ("ಹೇಳಿದೆ", "ಹೇಳ್ದೆ"),
            ("ಹೇಳಿದರು", "ಹೇಳ್ದ್ರು"), ("ತಿಂದಿರಿ", "ತಿಂಡ್ರಿ")
        ]
        self.co_vocab = {
            "ಏನು": "ಎಂತ", "ಏತಕ್ಕೆ": "ಎಂತಕೆ", "ಗೆಳೆಯ": "ಮಾರೆ", "ಗೆಳೆಯರೇ": "ಮಾರ್ರೆ",
            "ಶಾಲೆಗೆ": "ಶಾಲೆಗ್", "ಮನೆಯಲ್ಲಿ": "ಮನೆಲ್", "ಪೇಟೆಗೆ": "ಪೇಟೆಗ್", "ಹಣ": "ಪೈಸೆ",
            "ಬರುತ್ತೇನೆ": "ಬರ್ಪೆ", "ಹೋಗುತ್ತೇನೆ": "ಪೋಪೆ", "ತಿನ್ನುತ್ತೇನೆ": "ತಿಂಬೆ", "ಹೋಗಿ": "ಪೋಯಿ",
            "ಆಯಿತು": "ಆತ್", "ಆಯಿತೇ": "ಆತಾ", "ರಜೆಯೇ": "ರಜಾನಾ", "ರಜೆಯೇ?": "ರಜಾನಾ?",
            "ತಾಯಿ": "ಅಪ್ಪೆ", "ತಂದೆ": "ಅಮ್ಮೆ", "ಕೋಳಿ": "ಕೋರಿ", "ಅಡುಗೆ": "ಅಡಿಗೆ",
            "ಇದೆ": "ಉಂಡು", "ಇದೆಯೇ?": "ಉಂಟಾ?", "ಮೀನು": "ಮೀನ್", "ಚೆನ್ನಾಗಿ": "ಲಯಿಕ್",
            "ಇಂದು": "ಇವತ್ತು", "ಚಹಾ": "ಚಾ", "ಅವನು": "ಆಯಿ", "ಅವಳು": "ಆಯ್ಕಿನು", "ನಾವು": "ಏಂಕ್ಲು",
            "ತರುತ್ತೇನೆ": "ತರ್ಪೆ", "ಕೊಡುತ್ತೇನೆ": "ಕೊಡ್ಪೆ"
        }

        self.uk_phrases = [
            ("ಹೋಗಿ ಬರುತ್ತೇನೆ", "ಹೋಗಿ ಬತ್ತೆ"), ("ಹೇಗಿದ್ದೀರಿ", "ಹೆಂಗಿದ್ದೀರಿ"),
            ("ಬರುತ್ತೀರಾ", "ಬರ್ತೀರಾ"), ("ಕುಳಿತುಕೋ", "ಕೂಡು"), ("ಕುಳಿತುಕೊಳ್ಳಿ", "ಕೂಡಿ"),
            ("ಕುಡಿಯೋಣ", "ಕುಡಿಯುವಾ"), ("ಕೇಳಿಸಿತು", "ಕೇಳ್ತು"), ("ಮಾಡಿದೆ", "ಗೇದು"),
            ("ಆಯಿತೇ?", "ಆತಾ?"), ("ಸುರಿಯುತ್ತಿದೆ", "ಸುರಿವುತ್ತೆ"), ("ಸುರಿಯುತ್ತದೆ", "ಸುರಿವುತ್ತೆ"),
            ("ಮಾಡಬೇಕು", "ಮಾಡತಕ್ಕು")
        ]
        self.uk_vocab = {
            "ನಾನು": "ನಾಂ", "ನೀನು": "ನೀಂ", "ಅವನು": "ಅವಂ", "ಅವಳು": "ಅವಳ್", "ಎಲ್ಲರೂ": "ಎಲ್ಲೋರು",
            "ಏನು": "ಏಂ", "ಹಣವಿಲ್ಲದೆ": "ಕಾಸಿಲ್ದೆ", "ಹಣ": "ಕಾಸು", "ಶಾಲೆಗೆ": "ಸಾಲೆಗೆ", "ಶಾಲೆ": "ಸಾಲೆ",
            "ಬರುತ್ತೇನೆ": "ಬತ್ತೆ", "ಹೋಗುತ್ತೇನೆ": "ಹೋತ್ತೆ", "ಆಗುವುದಿಲ್ಲ": "ಆಪೋದಿಲ್ಲ", "ತಿಳಿಯುವುದಿಲ್ಲ": "ಗೊತ್ತಾಪೋದಿಲ್ಲ",
            "ತಂದೆ": "ಅಪ್ಪಯ್ಯ", "ತಾಯಿ": "ಅಮ್ಮಯ್ಯ", "ಸ್ವಲ್ಪ": "ಚೂರು", "ಸುಂದರ": "ಚಂದ",
            "ಚೆನ್ನಾಗಿ": "ಚಂದ", "ಮನೆಯಲ್ಲಿ": "ಮನೆಲ್", "ಮುಂಜಾನೆ": "ಬೆಳ್ಳಿಗ್ಗೆ", "ಹಿತ್ತಿಲು": "ಹಿತ್ತಿಲು",
            "ಅಡುಗೆ": "ಅಡಿಗೆ", "ಚಹಾ": "ಕಷಾಯ"
        }

        self.sm_phrases = [
            ("ಮಾಡುತ್ತಿದ್ದಾನೆ", "ಮಾಡ್ತಾವನೆ"), ("ಹೋಗುತ್ತಿದ್ದಾನೆ", "ಹೋಗ್ತಾವನೆ"),
            ("ಬರುತ್ತಿದ್ದಾನೆ", "ಬರ್ತಾವನೆ")
        ]
        self.sm_vocab = {
            "ಬರುತ್ತಿದ್ದಾನೆ": "ಬರ್ತಾವನೆ", "ಹೋಗುತ್ತಿದ್ದಾನೆ": "ಹೋಗ್ತಾವನೆ", "ಮಾಡುತ್ತಿದ್ದಾನೆ": "ಮಾಡ್ತಾವನೆ",
            "ಬರುತ್ತಾನೆ": "ಬರ್ತಾನೆ", "ಹೋಗುತ್ತಾನೆ": "ಹೋಗ್ತಾನೆ", "ಮಾಡುತ್ತಾನೆ": "ಮಾಡ್ತಾನೆ",
            "ಬರುವುದಿಲ್ಲ": "ಬರಲ್ಲ", "ಹೋಗುವುದಿಲ್ಲ": "ಹೋಗಲ್ಲ", "ಮಾಡಿದೆ": "ಮಾಡ್ದೆ", "ಹೇಳಿದೆ": "ಹೇಳ್ದೆ",
            "ಹೋಗಬೇಕು": "ಹೋಗ್ಬೇಕು", "ಮಾಡಬೇಕು": "ಮಾಡ್ಬೇಕು"
        }

        # 2. Augment from glossary.csv
        if os.path.exists(glossary_path):
            try:
                with open(glossary_path, "r", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    for r in reader:
                        dialect = r.get("dialect", "").strip()
                        item = r.get("dialect_item", "").strip()
                        std_raw = r.get("standard_kannada", "").strip()
                        std = std_raw.split("/")[0].strip()
                        if not item or item.startswith("-") or not std:
                            continue
                        if dialect == "Hubballi-Dharwad":
                            target_phr = self.nk_phrases
                            target_voc = self.nk_vocab
                        elif dialect == "Mangaluru":
                            target_phr = self.co_phrases
                            target_voc = self.co_vocab
                        elif dialect == "Uttara Kannada":
                            target_phr = self.uk_phrases
                            target_voc = self.uk_vocab
                        else:
                            continue

                        if " " in std:
                            if not any(pair[0] == std for pair in target_phr):
                                target_phr.append((std, item))
                        else:
                            if std not in target_voc:
                                target_voc[std] = item
            except Exception:
                pass

        # Sort phrases by descending length for greedy matching
        self.nk_phrases.sort(key=lambda x: len(x[0]), reverse=True)
        self.kk_phrases.sort(key=lambda x: len(x[0]), reverse=True)
        self.co_phrases.sort(key=lambda x: len(x[0]), reverse=True)
        self.uk_phrases.sort(key=lambda x: len(x[0]), reverse=True)
        self.sm_phrases.sort(key=lambda x: len(x[0]), reverse=True)

    def _synthesize(self, text: str, region_key: str) -> str:
        res = text
        if region_key == "nk":
            for s, d in self.nk_phrases:
                res = res.replace(s, d)
            for s, d in self.nk_vocab.items():
                res = re.sub(r"(?<![\u0C80-\u0D00])" + re.escape(s) + r"(?=[^\u0C80-\u0D00]|$)", d, res)
            # NK morphology
            res = re.sub(r"([ಕ-ಹ]+)ುತ್ತಿದ್ದಾನೆ", r"\1ಾಕತ್ತಾನ", res)
            res = re.sub(r"([ಕ-ಹ]+)ುತ್ತಿದ್ದಾಳೆ", r"\1ಾಕತ್ತಾಳ", res)
            res = re.sub(r"([ಕ-ಹ]+)ುತ್ತಿದ್ದಾರೆ", r"\1ಾಕತ್ತಾರ", res)
            res = re.sub(r"([ಕ-ಹ]+)ುತ್ತಿದ್ದೇನೆ", r"\1ಾಕತ್ತೀನಿ", res)
            res = re.sub(r"([ಕ-ಹ]+)ುತ್ತಿದೆ", r"\1ಾಕತ್ತೈತಿ", res)
            res = re.sub(r"([ಕ-ಹ]+)ತ್ತಾನೆ", r"\1್ತಾನ", res)
            res = re.sub(r"([ಕ-ಹ]+)ತ್ತಾಳೆ", r"\1್ತಾಳ", res)
            res = re.sub(r"([ಕ-ಹ]+)ತ್ತಾರೆ", r"\1್ತಾರ", res)
            res = re.sub(r"([ಕ-ಹ]+)ತ್ತೀರಿ", r"\1್ತೀರಿ", res)
            res = re.sub(r"([ಕ-ಹ]+)ತ್ತೇನೆ", r"\1್ತೀನಿ", res)
            res = re.sub(r"([ಕ-ಹ]+)ಬೇಕು(?=[^\u0C80-\u0D00]|$)", r"\1್ಬೇಕು", res)
            res = re.sub(r"([ಕ-ಹ]+)ಬೇಡ(?=[^\u0C80-\u0D00]|$)", r"\1್ಬ್ಯಾಡ", res)
            res = re.sub(r"([ಕ-ಹ]+)ಬೇಡಿ(?=[^\u0C80-\u0D00]|$)", r"\1್ಬ್ಯಾಡ್ರಿ", res)
            res = re.sub(r"ದಲ್ಲಿ(?=[^\u0C80-\u0D00]|$)", "ದಾಗ", res)
            res = re.sub(r"ನಲ್ಲಿ(?=[^\u0C80-\u0D00]|$)", "ನಾಗ", res)
            res = re.sub(r"ಗಳನ್ನು(?=[^\u0C80-\u0D00]|$)", "", res)
            res = re.sub(r"ಕೊಳ್ಳಿ(?=[^\u0C80-\u0D00]|$)", "ಕೊಳ್ರಿ", res)
            res = re.sub(r"(ಮಾಡಿ|ಹಾಕಿ|ನೋಡಿ|ಕೊಡಿ|ಹೇಳಿ|ತುಂಬಿ)(?=[^\u0C80-\u0D00]|$)", lambda m: m.group(1)[:-1] + "್ರಿ", res)
            return res

        elif region_key == "kk":
            for s, d in self.kk_phrases:
                res = res.replace(s, d)
            for s, d in self.kk_vocab.items():
                res = re.sub(r"(?<![\u0C80-\u0D00])" + re.escape(s) + r"(?=[^\u0C80-\u0D00]|$)", d, res)
            res = re.sub(r"([ಕ-ಹ]+)ುತ್ತಿದ್ದಾನೆ", r"\1ಲಿಕ್ಕತ್ತಾನ", res)
            res = re.sub(r"([ಕ-ಹ]+)ುತ್ತಿದ್ದಾಳೆ", r"\1ಲಿಕ್ಕತ್ತಾಳ", res)
            res = re.sub(r"([ಕ-ಹ]+)ುತ್ತಿದ್ದಾರೆ", r"\1ಲಿಕ್ಕತ್ತಾರ", res)
            res = re.sub(r"([ಕ-ಹ]+)ುತ್ತಿದ್ದೇನೆ", r"\1ಲಿಕ್ಕತ್ತೀನಿ", res)
            res = re.sub(r"ದಲ್ಲಿ(?=[^ಀ-ഀ]|$)", "ದಾಗ", res)
            res = re.sub(r"ನಲ್ಲಿ(?=[^ಀ-ഀ]|$)", "ನಾಗ", res)
            res = re.sub(r"ಗಳನ್ನು(?=[^ಀ-ഀ]|$)", "", res)
            res = re.sub(r"ಕೊಳ್ಳಿ(?=[^ಀ-ഀ]|$)", "ಕೊಳ್ರಿ", res)
            res = re.sub(r"(ಮಾಡಿ|ಹಾಕಿ|ನೋಡಿ|ಕೊಡಿ|ಹೇಳಿ|ತುಂಬಿ)(?=[^ಀ-ഀ]|$)", lambda m: m.group(1)[:-1] + "್ರಿ", res)
            if "ದೋಸ್ತ್" not in res and ("ರೊಕ್ಕ" in res or "ಕೊಳ್ರಿ" in res or "ಸಾಲಿ" in res):
                res = "ದೋಸ್ತ್, " + res.lstrip()
            return res

        elif region_key == "co":
            for s, d in self.co_phrases:
                res = res.replace(s, d)
            for s, d in self.co_vocab.items():
                res = re.sub(r"(?<![\u0C80-\u0D00])" + re.escape(s) + r"(?=[^\u0C80-\u0D00]|$)", d, res)
            # Coastal morphology
            res = re.sub(r"([ಕ-ಹ]+)ುತ್ತಿದ್ದಾನೆ", r"\1್ತಾ ಇದ್ದಾನೆ", res)
            res = re.sub(r"([ಕ-ಹ]+)ುತ್ತಿದ್ದಾಳೆ", r"\1್ತಾ ಇದ್ದಾಳೆ", res)
            res = re.sub(r"([ಕ-ಹ]+)ುತ್ತಿದ್ದಾರೆ", r"\1್ತಾ ಇದ್ದಾರೆ", res)
            res = re.sub(r"([ಕ-ಹ]+)ುತ್ತಿದ್ದೀರಿ", r"\1್ತಾ ಇದ್ದೀರಿ", res)
            res = re.sub(r"([ಕ-ಹ]+)ುತ್ತಿದ್ದೇನೆ", r"\1್ತಾ ಇದ್ದೇನೆ", res)
            res = re.sub(r"([ಕ-ಹ]+)ುತ್ತಿದೆ", r"\1್ತಾ ಉಂಡು", res)
            res = re.sub(r"([ಕ-ಹ]+)ಲಿಲ್ಲವೇ\?", r"\1ಿಲ್ವಾ?", res)
            res = re.sub(r"ದಲ್ಲಿ(?=[^ಀ-ഀ]|$)", "ಲ್", res)
            res = re.sub(r"ನಲ್ಲಿ(?=[^ಀ-ഀ]|$)", "ಲ್", res)
            res = re.sub(r"ಗಳನ್ನು(?=[^ಀ-ഀ]|$)", "", res)
            res = re.sub(r"ಕೊಳ್ಳಿ(?=[^ಀ-ഀ]|$)", "ಕೊಳಿ", res)
            if "ಮಾರೆ" not in res and not res.endswith("?"):
                res = "ಮಾರೆ, " + res.lstrip()
            return res

        elif region_key == "uk":
            for s, d in self.uk_phrases:
                res = res.replace(s, d)
            for s, d in self.uk_vocab.items():
                res = re.sub(r"(?<![\u0C80-\u0D00])" + re.escape(s) + r"(?=[^\u0C80-\u0D00]|$)", d, res)
            # UK morphology
            res = re.sub(r"([ಕ-ಹ]+)(ತ್ತದೆ|ತ್ತಿದೆ)(?=[^\u0C80-\u0D00]|$)", r"\1ವುತ್ತೆ", res)
            res = re.sub(r"([ಕ-ಹ]+)ಬೇಕು(?=[^\u0C80-\u0D00]|$)", r"\1ತಕ್ಕು", res)
            res = re.sub(r"([ಕ-ಹ]+)ೋಣ(?=[^\u0C80-\u0D00]|$)", r"\1ುವಾ", res)
            res = re.sub(r"([ಕ-ಹ]+)ಿದ್ದೇನೆ(?=[^\u0C80-\u0D00]|$)", r"\1ಿದೀನಿ", res)
            res = re.sub(r"ದಲ್ಲಿ(?=[^\u0C80-\u0D00]|$)", "ಲ್ಲಿ", res)
            res = re.sub(r"ನಲ್ಲಿ(?=[^\u0C80-\u0D00]|$)", "ನಲ್ಲಿ", res)
            res = re.sub(r"ಗಳನ್ನು(?=[^\u0C80-\u0D00]|$)", "", res)
            res = re.sub(r"ಕೊಳ್ಳಿ(?=[^\u0C80-\u0D00]|$)", "ಗೊಳ್ಳಿ", res)
            return res

        elif region_key == "sm":
            for s, d in self.sm_phrases:
                res = res.replace(s, d)
            for s, d in self.sm_vocab.items():
                res = re.sub(r"(?<![\u0C80-\u0D00])" + re.escape(s) + r"(?=[^\u0C80-\u0D00]|$)", d, res)
            res = re.sub(r"ಗಳನ್ನು(?=[^ಀ-ഀ]|$)", "", res)
            if not res.endswith("?") and not res.endswith("ಕಣ್ರೀ") and not res.endswith("ಕಣ್ರೀ."):
                res = res.rstrip(". ") + " ಕಣ್ರೀ."
            return res

        return res

    def generate_all_dialects(self, standard_text: str) -> Dict[str, Dict[str, str]]:
        """
        Takes standard textbook Kannada text (or spoken dialect text) and generates
        authentic regional spoken Kannada sentences across the major Karnataka dialects.
        """
        if not standard_text or not standard_text.strip():
            return {}

        clean = standard_text.strip()

        nk = self._synthesize(clean, "nk")
        kk = self._synthesize(clean, "kk")
        co = self._synthesize(clean, "co")
        uk = self._synthesize(clean, "uk")
        sm = self._synthesize(clean, "sm")

        return {
            "North Karnataka": {
                "name_kn": "ಉತ್ತರ ಕರ್ನಾಟಕ (ಧಾರವಾಡ/ಹುಬ್ಬಳ್ಳಿ)",
                "icon": "🌾",
                "text": nk,
                "accent_tag": "-ಆಕತ್ತ ಕ್ರಿಯಾಪದ & ಉತ್ತರ ಕರ್ನಾಟಕ ಶೈಲಿ"
            },
            "Kalyana Karnataka": {
                "name_kn": "ಕಲ್ಯಾಣ ಕರ್ನಾಟಕ (ಕಲಬುರಗಿ/ಬೀದರ್)",
                "icon": "🕌",
                "text": kk,
                "accent_tag": "-ಲಿಕ್ಕತ್ತ ಪ್ರತ್ಯಯ & ಗಡಿನಾಡ ರೊಕ್ಕ/ದೋಸ್ತ್ ಶೈಲಿ"
            },
            "Coastal / Kundagannada": {
                "name_kn": "ಕರಾವಳಿ / ಕುಂದಗನ್ನಡ (ಮಂಗಳೂರು/ಕುಂದಾಪುರ)",
                "icon": "🌊",
                "text": co,
                "accent_tag": "ಎಂತ ಮಾರೆ ಸಂಬೋಧನೆ & ಕರಾವಳಿ ಕ್ರಿಯಾರೂಪ"
            },
            "Uttara Kannada / Havyaka": {
                "name_kn": "ಉತ್ತರ ಕನ್ನಡ / ಹವ್ಯಕ (ಶಿರಸಿ/ಕಾರವಾರ)",
                "icon": "🌿",
                "text": uk,
                "accent_tag": "ಅನುನಾಸಿಕ ಸರ್ವನಾಮಗಳು (ನಾಂ, ನೀಂ, ಅವಂ)"
            },
            "Mysuru-Mandya": {
                "name_kn": "ಮೈಸೂರು-ಮಂಡ್ಯ (ದಕ್ಷಿಣ ಕರ್ನಾಟಕ)",
                "icon": "🏛️",
                "text": sm,
                "accent_tag": "-ಆವನೆ ಪ್ರವರ್ತಮಾನ & ಕಣ್ರೀ ವಿಸ್ತರಣೆ"
            }
        }

ETYMOLOGY_DATA = {
    "ರೊಕ್ಕ": {
        "word": "ರೊಕ್ಕ",
        "standard": "ಹಣ (Money)",
        "region": "ಕಲ್ಯಾಣ & ಉತ್ತರ ಕರ್ನಾಟಕ",
        "context": "ಹೈದರಾಬಾದ್-ಕರ್ನಾಟಕ ಹಾಗೂ ಬಹಮನಿ ಕಾಲದ 'ರೊಕ್ಕಂ' (ನಗದು ದಾಖಲೆ) ಆಡಳಿತ ಶಬ್ದದಿಂದ ಬಂದಿದೆ."
    },
    "ದೋಸ್ತ್": {
        "word": "ದೋಸ್ತ್",
        "standard": "ಗೆಳೆಯ / ಮಿತ್ರ (Friend)",
        "region": "ಕಲ್ಯಾಣ ಕರ್ನಾಟಕ (ಕಲಬುರಗಿ-ಬೀದರ್)",
        "context": "ದಖ್ಖನಿ ಹಾಗೂ ಗಡಿನಾಡ ಭ್ರಾತೃತ್ವದ ಸ್ನೇಹಪರ ಸಂಬೋಧನೆ."
    },
    "ಎಂತ": {
        "word": "ಎಂತ",
        "standard": "ಏನು (What)",
        "region": "ಕರಾವಳಿ & ಕುಂದಗನ್ನಡ",
        "context": "ಕರಾವಳಿ ಭಾಗದ ವಿಶಿಷ್ಟ ಪ್ರಶ್ನಾವಾಚಕ ಧಾತು."
    },
    "ಮಾರೆ": {
        "word": "ಮಾರೆ",
        "standard": "ಗೆಳೆಯ / ಒಡನಾಡಿ (Pal)",
        "region": "ಕುಂದಗನ್ನಡ & ಕರಾವಳಿ",
        "context": "ಸ್ನೇಹಿತರನ್ನು ಗೌರವ ಹಾಗೂ ಸಲುಗೆಯಿಂದ ಕರೆಯುವ ಕರಾವಳಿಯ ವಿಶಿಷ್ಟ ಸಂಬೋಧನೆ."
    },
    "ಬರಾಕತ್ತಾನ": {
        "word": "ಬರಾಕತ್ತಾನ",
        "standard": "ಬರುತ್ತಿದ್ದಾನೆ (Coming)",
        "region": "ಉತ್ತರ ಕರ್ನಾಟಕ (ಧಾರವಾಡ-ಹುಬ್ಬಳ್ಳಿ)",
        "context": "ಹಳಗನ್ನಡದ 'ಬರಲ್ + ಕೆಯ್' (ಕ್ರಿಯೆ ಜಾರಿಯಲ್ಲಿರುವಿಕೆ) ಪ್ರತ್ಯಯವು ಧಾರವಾಡ ಕನ್ನಡದಲ್ಲಿ ಇಂದಿಗೂ ಸಜೀವವಾಗಿದೆ."
    },
    "ಸಾಲಿಗೆ": {
        "word": "ಸಾಲಿಗೆ",
        "standard": "ಶಾಲೆಗೆ (To School)",
        "region": "ಉತ್ತರ & ಕಲ್ಯಾಣ ಕರ್ನಾಟಕ",
        "context": "ಸಂಸ್ಕೃತ 'ಶಾಲಾ' ಶಬ್ದವು ಪ್ರಾಕೃತದ ಮೂಲಕ 'ಸಾಲಿ' ಆಗಿ ದೇಶೀಯ ಕನ್ನಡದಲ್ಲಿ ಉಳಿದುಕೊಂಡಿದೆ."
    },
    "ಐತಿ": {
        "word": "ಐತಿ",
        "standard": "ಇದೆ (Exists)",
        "region": "ಉತ್ತರ & ಕಲ್ಯಾಣ ಕರ್ನಾಟಕ",
        "context": "ದ್ರಾವಿಡ ಮೂಲದ ಅಸ್ತಿತ್ವವಾಚಕ ಕ್ರಿಯಾಪದದ ಪುರಾತನ ದೇಶ್ಯ ರೂಪ."
    },
    "ನಾಂ": {
        "word": "ನಾಂ",
        "standard": "ನಾನು (I)",
        "region": "ಹವ್ಯಕ & ಉತ್ತರ ಕನ್ನಡ",
        "context": "ಮಧ್ಯಕಾಲೀನ ಕನ್ನಡದ ಅನುನಾಸಿಕ ಅಂತ್ಯವು ಹವ್ಯಕ ಭಾಷಿಕರಲ್ಲಿ ಇಂದಿಗೂ ನೈಜವಾಗಿ ಉಳಿದಿದೆ."
    }
}

def get_etymology(text: str) -> list:
    results = []
    for word, info in ETYMOLOGY_DATA.items():
        if word in text:
            results.append(info)
    return results
