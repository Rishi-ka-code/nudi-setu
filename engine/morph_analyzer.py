# -*- coding: utf-8 -*-
"""
Morphological Analyzer & Transformer:
Universal rule engine for Kannada verb and noun morphology.
Handles open-ended inputs across all dialect variations.
"""

import re
import json
import os
from typing import Tuple, List, Dict, Any

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
            'ತಗೋ': 'ತೆಗೆದುಕೊಳ್ಳು'
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

    def apply_rules(self, text: str) -> Tuple[str, List[Dict[str, str]]]:
        transformed = text
        applied_rules = []

        # ========================================================
        # PHONETIC KEYBOARD METATHESIS & TYPO CORRECTIONS
        # (Handles 'batarna' -> 'ಬತಾರ್ನ' keyboard transposition for 'ಬರ್ತಾನ')
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
        # UNIVERSAL VERBAL INFLECTION TRANSFORMS
        # ========================================================

        # 1. Habitual 3rd Masc Interrogative (-್ತಾನಾ? / -್ತಾನಾ / -್ತಾನ?)
        # e.g. ಅವನು ಬರ್ತಾನಾ? -> ಅವನು ಬರುತ್ತಾನೆಯೇ?, ಅವನು ಬರ್ತಾನ? -> ಅವನು ಬರುತ್ತಾನೆಯೇ?
        p1 = r'([\u0C80-\u0CFF]+)್ತಾನಾ\?(?=[^\u0C80-\u0CFF]|$)|([\u0C80-\u0CFF]+)್ತಾನ\?(?=[^\u0C80-\u0CFF]|$)'
        def p1_sub(m):
            root = m.group(1) or m.group(2)
            stem = self.resolve_stem(root)
            return self.attach_present(stem, 'ುತ್ತಾನೆಯೇ?')
        if re.search(p1, transformed):
            transformed = re.sub(p1, p1_sub, transformed)
            applied_rules.append({
                "description": "ಪ್ರಶ್ನಾರ್ಥಕ ಕ್ರಿಯಾಪದ ಪ್ರತ್ಯಯ ಸಾರ್ವತ್ರಿಕ ಶಿಷ್ಟೀಕರಣ (-್ತಾನಾ? -> -ತ್ತಾನೆಯೇ?)"
            })

        def p1_long(m):
            stem = self.resolve_stem(m.group(1))
            return self.attach_present(stem, 'ುತ್ತಾನೆಯೇ')
        p1_l = r'([\u0C80-\u0CFF]+)್ತಾನಾ(?=[^\u0C80-\u0CFF]|$)'
        if re.search(p1_l, transformed):
            transformed = re.sub(p1_l, p1_long, transformed)
            applied_rules.append({
                "description": "ಪ್ರಶ್ನಾರ್ಥಕ ಕ್ರಿಯಾಪದ ಪ್ರತ್ಯಯ ಶಿಷ್ಟೀಕರಣ (-್ತಾನಾ -> -ತ್ತಾನೆಯೇ)"
            })

        # 2. Habitual 3rd Masc Declarative (-್ತಾನ / -್ತಾನೆ)
        # e.g. ಅವನು ಬರ್ತಾನ -> ಅವನು ಬರುತ್ತಾನೆ, ಅವನು ಮಾಡ್ತಾನ -> ಅವನು ಮಾಡುತ್ತಾನೆ
        def repl_hm_dec(m):
            stem = self.resolve_stem(m.group(1))
            return self.attach_present(stem, 'ುತ್ತಾನೆ')
        p2 = r'([\u0C80-\u0CFF]+)್ತಾನ[ೆ]?(?=[^\u0C80-\u0CFF]|$)'
        if re.search(p2, transformed):
            transformed = re.sub(p2, repl_hm_dec, transformed)
            applied_rules.append({
                "description": "ತೃತೀಯ ಪುರುಷ ಪುಲ್ಲಿಂಗ ವರ್ತಮಾನ ಕ್ರಿಯಾರೂಪ (-್ತಾನ -> -ತ್ತಾನೆ)"
            })

        # 3. Habitual 3rd Fem Interrogative & Declarative (-್ತಾಳಾ?, -್ತಾಳ / -್ತಾಳೆ)
        p3_int = r'([\u0C80-\u0CFF]+)್ತಾಳ[ಾ]?\?(?=[^\u0C80-\u0CFF]|$)'
        if re.search(p3_int, transformed):
            transformed = re.sub(p3_int, lambda m: self.attach_present(self.resolve_stem(m.group(1)), 'ುತ್ತಾಳೆಯೇ?'), transformed)
            applied_rules.append({
                "description": "ಸ್ತ್ರೀಲಿಂಗ ಪ್ರಶ್ನಾರ್ಥಕ ಕ್ರಿಯಾರೂಪ (-್ತಾಳಾ? -> -ತ್ತಾಳೆಯೇ?)"
            })

        p3_dec = r'([\u0C80-\u0CFF]+)್ತಾಳ[ೆ]?(?=[^\u0C80-\u0CFF]|$)'
        if re.search(p3_dec, transformed):
            transformed = re.sub(p3_dec, lambda m: self.attach_present(self.resolve_stem(m.group(1)), 'ುತ್ತಾಳೆ'), transformed)
            applied_rules.append({
                "description": "ಸ್ತ್ರೀಲಿಂಗ ವರ್ತಮಾನ ಕ್ರಿಯಾರೂಪ (-್ತಾಳ -> -ತ್ತಾಳೆ)"
            })

        # 4. Habitual 3rd Plural (-್ತಾರಾ?, -್ತಾರ / -್ತಾರೆ)
        p4_int = r'([\u0C80-\u0CFF]+)್ತಾರ[ಾ]?\?(?=[^\u0C80-\u0CFF]|$)'
        if re.search(p4_int, transformed):
            transformed = re.sub(p4_int, lambda m: self.attach_present(self.resolve_stem(m.group(1)), 'ುತ್ತಾರೆಯೇ?'), transformed)
            applied_rules.append({
                "description": "ಬಹುವಚನ ಪ್ರಶ್ನಾರ್ಥಕ ಕ್ರಿಯಾರೂಪ (-್ತಾರಾ? -> -ತ್ತಾರೆಯೇ?)"
            })

        p4_dec = r'([\u0C80-\u0CFF]+)್ತಾರ[ೆ]?(?=[^\u0C80-\u0CFF]|$)'
        if re.search(p4_dec, transformed):
            transformed = re.sub(p4_dec, lambda m: self.attach_present(self.resolve_stem(m.group(1)), 'ುತ್ತಾರೆ'), transformed)
            applied_rules.append({
                "description": "ಬಹುವಚನ ವರ್ತಮಾನ ಕ್ರಿಯಾರೂಪ (-್ತಾರ -> -ುತ್ತಾರೆ)"
            })

        # 5. Habitual 1st Sing (-್ತೀನಿ) & Plural (-್ತೀವಿ)
        p5_1s = r'([\u0C80-\u0CFF]+)್ತೀನಿ(?=[^\u0C80-\u0CFF]|$)'
        if re.search(p5_1s, transformed):
            transformed = re.sub(p5_1s, lambda m: self.attach_present(self.resolve_stem(m.group(1)), 'ುತ್ತೇನೆ'), transformed)
            applied_rules.append({
                "description": "ಪ್ರಥಮ ಪುರುಷ ಏಕವಚನ ಕ್ರಿಯಾರೂಪ (-್ತೀನಿ -> -ುತ್ತೇನೆ)"
            })

        p5_1p = r'([\u0C80-\u0CFF]+)್ತೀವಿ(?=[^\u0C80-\u0CFF]|$)'
        if re.search(p5_1p, transformed):
            transformed = re.sub(p5_1p, lambda m: self.attach_present(self.resolve_stem(m.group(1)), 'ುತ್ತೇವೆ'), transformed)
            applied_rules.append({
                "description": "ಪ್ರಥಮ ಪುರುಷ ಬಹುವಚನ ಕ್ರಿಯಾರೂಪ (-್ತೀವಿ -> -ುತ್ತೇವೆ)"
            })

        # 6. Habitual 2nd Person (-್ತೀಯಾ, -್ತಿಯಾ, -ತಿಯಾ, -್ತೀರಿ)
        p6_2s = r'([\u0C80-\u0CFF]+?)(?:್ತೀಯ|್ತಿಯ|ತಿಯ)[ಾ]?(?=\?|[^\u0C80-\u0CFF]|$)'
        if re.search(p6_2s, transformed):
            transformed = re.sub(p6_2s, lambda m: self.attach_present(self.resolve_stem(m.group(1)), 'ುತ್ತೀಯಾ'), transformed)
            applied_rules.append({
                "description": "ಮಧ್ಯಮ ಪುರುಷ ಕ್ರಿಯಾರೂಪ (-್ತೀಯಾ / -ತಿಯಾ -> -ುತ್ತೀಯಾ)"
            })

        p6_2p = r'([\u0C80-\u0CFF]+)್ತೀರಿ(?=[^\u0C80-\u0CFF]|$)'
        if re.search(p6_2p, transformed):
            transformed = re.sub(p6_2p, lambda m: self.attach_present(self.resolve_stem(m.group(1)), 'ುತ್ತೀರಿ'), transformed)
            applied_rules.append({
                "description": "ಮಧ್ಯಮ ಪುರುಷ ಗೌರವಾರ್ಥಕ ಕ್ರಿಯಾರೂಪ (-್ತೀರಿ -> -ುತ್ತೀರಿ)"
            })

        # 7. Negative Verbs (-ಲ್ಲ, -ೋಲ್ಲ -> -ುವುದಿಲ್ಲ)
        def repl_neg(m):
            root = m.group(1)
            if root in ['ಇ', 'ಅ', 'ಸ', 'ಇಲ್ಲ', 'ಅಲ್ಲ', 'ಎಲ್ಲ']:
                return m.group(0)
            if root.endswith('ೋ'):
                root = root[:-1]
            return f"{root}ುವುದಿಲ್ಲ"
        p7_neg = r'([\u0C80-\u0CFF]+)ಲ್ಲ(?=[^\u0C80-\u0CFF]|$)'
        if re.search(p7_neg, transformed):
            new_t = re.sub(p7_neg, repl_neg, transformed)
            if new_t != transformed:
                transformed = new_t
                applied_rules.append({
                    "description": "ನಕಾರಾತ್ಮಕ ಕ್ರಿಯಾಪದ ಶಿಷ್ಟೀಕರಣ (-ಲ್ಲ -> -ುವುದಿಲ್ಲ)"
                })

        # 8. Past Negatives (-್ಲಿಲ್ಲ -> -ಲಿಲ್ಲ)
        p8_pneg = r'([\u0C80-\u0CFF]+)್ಲಿಲ್ಲ(?=[^\u0C80-\u0CFF]|$)'
        if re.search(p8_pneg, transformed):
            def repl_pneg(m):
                root = m.group(1)
                stem = self.resolve_stem(root)
                if stem.endswith('\u0CC1'):
                    stem = stem[:-1]
                return f"{stem}ಲಿಲ್ಲ"
            transformed = re.sub(p8_pneg, repl_pneg, transformed)
            applied_rules.append({
                "description": "ಭೂತಕಾಲ ನಕಾರಾತ್ಮಕ ಕ್ರಿಯಾರೂಪ (-್ಲಿಲ್ಲ -> -ಲಿಲ್ಲ)"
            })

        # 9. Colloquial Continuous (-್ತಾವನೆ / -್ತಾವ್ನೆ -> -ುತ್ತಿದ್ದಾನೆ)
        p9_prog = r'([\u0C80-\u0CFF]+)್ತಾವ[್]?ನೆ(?=[^\u0C80-\u0CFF]|$)'
        if re.search(p9_prog, transformed):
            transformed = re.sub(p9_prog, lambda m: self.attach_present(self.resolve_stem(m.group(1)), 'ುತ್ತಿದ್ದಾನೆ'), transformed)
            applied_rules.append({
                "description": "ಆಡುಮಾತಿನ ಪ್ರವರ್ತಮಾನ ರೂಪ (-್ತಾವನೆ -> -ುತ್ತಿದ್ದಾನೆ)"
            })

        p9_prog_f = r'([\u0C80-\u0CFF]+)್ತಾವಳೆ(?=[^\u0C80-\u0CFF]|$)'
        if re.search(p9_prog_f, transformed):
            transformed = re.sub(p9_prog_f, lambda m: self.attach_present(self.resolve_stem(m.group(1)), 'ುತ್ತಿದ್ದಾಳೆ'), transformed)

        p9_prog_p = r'([\u0C80-\u0CFF]+)್ತಾವ್ರೆ(?=[^\u0C80-\u0CFF]|$)'
        if re.search(p9_prog_p, transformed):
            transformed = re.sub(p9_prog_p, lambda m: self.attach_present(self.resolve_stem(m.group(1)), 'ುತ್ತಿದ್ದಾರೆ'), transformed)

        # 10. Purposive Infinitives (-ೋಕೆ, -ಾಕ -> -ಲು)
        p10_purp = r'([\u0C80-\u0CFF]+)ೋಕೆ(?=[^\u0C80-\u0CFF]|$)'
        if re.search(p10_purp, transformed):
            def repl_purp(m):
                r = m.group(1)
                if r.endswith('ೋ'): r = r[:-1]
                return f"{r}ಲು"
            transformed = re.sub(p10_purp, repl_purp, transformed)
            applied_rules.append({
                "description": "ಹೇತ್ವಾರ್ಥಕ ಕ್ರಿಯಾರೂಪ (-ೋಕೆ -> -ಲು)"
            })

        # 11. Verbal Nouns (-ೋದು -> -ುವುದು)
        p11_vn = r'([\u0C80-\u0CFF]+)ೋದು(?=[^\u0C80-\u0CFF]|$)'
        if re.search(p11_vn, transformed):
            def repl_vn(m):
                r = m.group(1)
                if r.endswith('ೋ'): r = r[:-1]
                return f"{r}ುವುದು"
            transformed = re.sub(p11_vn, repl_vn, transformed)
            applied_rules.append({
                "description": "ಭಾವನಾಮ ಕ್ರಿಯಾರೂಪ (-ೋದು -> -ುವುದು)"
            })

        # 12. Conditional & Concessive Verb Suffixes (-ದ್ರೆ -> -ದರೆ, -ಂದ್ರೆ -> -ಂದರೆ, -ದ್ರೂ -> -ದರೂ)
        # e.g. ಹೋದ್ರೆ -> ಹೋದರೆ, ಬಂದ್ರೆ -> ಬಂದರೆ, ಕೊಟ್ರೆ -> ಕೊಟ್ಟರೆ, ಹೋದ್ರೂ -> ಹೋದರೂ
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

        # 13. Compound & Colloquial Aspectual Verbs
        # e.g. ಹೋಗ್ಬರ್ತೀನಿ -> ಹೋಗಿ ಬರುತ್ತೇನೆ, ಬಂದ್ಬಿಟ್ಟ -> ಬಂದುಬಿಟ್ಟ, ಮಾಡ್ಬಿಟ್ಟ -> ಮಾಡಿಬಿಟ್ಟ
        if re.search(r'ಹೋಗ್ಬರ್ತೀನಿ(?=[^\u0C80-\u0CFF]|$)', transformed):
            transformed = re.sub(r'ಹೋಗ್ಬರ್ತೀನಿ(?=[^\u0C80-\u0CFF]|$)', 'ಹೋಗಿ ಬರುತ್ತೇನೆ', transformed)
            applied_rules.append({"description": "ಸಂಯುಕ್ತ ಕ್ರಿಯಾಪದ ಶಿಷ್ಟೀಕರಣ (ಹೋಗ್ಬರ್ತೀನಿ -> ಹೋಗಿ ಬರುತ್ತೇನೆ)"})

        if re.search(r'ಬಂದ್ಬಿಟ್ಟ([ೆುರು]?)(?=[^\u0C80-\u0CFF]|$)', transformed):
            transformed = re.sub(r'ಬಂದ್ಬಿಟ್ಟ([ೆುರು]?)(?=[^\u0C80-\u0CFF]|$)', r'ಬಂದುಬಿಟ್ಟ\1', transformed)
            applied_rules.append({"description": "ಸಂಯುಕ್ತ ಸಹಾಯಕ ಕ್ರಿಯಾಪದ (ಬಂದ್ಬಿಟ್ಟ -> ಬಂದುಬಿಟ್ಟ)"})

        if re.search(r'([ಕ-ಹ][ಾ-್]*)್ಬಿಟ್ಟ([ೆುರು]?)(?=[^\u0C80-\u0CFF]|$)', transformed):
            transformed = re.sub(r'([ಕ-ಹ][ಾ-್]*)್ಬಿಟ್ಟ([ೆುರು]?)(?=[^\u0C80-\u0CFF]|$)', r'\1ಿಬಿಟ್ಟ\2', transformed)
            applied_rules.append({"description": "ಸಂಯುಕ್ತ ಸಹಾಯಕ ಕ್ರಿಯಾಪದ (-್ಬಿಟ್ಟ -> -ಿಬಿಟ್ಟ)"})

        # 14. Emphatic Obligation & Interrogative Modals (-ಲೇ, -್ಲೇ)
        # e.g. ಅವನು ಬರಲೇ -> ಅವನು ಬರಲೇಬೇಕು, ಅವನು ಬರಲೇ? -> ಅವನು ಬರಬೇಕೇ?
        p_emph_q = r'([\u0C80-\u0CFF]+?)(?:ಲೇ|್ಲೇ)\?'
        if re.search(p_emph_q, transformed):
            transformed = re.sub(p_emph_q, r'\1ಬೇಕೇ?', transformed)
            applied_rules.append({"description": "ಪ್ರಶ್ನಾರ್ಥಕ ಸಂಭಾವ್ಯರೂಪ (-ಲೇ? -> -ಬೇಕೇ?)"})

        p_emph_d = r'([\u0C80-\u0CFF]+?)(?:ಲೇ|್ಲೇ)(?!\s*ಇಲ್ಲ)(?=[^\u0C80-\u0CFF]|$)'
        if re.search(p_emph_d, transformed):
            transformed = re.sub(p_emph_d, r'\1ಲೇಬೇಕು', transformed)
            applied_rules.append({"description": "ಅವಧಾರಣಾ ವಿಧ್ಯರ್ಥಕ ಕ್ರಿಯಾರೂಪ (-ಲೇ -> -ಲೇಬೇಕು)"})

        # 15. Permissive Imperative (-್ಲಿ -> -ಲಿ)
        # e.g. ಬರ್ಲಿ -> ಬರಲಿ, ಹೋಗ್ಲಿ -> ಹೋಗಲಿ, ಮಾಡ್ಲಿ -> ಮಾಡಲಿ, ಹೇಳ್ಲಿ -> ಹೇಳಲಿ
        p_perm = r'([\u0C80-\u0CFF]+?)್ಲಿ(?=[^\u0C80-\u0CFF]|$)'
        if re.search(p_perm, transformed):
            transformed = re.sub(p_perm, r'\1ಲಿ', transformed)
            applied_rules.append({"description": "ಆಜ್ಞಾರ್ಥಕ/ಅನುಮತ್ಯರ್ಥಕ ಕ್ರಿಯಾರೂಪ (-್ಲಿ -> -ಲಿ)"})

        # 16. Comparative / Manner Suffixes (-ದಂಗೆ -> -ದಂತೆ)
        # e.g. ಹೇಳಿದಂಗೆ -> ಹೇಳಿದಂತೆ, ಮಾಡಿದಂಗೆ -> ಮಾಡಿದಂತೆ, ಹೋದಂಗೆ -> ಹೋದಂತೆ
        p_manner = r'([\u0C80-\u0CFF]+)ದಂಗೆ(?=[^\u0C80-\u0CFF]|$)'
        if re.search(p_manner, transformed):
            transformed = re.sub(p_manner, r'\1ದಂತೆ', transformed)
            applied_rules.append({"description": "ರೀತ್ಯರ್ಥಕ ಪ್ರತ್ಯಯ ಶಿಷ್ಟೀಕರಣ (-ದಂಗೆ -> -ದಂತೆ)"})

        # 17. Potential & Ability Contractions (-ೋಕಾಗಲ್ಲ, -ೋಕಾಗುತ್ತೆ)
        p_pot_neg = r'([\u0C80-\u0CFF]+)ೋಕಾಗಲ್ಲ(?=[^\u0C80-\u0CFF]|$)'
        if re.search(p_pot_neg, transformed):
            transformed = re.sub(p_pot_neg, r'\1ಲು ಸಾಧ್ಯವಿಲ್ಲ', transformed)
            applied_rules.append({"description": "ಸಾಮರ್ಥ್ಯ ನಕಾರಾತ್ಮಕ ಕ್ರಿಯಾರೂಪ (-ೋಕಾಗಲ್ಲ -> -ಲು ಸಾಧ್ಯವಿಲ್ಲ)"})

        p_pot_pos = r'([\u0C80-\u0CFF]+)ೋಕಾಗುತ್ತೆ(?=[^\u0C80-\u0CFF]|$)'
        if re.search(p_pot_pos, transformed):
            transformed = re.sub(p_pot_pos, r'\1ಲು ಸಾಧ್ಯವಾಗುತ್ತದೆ', transformed)
            applied_rules.append({"description": "ಸಾಮರ್ಥ್ಯ ಸಕಾರಾತ್ಮಕ ಕ್ರಿಯಾರೂಪ (-ೋಕಾಗುತ್ತೆ -> -ಲು ಸಾಧ್ಯವಾಗುತ್ತದೆ)"})

        # ========================================================
        # LOADED RULES FROM REGIONAL_MARKERS.JSON
        # ========================================================
        for rule in self.rules:
            pattern = rule["pattern"]
            replacement = rule["replacement"]
            desc = rule.get("description", "")

            if re.search(pattern, transformed):
                new_text = re.sub(pattern, replacement, transformed)
                if new_text != transformed:
                    applied_rules.append({
                        "pattern": pattern,
                        "description": desc,
                        "before": transformed,
                        "after": new_text
                    })
                    transformed = new_text

        # ========================================================
        # NOUN CASE SUFFIXES & DISCOURSE CLEANUP
        # ========================================================
        # Locative -ದಾಗ -> -ದಲ್ಲಿ (e.g. ಹೊಲದಾಗ -> ಹೊಲದಲ್ಲಿ)
        if re.search(r'([ಕ-ಹ]+)ದಾಗ(?=[^\u0C80-\u0CFF]|$)', transformed):
            transformed = re.sub(r'([ಕ-ಹ]+)ದಾಗ(?=[^\u0C80-\u0CFF]|$)', r'\1ದಲ್ಲಿ', transformed)
            applied_rules.append({"description": "ಅಧಿಕರಣ ವಿಭಕ್ತಿ ಪ್ರತ್ಯಯ (-ದಾಗ -> -ದಲ್ಲಿ)"})

        # Locative -ನ್ಯಾಗ -> -ನೆಯಲ್ಲಿ (e.g. ಮನ್ಯಾಗ -> ಮನೆಯಲ್ಲಿ)
        if re.search(r'([ಕ-ಹ]+)ನ್ಯಾಗ(?=[^\u0C80-\u0CFF]|$)', transformed):
            transformed = re.sub(r'([ಕ-ಹ]+)ನ್ಯಾಗ(?=[^\u0C80-\u0CFF]|$)', r'\1ನೆಯಲ್ಲಿ', transformed)
            applied_rules.append({"description": "ಸ್ಥಳವಾಚಿ ಅಧಿಕರಣ ಪ್ರತ್ಯಯ (-ನ್ಯಾಗ -> -ನೆಯಲ್ಲಿ)"})

        # Pronoun datives: ನಂಗ್ -> ನನಗೆ, ನಿಂಗ್ -> ನಿನಗೆ, ಅವಂಗ್ -> ಅವನಿಗೆ, ಅವಳ್ಗ್ -> ಅವಳಿಗೆ
        pr_map = {
            r'\bನಂಗ್(?=[^\u0C80-\u0CFF]|$)': 'ನನಗೆ',
            r'\bನಿಂಗ್(?=[^\u0C80-\u0CFF]|$)': 'ನಿನಗೆ',
            r'\bಅವಂಗ್(?=[^\u0C80-\u0CFF]|$)': 'ಅವನಿಗೆ',
            r'\bಅವಳ್ಗ್(?=[^\u0C80-\u0CFF]|$)': 'ಅವಳಿಗೆ',
            r'\bನಮ್ದು(?=[^\u0C80-\u0CFF]|$)': 'ನಮ್ಮದು',
            r'\bನಿಮ್ದು(?=[^\u0C80-\u0CFF]|$)': 'ನಿಮ್ಮದು',
            r'\bಯಾರ್ದು(?=[^\u0C80-\u0CFF]|$)': 'ಯಾರದು'
        }
        for pr_pat, pr_rep in pr_map.items():
            if re.search(pr_pat, transformed):
                transformed = re.sub(pr_pat, pr_rep, transformed)

        # Question mark spacing & punctuation normalization
        transformed = re.sub(r"\s+\?", "?", transformed)
        transformed = re.sub(r"\s+!", "!", transformed)
        transformed = re.sub(r"\s+\.", ".", transformed)
        transformed = re.sub(r"\s{2,}", " ", transformed).strip()

        return transformed, applied_rules
