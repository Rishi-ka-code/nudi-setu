# Phase 2 — Converter Evaluation Report (Genuine Data Baseline)

**Evaluation Date**: November 2026  
**Scope**: All 315 genuine sentence pairs in `data/dataset.csv` (105 per dialect across Hubballi-Dharwad, Mangaluru, Uttara Kannada).  
**Methodology**: Tested the actual rule, morphological, and lexical conversion engine directly (bypassing full-sentence parallel corpus dictionary lookup to measure true generalizability).

---

## Executive Summary

| Dialect | Test Cases | Exact-Match Accuracy | Character Error Rate (CER) | Unchanged Outputs | Incorrect / Partial Conversions |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Hubballi-Dharwad** | 105 | **5.71%** (6 / 105) | **27.22%** | 31 (29.52%) | 68 (64.76%) |
| **Mangaluru** | 105 | **5.71%** (6 / 105) | **21.72%** | 46 (43.81%) | 53 (50.48%) |
| **Uttara Kannada** | 105 | **3.81%** (4 / 105) | **19.39%** | 59 (56.19%) | 42 (40.00%) |
| **AGGREGATE** | **315** | **5.08%** (16 / 315) | **22.77%** | **136** (43.17%) | **163** (51.75%) |

---

## Detailed Dialect Breakdowns

### 1. Hubballi-Dharwad (105 Cases)
* **Exact Match**: 6 / 105 (5.71%)
* **Average CER**: 27.22%
* **Unchanged Outputs**: 31 / 105 (29.52%) (Dialect sentences left completely un-normalized)
* **Incorrect Conversions**: 68 / 105 (64.76%)

#### 5 Representative Failure Examples:
1. **Case `HD_003`** (Morphological stem corruption):
   * **Input**: `ಅವ್ವ ಬಂದು ಅಡಿಗೆ ಮಾಡಾಕತ್ತಾಳ.`
   * **Expected**: `ತಾಯಿ ಬಂದು ಅಡುಗೆ ಮಾಡುತ್ತಿದ್ದಾಳೆ.`
   * **Actual**: `ಅವ್ವ ಬಂದು ಅಡಿಗೆ ಮಾಡುತುತ್ತಾಳೆ.`
   * **CER**: 0.290
   * **Failure Cause**: Progressive suffix `-ಆಕತ್ತಾಳ` replacement caused duplicated syllable (`ಮಾಡುತುತ್ತಾಳೆ`), and dialect noun `ಅವ್ವ` was unmapped.
2. **Case `HD_004`** (Interrogative honorific clitic):
   * **Input**: `ಊಟ ಆತೇನ್ರಿ ಎಲ್ಲಾರದೂ?`
   * **Expected**: `ಎಲ್ಲರ ಊಟವಾಯಿತೇ?`
   * **Actual**: `ಊಟ ಆಯಿತೇ ಎಲ್ಲಾರದೂ?`
   * **CER**: 1.067
   * **Failure Cause**: Word order and clitic `-ನ್ರಿ` partially resolved (`ಆತೇನ್ರಿ` ➔ `ಆಯಿತೇ`), but pronoun `ಎಲ್ಲಾರದೂ` remained un-standardized.
3. **Case `HD_005`** (Colloquial verb conjunctions):
   * **Input**: `ಏನ್ರಿ ಅಪ್ಪಾ, ಕುಂತ್ರೇನ್ ನಿಂತ್ರೇನ್ ಬರೀ ಕೆಲ್ಸಾನ.`
   * **Expected**: `ಏನಪ್ಪಾ, ಕುಳಿತರೂ ನಿಂತರೂ ಬರೀ ಕೆಲಸವೇ.`
   * **Actual**: `ಏನು ಅಪ್ಪಾ, ಕುಂತ್ರೇನ್ ನಿಂತ್ರೇನ್ ಬರೀ ಕೆಲಸವೇ.`
   * **CER**: 0.382
   * **Failure Cause**: `ಕುಂತ್ರೇನ್` / `ನಿಂತ್ರೇನ್` conditionals were unhandled.
