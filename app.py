# -*- coding: utf-8 -*-
"""
ಮಾತಿನ ಕನ್ನಡ → ಪ್ರಮಾಣ ಕನ್ನಡ (Nudi Parivartaka)
Unique, Intelligent & Comprehensive Karnataka Dialect NLP Platform
Features:
  1. Auto-Detection or Custom Dialect Selection (5 Major Regions)
  2. Spoken to Standard Textbook Kannada Normalization
  3. All-Karnataka Cross-Dialect Generator (View sentence in all 5 dialects!)
  4. Dialect Radar / Probability Distribution Meter
  5. Cultural Etymology & Linguistic Context Cards
  6. Zero API Key Friction in UI (Seamless Backend Handling)
"""

import streamlit as st
import json
import os
import re
import pandas as pd
import importlib

import engine.config
importlib.reload(engine.config)
from engine.config import GEMINI_API_KEY
from engine.normalizer import DialectNormalizer

# Page configuration
st.set_page_config(
    page_title="ನುಡಿ ಪರಿವರ್ತಕ | Karnataka Dialect AI",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tiro+Kannada&family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Main App Header */
    .app-header {
        text-align: center;
        margin-top: -1.2rem;
        margin-bottom: 1.2rem;
    }
    .app-title {
        font-family: 'Tiro Kannada', serif;
        font-size: 2.3rem;
        font-weight: 700;
        color: #991B1B;
        margin-bottom: 0.2rem;
    }
    .app-subtitle {
        font-size: 1.05rem;
        color: #4B5563;
    }

    /* Cards */
    .card-header-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.6rem;
        padding-bottom: 0.4rem;
        border-bottom: 1px solid #E5E7EB;
    }
    
    .card-label {
        font-weight: 600;
        font-size: 0.95rem;
        color: #374151;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    .output-text-box {
        font-family: 'Tiro Kannada', serif;
        font-size: 1.45rem;
        line-height: 1.8;
        color: #15803D;
        background-color: #F0FDF4;
        border: 1px solid #BBF7D0;
        border-radius: 8px;
        padding: 1.2rem;
        min-height: 125px;
    }

    .empty-output-box {
        font-size: 1.05rem;
        color: #9CA3AF;
        font-style: italic;
        background-color: #F9FAFB;
        border: 1px dashed #D1D5DB;
        border-radius: 8px;
        padding: 2.5rem 1rem;
        text-align: center;
        min-height: 125px;
    }

    /* Badges & Chips */
    .region-pill {
        background-color: #FEF3C7;
        color: #92400E;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.82rem;
        font-weight: 600;
        display: inline-block;
    }
    .auto-pill {
        background-color: #E0E7FF;
        color: #3730A3;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.82rem;
        font-weight: 600;
        display: inline-block;
    }

    .word-change-chip {
        display: inline-flex;
        align-items: center;
        gap: 4px;
        background-color: #EFF6FF;
        border: 1px solid #DBEAFE;
        color: #1E40AF;
        border-radius: 6px;
        padding: 4px 10px;
        font-size: 0.9rem;
        font-family: 'Tiro Kannada', serif;
        margin: 3px;
    }

    /* Multi-dialect card */
    .dialect-card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 12px 14px;
        margin-bottom: 8px;
    }
    .dialect-card-title {
        font-weight: 700;
        font-size: 0.88rem;
        color: #1E293B;
        margin-bottom: 4px;
        display: flex;
        justify-content: space-between;
    }
    .dialect-card-text {
        font-family: 'Tiro Kannada', serif;
        font-size: 1.15rem;
        color: #0F172A;
        line-height: 1.6;
    }
    .dialect-card-tag {
        font-size: 0.75rem;
        color: #64748B;
        font-weight: 500;
    }

    /* Etymology Card */
    .etym-card {
        background-color: #FFFBEB;
        border-left: 4px solid #F59E0B;
        padding: 10px 14px;
        border-radius: 4px;
        margin-bottom: 8px;
    }
    .etym-title {
        font-weight: 700;
        font-size: 0.95rem;
        color: #B45309;
        margin-bottom: 3px;
    }
    .etym-body {
        font-size: 0.88rem;
        color: #78350F;
        line-height: 1.5;
    }

    /* Buttons */
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Normalizer (backend handles API key and local models silently)
normalizer = DialectNormalizer(gemini_api_key=GEMINI_API_KEY)
if not normalizer.ai_rewriter.is_available() and GEMINI_API_KEY:
    normalizer.ai_rewriter.api_key = GEMINI_API_KEY

