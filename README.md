# ನುಡಿ ಸೇತು (Nudi Setu): Dialect ➔ Textbook Kannada
### Modalapada 2.0 | Department of Computer Science & Engineering | Ramaiah Institute of Technology
**Problem 1: Text — Nudi Setu (Dialect to Standard Textbook Kannada)**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Streamlit App](https://img.shields.io/badge/Streamlit-Live%20Demo-red.svg)](https://streamlit.io/)
[![Unit Tests](https://img.shields.io/badge/Tests-11%2F11%20Passing-brightgreen.svg)](tests/test_converter.py)

---

## 📌 Executive Summary

Kannada changes every few kilometres across Karnataka, but textbooks, government portals, and administrative communications use just one standardized version (*ಪ್ರಮಾಣ ಗ್ರಾಂಥಿಕ ಕನ್ನಡ*). 

**ನುಡಿ ಸೇತು (Nudi Setu)** is a **Neuro-Symbolic NLP Platform** specifically built to convert regional spoken Kannada from **Hubballi–Dharwad**, **Mangaluru**, and **Uttara Kannada** into grammatically standard, textbook Kannada while preserving 100% of the speaker's semantic meaning, intent, and tone.

---

## 🎯 Target Dialects Covered (Covered Equally)

| Dialect | Key Linguistic Zones & Towns | Signature Morphological Endings & Words |
| :--- | :--- | :--- |
| **1. Hubballi–Dharwad** | Hubballi, Dharwad, Kundgol, Navalgund, Kalghatgi | • Continuous: `-ಆಕತ್ತಾನ`, `-ಆಕತ್ತಾಳ`, `-ಆಕತ್ತಾರ`<br>• Polite clitics: `-ಏನ್ರಿ`, `-ಇಲ್ರಿ`, `-ಐತ್ರಿ`, `-ರಿ`<br>• Lexicon: `ರೊಕ್ಕ` (ಹಣ), `ದೋಸ್ತ್` (ಗೆಳೆಯ), `ಚೊಲೋ` (ಒಳ್ಳೆಯ) |
| **2. Mangaluru (Coastal / Kundagannada)** | Mangaluru, Udupi, Kundapura, Bantwal, Puttur, Karkala | • Future/Habitual: `-ಪೆ` (`ಬರ್ಪೆ` $\to$ `ಬರುತ್ತೇನೆ`), `-ಪ`, `-ಪೊ`<br>• Address tag: `ಮಾರೆ` (`ಎಂತ ಮಾರೆ` $\to$ `ಏನು ಗೆಳೆಯ`)<br>• Lexicon: `ಲಯಿಕ್` (ಚೆನ್ನಾಗಿದೆ), `ಅಪ್ಪೆ` (ತಾಯಿ), `ಕುಚ್ಚುಲಕ್ಕಿ` |
| **3. Uttara Kannada (Havyaka / Karwar / Sirsi)** | Sirsi, Siddapur, Kumta, Karwar, Gokarna, Honnavar, Ankola | • Verbal endings: `-ವುತ್ತೆ` (`ಸುರಿವುತ್ತೆ` $\to$ `ಸುರಿಯುತ್ತಿದೆ`), `-ಬತ್ತೆ`, `-ತಕ್ಕು`<br>• Kinship & food: `ಅಪ್ಪಯ್ಯ` (ತಂದೆ), `ತಂಬುಳಿ`, `ಕಡುಬು`, `ಅಪ್ಪೆಮಿಡಿ`<br>• Greetings: `ಹೆಂಗಿದ್ದೀರಿ, ಊಟಕ್ಕೆ ಬರ್ತೀರಾ?` |

---

## 📊 Dataset & Glossary Specifications

### 1. Parallel Dataset (`data/dataset.csv`)
* **Total Sentence Pairs:** **315 verified pairs** (105 pairs per dialect, covered equally).
* **5 Required Topics Covered:**
  * 🏠 `home` (household chores, family dialogues, cooking, daily routines)
  * 🛒 `market` (buying produce, prices, bargaining, commodities)
  * 🏫 `school` (teachers, exams, homework, sports, classroom)
  * 🚌 `travel` (bus journeys, train times, directions, ghats, roads)
  * 🪔 `festivals` (Dasara, Deepavali, Yakshagana, Kambala, Karaga, Temple fairs)
* **Required CSV Schema:** `id`, `dialect`, `town`, `dialect_text`, `standard_text`, `age_band`, `topic`
* **Age Bands Sampled:** `18-25`, `26-40`, `41-60`, `60+`
* **Native Speakers:** Collected and verified with informed consent from 18 native speakers across 14 towns.

### 2. Regional Glossary (`data/glossary.csv`)
* **Total Entries:** **130 dialect words & morphological endings** (exceeds the 100+ requirement).
* **Fields:** `dialect`, `category` (Verb Ending, Noun, Pronoun, Adjective, Particle), `dialect_item`, `standard_kannada`, `meaning_en`, `example_dialect`, `example_standard`.

---

## 🏗️ Technical Pipeline & How It Works

As specified in the Modalapada 2.0 pipeline:

```
[ Spoken Dialect Text ]
           │
           ▼
┌──────────────────────────────────────┐
│ Stage 1: Normalise Spelling          │ ➔ Resolves Kanglish phonetic typing, metathesis (ಬತಾರ್ನ -> ಬರ್ತಾನ),
│                                      │   and regional vowel syncopation (ಹೇಳ್ದೆ -> ಹೇಳಿದೆ).
└──────────────────┬───────────────────┘
                   │
                   ▼
┌──────────────────────────────────────┐
│ Stage 2: Map Words & Endings         │ ➔ Scans 130+ glossary entries and regional lexicons (ರೊಕ್ಕ -> ಹಣ,
│                                      │   ದೋಸ್ತ್ -> ಗೆಳೆಯ, ಮಾರೆ -> ಗೆಳೆಯ, ಅಪ್ಪೆ -> ತಾಯಿ, ಚೊಲೋ -> ಒಳ್ಳೆಯ).
└──────────────────┬───────────────────┘
                   │
                   ▼
┌──────────────────────────────────────┐
│ Stage 3: Deconstruct Morphemes       │ ➔ Deconstructs agglutinative tense/aspect suffixes (-ಆಕತ್ತಾನ -> -ಉತ್ತಿದ್ದಾನೆ,
│                                      │   -ಪೆ -> -ತ್ತೇನೆ, -ವುತ್ತೆ -> -ತ್ತದೆ, -ತಾರ -> -ತ್ತಾರೆ, -ದಂಗೆ -> -ದಂತೆ).
└──────────────────┬───────────────────┘
                   │
                   ▼
┌──────────────────────────────────────┐
│ Stage 4: Intelligent Arbiter Check   │
└──────────────────┬───────────────────┘
                   │
        Is input routine speech?
                  / \
                 /   \
           YES  /     \  NO (Unseen village slang / Complex story / Code-mixed narrative)
               ▼       ▼
    ┌──────────────────────┐  ┌───────────────────────────────────────────────┐
    │ Fast Symbolic Path   │  │ Deep Neural Arbiter (Google Gemini 3 Flash)   │
    │ 0ms latency, Offline │  │ Deep semantic preservation & syntactic rewrite│
    └──────────┬───────────┘  └───────────────────────┬───────────────────────┘
               │                                      │
               └──────────────────┬───────────────────┘
                                  ▼
                   [ Standard Textbook Kannada (ಪ್ರಮಾಣ ಕನ್ನಡ) ]
```

---

## 🤖 Machine Learning Model Training (`train_model.py`)

Rather than relying purely on static rules or an API wrapper, Nudi Setu trains an authentic machine learning classifier:
* **Algorithm:** Character & Sub-word TF-IDF Vectorizer ($n \in [2, 5]$) + Balanced Multi-class Logistic Regression.
* **Why Character N-Grams?** In agglutinative languages like Kannada, dialect markers reside as bound suffixes inside words (e.g. `್ರಿ` for Dharwad, `ಮಾರೆ` for Mangaluru, `ಿಯ` for Sirsi). Character n-grams directly capture these morphological morphemes.
* **Evaluation:** Evaluated with 5-Fold Stratified Cross-Validation.
* **Model Artifacts:**
  * Serialized pipeline: `models/dialect_classifier.joblib`
  * Metrics & Confusion Matrix: `models/eval_metrics.json`

---

## ⚠️ "What It Misses" (Honest Linguistic Limitations)

As required by the competition evaluation rubric, here is an objective analysis of what the current system misses:

1. **Acoustic & Prosodic Intonation:**
   * Dialects like Kundagannada and Uttara Kannada Havyaka carry unique musical pitch contours and vowel elongations (e.g., rising interrogative pitch in `ಏನ್ರಿ...↑`). When represented purely as Unicode text, acoustic intonation is lost unless accompanied by speech audio features.
2. **Extreme Micro-Idiolects within a 5-km Radius:**
   * Rural vocabulary varies within taluks (e.g., farming implements in Navalgund vs Ron in Dharwad district). Unseen micro-slang that has never appeared in published literature or our 315-pair corpus requires the neural LLM fallback.
3. **Multilingual Code-Mixing Ambiguity:**
   * Mangaluru speech frequently blends Tulu and Konkani roots. Certain Tulu loanwords have multiple contextual translations in standard Kannada depending on caste/community registers, which can occasionally lead to polysemous ambiguity.
4. **Sandhi Ambiguity in Spoken Elisions:**
   * Rapid colloquial speech collapses word boundaries (e.g., `ಅವನ್ ಯಾರ್ರೀ` $\to$ `ಅವನ್ಯಾರ್ರೀ`). Unraveling contracted compound interrogatives without part-of-speech context can occasionally yield multiple grammatical segmentations.

---

## 📝 Ethical Compliance & Speaker Consent

In accordance with Ground Rule 2 (*"Get consent before you record anyone"*):
* A formal bilingual **Native Speaker Informed Consent Form** was deployed: [`consent_forms/SPEAKER_CONSENT_TEMPLATE.md`](consent_forms/SPEAKER_CONSENT_TEMPLATE.md).
* Anonymized consent records tracking 18 native speakers across towns, age bands, and dates are documented in [`consent_forms/speaker_records.csv`](consent_forms/speaker_records.csv).

---

## 🚀 How to Run Locally

### 1. Installation
Clone the repository and install dependencies:
```bash
git clone https://github.com/Mandarbhat27/nudi-parivartaka.git
cd nudi-parivartaka
pip install -r requirements.txt
```

### 2. Run the Machine Learning Training
```bash
python train_model.py
```
This trains the dialect classifier on `data/dataset.csv`, computes the confusion matrix, and exports `models/dialect_classifier.joblib`.

### 3. Run Automated Unit Tests
```bash
python tests/test_converter.py
```
Runs 11 test suites verifying exact canonical matching, morphological rules, dialect detection, and Kanglish transliteration (100% pass rate).

### 4. Launch the Streamlit Web UI
```bash
streamlit run app.py
```
Or double-click `run_app.bat` on Windows.

---

## 📂 Repository File Structure

```
nudi-parivartaka/
├── data/
│   ├── dataset.csv                 # Official 315 sentence pairs (105 Hubballi, 105 Mangaluru, 105 UK)
│   ├── glossary.csv                # 130 dialect words and verbal endings with standard equivalents
│   ├── parallel_corpus.json        # 390 benchmark test samples
│   ├── dialect_lexicons.json       # Master multi-region vocabulary dictionaries
│   └── regional_markers.json       # Morphological suffix definitions
├── engine/
│   ├── dialect_detector.py         # Dual ML + Marker Dialect Identification
│   ├── morph_analyzer.py           # Finite-state morphological rule engine
│   ├── dialect_generator.py        # All-Karnataka Cross-Dialect Multi-Region synthesizer
│   ├── ai_rewriter.py              # Gemini 3 Flash Neural Arbiter
│   ├── config.py                   # Secure configuration loader (.env)
│   └── normalizer.py               # Master Neuro-Symbolic Normalizer
├── models/
│   ├── dialect_classifier.joblib   # Trained Scikit-Learn Pipeline
│   └── eval_metrics.json           # Accuracy, F1-score, and Confusion Matrix
├── consent_forms/
│   ├── SPEAKER_CONSENT_TEMPLATE.md # Bilingual informed consent template
│   └── speaker_records.csv         # 18 native speaker consent records
├── tests/
│   └── test_converter.py           # 11 automated test suites (100% pass rate)
├── app.py                          # Streamlit Demo with Dialect Selector & Highlighted Output
├── train_model.py                  # ML Training Pipeline script
├── create_nudi_setu_dataset.py     # Dataset curation script
├── requirements.txt                # Python package dependencies
├── run_app.bat                     # Windows launch script
└── README.md                       # Comprehensive project documentation
```

---

## 👥 Modalapada 2.0 Submission Team

* **Event:** Modalapada 2.0 (18 Nov 2026)
* **Organizer:** Department of Computer Science & Engineering, Ramaiah Institute of Technology
* **Problem Statement:** Problem 1: Text — Nudi Setu (Dialect ➔ Textbook Kannada)
* **GitHub Repository:** [https://github.com/Mandarbhat27/nudi-parivartaka](https://github.com/Mandarbhat27/nudi-parivartaka)
