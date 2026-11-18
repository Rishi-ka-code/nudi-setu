# -*- coding: utf-8 -*-
"""
Generates comprehensive dialect lexicons and morphological transformation rules
for Kannada dialect normalizer.
Covers:
- North Karnataka (Hubballi-Dharwad, Belagavi, Vijayapura)
- Kalyana Karnataka (Kalaburagi, Bidar, Raichur, Koppal, Yadgir)
- Coastal / Kundagannada (Mangaluru, Udupi, Kundapura)
- Uttara Kannada / Havyaka (Sirsi, Karwar, Gokarna)
- Mysuru-Mandya / South Karnataka
"""

import json
import os

LEXICONS = {
    "North Karnataka": {
        "region_code": "NK",
        "name_kn": "ಉತ್ತರ ಕರ್ನಾಟಕ (ಹುಬ್ಬಳ್ಳಿ-ಧಾರವಾಡ, ಬೆಳಗಾವಿ, ವಿಜಯಪುರ)",
        "vocabulary": {
            # Pronouns
            "ಅವ": "ಅವನು",
            "ಅಕಿ": "ಅವಳು",
            "ಅಕೀ": "ಅವಳು",
            "ಅವ್ರು": "ಅವರು",
            "ನಾವ್ರ": "ನಾವು",
            "ನಮ್ದ": "ನಮ್ಮದು",
            "ನಿಮ್ದ": "ನಿಮ್ಮದು",
            "ಅವ್ದ": "ಅವರದು",
            "ಯಾರ್ದ": "ಯಾರದು",
            "ನನಗ": "ನನಗೆ",
            "ನಿನಗ": "ನಿನಗೆ",
            "ಅವನಗ": "ಅವನಿಗೆ",
            "ನಂಗೂ": "ನನಗೂ",
            "ನಂಗ್": "ನನಗೆ",
            "ನಿಂಗ್": "ನಿನಗೆ",
            "ಅವಂಗ್": "ಅವನಿಗೆ",
            # Interrogatives
            "ಯಾಕ": "ಏಕೆ",
            "ಯಾಕ್ರಿ": "ಏಕೆ",
            "ಯಾಕಪ್ಪಾ": "ಏಕೆ",
            "ಏನ್ರಿ": "ಏನು",
            "ಏನ್ಪಾ": "ಏನು",
            "ಎಲ್ಲಿಗ್": "ಎಲ್ಲಿಗೆ",
            "ಹೆಂಗ": "ಹೇಗೆ",
            "ಹಿಂಗ್ಯಾಕ್": "ಏಕೆ ಹೀಗೆ",
            "ಹಂಗ್ಯಾಕ್": "ಏಕೆ ಹಾಗೆ",
            # Adverbs & Time
            "ಹಿಂಗ": "ಹೀಗೆ",
            "ಹಂಗ": "ಹಾಗೆ",
            "ಇವ್ವತ್": "ಇಂದು",
            "ನಾಳಿಕಿ": "ನಾಳೆ",
            "ಅಂದರ್ತಿ": "ಹಾಗಾದರೆ",
            "ಹಂಗಾರ": "ಹಾಗಾದರೆ",
            "ಇಲ್ಲೇ": "ಇಲ್ಲಿಯೇ",
            "ಅಲ್ಲೇ": "ಅಲ್ಲಿಯೇ",
            "ಅಲ್ರೀ": "ಅಲ್ಲವೇ",
            # Adjectives & Modifiers
            "ಬೊವ್ವ": "ತುಂಬಾ",
            "ಬಹಳ": "ತುಂಬಾ",
            "ಚೊಲೋ": "ಒಳ್ಳೆಯ",
            "ಖರೆ": "ನಿಜ",
            "ಖರೇ": "ನಿಜ",
            "ಸುಮ್ನ": "ಸುಮ್ಮನೆ",
            "ಮಳಿ": "ಮಳೆ",
            "ಕೆಲ್ಸ": "ಕೆಲಸ",
            "ಕೆಲ್ಸಾನ": "ಕೆಲಸವೇ",
            "ಮಾತ": "ಮಾತು",
            "ಹೊತ್ತ": "ಸಮಯ",
            # Verbs & Copulas
            "ಐತಿ": "ಇದೆ",
            "ಐತ್ರಿ": "ಇದೆ",
            "ಇಲ್ಲೇನ್ರಿ": "ಇಲ್ಲವೇ",
            "ಗೊತ್ತಿಲ್ರಿ": "ಗೊತ್ತಿಲ್ಲ",
            "ಗೊತ್ತಿತ್ರಿ": "ಗೊತ್ತಿತ್ತು",
            "ಆತೇನ್ರಿ": "ಆಯಿತೇ",
            "ಹೊಂಟಿ": "ಹೊರಟಿದ್ದೀಯಾ",
            "ಹೊಂಟೆ": "ಹೊರಟಿದ್ದೇನೆ",
            "ಹೊಂಟಾರ": "ಹೊರಟಿದ್ದಾರೆ",
            "ನಡೀರಿ": "ನಡೆಯಿರಿ",
            "ನೋಡ್ರಿ": "ನೋಡಿ",
            "ಅಂದಿದ್ವಿ": "ಹೇಳಿದ್ದೆವು",
            "ಬ್ಯಾಡ": "ಬೇಡ",
            "ಬೇಡ್ರಿ": "ಬೇಡ",
            "ಆತ್ರಿ": "ಆಯಿತು",
            "ಹೌದ್ರಿ": "ಹೌದು",
            "ಇಲ್ರಿ": "ಇಲ್ಲ"
        }
    },
    "Kalyana Karnataka": {
        "region_code": "KK",
        "name_kn": "ಕಲ್ಯಾಣ ಕರ್ನಾಟಕ (ಕಲಬುರಗಿ, ಬೀದರ್, ರಾಯಚೂರು, ಕೊಪ್ಪಳ, ಯಾದಗಿರಿ)",
        "vocabulary": {
            # Unique KK vocabulary (Urdu/Deccan influenced)
            "ರೊಕ್ಕ": "ಹಣ",
            "ಮನಿ": "ಮನೆ",
            "ಸಾಲಿ": "ಶಾಲೆ",
            "ದೋಸ್ತ್": "ಗೆಳೆಯ",
            "ದೋಸ್ತ್ರ": "ಗೆಳೆಯರೇ",
            "ಬಾಳಾ": "ತುಂಬಾ",
            "ಖೂಬ್": "ತುಂಬಾ",
            "ಜಲ್ದಿ": "ಬೇಗ",
            "ಬೆಪ್ಸಾ": "ಮೂರ್ಖ",
            "ತಕ್ಲಿಫ್": "ತೊಂದರೆ",
            "ಗಮ್ಮತ್": "ಮೋಜು",
            "ದಂಡಿ": "ದಡ",
            "ಆರಾಮ್": "ಕ್ಷೇಮ",
            "ಬ್ಯಾರೆ": "ಬೇರೆ",
            "ಗಿಂಡಿ": "ಚೊಂಬು",
            "ಹುಡುಗ್ಯಾ": "ಹುಡುಗ",
            "ಕಮಾಯಿ": "ಗಳಿಕೆ",
            "ವಖ್ತ್": "ಸಮಯ",
            "ಪರೇಶಾನ್": "ಚಿಂತೆ",
            "ಮಾತ್": "ಮಾತು",
            "ನಾವ್ರ": "ನಾವು",
            "ಅವ್ರ": "ಅವರು",
            "ನಮ್ದು": "ನಮ್ಮದು",
            "ನಿಮ್ದು": "ನಿಮ್ಮದು"
        }
    },
    "Coastal / Kundagannada": {
        "region_code": "CO",
        "name_kn": "ಕರಾವಳಿ / ಕುಂದಗನ್ನಡ (ಮಂಗಳೂರು, ಉಡುಪಿ, ಕುಂದಾಪುರ)",
        "vocabulary": {
            # Address & Particles
            "ಮಾರೆ": "ಗೆಳೆಯ",
            "ಮಾರ್ರೆ": "ಗೆಳೆಯರೇ",
            "ಎಂತ": "ಏನು",
            "ಎಂತಕ್ಕ್": "ಏತಕ್ಕಾಗಿ",
            "ಎಂತಕೆ": "ಏತಕ್ಕೆ",
            "ಅದ್ಕೆ": "ಅದಕ್ಕೆ",
            "ಇದ್ಕೆ": "ಇದಕ್ಕೆ",
            # Pronouns
            "ನಾನ್": "ನಾನು",
            "ನೀನ್": "ನೀನು",
            "ಅವ್ರ": "ಅವರ",
            "ನೀವ್": "ನೀವು",
            "ಯಾರ್": "ಯಾರೂ",
            "ಅದ್": "ಅದು",
            # Adverbs & Time
            "ಇವತ್ತು": "ಇಂದು",
            "ಹಿಂಗ್": "ಹೀಗೆ",
            "ಹಂಗ್": "ಹಾಗೆ",
            "ಬಾರೀ": "ತುಂಬಾ",
            "ಆರಾಮಾ": "ಕ್ಷೇಮವೇ",
            "ಆರಾಮ್ದಲ್ಲಿ": "ಕ್ಷೇಮವಾಗಿ",
            "ಚಾ": "ಚಹಾ",
            # Verbs & Participles
            "ಪೋಯಿ": "ಹೋಗಿ",
            "ಬರ್ಪೆ": "ಬರುತ್ತೇನೆ",
            "ಪೋಪೆ": "ಹೋಗುತ್ತೇನೆ",
            "ತಿಂಬೆ": "ತಿನ್ನುತ್ತೇನೆ",
            "ತಿಂದ್ಯಾ": "ತಿಂದೆಯಾ",
            "ಆತ್": "ಆಯಿತು",
            "ಆತಾ": "ಆಯಿತೇ",
            "ಹೇಳ್ದೆ": "ಹೇಳಿದೆ",
            "ಕೇಳ್ದೆ": "ಕೇಳಿದೆ",
            "ಕುಡ್ದ್ರಾ": "ಕುಡಿದಿರಾ",
            "ಹೋದ್ರೆ": "ಹೋದರೆ",
            "ಸಿಗ್ಲಿಲ್ಲ": "ಸಿಗಲಿಲ್ಲ",
            "ಗೊತ್ತಾತ್": "ತಿಳಿಯಿತು",
            "ಬಿಟ್ಬುಡ್ತಾರೆ": "ಹೊರಟುಬಿಡುತ್ತಾರೆ",
            "ತಡ್ಕೋ": "ಸಹಿಸಿಕೋ",
            "ಶಾಲೆಗ್": "ಶಾಲೆಗೆ",
            "ಮನೆಲ್": "ಮನೆಯಲ್ಲಿ",
            "ಪೇಟೆಗ್": "ಪೇಟೆಗೆ"
        }
    },
    "Uttara Kannada / Havyaka": {
        "region_code": "UK",
        "name_kn": "ಉತ್ತರ ಕನ್ನಡ / ಹವ್ಯಕ (ಶಿರಸಿ, ಕಾರವಾರ, ಗೋಕರ್ಣ)",
        "vocabulary": {
            # Archaic Pronouns (Nasal endings)
            "ನಾಂ": "ನಾನು",
            "ನೀಂ": "ನೀನು",
            "ಅವಂ": "ಅವನು",
            "ಅವಳ್": "ಅವಳು",
            "ಎಲ್ಲೋರು": "ಎಲ್ಲರೂ",
            # Interrogatives & Modifiers
            "ಏಂ": "ಏನು",
            "ಹೆಂಗೆ": "ಹೇಗೆ",
            "ಎಲ್ಲಿಗೆ": "ಎಲ್ಲಿಗೆ",
            "ಕಾಸಿಲ್ದೆ": "ಹಣವಿಲ್ಲದೆ",
            "ಅಪ್ಪಚ್ಚಿ": "ತಂದೆಯವರು",
            "ಅಪ್ಪ": "ತಂದೆ",
            "ಕೊಡೆ": "ಛತ್ರಿ",
            # Verbs
            "ಬತ್ತೆ": "ಬರುತ್ತೇನೆ",
            "ಬತ್ತಿ": "ಬರುತ್ತೀಯ",
            "ಹೋತ್ತೆ": "ಹೋಗುತ್ತೇನೆ",
            "ಮಾಡ್ತಿದ್ದಿ": "ಮಾಡುತ್ತಿದ್ದೀಯಾ",
            "ತಕ್ಕೋ": "ತೆಗೆದುಕೊ",
            "ಗೊತ್ತಾಪೋದಿಲ್ಲ": "ತಿಳಿಯುವುದಿಲ್ಲ",
            "ಹಾಳಾಪೋದು": "ಹಾಳಾಗುವುದು",
            "ಆಪೋದಿಲ್ಲ": "ಆಗುವುದಿಲ್ಲ",
            "ಕೂತ್ಕಂಡ್ರಾ": "ಕುಳಿತುಕೊಂಡಿರಾ",
            "ಹೇಳಿದ್ದ": "ಹೇಳಿದ"
        }
    },
    "Mysuru-Mandya": {
        "region_code": "SM",
        "name_kn": "ಮೈಸೂರು-ಮಂಡ್ಯ (ದಕ್ಷಿಣ ಕರ್ನಾಟಕ)",
        "vocabulary": {
            # Discourse particles
            "ಕಣಯ್ಯ": "",
            "ಕಣ್ರೀ": "",
            "ಕಣೋ": "",
            "ಕಣೇ": "",
            "ಅಯ್ಯೋ": "ಅಯ್ಯೋ",
            "ಹಂಗ್ಯಾಕೆ": "ಹಾಗೇಕೆ",
            "ಹಿಂಗ್ಯಾಕೆ": "ಹಾಗೇಕೆ",
            "ಮಾಡ್ದೆ": "ಮಾಡಿದೆ",
            "ಬಂದ್ರಿ": "ಬಂದಿರಿ",
            "ಹೋದ್ರಿ": "ಹೋದಿರಿ",
            "ತಿಂಡ್ರಿ": "ತಿಂದಿರಿ",
            "ನಾವೆಲ್ಲಾ": "ನಾವೆಲ್ಲರೂ",
            "ಸುಮ್ನಿರು": "ಸುಮ್ಮನಿರು",
            "ರೇಗಾಡಬೇಡ": "ಕೋಪಿಸಿಕೊಳ್ಳಬೇಡ",
            "ತಲೆ ತಿಂತಾವನೆ": "ತೊಂದರೆ ಕೊಡುತ್ತಿದ್ದಾನೆ",
            "ಹೋಗ್ಬಿಟ್ಟವನೆ": "ಹೋಗಿಬಿಟ್ಟಿದ್ದಾನೆ",
            "ಇಟ್ಬುಟ್ಟು": "ಇಟ್ಟುಬಿಟ್ಟು",
            "ಮಾಡೋದು": "ಮಾಡುವುದು",
            "ಹೋಗೋದು": "ಹೋಗುವುದು",
            "ಬರೋದು": "ಬರುವುದು",
            "ಮಾಡೋಕಾಗುತ್ತೆ": "ಮಾಡಲು ಸಾಧ್ಯ",
            "ಮಾಡೋಕಾಗಲ್ಲ": "ಮಾಡಲು ಸಾಧ್ಯವಿಲ್ಲ"
        }
    }
}