# Session state initialization
if "input_val" not in st.session_state:
    st.session_state["input_val"] = "ಅವನು ಬರ್ತಾನ"

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("## 🌸 ನುಡಿ ಸೇತು")
    st.caption("Modalapada 2.0 | Dept of CS&E - RIT")
    st.markdown("**Problem 1: Dialect to Standard Kannada**")
    
    st.divider()
    st.markdown("### 📍 ಒಳಗೊಂಡಿರುವ 3 ಪ್ರಮುಖ ಪ್ರಾಂತ್ಯಗಳು:")
    st.markdown("""
    1. **Hubballi–Dharwad (ಹುಬ್ಬಳ್ಳಿ-ಧಾರವಾಡ)**
       • ಧಾರವಾಡ, ಹುಬ್ಬಳ್ಳಿ, ಕುಂದಗೋಳ
    2. **Mangaluru (ಮಂಗಳೂರು / ಕುಂದಗನ್ನಡ)**
       • ಮಂಗಳೂರು, ಉಡುಪಿ, ಕುಂದಾಪುರ
    3. **Uttara Kannada (ಉತ್ತರ ಕನ್ನಡ / ಹವ್ಯಕ)**
       • ಶಿರಸಿ, ಕಾರವಾರ, ಕುಮಟಾ, ಗೋಕರ್ಣ
    """)
    st.divider()
    st.caption("💡 ಮೇಲಿನ ಉದಾಹರಣೆ ಬಟನ್‌ಗಳನ್ನು ಕ್ಲಿಕ್ ಮಾಡಿ ಅಥವಾ ನಿಮ್ಮದೇ ವಾಕ್ಯವನ್ನು ನಮೂದಿಸಿ.")

# Automatic smart hybrid mode (0ms offline for routine grammar, AI for complex slang)
exec_mode = "hybrid" if normalizer.ai_rewriter.is_available() else "local"

# --- MAIN CONTENT ---
st.markdown("""
<div class="app-header">
    <div class="app-title">🌸 ನುಡಿ ಸೇತು (Nudi Setu)</div>
    <div class="app-subtitle">ಪ್ರಾದೇಶಿಕ ಆಡುಮಾತಿನಿಂದ ಶಿಷ್ಟ ಕನ್ನಡಕ್ಕೆ ಪರಿವರ್ತನೆ (Spoken Dialect ➔ Textbook Kannada)</div>
</div>
""", unsafe_allow_html=True)

# Official Starter Examples from Modalapada 2.0 (Slide 4)
st.write("##### 💡 ಅಧಿಕೃತ ಪರೀಕ್ಷಾ ವಾಕ್ಯಗಳು (Starter Examples from Slide 4):")
col_c1, col_c2, col_c3, col_c4, col_c5 = st.columns(5)
with col_c1:
    if st.button("ಏನ್ರಿ, ಊಟ ಆತೇನ್ರಿ?", use_container_width=True, help="Hubballi-Dharwad starter example"):
        st.session_state["input_val"] = "ಏನ್ರಿ, ಊಟ ಆತೇನ್ರಿ?"
        st.rerun()
with col_c2:
    if st.button("ಎಂತ ಮಾಡ್ತಾ ಇದ್ದೀರಿ?", use_container_width=True, help="Mangaluru starter example"):
        st.session_state["input_val"] = "ಎಂತ ಮಾಡ್ತಾ ಇದ್ದೀರಿ?"
        st.rerun()
with col_c3:
    if st.button("ಹೆಂಗಿದ್ದೀರಿ, ಊಟಕ್ಕೆ ಬರ್ತೀರಾ?", use_container_width=True, help="Uttara Kannada starter example"):
        st.session_state["input_val"] = "ಹೆಂಗಿದ್ದೀರಿ, ಊಟಕ್ಕೆ ಬರ್ತೀರಾ?"
        st.rerun()
with col_c4:
    if st.button("ದೋಸ್ತ್, ರೊಕ್ಕ ಕೊಡತಿಯಾ?", use_container_width=True, help="Market conversation"):
        st.session_state["input_val"] = "ದೋಸ್ತ್, ರೊಕ್ಕ ಕೊಡತಿಯಾ?"
        st.rerun()
with col_c5:
    if st.button("ಅವನು ಇವ್ವತ್ ಬರಾಕತ್ತಾನ.", use_container_width=True, help="Aspectual continuous"):
        st.session_state["input_val"] = "ಅವನು ಇವ್ವತ್ ಬರಾಕತ್ತಾನ."
        st.rerun()