4. **Case `HD_006`** (Kinship noun + Dative + Negation):
   * **Input**: `ನಮ್ಮಪ್ಪ ಇನ್ನು ಮನಿಗ ಬಂದಿಲ್ರಿ.`
   * **Expected**: `ನಮ್ಮ ತಂದೆ ಇನ್ನೂ ಮನೆಗೆ ಬಂದಿಲ್ಲ.`
   * **Actual**: `ನಮ್ಮಪ್ಪ ಇನ್ನು ಮನಿಗ ಬಂದಿಲ್ರಿ.` (Completely unchanged)
   * **CER**: 0.333
   * **Failure Cause**: Kinship noun `ನಮ್ಮಪ್ಪ`, dative `ಮನಿಗ`, and negative clitic `ಬಂದಿಲ್ರಿ` lacked rules.
5. **Case `HD_007`** (Adverb + Verb honorific imperative):
   * **Input**: `ಬಿಸಿ ಬಿಸಿ ಚಾ ಕುಡೀರಿ ಮೊದ್ಲು.`
   * **Expected**: `ಮೊದಲು ಬಿಸಿ ಬಿಸಿಯಾದ ಚಹಾ ಕುಡಿಯಿರಿ.`
   * **Actual**: `ಬಿಸಿ ಬಿಸಿ ಚಹಾ ಕುಡೀರಿ ಮೊದ್ಲು.`
   * **CER**: 0.562
   * **Failure Cause**: `ಮೊದ್ಲು` ➔ `ಮೊದಲು` and imperative `ಕುಡೀರಿ` ➔ `ಕುಡಿಯಿರಿ` were unhandled.

---

### 2. Mangaluru / Coastal Kundagannada (105 Cases)
* **Exact Match**: 6 / 105 (5.71%)
* **Average CER**: 21.72%
* **Unchanged Outputs**: 46 / 105 (43.81%) (Nearly half of all coastal sentences left unconverted!)
* **Incorrect Conversions**: 53 / 105 (50.48%)

#### 5 Representative Failure Examples:
1. **Case `CO_001`** (Coastal auxiliary continuous):
   * **Input**: `ಎಂತ ಮಾಡ್ತಾ ಇದ್ದೀರಿ?`
   * **Expected**: `ಏನು ಮಾಡುತ್ತಿದ್ದೀರಿ?`
   * **Actual**: `ಏನು ಮಾಡ್ತಾ ಇದ್ದೀರಿ?`
   * **CER**: 0.211
   * **Failure Cause**: Interrogative `ಎಂತ` converted to `ಏನು`, but continuous verb `ಮಾಡ್ತಾ ಇದ್ದೀರಿ` was not standardized to `ಮಾಡುತ್ತಿದ್ದೀರಿ`.
2. **Case `CO_002`** (Interrogative tag clitic `-ನಾ?`):
   * **Input**: `ಎಂತ ಮಾರೆ, ಇವತ್ತು ಶಾಲೆಗ್ ರಜಾನಾ?`
   * **Expected**: `ಏನು ಗೆಳೆಯ, ಇಂದು ಶಾಲೆಗೆ ರಜೆಯೇ?`
   * **Actual**: `ಏನು ಗೆಳೆಯ, ಇಂದು ಶಾಲೆಗೆ ರಜಾನಾ?`
   * **CER**: 0.103
   * **Failure Cause**: Clitic `-ನಾ?` on noun `ರಜಾ` remained unconverted.
