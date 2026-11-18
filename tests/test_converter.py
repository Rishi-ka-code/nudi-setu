# -*- coding: utf-8 -*-
"""
Unit tests for Kannada Dialect Converter:
- Canonical Prompt Example (ಅವನು ಬರ್ತಾನಾ? -> ಅವನು ಬರುತ್ತಾನೆಯೇ?)
- North Karnataka Progressive & Clitic Tests
- Kalyana Karnataka Tests
- Coastal Kundagannada Tests
- Unseen Sentence Generalization (Modals, Perfectives)
- Dialect Classification across 5 regions
- Full Parallel Corpus Batch Evaluation
"""

import sys
import os

# Add parent dir to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engine.normalizer import DialectNormalizer
from engine.dialect_detector import DialectDetector

def test_prompt_canonical_example():
    normalizer = DialectNormalizer()
    res = normalizer.normalize("ಅವನು ಬರ್ತಾನಾ?")
    print(f"\n[Test Canonical] Input: ಅವನು ಬರ್ತಾನಾ? -> Output: {res['standard_text']}")
    assert "ಬರುತ್ತಾನೆಯೇ" in res["standard_text"], f"Expected ಬರುತ್ತಾನೆಯೇ, got {res['standard_text']}"
    print("PASS: Prompt canonical transformation passed!")

def test_north_karnataka_progressive():
    normalizer = DialectNormalizer()
    res = normalizer.normalize("ಅವನು ಇವ್ವತ್ ಬರಾಕತ್ತಾನ.")
    print(f"\n[Test NK] Input: ಅವನು ಇವ್ವತ್ ಬರಾಕತ್ತಾನ. -> Output: {res['standard_text']}")
    assert "ಬರುತ್ತಿದ್ದಾನೆ" in res["standard_text"], f"Expected ಬರುತ್ತಿದ್ದಾನೆ, got {res['standard_text']}"
    assert "ಇಂದು" in res["standard_text"], f"Expected ಇಂದು, got {res['standard_text']}"
    print("PASS: North Karnataka transformation passed!")

def test_kalyana_karnataka():
    normalizer = DialectNormalizer()
    res = normalizer.normalize("ಅವನು ಸಾಲಿಗೆ ಹೋಗಲಿಕ್ಕತ್ತಾನ.")
    print(f"\n[Test KK] Input: ಅವನು ಸಾಲಿಗೆ ಹೋಗಲಿಕ್ಕತ್ತಾನ. -> Output: {res['standard_text']}")
    assert "ಹೋಗುತ್ತಿದ್ದಾನೆ" in res["standard_text"], f"Expected ಹೋಗುತ್ತಿದ್ದಾನೆ, got {res['standard_text']}"
    assert "ಶಾಲೆಗೆ" in res["standard_text"], f"Expected ಶಾಲೆಗೆ, got {res['standard_text']}"

    res2 = normalizer.normalize("ದೋಸ್ತ್, ನನಗ ಸ್ವಲ್ಪ ರೊಕ್ಕ ಕೊಡತಿಯಾ?")
    print(f"[Test KK Loanwords] Input: ದೋಸ್ತ್, ರೊಕ್ಕ -> Output: {res2['standard_text']}")
    assert "ಗೆಳೆಯ" in res2["standard_text"], f"Expected ಗೆಳೆಯ, got {res2['standard_text']}"
    assert "ಹಣ" in res2["standard_text"], f"Expected ಹಣ, got {res2['standard_text']}"
    print("PASS: Kalyana Karnataka transformation passed!")

def test_coastal_kundagannada():
    normalizer = DialectNormalizer()
    res = normalizer.normalize("ಎಂತ ಮಾರೆ, ಇವತ್ತು ಶಾಲೆಗ್ ರಜಾನಾ?")
    print(f"\n[Test Coastal] Input: ಎಂತ ಮಾರೆ -> Output: {res['standard_text']}")
    assert "ಗೆಳೆಯ" in res["standard_text"] or "ಏನು" in res["standard_text"], f"Unexpected output: {res['standard_text']}"
    print("PASS: Coastal transformation passed!")

def test_unseen_modal_contractions():
    normalizer = DialectNormalizer()
    # Test novel sentence not in corpus
    res1 = normalizer.normalize("ಅವನು ನಾಳೆ ಊರಿಗೆ ಹೋಗ್ಬೇಕು")
    print(f"\n[Test Unseen Modal] Input: ಅವನು ನಾಳೆ ಊರಿಗೆ ಹೋಗ್ಬೇಕು -> Output: {res1['standard_text']}")
    assert res1["standard_text"] == "ಅವನು ನಾಳೆ ಊರಿಗೆ ಹೋಗಬೇಕು", f"Expected ಹೋಗಬೇಕು, got {res1['standard_text']}"

    res2 = normalizer.normalize("ನೀನು ಆ ಕೆಲಸ ಮಾಡ್ಬಾರ್ದು")
    print(f"[Test Unseen Prohibitive] Input: ನೀನು ಆ ಕೆಲಸ ಮಾಡ್ಬಾರ್ದು -> Output: {res2['standard_text']}")
    assert res2["standard_text"] == "ನೀನು ಆ ಕೆಲಸ ಮಾಡಬಾರದು", f"Expected ಮಾಡಬಾರದು, got {res2['standard_text']}"
    print("PASS: Unseen modal contractions passed!")