st.write("")

# Dialect Selection Bar (3 Target Dialects)
selected_dialect_choice = st.selectbox(
    "📍 ಪ್ರಾದೇಶಿಕ ಉಪಭಾಷೆ ಆಯ್ಕೆ (Dialect Selection):",
    options=[
        "🔍 ಸ್ವಯಂ ಪತ್ತೆ (Auto-Detect)",
        "🌾 Hubballi-Dharwad (ಹುಬ್ಬಳ್ಳಿ-ಧಾರವಾಡ)",
        "🌊 Mangaluru (ಮಂಗಳೂರು / ಕುಂದಗನ್ನಡ)",
        "🌿 Uttara Kannada (ಉತ್ತರ ಕನ್ನಡ / ಹವ್ಯಕ)"
    ],
    index=0,
    help="Modalapada 2.0 ಸ್ಪರ್ಧೆಯ 3 ಅಧಿಕೃತ ಪ್ರಾಂತ್ಯಗಳು."
)

# Region mapping
region_mapping = {
    "🔍 ಸ್ವಯಂ ಪತ್ತೆ (Auto-Detect)": None,
    "🌾 Hubballi-Dharwad (ಹುಬ್ಬಳ್ಳಿ-ಧಾರವಾಡ)": "North Karnataka",
    "🌊 Mangaluru (ಮಂಗಳೂರು / ಕುಂದಗನ್ನಡ)": "Coastal / Kundagannada",
    "🌿 Uttara Kannada (ಉತ್ತರ ಕನ್ನಡ / ಹವ್ಯಕ)": "Uttara Kannada / Havyaka"
}
target_region = region_mapping.get(selected_dialect_choice)

# Side-by-Side Translation Deck
col_left, col_right = st.columns(2)

with col_left:
    st.markdown("""
    <div class="card-header-bar">
        <span class="card-label">🗣️ ಮೂಲ ಆಡುಮಾತು (Spoken Dialect)</span>
    </div>
    """, unsafe_allow_html=True)

    user_input = st.text_area(
        "ಆಡುಮಾತಿನ ವಾಕ್ಯ:",
        value=st.session_state["input_val"],
        height=140,
        label_visibility="collapsed",
        placeholder="ಯಾವುದೇ ಪ್ರಾದೇಶಿಕ ಆಡುಮಾತಿನ ವಾಕ್ಯವನ್ನು ಇಲ್ಲಿ ಟೈಪ್ ಮಾಡಿ (ಅಥವಾ ಇಂಗ್ಲಿಷ್‌ನಲ್ಲಿ 'avanu bartana' ಎಂದೂ ಟೈಪ್ ಮಾಡಬಹುದು)..."
    )

    col_b1, col_b2 = st.columns([3, 1])
    with col_b1:
        convert_clicked = st.button("🚀 ಪರಿವರ್ತಿಸಿ (Convert)", type="primary", use_container_width=True)
    with col_b2:
        if st.button("🔄 ತೆರವು (Clear)", use_container_width=True):
            st.session_state["input_val"] = ""
            st.rerun()

    st.write("")
    with st.expander("⌨️ ಲ್ಯಾಪ್ಟಾಪ್‌ನಲ್ಲಿ ಕನ್ನಡ ಟೈಪ್ ಮಾಡುವುದು ಹೇಗೆ? (How to Type Kannada on Laptop)", expanded=False):
        st.markdown("""
        **ವಿಧಾನ 1: ಇಂಗ್ಲಿಷ್ ಅಕ್ಷರಗಳಲ್ಲೇ ನೇರವಾಗಿ ಟೈಪ್ ಮಾಡಿ (Direct Kanglish)**:
        - ನಿಮ್ಮ ಬಳಿ ಕನ್ನಡ ಕೀಬೋರ್ಡ್ ಇಲ್ಲದಿದ್ದರೂ ಪರವಾಗಿಲ್ಲ!
        - ಮೇಲಿನ ಬಾಕ್ಸ್‌ನಲ್ಲಿ ಇಂಗ್ಲಿಷ್‌ನಲ್ಲಿ `avanu bartana`, `naale hogbeku`, `baralla` ಎಂದು ಟೈಪ್ ಮಾಡಿದರೆ ಸಾಕು, ಸಿಸ್ಟಮ್ ತಾನಾಗಿಯೇ ಕನ್ನಡಕ್ಕೆ ಬದಲಾಯಿಸಿ ಪರಿವರ್ತಿಸುತ್ತದೆ.

        **ವಿಧಾನ 2: Windows ನಲ್ಲಿ ಕನ್ನಡ ಫೋನೆಟಿಕ್ ಕೀಬೋರ್ಡ್ ಆನ್ ಮಾಡಲು (ಕೇವಲ 1 ನಿಮಿಷ)**:
        1. ನಿಮ್ಮ ಲ್ಯಾಪ್ಟಾಪ್‌ನಲ್ಲಿ **`Win + I`** ಒತ್ತಿ (Settings).
        2. **Time & Language** $\\to$ **Language & region** ತೆರೆಯಿರಿ.
        3. **Add a language** ಕ್ಲಿಕ್ ಮಾಡಿ $\\to$ **Kannada (ಕನ್ನಡ)** ಹುಡುಕಿ Install ಮಾಡಿ.
        4. ಕನ್ನಡ ಪಕ್ಕದಲ್ಲಿರುವ **`...`** $\\to$ **Language options** $\\to$ **Add a keyboard** $\\to$ **Kannada Phonetic** ಆಯ್ಕೆಮಾಡಿ.
        5. ಈಗ ಕೀಬೋರ್ಡ್‌ನಲ್ಲಿ **`Win + Space`** ಒತ್ತಿದರೆ ನೀವು ಇಂಗ್ಲಿಷ್‌ನಲ್ಲಿ ಟೈಪ್ ಮಾಡುವ ಅಕ್ಷರಗಳು (`avanu` $\\to$ `ಅವನು`) ತಾನಾಗಿಯೇ ಕನ್ನಡಕ್ಕೆ ಟೈಪ್ ಆಗುತ್ತವೆ!
        """)

