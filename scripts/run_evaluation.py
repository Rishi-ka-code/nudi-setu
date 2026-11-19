# -*- coding: utf-8 -*-
"""
Full Evaluation Runner for Stage 2
Evaluates the updated DialectNormalizer against all 315 sentence pairs in data/dataset.csv
and evaluates 10 novel unseen sentences per dialect.
"""

import os
import sys
sys.path.insert(0, os.getcwd())
import pandas as pd
import json

from engine.normalizer import DialectNormalizer

def levenshtein(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])
    return dp[m][n]

def calculate_cer(ref, hyp):
    if not ref:
        return 0.0 if not hyp else 1.0
    return levenshtein(ref, hyp) / len(ref)

def evaluate_315_dataset():
    df = pd.read_csv('data/dataset.csv')
    normalizer = DialectNormalizer()

    results = []
    for idx, row in df.iterrows():
        spoken = row['dialect_text'].strip()
        expected = row['standard_text'].strip()
        dialect = row['dialect'].strip()
        town = row.get('town', '')
        category = row.get('category', '')

        # Pass target_region explicitly as requested: "Use the correct manually selected dialect"
        # Pass bypass_corpus=True to test the genuine rule & vocabulary engine without parallel_corpus shortcuts
        norm_res = normalizer.normalize(spoken, target_region=dialect, mode='local', bypass_corpus=True)
        actual = norm_res['standard_text']

        is_exact = (actual == expected)
        cer = calculate_cer(expected, actual)
        is_unchanged = (actual == spoken)
        should_be_unchanged = (spoken == expected)

        results.append({
            'index': idx,
            'dialect': dialect,
            'town': town,
            'category': category,
            'input': spoken,
            'expected': expected,
            'actual': actual,
            'is_exact': is_exact,
            'is_unchanged': is_unchanged,
            'should_be_unchanged': should_be_unchanged,
            'cer': cer,
            'transformations': norm_res.get('transformations', []),
            'rules': [r.get('description', '') for r in norm_res.get('rules_applied', [])]
        })

    rdf = pd.DataFrame(results)

    # Save detailed CSV
    os.makedirs('reports', exist_ok=True)
    rdf.to_csv('reports/stage2_evaluation_details.csv', index=False, encoding='utf-8')

    print("=" * 60)
    print("STAGE 2: EVALUATION ON ALL 315 DATASET SENTENCE PAIRS")
    print("=" * 60)

    summary = {}
    for d in ['Hubballi-Dharwad', 'Mangaluru', 'Uttara Kannada']:
        sub = rdf[rdf['dialect'] == d]
        total = len(sub)
        exact = int(sub['is_exact'].sum())
        mean_cer = float(sub['cer'].mean())
        unchanged = int(sub['is_unchanged'].sum())
        legit_unchanged = int((sub['is_unchanged'] & sub['should_be_unchanged']).sum())
        unwanted_unchanged = unchanged - legit_unchanged

        # Failure examples (up to 5)
        failures = sub[~sub['is_exact']]
        fail_samples = []
        for _, f in failures.head(5).iterrows():
            fail_samples.append({
                'input': f['input'],
                'actual': f['actual'],
                'expected': f['expected'],
                'cer': round(f['cer'], 4)
            })

        summary[d] = {
            'total': total,
            'exact_matches': exact,
            'exact_accuracy_pct': round((exact / total) * 100, 2),
            'mean_cer_pct': round(mean_cer * 100, 2),
            'total_unchanged': unchanged,
            'unwanted_unchanged': unwanted_unchanged,
            'legitimate_unchanged': legit_unchanged,
            'failure_samples': fail_samples
        }

        print(f"\n[{d}]")
        print(f"  Total test cases: {total}")
        print(f"  Exact-match: {exact}/{total} ({exact/total*100:.2f}%)")
        print(f"  Character Error Rate (CER): {mean_cer*100:.2f}%")
        print(f"  Total Unchanged: {unchanged}/{total} (Legitimate: {legit_unchanged}, Unwanted: {unwanted_unchanged})")
        print(f"  First 3 failure examples:")
        for idx_f, f in enumerate(fail_samples[:3]):
            print(f"    {idx_f+1}. In:  {f['input']}")
            print(f"       Act: {f['actual']}")
            print(f"       Exp: {f['expected']}")

    total_all = len(rdf)
    exact_all = int(rdf['is_exact'].sum())
    cer_all = float(rdf['cer'].mean())
    unchanged_all = int(rdf['is_unchanged'].sum())
    legit_all = int((rdf['is_unchanged'] & rdf['should_be_unchanged']).sum())

    summary['Overall'] = {
        'total': total_all,
        'exact_matches': exact_all,
        'exact_accuracy_pct': round((exact_all / total_all) * 100, 2),
        'mean_cer_pct': round(cer_all * 100, 2),
        'total_unchanged': unchanged_all,
        'unwanted_unchanged': unchanged_all - legit_all,
        'legitimate_unchanged': legit_all
    }

    print("\n" + "=" * 60)
    print(f"OVERALL SUMMARY:")
    print(f"  Total Sentences: {total_all}")
    print(f"  Exact Match Accuracy: {exact_all}/{total_all} ({exact_all/total_all*100:.2f}%)")
    print(f"  Mean CER: {cer_all*100:.2f}%")
    print(f"  Total Unchanged: {unchanged_all}/{total_all} (Legitimate: {legit_all})")
    print("=" * 60)

    # Save summary json
    with open('reports/stage2_evaluation_summary.json', 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    return summary

def evaluate_unseen_sentences():
    normalizer = DialectNormalizer()

    unseen_tests = {
        "Hubballi-Dharwad": [
            ("ಅವನು ಹೊಲದಾಗ ಕೆಲಸ ಮಾಡಾಕತ್ತಾನ ನೋಡ್ರಿ.", "ಅವನು ಹೊಲದಲ್ಲಿ ಕೆಲಸ ಮಾಡುತ್ತಿದ್ದಾನೆ ನೋಡಿ.", "Locative -ದಾಗ, Continuous -ಾಕತ್ತಾನ, Imperative -್ರಿ"),
            ("ನಮ್ಮವ್ವ ಇವ್ವತ್ ರೊಟ್ಟಿ ಮಾಡಾಕತ್ತಾಳ.", "ನಮ್ಮ ತಾಯಿ ಇಂದು ರೊಟ್ಟಿ ಮಾಡುತ್ತಿದ್ದಾಳೆ.", "Vocabulary ಅವ್ವ, ಇವ್ವತ್, Continuous -ಾಕತ್ತಾಳ"),
            ("ದೋಸ್ತ್, ನನಗ ಸ್ವಲ್ಪ ರೊಕ್ಕ ಕೊಡ್ರಿ.", "ಗೆಳೆಯ, ನನಗೆ ಸ್ವಲ್ಪ ಹಣ ಕೊಡಿ.", "Vocabulary ದೋಸ್ತ್, ರೊಕ್ಕ, Dative ನನಗ, Imperative ಕೊಡ್ರಿ"),
            ("ಬಿಸಿ ಬಿಸಿ ಚಾ ಕುಡೀರಿ ಮೊದ್ಲು.", "ಬಿಸಿ ಬಿಸಿ ಚಹಾ ಕುಡಿಯಿರಿ ಮೊದಲು.", "Vocabulary ಚಾ, ಮೊದ್ಲು, Imperative ಕುಡೀರಿ"),
            ("ಊಟ ಆತೇನ್ರಿ ಅಣ್ಣಾ?", "ಊಟ ಆಯಿತೇ ಅಣ್ಣ?", "Clitic ಆತೇನ್ರಿ, Vocative ಅಣ್ಣಾ"),
            ("ಮನ್ಯಾಗ ಯಾರೂ ಇಲ್ರಿ ಈಗ.", "ಮನೆಯಲ್ಲಿ ಯಾರೂ ಇಲ್ಲ ಈಗ.", "Locative ಮನ್ಯಾಗ, Negative ಇಲ್ರಿ"),
            ("ನೀವು ನಾಳಿಕಿ ಸಾಲಿಗೆ ಬರ್ತೀರಾ?", "ನೀವು ನಾಳೆ ಶಾಲೆಗೆ ಬರುತ್ತೀರಾ?", "Vocabulary ನಾಳಿಕಿ, ಸಾಲಿಗೆ, Interrogative ಬರ್ತೀರಾ?"),
            ("ಅವರು ಊರಿಗೆ ಹೊಂಟಾರ ನೋಡ್ರಿ.", "ಅವರು ಊರಿಗೆ ಹೊರಟಿದ್ದಾರೆ ನೋಡಿ.", "Continuous ಹೊಂಟಾರ, Imperative ನೋಡ್ರಿ"),
            ("ಖರೇ ಹೇಳ್ತೀನಿ, ನನಗೆ ಗೊತ್ತಿಲ್ರಿ.", "ನಿಜ ಹೇಳುತ್ತೇನೆ, ನನಗೆ ಗೊತ್ತಿಲ್ಲ.", "Vocabulary ಖರೇ, Clitic ಗೊತ್ತಿಲ್ರಿ"),
            ("ಚೌಕಾಶಿ ಮಾಡಬ್ಯಾಡ್ರಿ ಸಾಹುಕಾರ್ರ.", "ಚೌಕಾಶಿ ಮಾಡಬೇಡಿ ಯಜಮಾನರೇ.", "Prohibitive ಮಾಡಬ್ಯಾಡ್ರಿ, Vocative ಸಾಹುಕಾರ್ರ")
        ],
        "Mangaluru": [
            ("ಎಂತ ಮಾರೆ, ಇವತ್ತು ಆರಾಮ್ದಲ್ಲಿ ಇದ್ದೀರಾ?", "ಏನು ಗೆಳೆಯ, ಇಂದು ಕ್ಷೇಮವಾಗಿ ಇದ್ದೀರಾ?", "Vocabulary ಎಂತ, ಮಾರೆ, ಇವತ್ತು, ಆರಾಮ್ದಲ್ಲಿ"),
            ("ನಾಳೆ ಬೆಳಿಗ್ಗೆ ಪೋಯಿ ಬರ್ಪೆ.", "ನಾಳೆ ಬೆಳಿಗ್ಗೆ ಹೋಗಿ ಬರುತ್ತೇನೆ.", "Verbs ಪೋಯಿ, ಬರ್ಪೆ"),
            ("ಅಪ್ಪೆ ಅಡಿಗೆ ಮಾಡ್ತಾ ಇದ್ದಾರೆ ಒಳಗೆ.", "ಅಮ್ಮ ಅಡುಗೆ ಮಾಡುತ್ತಿದ್ದಾರೆ ಒಳಗೆ.", "Vocabulary ಅಪ್ಪೆ, ಅಡಿಗೆ, Auxiliary continuous ಮಾಡ್ತಾ ಇದ್ದಾರೆ"),
            ("ಶಾಲೆಗ್ ರಜಾನಾ ಇವತ್ತು?", "ಶಾಲೆಗೆ ರಜೆಯೇ ಇಂದು?", "Dative ಶಾಲೆಗ್, Interrogative ರಜಾನಾ, Vocabulary ಇವತ್ತು"),
            ("ಮನೆಲ್ ಕೋರಿ ರೊಟ್ಟಿ ಉಂಡು.", "ಮನೆಯಲ್ಲಿ ಕೋಳಿ ರೊಟ್ಟಿ ಇದೆ.", "Locative ಮನೆಲ್, Vocabulary ಕೋರಿ, Verb ಉಂಡು"),
            ("ಅದ್ಕೆ ನಾನ್ ಹೇಳ್ದೆ ಕೇಳಿಲ್ವಾ?", "ಅದಕ್ಕೆ ನಾನು ಹೇಳಿದೆ ಕೇಳಿಸಿಕೊಳ್ಳಲಿಲ್ಲವೇ?", "Vocabulary ಅದ್ಕೆ, ನಾನ್, Verb ಹೇಳ್ದೆ, Tag ಕೇಳಿಲ್ವಾ?"),
            ("ಬಂದು ಕುತ್ಕೊಳಿ ಮಾರೆ ಇಲ್ಲಿ.", "ಬಂದು ಕುಳಿತುಕೊಳ್ಳಿ ಗೆಳೆಯ ಇಲ್ಲಿ.", "Imperative ಕುತ್ಕೊಳಿ, Address ಮಾರೆ"),
            ("ಅಂಗಡಿಗ್ ಹೋಗಿ ಮೀನ್ ತರ್ಪೆ.", "ಅಂಗಡಿಗೆ ಹೋಗಿ ಮೀನು ತರುತ್ತೇನೆ.", "Dative ಅಂಗಡಿಗ್, Noun ಮೀನ್, Verb ತರ್ಪೆ"),
            ("ಮಳೆ ಜೋರಾಗಿ ಬರ್ತಾ ಉಂಡು.", "ಮಳೆ ಜೋರಾಗಿ ಬರುತ್ತಿದೆ.", "Continuous ಬರ್ತಾ ಉಂಡು"),
            ("ಆರಾಮ್ ಆಯ್ತು ನಿನ್ನನ್ನು ಕಂಡು.", "ಆರಾಮವಾಯಿತು ನಿನ್ನನ್ನು ಕಂಡು.", "Phrase ಆರಾಮ್ ಆಯ್ತು")
        ],
        "Uttara Kannada": [
            ("ಹೆಂಗಿದ್ದೀರಿ, ಊಟಕ್ಕೆ ಬರ್ತೀರಾ?", "ಹೇಗಿದ್ದೀರಿ, ಊಟಕ್ಕೆ ಬರುತ್ತೀರಾ?", "Greeting ಹೆಂಗಿದ್ದೀರಿ, Interrogative ಬರ್ತೀರಾ?"),
            ("ಅಪ್ಪಯ್ಯ ತೋಟಕ್ಕೆ ಹೋಗಿ ಬತ್ತೆ ಅಂದ್ರು.", "ತಂದೆ ತೋಟಕ್ಕೆ ಹೋಗಿ ಬರುತ್ತೇನೆ ಎಂದರು.", "Vocabulary ಅಪ್ಪಯ್ಯ, Phrase ಹೋಗಿ ಬತ್ತೆ, Verb ಅಂದ್ರು"),
            ("ಮನೆಲ್ ಅಡಿಗೆ ಆತಾ ಹೆಂಗಸ್ರೇ?", "ಮನೆಯಲ್ಲಿ ಅಡುಗೆ ಆಯಿತೇ ಹೆಂಗಳೆಯರೇ?", "Locative ಮನೆಲ್, Vocabulary ಅಡಿಗೆ, Verb ಆತಾ"),
            ("ಅಲ್ಲಿ ಕೂಡು, ಚೂರು ಕಷಾಯ ಕುಡಿಯುವಾ.", "ಅಲ್ಲಿ ಕುಳಿತುಕೊ, ಸ್ವಲ್ಪ ಕಷಾಯ ಕುಡಿಯೋಣ.", "Imperative ಕೂಡು, Vocabulary ಚೂರು, Modal ಕುಡಿಯುವಾ"),
            ("ಮಳೆ ಜೋರಾಗಿ ಸುರಿವುತ್ತೆ ಹೊರಗೆ.", "ಮಳೆ ಜೋರಾಗಿ ಸುರಿಯುತ್ತದೆ ಹೊರಗೆ.", "Neuter habitual ಸುರಿವುತ್ತೆ"),
            ("ನಾಳೆ ನಾನಲ್ಲಿ ಬತ್ತೆ ಹೌದಾ?", "ನಾಳೆ ನಾನು ಅಲ್ಲಿಗೆ ಬರುತ್ತೇನೆ ಹೌದಾ?", "Pronoun ನಾನಲ್ಲಿ, Verb ಬತ್ತೆ"),
            ("ಅಮ್ಮಯ್ಯ ಹಿತ್ತಿಲಲ್ಲಿ ಕೆಲಸ ಮಾಡ್ತಾ ಇದ್ದಾರೆ.", "ತಾಯಿ ಹಿತ್ತಿಲಿನಲ್ಲಿ ಕೆಲಸ ಮಾಡುತ್ತಿದ್ದಾರೆ.", "Vocabulary ಅಮ್ಮಯ್ಯ, Auxiliary continuous"),
            ("ಹಿತ್ತಿಲಲ್ಲಿ ಹಣ್ಣು ಕೊಯ್ದು ತಂದಿದೀನಿ.", "ಹಿತ್ತಿಲಿನಲ್ಲಿ ಹಣ್ಣು ಕೊಯ್ದು ತಂದಿದ್ದೇನೆ.", "Experiential perfective -ಿದೀನಿ"),
            ("ಕಡುಬು ತಿಂಬೋದು ತುಂಬಾ ಚಂದ.", "ಕಡುಬು ತಿನ್ನುವುದು ತುಂಬಾ ಸುಂದರ.", "Verbal noun ತಿಂಬೋದು, Adjective ಚಂದ"),
            ("ಧ್ವನಿ ದೂರದಿಂದ ಕೇಳ್ತು ನಮಗೆ.", "ಧ್ವನಿ ದೂರದಿಂದ ಕೇಳಿಸಿತು ನಮಗೆ.", "Neuter past ಕೇಳ್ತು")
        ]
    }

    print("\n" + "=" * 60)
    print("STAGE 2: EVALUATION ON 10 UNSEEN SENTENCES PER DIALECT")
    print("=" * 60)

    unseen_results = []
    for dialect, items in unseen_tests.items():
        print(f"\n--- {dialect} (10 Unseen Generalization Tests) ---")
        d_exact = 0
        for i, (inp, exp, notes) in enumerate(items, 1):
            res = normalizer.normalize(inp, target_region=dialect, mode='local')
            act = res['standard_text']
            is_exact = (act == exp)
            if is_exact:
                d_exact += 1
            cer = calculate_cer(exp, act)
            print(f"{i:2d}. Input:    {inp}")
            print(f"    Expected: {exp}")
            print(f"    Actual:   {act}")
            print(f"    Match:    {'EXACT MATCH' if is_exact else f'DIFF (CER: {cer*100:.1f}%)'} [{notes}]")
            unseen_results.append({
                'dialect': dialect,
                'input': inp,
                'expected': exp,
                'actual': act,
                'exact': is_exact,
                'cer': cer,
                'notes': notes
            })
        print(f"Subtotal {dialect}: {d_exact}/10 ({d_exact*10}%) exact matches")

    total_unseen = len(unseen_results)
    exact_unseen = sum(1 for r in unseen_results if r['exact'])
    print(f"\nOVERALL UNSEEN ACCURACY: {exact_unseen}/{total_unseen} ({exact_unseen/total_unseen*100:.1f}%)")

if __name__ == '__main__':
    evaluate_315_dataset()
    evaluate_unseen_sentences()