REGIONAL_MARKERS = {
    "morphological_rules": [
        # --- 1. North Karnataka & Kalyana Karnataka Progressive Aspect ---
        {
            "pattern": r"([ಕ-ಹ][ಾ-್]*)ಾಕತ್ತಾನ(?=[^\u0C80-\u0CFF]|$)",
            "replacement": r"\1ುತ್ತಿದ್ದಾನೆ",
            "description": "North Karnataka 3rd masc continuous (-ಆಕತ್ತಾನ -> -ಉತ್ತಿದ್ದಾನೆ)"
        },
        {
            "pattern": r"([ಕ-ಹ][ಾ-್]*)ಾಕತ್ತಾಳ(?=[^\u0C80-\u0CFF]|$)",
            "replacement": r"\1ುತ್ತಿದ್ದಾಳೆ",
            "description": "North Karnataka 3rd fem continuous (-ಆಕತ್ತಾಳ -> -ಉತ್ತಿದ್ದಾಳೆ)"
        },
        {
            "pattern": r"([ಕ-ಹ][ಾ-್]*)ಾಕತ್ತಾರ(?=[^\u0C80-\u0CFF]|$)",
            "replacement": r"\1ುತ್ತಿದ್ದಾರೆ",
            "description": "North Karnataka 3rd plural continuous (-ಆಕತ್ತಾರ -> -ಉತ್ತಿದ್ದಾರೆ)"
        },
        {
            "pattern": r"([ಕ-ಹ][ಾ-್]*)ಾಕತ್ತೀನಿ(?=[^\u0C80-\u0CFF]|$)",
            "replacement": r"\1ುತ್ತಿದ್ದೇನೆ",
            "description": "North Karnataka 1st person continuous (-ಆಕತ್ತೀನಿ -> -ಉತ್ತಿದ್ದೇನೆ)"
        },
        {
            "pattern": r"([ಕ-ಹ][ಾ-್]*)ಾಕತ್ತೈತಿ(?=[^\u0C80-\u0CFF]|$)",
            "replacement": r"\1ುತ್ತಿದೆ",
            "description": "North Karnataka neuter continuous (-ಆಕತ್ತೈತಿ -> -ಉತ್ತಿದೆ)"
        },
        {
            "pattern": r"([ಕ-ಹ][ಾ-್]*)ಲಿಕ್ಕತ್ತಾನ(?=[^\u0C80-\u0CFF]|$)",
            "replacement": r"\1ುತ್ತಿದ್ದಾನೆ",
            "description": "Kalyana Karnataka 3rd masc continuous (-ಲಿಕ್ಕತ್ತಾನ -> -ುತ್ತಿದ್ದಾನೆ)"
        },
        {
            "pattern": r"([ಕ-ಹ][ಾ-್]*)ಲಿಕ್ಕತ್ತಾಳ(?=[^\u0C80-\u0CFF]|$)",
            "replacement": r"\1ುತ್ತಿದ್ದಾಳೆ",
            "description": "Kalyana Karnataka 3rd fem continuous (-ಲಿಕ್ಕತ್ತಾಳ -> -ುತ್ತಿದ್ದಾಳೆ)"
        },
        {
            "pattern": r"([ಕ-ಹ][ಾ-್]*)ಲಿಕ್ಕತ್ತಾರ(?=[^\u0C80-\u0CFF]|$)",
            "replacement": r"\1ುತ್ತಿದ್ದಾರೆ",
            "description": "Kalyana Karnataka 3rd plural continuous (-ಲಿಕ್ಕತ್ತಾರ -> -ುತ್ತಿದ್ದಾರೆ)"
        },
        {
            "pattern": r"([ಕ-ಹ][ಾ-್]*)ಅಲಿಕ್ಕತ್ತೈತಿ(?=[^\u0C80-\u0CFF]|$)",
            "replacement": r"\1ುತ್ತಿದೆ",
            "description": "Continuous neuter variant (-ಅಲಿಕ್ಕತ್ತೈತಿ -> -ಉತ್ತಿದೆ)"
        },

        # --- 2. NK & KK Perfective Suffixes ---
        {
            "pattern": r"([ಕ-ಹ]+)್ಯಾನ(?=[^\u0C80-\u0CFF]|$)",
            "replacement": r"\1ಿದ್ದಾನೆ",
            "description": "NK/KK 3rd masc perfective (-್ಯಾನ -> -ಿದ್ದಾನೆ, e.g. ಬಂದ್ಯಾನ -> ಬಂದಿದ್ದಾನೆ)"
        },
        {
            "pattern": r"([ಕ-ಹ]+)್ಯಾರ(?=[^\u0C80-\u0CFF]|$)",
            "replacement": r"\1ಿದ್ದಾರೆ",
            "description": "NK/KK 3rd plural perfective (-್ಯಾರ -> -ಿದ್ದಾರೆ, e.g. ಮಾಡ್ಯಾರ -> ಮಾಡಿದ್ದಾರೆ)"
        },
        {
            "pattern": r"([ಕ-ಹ]+)್ಯಾವ(?=[^\u0C80-\u0CFF]|$)",
            "replacement": r"\1ಿವೆ",
            "description": "NK/KK neuter plural perfective (-್ಯಾವ -> -ಿವೆ)"
        },
        {
            "pattern": r"([ಕ-ಹ]+)ೀನಿ(?=[^\u0C80-\u0CFF]|$)",
            "replacement": r"\1ಿದ್ದೇನೆ",
            "description": "NK/KK 1st person perfective (-ೀನಿ -> -ಿದ್ದೇನೆ, e.g. ಮಾಡೀನಿ -> ಮಾಡಿದ್ದೇನೆ, ಬಂದೀನಿ -> ಬಂದಿದ್ದೇನೆ)"
        },

        # --- 3. Modal Necessity & Prohibitive Contractions ---
        {
            "pattern": r"([ಕ-ಹ][ಾ-್]*)್ಬೇಕು(?=[^\u0C80-\u0CFF]|$)",
            "replacement": r"\1ಬೇಕು",
            "description": "Modal necessity contraction (-್ಬೇಕು -> -ಬೇಕು, e.g. ಹೋಗ್ಬೇಕು -> ಹೋಗಬೇಕು, ಮಾಡ್ಬೇಕು -> ಮಾಡಬೇಕು)"
        },
        {
            "pattern": r"([ಕ-ಹ][ಾ-್]*)್ಬಾರ್ದು(?=[^\u0C80-\u0CFF]|$)",
            "replacement": r"\1ಬಾರದು",
            "description": "Modal prohibitive contraction (-್ಬಾರ್ದು -> -ಬಾರದು, e.g. ಮಾಡ್ಬಾರ್ದು -> ಮಾಡಬಾರದು)"
        },
        {
            "pattern": r"([ಕ-ಹ][ಾ-್]*)್ಕೂಡ್ದು(?=[^\u0C80-\u0CFF]|$)",
            "replacement": r"\1ಕೂಡದು",
            "description": "Prohibitive contraction (-್ಕೂಡ್ದು -> -ಕೂಡದು)"
        },

        # --- 4. Purposive Infinitives & Impossibility ---
        {
            "pattern": r"([ಕ-ಹ][ಾ-್]*)ೋಕಾಗಲ್ಲ(?=[^\u0C80-\u0CFF]|$)",
            "replacement": r"\1ಲು ಸಾಧ್ಯವಿಲ್ಲ",
            "description": "Colloquial impossibility (-ೋಕಾಗಲ್ಲ -> -ಲು ಸಾಧ್ಯವಿಲ್ಲ, e.g. ಮಾಡೋಕಾಗಲ್ಲ -> ಮಾಡಲು ಸಾಧ್ಯವಿಲ್ಲ)"
        },
        {
            "pattern": r"([ಕ-ಹ][ಾ-್]*)ಾಕಾಗಲ್ಲ(?=[^\u0C80-\u0CFF]|$)",
            "replacement": r"\1ಲು ಸಾಧ್ಯವಿಲ್ಲ",
            "description": "NK impossibility (-ಾಕಾಗಲ್ಲ -> -ಲು ಸಾಧ್ಯವಿಲ್ಲ, e.g. ಮಾಡಾಕಾಗಲ್ಲ -> ಮಾಡಲು ಸಾಧ್ಯವಿಲ್ಲ)"
        },
        {
            "pattern": r"([ಕ-ಹ][ಾ-್]*)ಕ್ಕಾಗಲ್ಲ(?=[^\u0C80-\u0CFF]|$)",
            "replacement": r"\1ಲು ಸಾಧ್ಯವಿಲ್ಲ",
            "description": "Impossibility contraction (-ಕ್ಕಾಗಲ್ಲ -> -ಲು ಸಾಧ್ಯವಿಲ್ಲ)"
        },
        {
            "pattern": r"([ಕ-ಹ][ಾ-್]*)ೋಕೆ(?=[^\u0C80-\u0CFF]|$)",
            "replacement": r"\1ಲು",
            "description": "Purposive infinitive (-ೋಕೆ -> -ಲು, e.g. ಮಾಡೋಕೆ -> ಮಾಡಲು, ಹೋಗೋಕೆ -> ಹೋಗಲು)"
        },
        {
            "pattern": r"([ಕ-ಹ][ಾ-್]*)ಾಕ(?=[^\u0C80-\u0CFF]|$)",
            "replacement": r"\1ಲು",
            "description": "NK purposive infinitive (-ಾಕ -> -ಲು, e.g. ಮಾಡಾಕ -> ಮಾಡಲು, ಬರಾಕ -> ಬರಲು)"
        },

        # --- 5. Contracted Interrogatives (Prompt canonical: ಅವನು ಬರ್ತಾನಾ? -> ಅವನು ಬರುತ್ತಾನೆಯೇ?) ---
        {
            "pattern": r"([ಕ-ಹ]+)ರ್ತಾನಾ\?",
            "replacement": r"\1ರುತ್ತಾನೆಯೇ?",
            "description": "Contracted interrogative 3rd masc (-ರ್ತಾನಾ? -> -ರುತ್ತಾನೆಯೇ?)"
        },
        {
            "pattern": r"([ಕ-ಹ]+)ರ್ತಾನಾ(?=[^\u0C80-\u0CFF]|$)",
            "replacement": r"\1ರುತ್ತಾನೆಯೇ",
            "description": "Contracted interrogative 3rd masc (-ರ್ತಾನಾ -> -ರುತ್ತಾನೆಯೇ)"
        },
        {
            "pattern": r"([ಕ-ಹ]+)ರ್ತಾಳಾ\?",
            "replacement": r"\1ರುತ್ತಾಳೆಯೇ?",
            "description": "Contracted interrogative 3rd fem (-ರ್ತಾಳಾ? -> -ರುತ್ತಾಳೆಯೇ?)"
        },
        {
            "pattern": r"([ಕ-ಹ]+)ರ್ತಾರಾ\?",
            "replacement": r"\1ರುತ್ತಾರೆಯೇ?",
            "description": "Contracted interrogative 3rd plural (-ರ್ತಾರಾ? -> -ರುತ್ತಾರೆಯೇ?)"
        },
        {
            "pattern": r"([ಕ-ಹ]+)ರ್ತೀರಾ\?",
            "replacement": r"\1ರುತ್ತೀರಾ?",
            "description": "Contracted interrogative 2nd plural honorific (-ರ್ತೀರಾ? -> -ರುತ್ತೀರಾ?)"
        },
        {
            "pattern": r"([ಕ-ಹ]+)ರ್ತೀಯಾ\?",
            "replacement": r"\1ರುತ್ತೀಯಾ?",
            "description": "Contracted interrogative 2nd person singular (-ರ್ತೀಯಾ? -> -ರುತ್ತೀಯಾ?)"
        },
        {
            "pattern": r"([ಕ-ಹ]+)ರ್ತಾರ(?=[^\u0C80-\u0CFF]|$)",
            "replacement": r"\1ರುತ್ತಾರೆ",
            "description": "Plural habitual contraction (-ರ್ತಾರ -> -ರುತ್ತಾರೆ)"
        },
        {
            "pattern": r"([ಕ-ಹ]+)ರ್ತಾನೆ(?=[^\u0C80-\u0CFF]|$)",
            "replacement": r"\1ರುತ್ತಾನೆ",
            "description": "3rd person masc habitual contraction (-ರ್ತಾನೆ -> -ರುತ್ತಾನೆ)"
        },
        {
            "pattern": r"([ಕ-ಹ]+)ರ್ತಾಳೆ(?=[^\u0C80-\u0CFF]|$)",
            "replacement": r"\1ರುತ್ತಾಳೆ",
            "description": "3rd person fem habitual contraction (-ರ್ತಾಳೆ -> -ರುತ್ತಾಳೆ)"
        },
        {
            "pattern": r"([ಕ-ಹ]+)ರ್ತೀವಿ(?=[^\u0C80-\u0CFF]|$)",
            "replacement": r"\1ರುತ್ತೇವೆ",
            "description": "1st person plural habitual contraction (-ರ್ತೀವಿ -> -ರುತ್ತೇವೆ)"
        },

        # --- 6. Spoken Past Tense Contractions ---
        {
            "pattern": r"([ಕ-ಹ]+)್ದೆ(?=[^\u0C80-\u0CFF]|$)",
            "replacement": r"\1ಿದೆ",
            "description": "Colloquial past 1st person (-್ದೆ -> -ಿದೆ, e.g. ಮಾಡ್ದೆ -> ಮಾಡಿದೆ, ಹೇಳ್ದೆ -> ಹೇಳಿದೆ)"
        },
        {
            "pattern": r"([ಕ-ಹ]+)್ದ(?=[^\u0C80-\u0CFF]|$)",
            "replacement": r"\1ಿದ",
            "description": "Colloquial past 3rd person (-್ದ -> -ಿದ, e.g. ಮಾಡ್ದ -> ಮಾಡಿದ, ಹೇಳ್ದ -> ಹೇಳಿದ)"
        },
        {
            "pattern": r"([ಕ-ಹ]+)್ದಿರಾ(?=[^\u0C80-\u0CFF]|$)",
            "replacement": r"\1ಿದಿರಾ",
            "description": "Colloquial past 2nd plural (-್ದಿರಾ -> -ಿದಿರಾ, e.g. ಮಾಡ್ದಿರಾ -> ಮಾಡಿದಿರಾ)"
        },
        {
            "pattern": r"([ಕ-ಹ]+)್ದ್ರಾ\?",
            "replacement": r"\1ಿದಿರಾ?",
            "description": "Colloquial past question (-್ದ್ರಾ? -> -ಿದಿರಾ?)"
        },

        # --- 7. Coastal & Havyaka Forms ---
        {
            "pattern": r"([ಕ-ಹ]+)ಗ್(?=[^\u0C80-\u0CFF]|$)",
            "replacement": r"\1ಗೆ",
            "description": "Coastal dative truncation (-ಗ್ -> -ಗೆ)"
        },
        {
            "pattern": r"([ಕ-ಹ]+)ಲ್(?=[^\u0C80-\u0CFF]|$)",
            "replacement": r"\1ನಲ್ಲಿ",
            "description": "Coastal locative truncation (-ಲ್ -> -ನಲ್ಲಿ)"
        },
        {
            "pattern": r"([ಕ-ಹ]+)ರ್ಪೆ(?=[^\u0C80-\u0CFF]|$)",
            "replacement": r"\1ರುತ್ತೇನೆ",
            "description": "Coastal future 1st person (-ರ್ಪೆ -> -ರುತ್ತೇನೆ, e.g. ಬರ್ಪೆ -> ಬರುತ್ತೇನೆ)"
        },
        {
            "pattern": r"([ಕ-ಹ]+)ಪೆ(?=[^\u0C80-\u0CFF]|$)",
            "replacement": r"\1ತ್ತೇನೆ",
            "description": "Coastal future 1st person (-ಪೆ -> -ತ್ತೇನೆ, e.g. ಪೋಪೆ -> ಹೋಗುತ್ತೇನೆ)"
        },
        {
            "pattern": r"([ಕ-ಹ]+)ಂಬೆ(?=[^\u0C80-\u0CFF]|$)",
            "replacement": r"\1ನ್ನುತ್ತೇನೆ",
            "description": "Coastal future 1st person (-ಂಬೆ -> -ನ್ನುತ್ತೇನೆ, e.g. ತಿಂಬೆ -> ತಿನ್ನುತ್ತೇನೆ)"
        },

        # --- 8. Question, Negation & Verbal Noun Tags ---
        {
            "pattern": r"([ಕ-ಹ]+)ತೇನ್ರಿ\?",
            "replacement": r"\1ಯಿತೇ?",
            "description": "North Karnataka polite question ending (-ತೇನ್ರಿ? -> -ಯಿತೇ?)"
        },
        {
            "pattern": r"([ಕ-ಹ]+)ಲ್ವಾ\?",
            "replacement": r"\1ಲಿಲ್ಲವೇ?",
            "description": "Tag question contraction (-ಲ್ವಾ? -> -ಲಿಲ್ಲವೇ?)"
        },
        {
            "pattern": r"([ಕ-ಹ]+)ಡೋದು(?=[^\u0C80-\u0CFF]|$)",
            "replacement": r"\1ಡುವುದು",
            "description": "Verbal noun contraction (-ಡೋದು -> -ಡುವುದು)"
        },
        {
            "pattern": r"([ಕ-ಹ]+)ಗೋದು(?=[^\u0C80-\u0CFF]|$)",
            "replacement": r"\1ಗುವುದು",
            "description": "Verbal noun contraction (-ಗೋದು -> -ಗುವುದು)"
        },
        {
            "pattern": r"([ಕ-ಹ]+)ರೋದು(?=[^\u0C80-\u0CFF]|$)",
            "replacement": r"\1ರುವುದು",
            "description": "Verbal noun contraction (-ರೋದು -> -ರುವುದು)"
        }
    ],
    # Distinctive keywords used for Region Detection
    "region_detection_keywords": {
        "North Karnataka": [
            "ಬರಾಕತ್ತಾನ", "ಮಾಡಾಕತ್ತಾಳ", "ಕುಂತ್ರೇನ್", "ನಿಂತ್ರೇನ್", "ಹಿಂಗ", "ಹಂಗ", "ಯಾಕ",
            "ಯಾಕ್ರಿ", "ಇವ್ವತ್", "ನಾಳಿಕಿ", "ಬೊವ್ವ", "ಚೊಲೋ", "ಖರೆ", "ಐತಿ", "ಐತ್ರಿ",
            "ಹೊಂಟಿ", "ಅಂದಿದ್ವಿ", "ನಾವ್ರ", "ನನಗ", "ನಿನಗ", "ಅಕಿ", "ಚೊಲೊ", "ಊರಾಗ", "ಬ್ಯಾಸರ",
            "ಮಾಡೀನಿ", "ಬಂದೀನಿ", "ಆತ್ರಿ", "ಹೌದ್ರಿ"
        ],
        "Kalyana Karnataka": [
            "ಮಾಡಲಿಕ್ಕತ್ತಾನ", "ಹೋಗಲಿಕ್ಕತ್ತಾನ", "ಬಂದ್ಯಾನ", "ಹೋಗ್ಯಾನ", "ಮಾಡ್ಯಾನ", "ಹೇಳ್ಯಾನ",
            "ರೊಕ್ಕ", "ಮನಿ", "ಸಾಲಿ", "ದೋಸ್ತ್", "ದೋಸ್ತ್ರ", "ಬಾಳಾ", "ಖೂಬ್", "ಜಲ್ದಿ",
            "ಬೆಪ್ಸಾ", "ತಕ್ಲಿಫ್", "ಗಮ್ಮತ್", "ದಂಡಿ", "ಬ್ಯಾರೆ", "ಗಿಂಡಿ", "ಹುಡುಗ್ಯಾ", "ಪರೇಶಾನ್"
        ],
        "Coastal / Kundagannada": [
            "ಮಾರೆ", "ಮಾರ್ರೆ", "ಎಂತ", "ಎಂತಕ್ಕ್", "ಪೋಯಿ", "ಬರ್ಪೆ", "ಪೋಪೆ", "ತಿಂಬೆ",
            "ಆತ್", "ಆತಾ", "ಕುಡ್ದ್ರಾ", "ಬಾರೀ", "ಚಾ", "ಶಾಲೆಗ್", "ಮನೆಲ್", "ಪೇಟೆಗ್",
            "ಸಿಗ್ಲಿಲ್ಲ", "ಗೊತ್ತಾತ್", "ತಿಂದ್ಯಾ", "ಹೋದ್ರೆ", "ತಡ್ಕೋ"
        ],
        "Uttara Kannada / Havyaka": [
            "ನಾಂ", "ನೀಂ", "ಅವಂ", "ಅವಳ್", "ಏಂ", "ಬತ್ತೆ", "ಬತ್ತಿ", "ಅಪ್ಪಚ್ಚಿ",
            "ಗೊತ್ತಾಪೋದಿಲ್ಲ", "ಹಾಳಾಪೋದು", "ಕಾಸಿಲ್ದೆ", "ತಕ್ಕೋ", "ಮಾಡ್ತಿದ್ದಿ", "ಹೆಂಗೆ",
            "ಕೂತ್ಕಂಡ್ರಾ", "ಎಲ್ಲೋರು", "ಹೋತ್ತೆ"
        ],
        "Mysuru-Mandya": [
            "ಕಣಯ್ಯ", "ಕಣ್ರೀ", "ಕಣೋ", "ಹಂಗ್ಯಾಕೆ", "ಹಿಂಗ್ಯಾಕೆ", "ಮಾಡ್ದೆ", "ಬಂದ್ರಿ",
            "ತಲೆ ತಿಂತಾವನೆ", "ಹೋಗ್ಬಿಟ್ಟವನೆ", "ಇಟ್ಬುಟ್ಟು", "ಮಾಡೋದು", "ಮಾಡೋಕಾಗುತ್ತೆ",
            "ಮಾಡೋಕಾಗಲ್ಲ", "ರೇಗಾಡಬೇಡ", "ಸುಮ್ನಿರು", "ನಾವೆಲ್ಲಾ"
        ]
    }
}

def main():
    target_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(target_dir, "data")
    os.makedirs(data_dir, exist_ok=True)

    lex_path = os.path.join(data_dir, "dialect_lexicons.json")
    with open(lex_path, "w", encoding="utf-8") as f:
        json.dump(LEXICONS, f, ensure_ascii=False, indent=2)
    print(f"Wrote dialect lexicons to {lex_path}")

    rules_path = os.path.join(data_dir, "regional_markers.json")
    with open(rules_path, "w", encoding="utf-8") as f:
        json.dump(REGIONAL_MARKERS, f, ensure_ascii=False, indent=2)
    print(f"Wrote regional markers & regex rules to {rules_path}")

if __name__ == "__main__":
    main()