with col_right:
    # Run conversion (Uses selected exec_mode with target_region)
    res = None
    if user_input and user_input.strip():
        res = normalizer.normalize(user_input.strip(), target_region=target_region, mode=exec_mode)

    # Header badge
    badge_html = ""
    if res and res.get("standard_text"):
        if target_region is None or res.get("is_auto_detected", True):
            badge_html = f'<span class="auto-pill">📍 ಪತ್ತೆಯಾದ ಪ್ರಾಂತ್ಯ: {res.get("region_name_kn", "ಸಾಮಾನ್ಯ ಆಡುಮಾತು")}</span>'
        else:
            chosen_name = selected_dialect_choice.split("(")[0].strip()
            badge_html = f'<span class="region-pill">🎯 ಪ್ರಾಂತ್ಯ: {chosen_name}</span>'

    st.markdown(f"""
    <div class="card-header-bar">
        <span class="card-label">✍️ ಪ್ರಮಾಣ ಕನ್ನಡ (Standard Textbook Kannada)</span>
        {badge_html}
    </div>
    """, unsafe_allow_html=True)

    if res and res.get("standard_text"):
        st.markdown(f"""
        <div class="output-text-box">
            {res["standard_text"]}
        </div>
        """, unsafe_allow_html=True)

        # Audio Read Aloud & Copy to Clipboard
        clean_audio_text = res["standard_text"].replace("'", "\\'").replace('"', '\\"')
        audio_bar_html = f"""
        <div style="margin-top: 10px; display: flex; gap: 10px; align-items: center; font-family: sans-serif;">
            <button onclick="playKannadaSpeech()" style="background-color: #15803D; color: white; border: none; padding: 7px 16px; border-radius: 6px; font-weight: 600; cursor: pointer; font-size: 0.9rem; display: flex; align-items: center; gap: 6px;">
                🔊 ಆಲಿಸಿ (Read Aloud)
            </button>
            <button onclick="copyOutputText()" id="copyBtn" style="background-color: #2563EB; color: white; border: none; padding: 7px 16px; border-radius: 6px; font-weight: 600; cursor: pointer; font-size: 0.9rem; display: flex; align-items: center; gap: 6px;">
                📋 ನಕಲಿಸಿ (Copy)
            </button>
            <span id="copyMsg" style="color: #16A34A; font-weight: 600; font-size: 0.85rem;"></span>
        </div>
        <script>
        function copyOutputText() {{
            var txt = '{clean_audio_text}';
            if (navigator.clipboard) {{
                navigator.clipboard.writeText(txt).then(function() {{
                    showCopied();
                }}).catch(function() {{
                    execCopy(txt);
                }});
            }} else {{
                execCopy(txt);
            }}
        }}
        function execCopy(txt) {{
            var ta = document.createElement('textarea');
            ta.value = txt;
            document.body.appendChild(ta);
            ta.select();
            document.execCommand('copy');
            document.body.removeChild(ta);
            showCopied();
        }}
        function showCopied() {{
            document.getElementById('copyMsg').innerText = '✅ ನಕಲಿಸಲಾಗಿದೆ!';
            setTimeout(function() {{
                document.getElementById('copyMsg').innerText = '';
            }}, 2000);
        }}
        function playKannadaSpeech() {{
            if ('speechSynthesis' in window) {{
                window.speechSynthesis.cancel();
                var utterance = new SpeechSynthesisUtterance('{clean_audio_text}');
                utterance.lang = 'kn-IN';
                utterance.rate = 0.9;
                window.speechSynthesis.speak(utterance);
            }} else {{
                alert('Audio playback not supported in this browser.');
            }}
        }}
        </script>
        """
        st.components.v1.html(audio_bar_html, height=48)
    else:
        st.markdown("""
        <div class="empty-output-box">
            ಎಡಭಾಗದಲ್ಲಿ ವಾಕ್ಯವನ್ನು ನಮೂದಿಸಿ 'ಪರಿವರ್ತಿಸಿ' ಕ್ಲಿಕ್ ಮಾಡಿ.
        </div>
        """, unsafe_allow_html=True)