3. **Case `CO_004`** (Coastal past negative tag `-ಲ್ವಾ`):
   * **Input**: `ಅದ್ಕೆ ನಾನ್ ಹೇಳ್ದೆ ಕೇಳಿಲ್ವಾ ನೀನು?`
   * **Expected**: `ಅದಕ್ಕೆ ನಾನು ಹೇಳಿದೆ, ನೀನು ಕೇಳಿಸಿಕೊಳ್ಳಲಿಲ್ಲವೇ?`
   * **Actual**: `ಅದಕ್ಕೆ ನಾನು ಹೇಳಿದೆ ಕೇಳಿಲ್ವಾ ನೀನು?`
   * **CER**: 0.432
   * **Failure Cause**: Coastal negative tag `ಕೇಳಿಲ್ವಾ` left unconverted.
4. **Case `CO_005`** (Standard word corruption bug `್ಲಿ` ➔ `ಲಲಿ`):
   * **Input**: `ಮನೆಲ್ ಎಲ್ಲರೂ ಆರಾಮ್ದಲ್ಲಿ ಇದ್ದಾರಾ?`
   * **Expected**: `ಮನೆಯಲ್ಲಿ ಎಲ್ಲರೂ ಕ್ಷೇಮವಾಗಿದ್ದಾರೆಯೇ?`
   * **Actual**: `ಮನೆಯಲಲಿ ಎಲ್ಲರೂ ಕ್ಷೇಮವಾಗಿ ಇದ್ದಾರಾ?`
   * **CER**: 0.176
   * **Failure Cause**: `ಮನೆಲ್` was replaced with `ಮನೆಯಲ್ಲಿ`, but an over-eager morphological regex corrupted `ಲ್ಲಿ` into `ಲಲಿ` (`ಮನೆಯಲಲಿ`).
5. **Case `CO_006`** (Coastal kinship noun):
   * **Input**: `ಅಪ್ಪೆ ಇನ್ನು ಅಡಿಗೆ ಮಾಡ್ತಾ ಇದ್ದಾರೆ.`
   * **Expected**: `ಅಮ್ಮ ಇನ್ನೂ ಅಡುಗೆ ಮಾಡುತ್ತಿದ್ದಾರೆ.`
   * **Actual**: `ಅಪ್ಪೆ ಇನ್ನು ಅಡಿಗೆ ಮಾಡ್ತಾ ಇದ್ದಾರೆ.` (Completely unchanged)
   * **CER**: 0.281
   * **Failure Cause**: Coastal mother term `ಅಪ್ಪೆ` not in lexicon.

---

### 3. Uttara Kannada / Havyaka (105 Cases)
* **Exact Match**: 4 / 105 (3.81%)
* **Average CER**: 19.39%
* **Unchanged Outputs**: 59 / 105 (56.19%) (Over 56% of sentences completely unchanged!)
* **Incorrect Conversions**: 42 / 105 (40.00%)

#### 5 Representative Failure Examples:
1. **Case `UK_001`** (Dialect question word):
   * **Input**: `ಹೆಂಗಿದ್ದೀರಿ, ಊಟಕ್ಕೆ ಬರ್ತೀರಾ?`
   * **Expected**: `ಹೇಗಿದ್ದೀರಿ, ಊಟಕ್ಕೆ ಬರುತ್ತೀರಾ?`
   * **Actual**: `ಹೆಂಗಿದ್ದೀರಿ, ಊಟಕ್ಕೆ ಬರುತ್ತೀರಾ?`
   * **CER**: 0.069
   * **Failure Cause**: `ಹೆಂಗಿದ್ದೀರಿ` ➔ `ಹೇಗಿದ್ದೀರಿ` was missing in UK lexicon.
2. **Case `UK_002`** (Havyaka 1st person future `-ತೆ` + `್ಲಿ` bug):
   * **Input**: `ನಾಳೆ ನಾನಲ್ಲಿ ಬತ್ತೆ ಹೌದಾ?`
   * **Expected**: `ನಾಳೆ ನಾನಲ್ಲಿಗೆ ಬರುತ್ತೇನೆ ಸರಿನಾ?`
   * **Actual**: `ನಾಳೆ ನಾನಲಲಿ ಬರುತ್ತೇನೆ ಹೌದು?`
   * **CER**: 0.258
   * **Failure Cause**: Standard locative `ನಾನಲ್ಲಿ` corrupted to `ನಾನಲಲಿ` by regex rule.