def test_unseen_perfective_suffixes():
    normalizer = DialectNormalizer()
    # Test novel perfective sentences
    res1 = normalizer.normalize("ಅವನು ಗ್ರಾಮಕ್ಕೆ ಬಂದ್ಯಾನ")
    print(f"\n[Test Unseen Perfective 3rd Masc] Input: ಅವನು ಗ್ರಾಮಕ್ಕೆ ಬಂದ್ಯಾನ -> Output: {res1['standard_text']}")
    assert "ಬಂದಿದ್ದಾನೆ" in res1["standard_text"], f"Expected ಬಂದಿದ್ದಾನೆ, got {res1['standard_text']}"

    res2 = normalizer.normalize("ನಾನು ಊಟ ಮಾಡೀನಿ")
    print(f"[Test Unseen Perfective 1st Person] Input: ನಾನು ಊಟ ಮಾಡೀನಿ -> Output: {res2['standard_text']}")
    assert "ಮಾಡಿದ್ದೇನೆ" in res2["standard_text"], f"Expected ಮಾಡಿದ್ದೇನೆ, got {res2['standard_text']}"
    print("PASS: Unseen perfective suffixes passed!")

def test_user_reported_variations():
    normalizer = DialectNormalizer()
    # The exact case the user showed in Image 1
    res1 = normalizer.normalize("ಅವನು ಬರ್ತಾನ")
    print(f"\n[Test User Reported Case 1] Input: ಅವನು ಬರ್ತಾನ -> Output: {res1['standard_text']}")
    assert res1["standard_text"] == "ಅವನು ಬರುತ್ತಾನೆ", f"Expected ಅವನು ಬರುತ್ತಾನೆ, got {res1['standard_text']}"

    # Phonetic metathesis keyboard spelling (ಬತಾರ್ನ)
    res_meta = normalizer.normalize("ಅವನು ಬತಾರ್ನ")
    print(f"[Test User Reported Metathesis] Input: ಅವನು ಬತಾರ್ನ -> Output: {res_meta['standard_text']}")
    assert res_meta["standard_text"] == "ಅವನು ಬರುತ್ತಾನೆ", f"Expected ಅವನು ಬರುತ್ತಾನೆ, got {res_meta['standard_text']}"

    # Question variant with ?
    res2 = normalizer.normalize("ಅವನು ಬರ್ತಾನ?")
    print(f"[Test User Reported Case 2] Input: ಅವನು ಬರ್ತಾನ? -> Output: {res2['standard_text']}")
    assert res2["standard_text"] == "ಅವನು ಬರುತ್ತಾನೆಯೇ?", f"Expected ಅವನು ಬರುತ್ತಾನೆಯೇ?, got {res2['standard_text']}"

    # Unseen verb roots
    res3 = normalizer.normalize("ಅವನು ಮಾಡ್ತಾನ")
    assert res3["standard_text"] == "ಅವನು ಮಾಡುತ್ತಾನೆ", f"Expected ಅವನು ಮಾಡುತ್ತಾನೆ, got {res3['standard_text']}"

    res4 = normalizer.normalize("ಅವರು ಹೋಗ್ತಾರ")
    assert res4["standard_text"] == "ಅವರು ಹೋಗುತ್ತಾರೆ", f"Expected ಅವರು ಹೋಗುತ್ತಾರೆ, got {res4['standard_text']}"

    res5 = normalizer.normalize("ಅವನು ಬರಲ್ಲ")
    assert res5["standard_text"] == "ಅವನು ಬರುವುದಿಲ್ಲ", f"Expected ಅವನು ಬರುವುದಿಲ್ಲ, got {res5['standard_text']}"

    # User reported emphatic modal case: ಅವನು ಬರಲೇ
    res6 = normalizer.normalize("ಅವನು ಬರಲೇ")
    assert res6["standard_text"] == "ಅವನು ಬರಲೇಬೇಕು", f"Expected ಅವನು ಬರಲೇಬೇಕು, got {res6['standard_text']}"

    res7 = normalizer.normalize("ಅವನು ಬರಲೇ?")
    assert res7["standard_text"] == "ಅವನು ಬರಬೇಕೇ?", f"Expected ಅವನು ಬರಬೇಕೇ?, got {res7['standard_text']}"

    res8 = normalizer.normalize("ಅವನು ಬರ್ಲಿ")
    assert res8["standard_text"] == "ಅವನು ಬರಲಿ", f"Expected ಅವನು ಬರಲಿ, got {res8['standard_text']}"
    print("PASS: User reported variations & open-ended verbs passed!")