# --- CHANGED WORDS HIGHLIGHTED (Slide 4 Requirement) ---
if res and res.get("standard_text"):
    st.markdown("---")

    info_col1, info_col2 = st.columns([3, 2])
    with info_col1:
        if res.get("transformations"):
            st.write("##### 🔍 ಬದಲಾದ ಪ್ರಾದೇಶಿಕ ಪದಗಳು (Changed Words Highlighted):")
            chips_html = ""
            for t in res["transformations"]:
                chips_html += f'<span class="word-change-chip"><b>{t.get("dialect", "")}</b> ➔ <b>{t.get("standard", "")}</b></span> '
            st.markdown(chips_html, unsafe_allow_html=True)
        elif res.get("rules_applied"):
            st.write("##### 📝 ಅನ್ವಯಿಸಲಾದ ವ್ಯಾಕರಣ ನಿಯಮ (Grammar Rule):")
            rule_descs = [f"• {r.get('description', '')}" for r in res["rules_applied"][:2]]
            st.info("\n".join(rule_descs))

    with info_col2:
        if res.get("english_meaning"):
            st.write("##### 🌐 English Semantic Translation:")
            st.write(f'*"{res["english_meaning"]}"*')
        elif res.get("explanation"):
            st.write("##### ℹ️ ವಿವರಣೆ (Linguistic Details):")
            st.caption(res["explanation"])

    # Cultural Etymology
    if res.get("etymology"):
        st.write("")
        st.write("##### 💡 ಸಾಂಸ್ಕೃತಿಕ ಹಿನ್ನೆಲೆ & ಪದ ವ್ಯುತ್ಪತ್ತಿ (Cultural Etymology & Linguistic Origin):")
        for et in res["etymology"]:
            st.markdown(f"""
            <div class="etym-card">
                <div class="etym-title">📖 '{et["word"]}' ➔ {et["standard"]} ({et["region"]})</div>
                <div class="etym-body">{et["context"]}</div>
            </div>
            """, unsafe_allow_html=True)

    # Cross-Dialect Multi-Region View
    if res.get("all_dialects"):
        st.write("")
        with st.expander("🌐 ಅಖಿಲ ಕರ್ನಾಟಕ 3 ಪ್ರಾಂತ್ಯಗಳಲ್ಲಿ ನೋಡಿ (Cross-Dialect View)", expanded=False):
            st.caption("ಇದೇ ವಾಕ್ಯವನ್ನು ಇತರ ಪ್ರಾಂತ್ಯಗಳಲ್ಲಿ ಹೇಗೆ ಮಾತನಾಡುತ್ತಾರೆಂದು ನೋಡಿ:")
            all_d = res["all_dialects"]
            target_keys = ["North Karnataka", "Coastal / Kundagannada", "Uttara Kannada / Havyaka"]
            c_cols = st.columns(3)
            col_idx = 0
            for k in target_keys:
                if k in all_d and col_idx < 3:
                    d_info = all_d[k]
                    with c_cols[col_idx]:
                        st.markdown(f"""
                        <div class="dialect-card">
                            <div class="dialect-card-title">
                                <span>{d_info["icon"]} {d_info["name_kn"]}</span>
                                <span class="dialect-card-tag">{d_info["accent_tag"]}</span>
                            </div>
                            <div class="dialect-card-text">{d_info["text"]}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    col_idx += 1


