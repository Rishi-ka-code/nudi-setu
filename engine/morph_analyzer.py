# -*- coding: utf-8 -*-
"""
Morphological Analyzer & Transformer:
Universal rule engine for Kannada verb and noun morphology.
Handles open-ended inputs across Hubballi-Dharwad, Mangaluru, and Uttara Kannada dialects.
"""

import re
import json
import os
from typing import Tuple, List, Dict, Any


def wrap_kannada_word(w: str) -> str:
    """Kannada Unicode safe word-boundary pattern (avoids Python \\b failure on non-spacing vowel marks)."""
    return r'(?<![\u0C80-\u0D00])' + re.escape(w) + r'(?=[^\u0C80-\u0D00]|$)'


class MorphAnalyzer:
    def __init__(self, markers_path: str = None):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if markers_path is None:
            markers_path = os.path.join(base_dir, "data", "regional_markers.json")

        self.rules: List[Dict[str, str]] = []
        if os.path.exists(markers_path):
            with open(markers_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.rules = data.get("morphological_rules", [])

        # Irregular verb roots in Kannada
        self.special_stems = {
            'ಬರ': 'ಬರು', 'ಇರ': 'ಇರು', 'ತಿನ': 'ತಿನ್ನು', 'ತೋರ್ಸ': 'ತೋರಿಸು',
            'ಕುಡೀ': 'ಕುಡಿಯು', 'ಕಲೀ': 'ಕಲಿಯು', 'ಮಾಡ': 'ಮಾಡು', 'ಹೋಗ': 'ಹೋಗು',
            'ನೋಡ': 'ನೋಡು', 'ಹೇಳ': 'ಹೇಳು', 'ಕೇಳ': 'ಕೇಳು', 'ಕೊಡ': 'ಕೊಡು',
            'ಬಿಡ': 'ಬಿಡು', 'ಓಡ': 'ಓಡು', 'ನೆನೆ': 'ನೆನೆಯು', 'ತೊಗೋ': 'ತೆಗೆದುಕೊಳ್ಳು',
            'ತಗೋ': 'ತೆಗೆದುಕೊಳ್ಳು', 'ತೊಳೀ': 'ತೊಳೆಯು', 'ಕರೀ': 'ಕರಿಯು', 'ಹಾಲು ಕರೀ': 'ಹಾಲು ಕರೆಯು',
            'ಹೊಡೀ': 'ಹೊಡೆಯು', 'ಮುಗಿ': 'ಮುಗಿಯಲು', 'ಮಾತಾಡ': 'ಮಾತನಾಡು'
        }

    def resolve_stem(self, root: str) -> str:
        if root in self.special_stems:
            return self.special_stems[root]
        # If root ends in consonant (inherent short 'a'), add 'u' vowel sign (\u0CC1)
        if root and '\u0C95' <= root[-1] <= '\u0CB9':
            return root + '\u0CC1'
        return root

    def attach_present(self, stem: str, suffix_with_u: str) -> str:
        """
        Attaches a present/habitual suffix (e.g. 'ುತ್ತಾನೆ') cleanly without duplicate 'u' vowels.
        """
        if stem.endswith('\u0CC1') and suffix_with_u.startswith('ು'):
            return stem + suffix_with_u[1:]
        return stem + suffix_with_u

    def apply_rules(self, text: str, dialect: str = None) -> Tuple[str, List[Dict[str, str]]]:
        transformed = text
        applied_rules: List[Dict[str, str]] = []

        # ========================================================
        # 0. PHONETIC KEYBOARD METATHESIS & TYPO CORRECTIONS
        # ========================================================
        meta_rules = [
            (r'([\u0C80-\u0CFF]+)ತಾರ್ನಾ\?(?=[^\u0C80-\u0CFF]|$)', r'\1ರ್ತಾನಾ?'),
            (r'([\u0C80-\u0CFF]+)ತಾರ್ನ\?(?=[^\u0C80-\u0CFF]|$)', r'\1ರ್ತಾನ?'),
            (r'([\u0C80-\u0CFF]+)ತಾರ್ನಾ(?=[^\u0C80-\u0CFF]|$)', r'\1ರ್ತಾನಾ'),
            (r'([\u0C80-\u0CFF]+)ತಾರ್ನ[ೆ]?(?=[^\u0C80-\u0CFF]|$)', r'\1ರ್ತಾನ'),
            (r'([\u0C80-\u0CFF]+)ತಾರ್ಳ[ೆ]?(?=[^\u0C80-\u0CFF]|$)', r'\1ರ್ತಾಳ'),
            (r'([\u0C80-\u0CFF]+)ತಾರ್ತಾ[ೆ]?(?=[^\u0C80-\u0CFF]|$)', r'\1ರ್ತಾರ'),
            (r'([\u0C80-\u0CFF]+)ತಾರ್ನಿ(?=[^\u0C80-\u0CFF]|$)', r'\1ರ್ತೀನಿ'),
            (r'([\u0C80-\u0CFF]+)ತಾರ್ವಿ(?=[^\u0C80-\u0CFF]|$)', r'\1ರ್ತೀವಿ')
        ]
        for m_pat, m_rep in meta_rules:
            if re.search(m_pat, transformed):
                transformed = re.sub(m_pat, m_rep, transformed)

        # ========================================================
        # 1. CONTINUOUS ASPECTS (Must run BEFORE generic habitual endings!)
        # ========================================================
        # Hubballi-Dharwad -ಆಕತ್ತ-
        def repl_cont_m(m):
            root = m.group(1)
            stem = self.resolve_stem(root)
            return self.attach_present(stem, 'ುತ್ತಿದ್ದಾನೆ')
        if re.search(r'([\u0C80-\u0CFF]+?)ಾಕತ್ತಾನ(?=[^\u0C80-\u0CFF]|$)', transformed):
            transformed = re.sub(r'([\u0C80-\u0CFF]+?)ಾಕತ್ತಾನ(?=[^\u0C80-\u0CFF]|$)', repl_cont_m, transformed)
            applied_rules.append({"description": "ಉತ್ತರ ಕರ್ನಾಟಕ ಪ್ರವರ್ತಮಾನ ಪುಲ್ಲಿಂಗ ರೂಪ (-ಆಕತ್ತಾನ -> -ುತ್ತಿದ್ದಾನೆ)"})

        def repl_cont_f(m):
            root = m.group(1)
            stem = self.resolve_stem(root)
            return self.attach_present(stem, 'ುತ್ತಿದ್ದಾಳೆ')
        if re.search(r'([\u0C80-\u0CFF]+?)ಾಕತ್ತಾಳ(?=[^\u0C80-\u0CFF]|$)', transformed):
            transformed = re.sub(r'([\u0C80-\u0CFF]+?)ಾಕತ್ತಾಳ(?=[^\u0C80-\u0CFF]|$)', repl_cont_f, transformed)
            applied_rules.append({"description": "ಉತ್ತರ ಕರ್ನಾಟಕ ಪ್ರವರ್ತಮಾನ ಸ್ತ್ರೀಲಿಂಗ ರೂಪ (-ಆಕತ್ತಾಳ -> -ುತ್ತಿದ್ದಾಳೆ)"})

        def repl_cont_p(m):
            root = m.group(1)
            stem = self.resolve_stem(root)
            return self.attach_present(stem, 'ುತ್ತಿದ್ದಾರೆ')
        if re.search(r'([\u0C80-\u0CFF]+?)ಾಕತ್ತಾರ(?=[^\u0C80-\u0CFF]|$)', transformed):
            transformed = re.sub(r'([\u0C80-\u0CFF]+?)ಾಕತ್ತಾರ(?=[^\u0C80-\u0CFF]|$)', repl_cont_p, transformed)
            applied_rules.append({"description": "ಉತ್ತರ ಕರ್ನಾಟಕ ಪ್ರವರ್ತಮಾನ ಬಹುವಚನ ರೂಪ (-ಆಕತ್ತಾರ -> -ುತ್ತಿದ್ದಾರೆ)"})

        def repl_cont_1s(m):
            root = m.group(1)
            stem = self.resolve_stem(root)
            return self.attach_present(stem, 'ುತ್ತಿದ್ದೇನೆ')
        if re.search(r'([\u0C80-\u0CFF]+?)ಾಕತ್ತೀನಿ(?=[^\u0C80-\u0CFF]|$)', transformed):
            transformed = re.sub(r'([\u0C80-\u0CFF]+?)ಾಕತ್ತೀನಿ(?=[^\u0C80-\u0CFF]|$)', repl_cont_1s, transformed)
            applied_rules.append({"description": "ಉತ್ತರ ಕರ್ನಾಟಕ ಪ್ರವರ್ತಮಾನ ಪ್ರಥಮ ಪುರುಷ ರೂಪ (-ಾಕತ್ತೀನಿ -> -ುತ್ತಿದ್ದೇನೆ)"})

        def repl_cont_neu(m):
            root = m.group(1)
            stem = self.resolve_stem(root)
            return self.attach_present(stem, 'ುತ್ತಿದೆ')
        if re.search(r'([\u0C80-\u0CFF]+?)ಾಕತ್ತೈತಿ(?=[^\u0C80-\u0CFF]|$)', transformed):
            transformed = re.sub(r'([\u0C80-\u0CFF]+?)ಾಕತ್ತೈತಿ(?=[^\u0C80-\u0CFF]|$)', repl_cont_neu, transformed)
            applied_rules.append({"description": "ಉತ್ತರ ಕರ್ನಾಟಕ ನಪುಂಸಕಲಿಂಗ ಪ್ರವರ್ತಮಾನ (-ಾಕತ್ತೈತಿ -> -ುತ್ತಿದೆ)"})

        def repl_cont_2s(m):
            root = m.group(1)
            stem = self.resolve_stem(root)
            return self.attach_present(stem, 'ುತ್ತಿದ್ದೀಯಾ')
        if re.search(r'([\u0C80-\u0CFF]+?)ಾಕತ್ತಿ(?=[^\u0C80-\u0CFF]|$)', transformed):
            transformed = re.sub(r'([\u0C80-\u0CFF]+?)ಾಕತ್ತಿ(?=[^\u0C80-\u0CFF]|$)', repl_cont_2s, transformed)
            applied_rules.append({"description": "ಉತ್ತರ ಕರ್ನಾಟಕ ಪ್ರವರ್ತಮಾನ ಮಧ್ಯಮ ಪುರುಷ ರೂಪ (-ಾಕತ್ತಿ -> -ುತ್ತಿದ್ದೀಯಾ)"})

        # Kalyana Karnataka -ಲಿಕ್ಕತ್ತ-
        if re.search(r'([\u0C80-\u0CFF]+?)ಲಿಕ್ಕತ್ತಾನ(?=[^\u0C80-\u0CFF]|$)', transformed):
            transformed = re.sub(r'([\u0C80-\u0CFF]+?)ಲಿಕ್ಕತ್ತಾನ(?=[^\u0C80-\u0CFF]|$)', repl_cont_m, transformed)
            applied_rules.append({"description": "ಕಲ್ಯಾಣ ಕರ್ನಾಟಕ ಪ್ರವರ್ತಮಾನ ರೂಪ (-ಲಿಕ್ಕತ್ತಾನ -> -ುತ್ತಿದ್ದಾನೆ)"})

        if re.search(r'([\u0C80-\u0CFF]+?)ಲಿಕ್ಕತ್ತಾಳ(?=[^\u0C80-\u0CFF]|$)', transformed):
            transformed = re.sub(r'([\u0C80-\u0CFF]+?)ಲಿಕ್ಕತ್ತಾಳ(?=[^\u0C80-\u0CFF]|$)', repl_cont_f, transformed)
            applied_rules.append({"description": "ಕಲ್ಯಾಣ ಕರ್ನಾಟಕ ಪ್ರವರ್ತಮಾನ ಸ್ತ್ರೀಲಿಂಗ ರೂಪ (-ಲಿಕ್ಕತ್ತಾಳ -> -ುತ್ತಿದ್ದಾಳೆ)"})

        if re.search(r'([\u0C80-\u0CFF]+?)ಲಿಕ್ಕತ್ತಾರ(?=[^\u0C80-\u0CFF]|$)', transformed):
            transformed = re.sub(r'([\u0C80-\u0CFF]+?)ಲಿಕ್ಕತ್ತಾರ(?=[^\u0C80-\u0CFF]|$)', repl_cont_p, transformed)
            applied_rules.append({"description": "ಕಲ್ಯಾಣ ಕರ್ನಾಟಕ ಪ್ರವರ್ತಮಾನ ಬಹುವಚನ ರೂಪ (-ಲಿಕ್ಕತ್ತಾರ -> -ುತ್ತಿದ್ದಾರೆ)"})

        # Auxiliary continuous:
        aux_cont_patterns = [
            (r'([\u0C80-\u0CFF]+?)್ತಾ\s+ಇದ್ದೀರಿ(?=[^\u0C80-\u0CFF]|$)', 'ುತ್ತಿದ್ದೀರಿ', 'ಮಂಗಳೂರು/ಕರಾವಳಿ ಗೌರವಾರ್ಥಕ ಪ್ರವರ್ತಮಾನ (-್ತಾ ಇದ್ದೀರಿ -> -ುತ್ತಿದ್ದೀರಿ)'),
            (r'([\u0C80-\u0CFF]+?)್ತಾ\s+ಇದ್ದಾರೆ(?=[^\u0C80-\u0CFF]|$)', 'ುತ್ತಿದ್ದಾರೆ', 'ಪ್ರವರ್ತಮಾನ ಬಹುವಚನ (-್ತಾ ಇದ್ದಾರೆ -> -ುತ್ತಿದ್ದಾರೆ)'),
            (r'([\u0C80-\u0CFF]+?)್ತಾ\s+ಇದ್ದೀವಿ(?=[^\u0C80-\u0CFF]|$)', 'ುತ್ತಿದ್ದೇವೆ', 'ಪ್ರವರ್ತಮಾನ ಉತ್ತಮ ಪುರುಷ ಬಹುವಚನ (-್ತಾ ಇದ್ದೀವಿ -> -ುತ್ತಿದ್ದೇವೆ)'),
            (r'([\u0C80-\u0CFF]+?)್ತಾ\s+ಇದ್ದಾನೆ(?=[^\u0C80-\u0CFF]|$)', 'ುತ್ತಿದ್ದಾನೆ', 'ಪ್ರವರ್ತಮಾನ ಪುಲ್ಲಿಂಗ (-್ತಾ ಇದ್ದಾನೆ -> -ುತ್ತಿದ್ದಾನೆ)'),
            (r'([\u0C80-\u0CFF]+?)್ತಾ\s+ಇದ್ದಾಳೆ(?=[^\u0C80-\u0CFF]|$)', 'ುತ್ತಿದ್ದಾಳೆ', 'ಪ್ರವರ್ತಮಾನ ಸ್ತ್ರೀಲಿಂಗ (-್ತಾ ಇದ್ದಾಳೆ -> -ುತ್ತಿದ್ದಾಳೆ)'),
            (r'([\u0C80-\u0CFF]+?)್ತಾ\s+ಇದೆ(?=[^\u0C80-\u0CFF]|$)', 'ುತ್ತಿದೆ', 'ಪ್ರವರ್ತಮಾನ ನಪುಂಸಕಲಿಂಗ (-್ತಾ ಇದೆ -> -ುತ್ತಿದೆ)'),
            (r'([\u0C80-\u0CFF]+?)್ತಾ\s+ಉಂಡು(?=[^\u0C80-\u0CFF]|$)', 'ುತ್ತಿದೆ', 'ಕರಾವಳಿ ಪ್ರವರ್ತಮಾನ ನಪುಂಸಕಲಿಂಗ (-್ತಾ ಉಂಡು -> -ುತ್ತಿದೆ)'),
            (r'([\u0C80-\u0CFF]+?)ೀತ\s+ಇದ್ದಾಳೆ(?=[^\u0C80-\u0CFF]|$)', 'ೆಯುತ್ತಿದ್ದಾಳೆ', 'ಪ್ರವರ್ತಮಾನ ಸ್ವರೂಪ ರೂಪಾಂತರ'),
            (r'([\u0C80-\u0CFF]+?)ೀತಾ\s+ಇದ್ದಾರೆ(?=[^\u0C80-\u0CFF]|$)', 'ೆಯುತ್ತಿದ್ದಾರೆ', 'ಪ್ರವರ್ತಮಾನ ಬಹುವಚನ ರೂಪಾಂತರ')
        ]
        for pat, suff, desc in aux_cont_patterns:
            if re.search(pat, transformed):
                def repl_aux(m, s=suff):
                    stem = self.resolve_stem(m.group(1))
                    if s.startswith('ೆಯ'):
                        if stem.endswith('ು'): stem = stem[:-1]
                        return stem + s
                    return self.attach_present(stem, s)
                transformed = re.sub(pat, repl_aux, transformed)
                applied_rules.append({"description": desc})

        # ========================================================
        # 2. DIALECT SPECIFIC VERBAL RULES
        # ========================================================
        # Coastal verbs:
        coastal_verbs = {
            'ಬರ್ಪೆ': 'ಬರುತ್ತೇನೆ', 'ಪೋಪೆ': 'ಹೋಗುತ್ತೇನೆ', 'ಕೊಡ್ಪೆ': 'ಕೊಡುತ್ತೇನೆ',
            'ತಿಂಬೆ': 'ತಿನ್ನುತ್ತೇನೆ', 'ತರ್ಪೆ': 'ತರುತ್ತೇನೆ', 'ಬರ್ಪ': 'ಬರುತ್ತಾನೆ',
            'ಪೋಪ': 'ಹೋಗುತ್ತಾನೆ', 'ಬರ್ಪೊ': 'ಬರುತ್ತೇವೆ', 'ಪೋಪೊ': 'ಹೋಗುತ್ತೇವೆ',
            'ಪೋಯಿ': 'ಹೋಗಿ', 'ಬರೋಡು': 'ಬನ್ನಿ', 'ಗೊತ್ತಿಲ್ಲಿ': 'ಗೊತ್ತಿಲ್ಲ',
            'ಕುಡ್ಕೊಂಡು': 'ಕುಡಿದುಕೊಂಡು', 'ಮಾತಾಡುವ': 'ಮಾತನಾಡೋಣ',
            'ನಿಕ್ಲು': 'ನೀವೂ', 'ಪುರಾ': 'ಎಲ್ಲರೂ'
        }
        for cv, cstd in coastal_verbs.items():
            if re.search(wrap_kannada_word(cv), transformed):
                transformed = re.sub(wrap_kannada_word(cv), cstd, transformed)
                applied_rules.append({"description": f"ಕರಾವಳಿ/ಕುಂದಗನ್ನಡ ಕ್ರಿಯಾಪದ ಶಿಷ್ಟೀಕರಣ ({cv} -> {cstd})"})

        # Coastal negative tag: ಹೇಳಿಲ್ವಾ? -> ಹೇಳಲಿಲ್ಲವೇ? / ಕೇಳಿಲ್ವಾ? -> ಕೇಳಿಸಿಕೊಳ್ಳಲಿಲ್ಲವೇ?
        if re.search(r'([\u0C80-\u0CFF]+)ಿಲ್ವಾ(?:\?)?(?=[^\u0C80-\u0CFF]|$)', transformed):
            transformed = re.sub(r'([\u0C80-\u0CFF]+)ಿಲ್ವಾ(?:\?)?(?=[^\u0C80-\u0CFF]|$)', r'\1ಲಿಲ್ಲವೇ?', transformed)
            applied_rules.append({"description": "ಕರಾವಳಿ ನಕಾರಾತ್ಮಕ ಪ್ರಶ್ನಾರ್ಥಕ ಪ್ರತ್ಯಯ (-ಿಲ್ವಾ -> -ಲಿಲ್ಲವೇ?)"})

        if re.search(r'([\u0C80-\u0CFF]+)ಲಿಲ್ವೇನು(\?)?(?=[^\u0C80-\u0CFF]|$)', transformed):
            transformed = re.sub(r'([\u0C80-\u0CFF]+)ಲಿಲ್ವೇನು(\?)?(?=[^\u0C80-\u0CFF]|$)', r'\1ಲಿಲ್ಲವೇನು\2', transformed)
            applied_rules.append({"description": "ನಕಾರಾತ್ಮಕ ಪ್ರಶ್ನಾರ್ಥಕ ಪ್ರತ್ಯಯ (-ಲಿಲ್ವೇನು -> -ಲಿಲ್ಲವೇನು)"})

        # Coastal & Malenadu past syncopations:
        past_syncopations = [
            ('ಹೇಳ್ದೆ', 'ಹೇಳಿದೆ', 'ಭೂತಕಾಲ ಪ್ರಥಮ ಪುರುಷ ಏಕವಚನ (ಹೇಳ್ದೆ -> ಹೇಳಿದೆ)'),
            ('ಕೇಳ್ದೆ', 'ಕೇಳಿದೆ', 'ಭೂತಕಾಲ ಪ್ರಥಮ ಪುರುಷ ಏಕವಚನ (ಕೇಳ್ದೆ -> ಕೇಳಿದೆ)'),
            ('ಹೇಳ್ದ', 'ಹೇಳಿದನು', 'ಭೂತಕಾಲ ತೃತೀಯ ಪುರುಷ ಪುಲ್ಲಿಂಗ (ಹೇಳ್ದ -> ಹೇಳಿದನು)'),
            ('ಹೇಳ್ದ್ರು', 'ಹೇಳಿದರು', 'ಭೂತಕಾಲ ಗೌರವಾರ್ಥಕ ಬಹುವಚನ (ಹೇಳ್ದ್ರು -> ಹೇಳಿದರು)'),
            ('ಹೇಳಿದ್ರು', 'ಹೇಳಿದರು', 'ಭೂತಕಾಲ ಗೌರವಾರ್ಥಕ ಬಹುವಚನ (ಹೇಳಿದ್ರು -> ಹೇಳಿದರು)'),
            ('ಬಂದ್ರು', 'ಬಂದರು', 'ಭೂತಕಾಲ ಗೌರವಾರ್ಥಕ ಬಹುವಚನ (ಬಂದ್ರು -> ಬಂದರು)'),
            ('ಹೋದ್ವಿ', 'ಹೋದೆವು', 'ಕರಾವಳಿ ಭೂತಕಾಲ ಉತ್ತಮ ಪುರುಷ ಬಹುವಚನ (-ದ್ವಿ -> -ದೆವು)'),
            ('ಮಾತಾಡಿದ್ವಿ', 'ಮಾತನಾಡಿದೆವು', 'ಭೂತಕಾಲ ಉತ್ತಮ ಪುರುಷ ಬಹುವಚನ (ಮಾತಾಡಿದ್ವಿ -> ಮಾತನಾಡಿದೆವು)'),
            ('ಕುತ್ಕೊಳಿ', 'ಕುಳಿತುಕೊಳ್ಳಿ', 'ಆಜ್ಞಾರ್ಥಕ ಕ್ರಿಯಾರೂಪ (ಕುತ್ಕೊಳಿ -> ಕುಳಿತುಕೊಳ್ಳಿ)'),
            ('ಕುತ್ಕೊಳ್ಳಿ', 'ಕುಳಿತುಕೊಳ್ಳಿ', 'ಆಜ್ಞಾರ್ಥಕ ಕ್ರಿಯಾರೂಪ (ಕುತ್ಕೊಳ್ಳಿ -> ಕುಳಿತುಕೊಳ್ಳಿ)'),
            ('ತಿಂಡ್ರಿ', 'ತಿಂದಿರಿ', 'ಭೂತಕಾಲ ಮಧ್ಯಮ ಪುರುಷ (ತಿಂಡ್ರಿ -> ತಿಂದಿರಿ)'),
            ('ಕುಡ್ದ್ರಾ', 'ಕುಡಿದಿರಾ', 'ಭೂತಕಾಲ ಮಧ್ಯಮ ಪುರುಷ ಪ್ರಶ್ನಾರ್ಥಕ (ಕುಡ್ದ್ರಾ -> ಕುಡಿದಿರಾ)'),
            ('ತಿಂದ್ಯಾ', 'ತಿಂದೆಯಾ', 'ಭೂತಕಾಲ ಮಧ್ಯಮ ಪುರುಷ ಪ್ರಶ್ನಾರ್ಥಕ (ತಿಂದ್ಯಾ -> ತಿಂದೆಯಾ)'),
            ('ಮಾಡ್ದೆ', 'ಮಾಡಿದೆ', 'ಭೂತಕಾಲ ಪ್ರಥಮ ಪುರುಷ (ಮಾಡ್ದೆ -> ಮಾಡಿದೆ)'),
            ('ಮಾಡತೀ', 'ಮಾಡುತ್ತಿದ್ದೀಯಾ', 'ಮಧ್ಯಮ ಪುರುಷ ಕ್ರಿಯಾರೂಪ (ಮಾಡತೀ -> ಮಾಡುತ್ತಿದ್ದೀಯಾ)'),
            ('ಮಾಡತಿ', 'ಮಾಡುತ್ತಿದ್ದೀಯಾ', 'ಮಧ್ಯಮ ಪುರುಷ ಕ್ರಿಯಾರೂಪ (ಮಾಡತಿ -> ಮಾಡುತ್ತಿದ್ದೀಯಾ)'),
            ('ಹೋಗಿದ್ವಿ', 'ಹೋಗಿದ್ದೆವು', 'ಭೂತಕಾಲ ಉತ್ತಮ ಪುರುಷ ಬಹುವಚನ (ಹೋಗಿದ್ವಿ -> ಹೋಗಿದ್ದೆವು)'),
            ('ಬಂದಿದ್ವಿ', 'ಬಂದಿದ್ದೆವು', 'ಭೂತಕಾಲ ಉತ್ತಮ ಪುರುಷ ಬಹುವಚನ (ಬಂದಿದ್ವಿ -> ಬಂದಿದ್ದೆವು)')
        ]
        for cp_p, cp_r, c_desc in past_syncopations:
            if re.search(wrap_kannada_word(cp_p), transformed):
                transformed = re.sub(wrap_kannada_word(cp_p), cp_r, transformed)
                applied_rules.append({"description": c_desc})

        # General syncopated -ದ್ವಿ -> -ದೆವು (from glossary.csv line 52)
        if re.search(r'([\u0C80-\u0CFF]+)ದ್ವಿ(?=[^\u0C80-\u0CFF]|$)', transformed):
            def repl_dvi(m):
                root = m.group(1)
                return root + 'ಿದೆವು' if root[-1] not in ['ಾ', 'ೋ', 'ೇ'] else root + 'ದೆವು'
            transformed = re.sub(r'([\u0C80-\u0CFF]+)ದ್ವಿ(?=[^\u0C80-\u0CFF]|$)', repl_dvi, transformed)
            applied_rules.append({"description": "ಕರಾವಳಿ ಭೂತಕಾಲ ಉತ್ತಮ ಪುರುಷ ಬಹುವಚನ (-ದ್ವಿ -> -ದೆವು)"})

        # Syncopated -ದ್ಲು -> -ದಳು (3rd fem past)
        if re.search(r'([\u0C80-\u0CFF]+)ದ್ಲು(?=[^\u0C80-\u0CFF]|$)', transformed):
            transformed = re.sub(r'([\u0C80-\u0CFF]+)ದ್ಲು(?=[^\u0C80-\u0CFF]|$)', r'\1ಿದಳು', transformed)
            applied_rules.append({"description": "ಭೂತಕಾಲ ಸ್ತ್ರೀಲಿಂಗ ಸಂಕ್ಷಿಪ್ತ ರೂಪ (-ದ್ಲು -> -ಿದಳು)"})

        # Uttara Kannada verbs:
        uk_verbs = [
            ('ಬತ್ತೆ', 'ಬರುತ್ತೇನೆ', 'ಉತ್ತರ ಕನ್ನಡ/ಹವ್ಯಕ ಪ್ರಥಮ ಪುರುಷ ಕ್ರಿಯಾರೂಪ (ಬತ್ತೆ -> ಬರುತ್ತೇನೆ)'),
            ('ಹೋಗಿ ಬತ್ತೆ', 'ಹೋಗಿ ಬರುತ್ತೇನೆ', 'ಉತ್ತರ ಕನ್ನಡ ವಿನಯಪೂರ್ವಕ ನಿರ್ಗಮನ (ಹೋಗಿ ಬತ್ತೆ -> ಹೋಗಿ ಬರುತ್ತೇನೆ)'),
            ('ಕೇಳ್ತು', 'ಕೇಳಿಸಿತು', 'ಉತ್ತರ ಕನ್ನಡ ನಪುಂಸಕಲಿಂಗ ಭೂತಕಾಲ (ಕೇಳ್ತು -> ಕೇಳಿಸಿತು)'),
            ('ಗೇದು', 'ಮಾಡಿದೆ', 'ಹವ್ಯಕ ಗೇದು ಕ್ರಿಯಾಪದ (ಗೇದು -> ಮಾಡಿದೆ)'),
            ('ಸಿಕ್ತು', 'ಸಿಕ್ಕಿತು', 'ಭೂತಕಾಲ ನಪುಂಸಕಲಿಂಗ (ಸಿಕ್ತು -> ಸಿಕ್ಕಿತು)'),
            ('ತಗೊಂಡೆ', 'ತೆಗೆದುಕೊಂಡೆ', 'ಕ್ರಿಯಾಪದ ಶಿಷ್ಟೀಕರಣ (ತಗೊಂಡೆ -> ತೆಗೆದುಕೊಂಡೆ)'),
            ('ತಗೋಂಡೆ', 'ತೆಗೆದುಕೊಂಡೆ', 'ಕ್ರಿಯಾಪದ ಶಿಷ್ಟೀಕರಣ (ತಗೋಂಡೆ -> ತೆಗೆದುಕೊಂಡೆ)'),
            ('ಇಟ್ಕೋ', 'ಇಟ್ಟುಕೋ', 'ಆಜ್ಞಾರ್ಥಕ ರೂಪ (ಇಟ್ಕೋ -> ಇಟ್ಟುಕೋ)'),
            ('ಉಣ್ಣೋದು', 'ಮಾಡುವುದು', 'ಭಾವನಾಮ ಕ್ರಿಯಾರೂಪ (ಉಣ್ಣೋದು -> ಮಾಡುವುದು)'),
            ('ತಿಂಬೋದು', 'ತಿನ್ನುವುದು', 'ಭಾವನಾಮ ಕ್ರಿಯಾರೂಪ (ತಿಂಬೋದು -> ತಿನ್ನುವುದು)'),
            ('ಹೇಳೋದು', 'ಹೇಳುವುದು', 'ಭಾವನಾಮ ಕ್ರಿಯಾರೂಪ (ಹೇಳೋದು -> ಹೇಳುವುದು)'),
            ('ತಿಂಬಲಕ್ಕು', 'ತಿನ್ನಲು ಬೇಕು', 'ಹವ್ಯಕ ವಿಧ್ಯರ್ಥಕ ಕ್ರಿಯಾರೂಪ (ತಿಂಬಲಕ್ಕು -> ತಿನ್ನಲು ಬೇಕು)'),
            ('ಕುಡಿಯುವಾ', 'ಕುಡಿಯೋಣ', 'ಉತ್ತರ ಕನ್ನಡ ಪ್ರೇರಣಾರ್ಥಕ ರೂಪ (ಕುಡಿಯುವಾ -> ಕುಡಿಯೋಣ)'),
            ('ಹೋಗುವಾ', 'ಹೋಗೋಣ', 'ಪ್ರೇರಣಾರ್ಥಕ ರೂಪ (ಹೋಗುವಾ -> ಹೋಗೋಣ)'),
            ('ಬರುವಾ', 'ಬರೋಣ', 'ಪ್ರೇರಣಾರ್ಥಕ ರೂಪ (ಬರುವಾ -> ಬರೋಣ)'),
            ('ಮಾಡುವಾ', 'ಮಾಡೋಣ', 'ಪ್ರೇರಣಾರ್ಥಕ ರೂಪ (ಮಾಡುವಾ -> ಮಾಡೋಣ)')
        ]
        for uv, ustd, u_desc in uk_verbs:
            if re.search(wrap_kannada_word(uv), transformed):
                transformed = re.sub(wrap_kannada_word(uv), ustd, transformed)
                applied_rules.append({"description": u_desc})

        # UK -ತಕ್ಕು -> -ಬೇಕು (ಮಾಡತಕ್ಕು -> ಮಾಡಬೇಕು, ಹೋಗತಕ್ಕು -> ಹೋಗಬೇಕು)
        if re.search(r'([\u0C80-\u0CFF]+)ತಕ್ಕು(?=[^\u0C80-\u0CFF]|$)', transformed):
            def repl_takku(m):
                root = m.group(1)
                stem = self.resolve_stem(root)
                if stem.endswith('ು'):
                    stem = stem[:-1]
                return stem + 'ಬೇಕು'
            transformed = re.sub(r'([\u0C80-\u0CFF]+)ತಕ್ಕು(?=[^\u0C80-\u0CFF]|$)', repl_takku, transformed)
            applied_rules.append({"description": "ಹವ್ಯಕ/ಉತ್ತರ ಕನ್ನಡ ವಿಧ್ಯರ್ಥಕ ಪ್ರತ್ಯಯ (-ತಕ್ಕು -> -ಬೇಕು)"})

        # UK neuter continuous/habitual -ವುತ್ತೆ -> -ತ್ತದೆ (ಸುರಿವುತ್ತೆ -> ಸುರಿಯುತ್ತದೆ, ಬರುವುತ್ತೆ -> ಬರುತ್ತದೆ)
        uk_neut_pats = [
            (r'([\u0C80-\u0CFF]+)ಿವುತ್ತೆ(?=[^\u0C80-\u0CFF]|$)', r'\1ಿಯುತ್ತದೆ'),
            (r'([\u0C80-\u0CFF]+)್ವುತ್ತೆ(?=[^\u0C80-\u0CFF]|$)', r'\1ುತ್ತದೆ'),
            (r'([\u0C80-\u0CFF]+)ುವುತ್ತೆ(?=[^\u0C80-\u0CFF]|$)', r'\1ುತ್ತದೆ'),
            (r'([\u0C80-\u0CFF]+)ಿಯುತ್ತೆ(?=[^\u0C80-\u0CFF]|$)', r'\1ಿಯುತ್ತದೆ'),
            (r'([\u0C80-\u0CFF]+)ುತ್ತೆ(?=[^\u0C80-\u0CFF]|$)', r'\1ುತ್ತದೆ')
        ]
        for n_pat, n_rep in uk_neut_pats:
            if re.search(n_pat, transformed):
                transformed = re.sub(n_pat, n_rep, transformed)
                applied_rules.append({"description": "ಉತ್ತರ ಕನ್ನಡ ನಪುಂಸಕಲಿಂಗ ವರ್ತಮಾನ ರೂಪ (-ವುತ್ತೆ/-ುತ್ತೆ -> -ತ್ತದೆ)"})
                break

        # UK past experiential -ಿದೀನಿ -> -ಿದ್ದೇನೆ (ತಂದಿದೀನಿ -> ತಂದಿದ್ದೇನೆ, ಮಾಡಿದೀನಿ -> ಮಾಡಿದ್ದೇನೆ)
        if re.search(r'([\u0C80-\u0CFF]+)ಿದೀನಿ(?=[^\u0C80-\u0CFF]|$)', transformed):
            transformed = re.sub(r'([\u0C80-\u0CFF]+)ಿದೀನಿ(?=[^\u0C80-\u0CFF]|$)', r'\1ಿದ್ದೇನೆ', transformed)
            applied_rules.append({"description": "ಭೂತಕಾಲ ಅನುಭವಾತ್ಮಕ ಪ್ರಥಮ ಪುರುಷ (-ಿದೀನಿ -> -ಿದ್ದೇನೆ)"})

        # Interrogative completion: ಆತಾ? / ಆತಾ -> ಆಯಿತೇ?
        if re.search(wrap_kannada_word('ಆತಾ?'), transformed):
            transformed = re.sub(wrap_kannada_word('ಆತಾ?'), 'ಆಯಿತೇ?', transformed)
            applied_rules.append({"description": "ಪ್ರಶ್ನಾರ್ಥಕ ಸಮಾಪ್ತಿ ರೂಪ (ಆತಾ? -> ಆಯಿತೇ?)"})
        elif re.search(wrap_kannada_word('ಆತಾ'), transformed):
            transformed = re.sub(wrap_kannada_word('ಆತಾ'), 'ಆಯಿತೇ', transformed)
            applied_rules.append({"description": "ಸಮಾಪ್ತಿ ರೂಪ (ಆತಾ -> ಆಯಿತೇ)"})

        # ========================================================
        # 3. GENERIC HABITUAL VERBS
        # ========================================================
        # Interrogative 3rd masc (-್ತಾನಾ? / -್ತಾನ?)
        p1 = r'([\u0C80-\u0CFF]+)್ತಾನಾ\?(?=[^\u0C80-\u0CFF]|$)|([\u0C80-\u0CFF]+)್ತಾನ\?(?=[^\u0C80-\u0CFF]|$)'
        if re.search(p1, transformed):
            def p1_sub(m):
                root = m.group(1) or m.group(2)
                stem = self.resolve_stem(root)
                return self.attach_present(stem, 'ುತ್ತಾನೆಯೇ?')
            transformed = re.sub(p1, p1_sub, transformed)
            applied_rules.append({"description": "ಪ್ರಶ್ನಾರ್ಥಕ ಕ್ರಿಯಾಪದ ಪ್ರತ್ಯಯ ಸಾರ್ವತ್ರಿಕ ಶಿಷ್ಟೀಕರಣ (-್ತಾನಾ? -> -ುತ್ತಾನೆಯೇ?)"})

        p1_l = r'([\u0C80-\u0CFF]+)್ತಾನಾ(?=[^\u0C80-\u0CFF]|$)'
        if re.search(p1_l, transformed):
            transformed = re.sub(p1_l, lambda m: self.attach_present(self.resolve_stem(m.group(1)), 'ುತ್ತಾನೆಯೇ'), transformed)
            applied_rules.append({"description": "ಪ್ರಶ್ನಾರ್ಥಕ ಕ್ರಿಯಾಪದ ಪ್ರತ್ಯಯ ಶಿಷ್ಟೀಕರಣ (-್ತಾನಾ -> -ುತ್ತಾನೆಯೇ)"})

        # Declarative 3rd masc (-್ತಾನ / -್ತಾನೆ -> -ುತ್ತಾನೆ)
        p2 = r"([\u0C80-\u0CFF]+?)(?<!\u0CA4)್ತಾನ[ೆ]?(?=[^\u0C80-\u0CFF]|$)"
        if re.search(p2, transformed):
            def repl_hm_dec(m):
                stem = self.resolve_stem(m.group(1))
                return self.attach_present(stem, "ುತ್ತಾನೆ")
            transformed = re.sub(p2, repl_hm_dec, transformed)
            applied_rules.append({"description": "ತೃತೀಯ ಪುರುಷ ಪುಲ್ಲಿಂಗ ವರ್ತಮಾನ ಕ್ರಿಯಾರೂಪ (-್ತಾನ -> -ುತ್ತಾನೆ)"})

        # Declarative 3rd fem (-್ತಾಳ / -್ತಾಳೆ -> -ುತ್ತಾಳೆ)
        p3_int = r'([\u0C80-\u0CFF]+?)(?<!\u0CA4)್ತಾಳ[ಾ]?\?(?=[^\u0C80-\u0CFF]|$)'
        if re.search(p3_int, transformed):
            transformed = re.sub(p3_int, lambda m: self.attach_present(self.resolve_stem(m.group(1)), 'ುತ್ತಾಳೆಯೇ?'), transformed)
            applied_rules.append({"description": "ಸ್ತ್ರೀಲಿಂಗ ಪ್ರಶ್ನಾರ್ಥಕ ಕ್ರಿಯಾರೂಪ (-್ತಾಳಾ? -> -ುತ್ತಾಳೆಯೇ?)"})
        p3_dec = r'([\u0C80-\u0CFF]+?)(?<!\u0CA4)್ತಾಳ[ೆ]?(?=[^\u0C80-\u0CFF]|$)'
        if re.search(p3_dec, transformed):
            transformed = re.sub(p3_dec, lambda m: self.attach_present(self.resolve_stem(m.group(1)), 'ುತ್ತಾಳೆ'), transformed)
            applied_rules.append({"description": "ಸ್ತ್ರೀಲಿಂಗ ವರ್ತಮಾನ ಕ್ರಿಯಾರೂಪ (-್ತಾಳ -> -ುತ್ತಾಳೆ)"})

        # Declarative 3rd plural (-್ತಾರ / -್ತಾರೆ -> -ುತ್ತಾರೆ)
        p4_int = r'([\u0C80-\u0CFF]+?)(?<!\u0CA4)್ತಾರ[ಾ]?\?(?=[^\u0C80-\u0CFF]|$)'
        if re.search(p4_int, transformed):
            transformed = re.sub(p4_int, lambda m: self.attach_present(self.resolve_stem(m.group(1)), 'ುತ್ತಾರೆಯೇ?'), transformed)
            applied_rules.append({"description": "ಬಹುವಚನ ಪ್ರಶ್ನಾರ್ಥಕ ಕ್ರಿಯಾರೂಪ (-್ತಾರಾ? -> -ುತ್ತಾರೆಯೇ?)"})
        p4_dec = r'([\u0C80-\u0CFF]+?)(?<!\u0CA4)್ತಾರ[ೆ]?(?=[^\u0C80-\u0CFF]|$)'
        if re.search(p4_dec, transformed):
            transformed = re.sub(p4_dec, lambda m: self.attach_present(self.resolve_stem(m.group(1)), 'ುತ್ತಾರೆ'), transformed)
            applied_rules.append({"description": "ಬಹುವಚನ ವರ್ತಮಾನ ಕ್ರಿಯಾರೂಪ (-್ತಾರ -> -ುತ್ತಾರೆ)"})

        # Habitual 1st Sing (-್ತೀನಿ -> -ುತ್ತೇನೆ) & Plural (-್ತೀವಿ -> -ುತ್ತೇವೆ)
        p5_1s = r'([\u0C80-\u0CFF]+?)(?<!\u0CA4)್ತೀನಿ(?=[^\u0C80-\u0CFF]|$)'
        if re.search(p5_1s, transformed):
            transformed = re.sub(p5_1s, lambda m: self.attach_present(self.resolve_stem(m.group(1)), 'ುತ್ತೇನೆ'), transformed)
            applied_rules.append({"description": "ಪ್ರಥಮ ಪುರುಷ ಏಕವಚನ ಕ್ರಿಯಾರೂಪ (-್ತೀನಿ -> -ುತ್ತೇನೆ)"})

        p5_1p = r'([\u0C80-\u0CFF]+?)(?<!\u0CA4)್ತೀವಿ(?=[^\u0C80-\u0CFF]|$)'
        if re.search(p5_1p, transformed):
            transformed = re.sub(p5_1p, lambda m: self.attach_present(self.resolve_stem(m.group(1)), 'ುತ್ತೇವೆ'), transformed)
            applied_rules.append({"description": "ಪ್ರಥಮ ಪುರುಷ ಬಹುವಚನ ಕ್ರಿಯಾರೂಪ (-್ತೀವಿ -> -ುತ್ತೇವೆ)"})

        # Habitual 2nd Sing (-್ತೀಯಾ -> -ುತ್ತೀಯಾ) & Plural (-್ತೀರಿ -> -ುತ್ತೀರಿ)
        p6_2s = r'([\u0C80-\u0CFF]+?)(?<!\u0CA4)(?:್ತೀಯ|್ತಿಯ|ತಿಯ)[ಾ]?(?=\?|[^\u0C80-\u0CFF]|$)'
        if re.search(p6_2s, transformed):
            transformed = re.sub(p6_2s, lambda m: self.attach_present(self.resolve_stem(m.group(1)), 'ುತ್ತೀಯಾ'), transformed)
            applied_rules.append({"description": "ಮಧ್ಯಮ ಪುರುಷ ಕ್ರಿಯಾರೂಪ (-್ತೀಯಾ / -ತಿಯಾ -> -ುತ್ತೀಯಾ)"})

        p6_2p = r'([\u0C80-\u0CFF]+?)(?<!\u0CA4)್ತೀರಿ(?=[^\u0C80-\u0CFF]|$)'
        if re.search(p6_2p, transformed):
            transformed = re.sub(p6_2p, lambda m: self.attach_present(self.resolve_stem(m.group(1)), 'ುತ್ತೀರಿ'), transformed)
            applied_rules.append({"description": "ಮಧ್ಯಮ ಪುರುಷ ಗೌರವಾರ್ಥಕ ಕ್ರಿಯಾರೂಪ (-್ತೀರಿ -> -ುತ್ತೀರಿ)"})

        # Polite 2nd interrogative: ಬರ್ತೀರಾ? -> ಬರುತ್ತೀರಾ?, ಮಾಡ್ತೀರಾ? -> ಮಾಡುತ್ತೀರಾ?
        p6_2pq = r'([\u0C80-\u0CFF]+?)(?<!\u0CA4)್ತೀರಾ\?(?=[^\u0C80-\u0CFF]|$)'
        if re.search(p6_2pq, transformed):
            transformed = re.sub(p6_2pq, lambda m: self.attach_present(self.resolve_stem(m.group(1)), 'ುತ್ತೀರಾ?'), transformed)
            applied_rules.append({"description": "ಮಧ್ಯಮ ಪುರುಷ ಗೌರವಾರ್ಥಕ ಪ್ರಶ್ನಾರ್ಥಕ ಕ್ರಿಯಾರೂಪ (-್ತೀರಾ? -> -ುತ್ತೀರಾ?)"})

        # ========================================================
        # 4. CLITICS & IMPERATIVES
        # ========================================================
        if re.search(wrap_kannada_word('ಏನ್ರಿ'), transformed):
            transformed = re.sub(wrap_kannada_word('ಏನ್ರಿ'), 'ಏನು', transformed)
            applied_rules.append({"description": "ಸಂಭಾಷಣಾ ಕ್ಲಿಟಿಕ್ ಶಿಷ್ಟೀಕರಣ (ಏನ್ರಿ -> ಏನು)"})

        if re.search(wrap_kannada_word('ಹೌದ್ರಿ'), transformed):
            transformed = re.sub(wrap_kannada_word('ಹೌದ್ರಿ'), 'ಹೌದು', transformed)
            applied_rules.append({"description": "ಸಂಭಾಷಣಾ ಕ್ಲಿಟಿಕ್ ಶಿಷ್ಟೀಕರಣ (ಹೌದ್ರಿ -> ಹೌದು)"})

        if re.search(r'([\u0C80-\u0CFF]+)ಿಲ್ರಿ(?=[^\u0C80-\u0CFF]|$)', transformed):
            transformed = re.sub(r'([\u0C80-\u0CFF]+)ಿಲ್ರಿ(?=[^\u0C80-\u0CFF]|$)', r'\1ಿಲ್ಲ', transformed)
            applied_rules.append({"description": "ನಕಾರಾತ್ಮಕ ಕ್ಲಿಟಿಕ್ ಶಿಷ್ಟೀಕರಣ (-ಿಲ್ರಿ -> -ಿಲ್ಲ)"})

        if re.search(r'([\u0C80-\u0CFF]+)ತೇನ್ರಿ(?=[^\u0C80-\u0CFF]|$)', transformed):
            transformed = re.sub(r'([\u0C80-\u0CFF]+)ತೇನ್ರಿ(?=[^\u0C80-\u0CFF]|$)', r'\1ಯಿತೇ?', transformed)
            applied_rules.append({"description": "ಉತ್ತರ ಕರ್ನಾಟಕ ಗೌರವಾರ್ಥಕ ಪ್ರಶ್ನಾರ್ಥಕ (-ತೇನ್ರಿ -> -ಯಿತೇ?)"})

        # Imperative virama verbs before ರಿ: ಮಾಡ್ರಿ -> ಮಾಡಿ, ನೋಡ್ರಿ -> ನೋಡಿ, ಹಾಕ್ರಿ -> ಹಾಕಿ, ಹೇಳ್ರಿ -> ಹೇಳಿ, ಇಡ್ರಿ -> ಇಡಿ
        # Restricted to verb consonant bases [ಡ|ಕ|ಳ|ಗ|ಸ] to avoid corrupting Sanskrit nouns like ರಾತ್ರಿ (ರಾತ್-ರಿ)
        p_imp = r'([\u0C80-\u0CFF]+?[ಡ|ಕ|ಳ|ಗ|ಸ])್[ರ್ರ]ಿ(?=[^\u0C80-\u0CFF]|$)'
        if re.search(p_imp, transformed):
            transformed = re.sub(p_imp, r'\1ಿ', transformed)
            applied_rules.append({"description": "ಆಜ್ಞಾರ್ಥಕ ಕ್ರಿಯಾರೂಪ ಶಿಷ್ಟೀಕರಣ (-್ರಿ -> -ಿ)"})

        if re.search(r'([\u0C80-\u0CFF]+)್ನ್ರಿ(?=[^\u0C80-\u0CFF]|$)', transformed):
            transformed = re.sub(r'([\u0C80-\u0CFF]+)್ನ್ರಿ(?=[^\u0C80-\u0CFF]|$)', lambda m: m.group(1) + '್ನಿ', transformed)

        if re.search(wrap_kannada_word('ಕುಡೀರಿ'), transformed):
            transformed = re.sub(wrap_kannada_word('ಕುಡೀರಿ'), 'ಕುಡಿಯಿರಿ', transformed)
            applied_rules.append({"description": "ಕ್ರಿಯಾಪದ ಶಿಷ್ಟೀಕರಣ (ಕುಡೀರಿ -> ಕುಡಿಯಿರಿ)"})

        if re.search(wrap_kannada_word('ನಡೀರಿ'), transformed):
            transformed = re.sub(wrap_kannada_word('ನಡೀರಿ'), 'ನಡೆಯಿರಿ', transformed)
            applied_rules.append({"description": "ಕ್ರಿಯಾಪದ ಶಿಷ್ಟೀಕರಣ (ನಡೀರಿ -> ನಡೆಯಿರಿ)"})

        # Polite & regional perfectives:
        # ಮಾಡ್ಯಾರ -> ಮಾಡಿದ್ದಾರೆ, ಹೇಳ್ಯಾರ -> ಹೇಳಿದ್ದಾರೆ
        if re.search(r'([\u0C80-\u0CFF]+)್ಯಾರ(?=[^\u0C80-\u0CFF]|$)', transformed):
            transformed = re.sub(r'([\u0C80-\u0CFF]+)್ಯಾರ(?=[^\u0C80-\u0CFF]|$)', r'\1ಿದ್ದಾರೆ', transformed)
            applied_rules.append({"description": "ಉತ್ತರ ಕರ್ನಾಟಕ ಗೌರವಾರ್ಥಕ ಭೂತಕಾಲ (-್ಯಾರ -> -ಿದ್ದಾರೆ)"})

        # ಬಂದ್ಯಾನ -> ಬಂದಿದ್ದಾನೆ, ಮಾಡ್ಯಾನ -> ಮಾಡಿದ್ದಾನೆ
        if re.search(r'([\u0C80-\u0CFF]+)್ಯಾನ(?=[^\u0C80-\u0CFF]|$)', transformed):
            transformed = re.sub(r'([\u0C80-\u0CFF]+)್ಯಾನ(?=[^\u0C80-\u0CFF]|$)', r'\1ಿದ್ದಾನೆ', transformed)
            applied_rules.append({"description": "ಉತ್ತರ ಕರ್ನಾಟಕ ತೃತೀಯ ಪುರುಷ ಭೂತಕಾಲ (-್ಯಾನ -> -ಿದ್ದಾನೆ)"})

        # ಮಾಡೀನಿ -> ಮಾಡಿದ್ದೇನೆ, ಬಂದೀನಿ -> ಬಂದಿದ್ದೇನೆ
        if re.search(r'([ಕ-ಹ]+)ೀನಿ(?=[^\u0C80-\u0CFF]|$)', transformed):
            transformed = re.sub(r'([ಕ-ಹ]+)ೀನಿ(?=[^\u0C80-\u0CFF]|$)', r'\1ಿದ್ದೇನೆ', transformed)
            applied_rules.append({"description": "ಉತ್ತರ ಕರ್ನಾಟಕ ಪ್ರಥಮ ಪುರುಷ ಭೂತಕಾಲ (-ೀನಿ -> -ಿದ್ದೇನೆ)"})

        # 3rd neuter plural perfective: -್ಯಾವ -> -ಿವೆ
        if re.search(r'([ಕ-ಹ]+)್ಯಾವ(?=[^\u0C80-\u0CFF]|$)', transformed):
            transformed = re.sub(r'([ಕ-ಹ]+)್ಯಾವ(?=[^\u0C80-\u0CFF]|$)', r'\1ಿವೆ', transformed)
            applied_rules.append({"description": "ಉತ್ತರ ಕರ್ನಾಟಕ ನಪುಂಸಕಲಿಂಗ ಬಹುವಚನ ಭೂತಕಾಲ (-್ಯಾವ -> -ಿವೆ)"})

        # ========================================================
        # 5. NEGATIVES & MODALS
        # ========================================================
        def repl_neg(m):
            root = m.group(1)
            if root in ['ಇ', 'ಅ', 'ಸ', 'ಇಲ್ಲ', 'ಅಲ್ಲ', 'ಎಲ್ಲ', 'ಮೇ', 'ಸಾ']:
                return m.group(0)
            if root.endswith('ೋ'):
                root = root[:-1]
            return f"{root}ುವುದಿಲ್ಲ"
        p7_neg = r'([ಕ-ಹ]+?)(?<![ಿ])ಲ್ಲ(?=[^ಀ-೿]|$)'
        if re.search(p7_neg, transformed):
            new_t = re.sub(p7_neg, repl_neg, transformed)
            if new_t != transformed:
                transformed = new_t
                applied_rules.append({"description": "ನಕಾರಾತ್ಮಕ ಕ್ರಿಯಾಪದ ಶಿಷ್ಟೀಕರಣ (-ಲ್ಲ -> -ುವುದಿಲ್ಲ)"})

        # Past Negatives (-್ಲಿಲ್ಲ -> -ಲಿಲ್ಲ)
        p8_pneg = r'([\u0C80-\u0CFF]+)್ಲಿಲ್ಲ(?=[^\u0C80-\u0CFF]|$)'
        if re.search(p8_pneg, transformed):
            def repl_pneg(m):
                root = m.group(1)
                stem = self.resolve_stem(root)
                if stem.endswith('ು'):
                    stem = stem[:-1]
                return f"{stem}ಲಿಲ್ಲ"
            transformed = re.sub(p8_pneg, repl_pneg, transformed)
            applied_rules.append({"description": "ಭೂತಕಾಲ ನಕಾರಾತ್ಮಕ ಕ್ರಿಯಾರೂಪ (-್ಲಿಲ್ಲ -> -ಲಿಲ್ಲ)"})

        # Infinitives (-ೋಕೆ, -ಾಕ -> -ಲು)
        def repl_purp(m):
            r = m.group(1)
            if r.endswith('ೋ'): r = r[:-1]
            return f"{r}ಲು"

        p10_purp = r'([\u0C80-\u0CFF]+)ೋಕೆ(?=[^\u0C80-\u0CFF]|$)'
        if re.search(p10_purp, transformed):
            transformed = re.sub(p10_purp, repl_purp, transformed)
            applied_rules.append({"description": "ಹೇತ್ವಾರ್ಥಕ ಕ್ರಿಯಾರೂಪ (-ೋಕೆ -> -ಲು)"})

        if re.search(r'([\u0C80-\u0CFF]+)ಾಕ(?=[^\u0C80-\u0CFF]|$)', transformed):
            transformed = re.sub(r'([\u0C80-\u0CFF]+)ಾಕ(?=[^\u0C80-\u0CFF]|$)', repl_purp, transformed)
            applied_rules.append({"description": "ಹೇತ್ವಾರ್ಥಕ ಕ್ರಿಯಾರೂಪ (-ಾಕ -> -ಲು)"})

        # Verbal nouns (-ೋದು -> -ುವುದು)
        p11_vn = r'([\u0C80-\u0CFF]+)ೋದು(?=[^\u0C80-\u0CFF]|$)'
        if re.search(p11_vn, transformed):
            def repl_vn(m):
                r = m.group(1)
                if r.endswith('ೋ'): r = r[:-1]
                return f"{r}ುವುದು"
            transformed = re.sub(p11_vn, repl_vn, transformed)
            applied_rules.append({"description": "ಭಾವನಾಮ ಕ್ರಿಯಾರೂಪ (-ೋದು -> -ುವುದು)"})

        # Conditionals (-ದ್ರೆ -> -ದರೆ, -ಂದ್ರೆ -> -ಂದರೆ, -ದ್ರೂ -> -ದರೂ)
        cond_patterns = [
            (r'([\u0C80-\u0CFF]+)ಂದ್ರೆ(?=[^\u0C80-\u0CFF]|$)', r'\1ಂದರೆ'),
            (r'([\u0C80-\u0CFF]+)ಂದ್ರೂ(?=[^\u0C80-\u0CFF]|$)', r'\1ಂದರೂ'),
            (r'([\u0C80-\u0CFF]+)ದ್ರೂ(?=[^\u0C80-\u0CFF]|$)', r'\1ದರೂ'),
            (r'([\u0C80-\u0CFF]+)ಟ್ರೂ(?=[^\u0C80-\u0CFF]|$)', r'\1ಟ್ಟರೂ'),
            (r'([\u0C80-\u0CFF]+)ದ್ರೆ(?=[^\u0C80-\u0CFF]|$)', r'\1ದರೆ'),
            (r'([\u0C80-\u0CFF]+)ಟ್ರೆ(?=[^\u0C80-\u0CFF]|$)', r'\1ಟ್ಟರೆ')
        ]
        for c_pat, c_rep in cond_patterns:
            if re.search(c_pat, transformed):
                transformed = re.sub(c_pat, c_rep, transformed)
                applied_rules.append({"description": "ಸಂಭಾವ್ಯಾರ್ಥಕ ಕ್ರಿಯಾರೂಪ ಶಿಷ್ಟೀಕರಣ (-ದ್ರೆ/-ಂದ್ರೆ -> -ದರೆ/-ಂದರೆ)"})

        # Emphatic Obligation & Interrogative Modals (-ಲೇ, -್ಲೇ)
        p_emph_q = r'([\u0C80-\u0CFF]+?)(?:ಲೇ|್ಲೇ)\?'
        if re.search(p_emph_q, transformed):
            transformed = re.sub(p_emph_q, r'\1ಬೇಕೇ?', transformed)
            applied_rules.append({"description": "ಪ್ರಶ್ನಾರ್ಥಕ ಸಂಭಾವ್ಯರೂಪ (-ಲೇ? -> -ಬೇಕೇ?)"})

        p_emph_d = r'([\u0C80-\u0CFF]+?)(?:ಲೇ|್ಲೇ)(?!\s*ಇಲ್ಲ)(?=[^\u0C80-\u0CFF]|$)'
        if re.search(p_emph_d, transformed):
            transformed = re.sub(p_emph_d, r'\1ಲೇಬೇಕು', transformed)
            applied_rules.append({"description": "ಅವಧಾರಣಾ ವಿಧ್ಯರ್ಥಕ ಕ್ರಿಯಾರೂಪ (-ಲೇ -> -ಲೇಬೇಕು)"})

        # Modal Contractions: -್ಬೇಕು -> -ಬೇಕು, -್ಬಾರ್ದು -> -ಬಾರದು
        if re.search(r'([\u0C80-\u0CFF]+)್ಬೇಕು(?=[^\u0C80-\u0CFF]|$)', transformed):
            transformed = re.sub(r'([\u0C80-\u0CFF]+)್ಬೇಕು(?=[^\u0C80-\u0CFF]|$)', r'\1ಬೇಕು', transformed)
            applied_rules.append({"description": "ವಿಧ್ಯರ್ಥಕ ಸಹಾಯಕ ಕ್ರಿಯಾಪದ (-್ಬೇಕು -> -ಬೇಕು)"})

        if re.search(r'([\u0C80-\u0CFF]+)್ಬಾರ್ದು(?=[^\u0C80-\u0CFF]|$)', transformed):
            transformed = re.sub(r'([\u0C80-\u0CFF]+)್ಬಾರ್ದು(?=[^\u0C80-\u0CFF]|$)', r'\1ಬಾರದು', transformed)
            applied_rules.append({"description": "ನಿಷೇಧಾರ್ಥಕ ಕ್ರಿಯಾರೂಪ (-್ಬಾರ್ದು -> -ಬಾರದು)"})

        # Ability contractions
        if re.search(r'([\u0C80-\u0CFF]+)ೋಕಾಗಲ್ಲ(?=[^\u0C80-\u0CFF]|$)', transformed):
            transformed = re.sub(r'([\u0C80-\u0CFF]+)ೋಕಾಗಲ್ಲ(?=[^\u0C80-\u0CFF]|$)', r'\1ಲು ಸಾಧ್ಯವಿಲ್ಲ', transformed)
            applied_rules.append({"description": "ಸಾಮರ್ಥ್ಯ ನಕಾರಾತ್ಮಕ ಕ್ರಿಯಾರೂಪ (-ೋಕಾಗಲ್ಲ -> -ಲು ಸಾಧ್ಯವಿಲ್ಲ)"})

        if re.search(r'([\u0C80-\u0CFF]+)ೋಕಾಗುತ್ತೆ(?=[^\u0C80-\u0CFF]|$)', transformed):
            transformed = re.sub(r'([\u0C80-\u0CFF]+)ೋಕಾಗುತ್ತೆ(?=[^\u0C80-\u0CFF]|$)', r'\1ಲು ಸಾಧ್ಯವಾಗುತ್ತದೆ', transformed)
            applied_rules.append({"description": "ಸಾಮರ್ಥ್ಯ ಸಕಾರಾತ್ಮಕ ಕ್ರಿಯಾರೂಪ (-ೋಕಾಗುತ್ತೆ -> -ಲು ಸಾಧ್ಯವಾಗುತ್ತದೆ)"})

        # ========================================================
        # 6. PERMISSIVE IMPERATIVE WITH STRICT EXCLUSION
        # (Fixes the critical bug: ಅಲ್ಲಿ -> ಅಲಲಿ)
        # ========================================================
        def repl_perm_imperative(m):
            w = m.group(1)
            full = m.group(0)
            # PROTECT geminate ಲ್ಲಿ (ಅಲ್ಲಿ, ಇಲ್ಲಿ, ಎಲ್ಲಿ, ಮನೆಯಲ್ಲಿ, ಹೊಲದಲ್ಲಿ, ಶಾಲೆಗಳಲ್ಲಿ)
            if w.endswith('\u0CB2') or full.endswith('ಲ್ಲಿ'):
                return full
            # Protect base pronouns and particles
            if w in ['ಅ', 'ಇ', 'ಎ', 'ನಾ', 'ಯಾ']:
                return full
            stem = self.resolve_stem(w)
            if stem.endswith('ು'):
                stem = stem[:-1]
            return stem + 'ಲಿ'
        p_perm = r'(?<![\u0C80-\u0CFF])([^\s\u0C80-\u0CFF]*[\u0C80-\u0CFF]+?)್ಲಿ(?=[^\u0C80-\u0CFF]|$)'
        if re.search(p_perm, transformed):
            new_t = re.sub(p_perm, repl_perm_imperative, transformed)
            if new_t != transformed:
                transformed = new_t
                applied_rules.append({"description": "ಆಜ್ಞಾರ್ಥಕ/ಅನುಮತ್ಯರ್ಥಕ ಕ್ರಿಯಾರೂಪ (-್ಲಿ -> -ಲಿ)"})

        # ========================================================
        # 7. NOUN CASES & SUFFIXES
        # ========================================================
        # Locative -ದಾಗ -> -ದಲ್ಲಿ
        if re.search(r'([ಕ-ಹ]+)ದಾಗ(?=[^\u0C80-\u0CFF]|$)', transformed):
            transformed = re.sub(r'([ಕ-ಹ]+)ದಾಗ(?=[^\u0C80-\u0CFF]|$)', r'\1ದಲ್ಲಿ', transformed)
            applied_rules.append({"description": "ಅಧಿಕರಣ ವಿಭಕ್ತಿ ಪ್ರತ್ಯಯ (-ದಾಗ -> -ದಲ್ಲಿ)"})

        # Locative -ನ್ಯಾಗ -> -ನೆಯಲ್ಲಿ
        if re.search(r'([ಕ-ಹ]+)ನ್ಯಾಗ(?=[^\u0C80-\u0CFF]|$)', transformed):
            transformed = re.sub(r'([ಕ-ಹ]+)ನ್ಯಾಗ(?=[^\u0C80-\u0CFF]|$)', r'\1ನೆಯಲ್ಲಿ', transformed)
            applied_rules.append({"description": "ಸ್ಥಳವಾಚಿ ಅಧಿಕರಣ ಪ್ರತ್ಯಯ (-ನ್ಯಾಗ -> -ನೆಯಲ್ಲಿ)"})

        # Locative -ಲ್ on coastal/UK nouns: ಮನೆಲ್ -> ಮನೆಯಲ್ಲಿ, ಶಾಲೆಲ್ -> ಶಾಲೆಯಲ್ಲಿ
        transformed = re.sub(wrap_kannada_word('ಮನೆಲ್'), 'ಮನೆಯಲ್ಲಿ', transformed)
        transformed = re.sub(wrap_kannada_word('ಮನೇಲಿ'), 'ಮನೆಯಲ್ಲಿ', transformed)
        transformed = re.sub(wrap_kannada_word('ಶಾಲೆಲ್'), 'ಶಾಲೆಯಲ್ಲಿ', transformed)

        # Dative -ಗ್ on nouns: ಶಾಲೆಗ್ -> ಶಾಲೆಗೆ, ಮನೆಗ್ -> ಮನೆಗೆ, ಪೇಟೆಗ್ -> ಪೇಟೆಗೆ, ಅಂಗಡಿಗ್ -> ಅಂಗಡಿಗೆ
        transformed = re.sub(wrap_kannada_word('ಶಾಲೆಗ್'), 'ಶಾಲೆಗೆ', transformed)
        transformed = re.sub(wrap_kannada_word('ಮನೆಗ್'), 'ಮನೆಗೆ', transformed)
        transformed = re.sub(wrap_kannada_word('ಪೇಟೆಗ್'), 'ಪೇಟೆಗೆ', transformed)
        transformed = re.sub(wrap_kannada_word('ಅಂಗಡಿಗ್'), 'ಅಂಗಡಿಗೆ', transformed)
        transformed = re.sub(wrap_kannada_word('ಸಾಲಿಗ್'), 'ಶಾಲೆಗೆ', transformed)
        transformed = re.sub(wrap_kannada_word('ಮನಿಗ'), 'ಮನೆಗೆ', transformed)
        transformed = re.sub(wrap_kannada_word('ಊಟಕ್ಕ'), 'ಊಟಕ್ಕೆ', transformed)
        transformed = re.sub(wrap_kannada_word('ಊರಕ್ಕ'), 'ಊರಿಗೆ', transformed)

        # Accusative -ವನ್ನ -> -ವನ್ನು (ಪುಸ್ತಕವನ್ನ -> ಪುಸ್ತಕವನ್ನು)
        if re.search(r'([\u0C80-\u0CFF]+)ವನ್ನ(?=[^\u0C80-\u0CFF]|$)', transformed):
            transformed = re.sub(r'([\u0C80-\u0CFF]+)ವನ್ನ(?=[^\u0C80-\u0CFF]|$)', r'\1ವನ್ನು', transformed)
            applied_rules.append({"description": "ದ್ವಿತೀಯಾ ವಿಭಕ್ತಿ ಪ್ರತ್ಯಯ (-ವನ್ನ -> -ವನ್ನು)"})

        # Vocative softening: ಅಣ್ಣಾ, -> ಅಣ್ಣ,, ತಮ್ಮಾ, -> ತಮ್ಮ,, ಮಗನೇ, -> ಮಗನೆ,
        transformed = re.sub(wrap_kannada_word('ಅಣ್ಣಾ,'), 'ಅಣ್ಣ,', transformed)
        transformed = re.sub(wrap_kannada_word('ತಮ್ಮಾ,'), 'ತಮ್ಮ,', transformed)
        transformed = re.sub(wrap_kannada_word('ಮಗನೇ,'), 'ಮಗನೆ,', transformed)
        transformed = re.sub(wrap_kannada_word('ಅಕ್ಕಾ,'), 'ಅಕ್ಕ,', transformed)

        # Pronoun mappings:
        pr_map = {
            'ನಂಗ್': 'ನನಗೆ', 'ನಿಂಗ್': 'ನಿನಗೆ', 'ಅವಂಗ್': 'ಅವನಿಗೆ',
            'ಅವಳ್ಗ್': 'ಅವಳಿಗೆ', 'ನಮ್ದು': 'ನಮ್ಮದು', 'ನಿಮ್ದು': 'ನಿಮ್ಮದು',
            'ಯಾರ್ದು': 'ಯಾರದು', 'ನನಗ': 'ನನಗೆ', 'ನಿನಗ': 'ನಿನಗೆ',
            'ಅವಂಗ': 'ಅವನಿಗೆ', 'ನಂಗೆ': 'ನನಗೆ', 'ನಿಂಗೆ': 'ನಿನಗೆ',
            'ಆಯ್ಕಿನು': 'ಅವಳು', 'ಆಯಿ': 'ಅವನು', 'ಏಂಕ್ಲು': 'ನಾವು',
            'ನಾವೆಲ್ಲಾ': 'ನಾವೆಲ್ಲರೂ', 'ನಾವೆಲ್ಲ': 'ನಾವೆಲ್ಲರೂ',
            'ಮಕ್ಕಳೆಲ್ಲಾ': 'ಮಕ್ಕಳೆಲ್ಲರೂ', 'ಮಕ್ಕಳೆಲ್ಲ': 'ಮಕ್ಕಳೆಲ್ಲರೂ',
            'ನಾನಲ್ಲಿ': 'ನಾನು ಅಲ್ಲಿಗೆ'
        }
        for pr_k, pr_v in pr_map.items():
            if re.search(wrap_kannada_word(pr_k), transformed):
                transformed = re.sub(wrap_kannada_word(pr_k), pr_v, transformed)

        # Contraction syncopations in high frequency words
        transformed = re.sub(wrap_kannada_word('ದೇವ್ರಿಗೆ'), 'ದೇವರಿಗೆ', transformed)
        transformed = re.sub(wrap_kannada_word('ದೇವ್ರು'), 'ದೇವರು', transformed)

        # ========================================================
        # 8. PUNCTUATION & IDEMPOTENCE CLEANUP
        # ========================================================
        transformed = re.sub(r'\?+', '?', transformed)
        transformed = re.sub(r"\s+\?", "?", transformed)
        transformed = re.sub(r"\s+!", "!", transformed)
        transformed = re.sub(r"\s+\.", ".", transformed)
        transformed = re.sub(r"\s{2,}", " ", transformed).strip()

        return transformed, applied_rules