def test_dialect_detection():
    detector = DialectDetector()
    res_nk = detector.detect("ಅವನು ಇವ್ವತ್ ಬರಾಕತ್ತಾನ ನೋಡ್ರಿ")
    print(f"\n[Test Detect NK] Detected: {res_nk['detected_region']} (confidence: {res_nk['confidence']})")
    assert res_nk["detected_region"] == "North Karnataka"

    res_kk = detector.detect("ದೋಸ್ತ್, ರೊಕ್ಕ ಇಲ್ಲದೆ ಬಾಳಾ ತಕ್ಲಿಫ್ ಐತಿ")
    print(f"[Test Detect KK] Detected: {res_kk['detected_region']} (confidence: {res_kk['confidence']})")
    assert res_kk["detected_region"] == "Kalyana Karnataka"

    res_co = detector.detect("ಎಂತ ಮಾರೆ ಪೋಯಿ ಬರ್ಪೆ")
    print(f"[Test Detect Coastal] Detected: {res_co['detected_region']} (confidence: {res_co['confidence']})")
    assert res_co["detected_region"] == "Coastal / Kundagannada"
    print("PASS: Dialect detection across regions passed!")

def test_batch_corpus_evaluation():
    normalizer = DialectNormalizer()
    eval_res = normalizer.batch_evaluate()
    print(f"\n[Batch Evaluation] Total: {eval_res['total_samples']}, Exact Matches: {eval_res['exact_matches']}")
    print(f"Accuracy: {eval_res['accuracy_percentage']}%, Avg Similarity: {eval_res['average_similarity']}%")
    assert eval_res["accuracy_percentage"] >= 95.0, "Expected at least 95% accuracy on verified corpus!"
    print("PASS: Batch evaluation passed!")

def test_smart_auto_router_arbiter():
    normalizer = DialectNormalizer()
    
    # Everyday conversational sentence should stay on local engine (0ms)
    local_case = normalizer.normalize("ಅವನು ಬರ್ತಾನ", mode="local")
    should_route_local, _ = normalizer.should_route_to_ai("ಅವನು ಬರ್ತಾನ", local_case)
    print(f"\n[Test Router Local] 'ಅವನು ಬರ್ತಾನ' should route to AI: {should_route_local}")
    assert should_route_local is False, "Everyday sentence should be handled locally!"

    # Code-switching sentence should be elevated to AI
    cs_case = normalizer.normalize("ನಾಳೆ meeting ಗೆ late ಆಗಿ ಬರ್ತಾನ", mode="local")
    should_route_cs, reason_cs = normalizer.should_route_to_ai("ನಾಳೆ meeting ಗೆ late ಆಗಿ ಬರ್ತಾನ", cs_case)
    print(f"[Test Router Code-Switch] Elevated to AI: {should_route_cs} (Reason: {reason_cs})")
    assert should_route_cs is True, "Code-switching sentence must be elevated to AI!"

    # Complex multi-clause sentence should be elevated to AI
    complex_text = "ಅವನು ಊರಿಗೆ ಹೋಗಿ, ಅಲ್ಲಿಂದ ಮೈಸೂರಿಗೆ ತೆರಳಿ ನಂತರ ಸಂಜೆ ಮನೆಗೆ ಬರ್ತಾನ"
    comp_case = normalizer.normalize(complex_text, mode="local")
    should_route_comp, reason_comp = normalizer.should_route_to_ai(complex_text, comp_case)
    print(f"[Test Router Narrative] Elevated to AI: {should_route_comp} (Reason: {reason_comp})")
    assert should_route_comp is True, "Complex narrative sentence must be elevated to AI!"
    print("PASS: Smart Auto-Router Arbiter decisions passed!")

def test_kanglish_transliteration():
    normalizer = DialectNormalizer()
    res1 = normalizer.normalize("avanu bartana")
    print(f"\n[Test Kanglish 1] 'avanu bartana' -> {res1['standard_text']}")
    assert res1["standard_text"] == "ಅವನು ಬರುತ್ತಾನೆ"

    res2 = normalizer.normalize("avanu baralla")
    print(f"[Test Kanglish 2] 'avanu baralla' -> {res2['standard_text']}")
    assert res2["standard_text"] == "ಅವನು ಬರುವುದಿಲ್ಲ"

    res3 = normalizer.normalize("naale hogbeku")
    print(f"[Test Kanglish 3] 'naale hogbeku' -> {res3['standard_text']}")
    assert res3["standard_text"] == "ನಾಳೆ ಹೋಗಬೇಕು"
    print("PASS: Kanglish transliteration passed!")

if __name__ == "__main__":
    test_prompt_canonical_example()
    test_north_karnataka_progressive()
    test_kalyana_karnataka()
    test_coastal_kundagannada()
    test_unseen_modal_contractions()
    test_unseen_perfective_suffixes()
    test_user_reported_variations()
    test_dialect_detection()
    test_batch_corpus_evaluation()
    test_smart_auto_router_arbiter()
    test_kanglish_transliteration()
    print("\nALL 11 TEST SUITES PASSED SUCCESSFULLY!")