3. **Case `UK_004`** (Havyaka colloquial verb & quantifier):
   * **Input**: `ಅಲ್ಲಿ ಕೂಡು, ಚೂರು ಕಷಾಯ ಕುಡಿಯುವಾ.`
   * **Expected**: `ಅಲ್ಲಿ ಕುಳಿತುಕೊ, ಸ್ವಲ್ಪ ಕಷಾಯ ಕುಡಿಯೋಣ.`
   * **Actual**: `ಅಲಲಿ ಕೂಡು, ಚೂರು ಕಷಾಯ ಕುಡಿಯುವಾ.`
   * **CER**: 0.444
   * **Failure Cause**: `ಕೂಡು` (sit) and `ಚೂರು` (a little) were untouched; `ಅಲ್ಲಿ` corrupted to `ಅಲಲಿ`.
4. **Case `UK_005`** (Havyaka kinship + speech connector):
   * **Input**: `ಅಪ್ಪಯ್ಯ ತೋಟಕ್ಕೆ ಹೋಗಿ ಬತ್ತೆ ಅಂದ್ರು.`
   * **Expected**: `ತಂದೆ ತೋಟಕ್ಕೆ ಹೋಗಿ ಬರುತ್ತೇನೆ ಎಂದರು.`
   * **Actual**: `ಅಪ್ಪಯ್ಯ ತೋಟಕ್ಕೆ ಹೋಗಿ ಬರುತ್ತೇನೆ ಅಂದ್ರು.`
   * **CER**: 0.265
   * **Failure Cause**: `ಅಪ್ಪಯ್ಯ` and `ಅಂದ್ರು` left unmapped.
5. **Case `UK_007`** (Havyaka habitual verb `-ವುತ್ತೆ`):
   * **Input**: `ಅಜ್ಜಿ ಕತೆ ಹೇಳುತ್ತೆ ಕೇಳಿ.`
   * **Expected**: `ಅಜ್ಜಿ ಕಥೆ ಹೇಳುತ್ತಾರೆ ಕೇಳಿ.`
   * **Actual**: `ಅಜ್ಜಿ ಕತೆ ಹೇಳುತ್ತೆ ಕೇಳಿ.` (Completely unchanged)
   * **CER**: 0.160
   * **Failure Cause**: Havyaka neuter honorific `-ವುತ್ತೆ` / `-ಉತ್ತೆ` not in morph analyzer.

---

## Root Cause Diagnostics

1. **Missing Glossary Integration**:
   `data/glossary.csv` contains 130 verified mappings (45 HD, 45 Mangaluru, 40 UK), but was **never loaded by the engine**. Only the smaller `dialect_lexicons.json` was used.
2. **Morphological Imbalance**:
   The engine only possessed verb rules for Hubballi-Dharwad. Mangaluru `-ಪೆ/-ಪ/-ಪೊ/-ಲ್ವಾ` and Uttara Kannada `-ವುತ್ತೆ/-ತಕ್ಕು/-ತೆ` were completely omitted from the code.
3. **Regressive Regex In `morph_analyzer.py`**:
   The permissive rule `r'([\u0C80-\u0CFF]+?)್ಲಿ'` was incorrectly matching the standard Kannada locative suffix `ಲ್ಲಿ` in words like `ಅಲ್ಲಿ`, `ಇಲ್ಲಿ`, and `ಮನೆಯಲ್ಲಿ`, converting them into broken `ಅಲಲಿ`, `ಇಲಲಿ`, and `ಮನೆಯಲಲಿ`.
4. **Hardcoded Cross-Dialect Generator**:
   `dialect_generator.py` only had 15 static words per dialect, making it unable to transform sentences dynamically.
