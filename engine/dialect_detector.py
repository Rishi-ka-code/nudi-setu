# -*- coding: utf-8 -*-
"""
Dialect Detector:
Identifies the regional origin of spoken Kannada sentences using
lexical fingerprints, morphological markers, and n-gram patterns.
"""

import json
import os
import re
from typing import Dict, Any, List, Tuple

class DialectDetector:
    def __init__(self, markers_path: str = None, lexicons_path: str = None):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if markers_path is None:
            markers_path = os.path.join(base_dir, "data", "regional_markers.json")
        if lexicons_path is None:
            lexicons_path = os.path.join(base_dir, "data", "dialect_lexicons.json")

        self.markers = {}
        self.lexicons = {}

        if os.path.exists(markers_path):
            with open(markers_path, "r", encoding="utf-8") as f:
                self.markers = json.load(f)

        if os.path.exists(lexicons_path):
            with open(lexicons_path, "r", encoding="utf-8") as f:
                self.lexicons = json.load(f)

        self.region_keywords = self.markers.get("region_detection_keywords", {})
        
        # Load trained ML model if available
        self.ml_model = None
        model_path = os.path.join(base_dir, "models", "dialect_classifier.joblib")
        if os.path.exists(model_path):
            try:
                import joblib
                self.ml_model = joblib.load(model_path)
            except Exception:
                self.ml_model = None

    def predict_ml(self, text: str):
        """
        Uses trained character n-gram ML pipeline to predict dialect probabilities.
        """
        if self.ml_model is not None and text and text.strip():
            try:
                probs = self.ml_model.predict_proba([text.strip()])[0]
                classes = self.ml_model.classes_
                prob_dict = {cls: round(float(p), 3) for cls, p in zip(classes, probs)}
                top_idx = int(probs.argmax())
                return {
                    "top_dialect": classes[top_idx],
                    "confidence": round(float(probs[top_idx]), 3),
                    "distribution": prob_dict
                }
            except Exception:
                return None
        return None

    def detect(self, text: str) -> Dict[str, Any]:
        """
        Detects the dialect region with confidence scores and evidence markers.
        """
        if not text or not text.strip():
            return {
                "detected_region": "Unknown",
                "region_name_kn": "ಅಜ್ಞಾತ",
                "confidence": 0.0,
                "scores": {},
                "detected_markers": []
            }

        cleaned = text.strip()
        tokens = re.findall(r"[\u0C80-\u0CFF]+", cleaned)

        # Initialize scores dynamically from registered regions
        scores: Dict[str, float] = {region: 0.0 for region in self.region_keywords.keys()}
        if not scores:
            scores = {
                "North Karnataka": 0.0,
                "Kalyana Karnataka": 0.0,
                "Coastal / Kundagannada": 0.0,
                "Uttara Kannada / Havyaka": 0.0,
                "Mysuru-Mandya": 0.0
            }

        detected_markers: List[Dict[str, str]] = []

        # 1. Exact token / phrase matching from regional keywords
        for region, kws in self.region_keywords.items():
            for kw in kws:
                if kw in cleaned:
                    weight = 2.0 if len(kw) > 4 else 1.5
                    scores[region] = scores.get(region, 0.0) + weight
                    detected_markers.append({
                        "marker": kw,
                        "region": region,
                        "type": "Key Regional Vocabulary"
                    })

        # 2. Check lexicon mappings
        for region, reg_data in self.lexicons.items():
            vocab = reg_data.get("vocabulary", {})
            for token in tokens:
                if token in vocab:
                    scores[region] = scores.get(region, 0.0) + 1.0
                    if not any(m["marker"] == token for m in detected_markers):
                        detected_markers.append({
                            "marker": token,
                            "region": region,
                            "type": "Lexical item"
                        })

        # 3. Morphological suffix patterns
        # North Karnataka continuous (-ಆಕತ್ತ-)
        if re.search(r"([ಕ-ಹ]+)ಾಕತ್ತ(ಾನ|ಾಳ|ಾರ|ೀನಿ|ೈತಿ)(?=[^\u0C80-\u0CFF]|$)", cleaned):
            scores["North Karnataka"] = scores.get("North Karnataka", 0.0) + 3.5
            match = re.search(r"([ಕ-ಹ]+)ಾಕತ್ತ(ಾನ|ಾಳ|ಾರ|ೀನಿ|ೈತಿ)(?=[^\u0C80-\u0CFF]|$)", cleaned).group(0)
            detected_markers.append({
                "marker": match,
                "region": "North Karnataka",
                "type": "Morphological Continuous Suffix (-ಆಕತ್ತ-)"
            })

        # Kalyana Karnataka continuous (-ಲಿಕ್ಕತ್ತ-)
        if re.search(r"([ಕ-ಹ]+)ಲಿಕ್ಕತ್ತ(ಾನ|ಾಳ|ಾರ|ೀನಿ)(?=[^\u0C80-\u0CFF]|$)", cleaned):
            scores["Kalyana Karnataka"] = scores.get("Kalyana Karnataka", 0.0) + 3.5
            match = re.search(r"([ಕ-ಹ]+)ಲಿಕ್ಕತ್ತ(ಾನ|ಾಳ|ಾರ|ೀನಿ)(?=[^\u0C80-\u0CFF]|$)", cleaned).group(0)
            detected_markers.append({
                "marker": match,
                "region": "Kalyana Karnataka",
                "type": "Morphological Continuous Suffix (-ಲಿಕ್ಕತ್ತ-)"
            })

        # North Karnataka clitic (-ಏನ್ರಿ, -ಇಲ್ರಿ, -ಐತ್ರಿ)
        if re.search(r"([ಕ-ಹ]+)(ಏನ್ರಿ|ಿಲ್ರಿ|ೈತ್ರಿ)(?=[^\u0C80-\u0CFF]|$)", cleaned):
            scores["North Karnataka"] = scores.get("North Karnataka", 0.0) + 2.5

        # Coastal Kundagannada vocative ಮಾರೆ / verb ending -ಪೆ
        if "ಮಾರೆ" in cleaned or "ಮಾರ್ರೆ" in cleaned:
            scores["Coastal / Kundagannada"] = scores.get("Coastal / Kundagannada", 0.0) + 3.5
        if re.search(r"([ಕ-ಹ]+)ರ್ಪೆ(?=[^\u0C80-\u0CFF]|$)", cleaned):
            scores["Coastal / Kundagannada"] = scores.get("Coastal / Kundagannada", 0.0) + 3.0

        # Havyaka nasal pronouns (ನಾಂ, ನೀಂ, ಅವಂ)
        if re.search(r"(?:^|[^\u0C80-\u0CFF])(ನಾಂ|ನೀಂ|ಅವಂ|ಅವಳ್)(?=[^\u0C80-\u0CFF]|$)", cleaned):
            scores["Uttara Kannada / Havyaka"] = scores.get("Uttara Kannada / Havyaka", 0.0) + 3.5

        # South Karnataka discourse clitic (ಕಣಯ್ಯ, ಕಣ್ರೀ, ಕಣೋ)
        if re.search(r"(?:^|[^\u0C80-\u0CFF])(ಕಣಯ್ಯ|ಕಣ್ರೀ|ಕಣೋ|ಕಣೇ)(?=[^\u0C80-\u0CFF]|$)", cleaned):
            scores["Mysuru-Mandya"] = scores.get("Mysuru-Mandya", 0.0) + 3.0

        # Calculate confidence
        total_score = sum(scores.values())
        if total_score == 0:
            return {
                "detected_region": "General / Colloquial Kannada",
                "region_name_kn": "ಸಾಮಾನ್ಯ ಆಡುಮಾತು",
                "confidence": 0.50,
                "scores": {k: round(1.0 / len(scores), 2) for k in scores},
                "detected_markers": []
            }

        sorted_regions = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        top_region, top_score = sorted_regions[0]
        confidence = round(min(0.98, top_score / (total_score + 1.0) + 0.35), 2)

        region_names_kn = {
            "North Karnataka": "ಉತ್ತರ ಕರ್ನಾಟಕ (ಹುಬ್ಬಳ್ಳಿ-ಧಾರವಾಡ/ಬೆಳಗಾವಿ)",
            "Kalyana Karnataka": "ಕಲ್ಯಾಣ ಕರ್ನಾಟಕ (ಕಲಬುರಗಿ/ಬೀದರ್/ರಾಯಚೂರು)",
            "Coastal / Kundagannada": "ಕರಾವಳಿ / ಕುಂದಗನ್ನಡ (ಮಂಗಳೂರು/ಉಡುಪಿ)",
            "Uttara Kannada / Havyaka": "ಉತ್ತರ ಕನ್ನಡ / ಹವ್ಯಕ (ಶಿರಸಿ/ಕಾರವಾರ)",
            "Mysuru-Mandya": "ಮೈಸೂರು-ಮಂಡ್ಯ (ದಕ್ಷಿಣ ಕರ್ನಾಟಕ)"
        }

        normalized_scores = {k: round(v / total_score, 2) for k, v in scores.items()}

        return {
            "detected_region": top_region,
            "region_name_kn": region_names_kn.get(top_region, top_region),
            "confidence": confidence,
            "scores": normalized_scores,
            "detected_markers": detected_markers
        }
