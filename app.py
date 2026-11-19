# -*- coding: utf-8 -*-
"""
ನುಡಿ ಸೇತು (Nudi Setu) | Kannada Dialect Normalization Platform
Modalapada 2.0 – Problem 1: Text — Nudi Setu (Dialect to Textbook Kannada)
Department of Computer Science & Engineering, Ramaiah Institute of Technology

Visual Upgrades:
- 360-Degree Rotating Royal Floral Emblem (Continuous smooth 360° rotation)
- Atmospheric Dual-Tone Dark Palette: Deep Twilight Navy (#13182C) & Rich Midnight Plum (#2B1536)
- Radiant Gold-Lit Headline Typography & Glowing Ambient Orbs
- 3-Page Architecture & 100% Protected Backend Engine & Datasets
"""

import streamlit as st
import json
import os
import re
import pandas as pd
import importlib

import engine.config
import engine.dialect_generator
import engine.normalizer
importlib.reload(engine.config)
importlib.reload(engine.dialect_generator)
importlib.reload(engine.normalizer)
from engine.config import GEMINI_API_KEY
from engine.normalizer import DialectNormalizer
from engine.dialect_generator import DialectGenerator

# --- Page Configuration ---
st.set_page_config(
    page_title="ನುಡಿ ಸೇತು | Nudi Setu",
    page_icon="📜",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Premium Frontend Design System with 360° Rotating Logo & Dual-Tone Dark Canvas ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Tiro+Kannada:ital@0;1&family=Anek+Kannada:wght@400;500;600;700;800&family=Cinzel:wght@600;700;800&display=swap');

    :root {
        /* Dual-Tone Dark Canvas */
        --bg-navy: #13182C;
        --bg-plum: #2B1536;
        --bg-twilight: #1C1938;
        
        /* Accents */
        --accent-saffron: #EA580C;
        --accent-saffron-hover: #C2410C;
        --accent-gold: #F59E0B;
        --accent-gold-light: #FDE68A;
        
        /* Textbook Kannada Emerald */
        --kannada-emerald: #065F46;
        --kannada-emerald-light: #10B981;
        --kannada-emerald-bg: #F0FDF4;
        
        /* Spring Physics */
        --ease-spring: cubic-bezier(0.34, 1.56, 0.64, 1);
        --ease-smooth: cubic-bezier(0.16, 1, 0.3, 1);
    }

    /* Continuous Flowing Shifting Dual-Tone Canvas Animation */
    @keyframes flowingCanvasDark {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    html, body, [class*="css"], .stApp, [data-testid="stAppViewContainer"], .main {
        font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
        color: #F8FAFC !important;
        background: linear-gradient(135deg, #13182C 0%, #1C1938 38%, #2B1536 74%, #161A32 100%) !important;
        background-size: 260% 260% !important;
        animation: flowingCanvasDark 22s ease-in-out infinite !important;
        position: relative;
    }

    [data-testid="stHeader"] {
        background: transparent !important;
    }

    /* Global Headings on Dark Canvas */
    h1, h2, h3, h4, h5 {
        color: #F8FAFC !important;
    }
    .stMarkdown p {
        color: #E2E8F0;
    }
    [data-testid="stWidgetLabel"] label, [data-testid="stWidgetLabel"] p {
        color: #F1F5F9 !important;
        font-weight: 700 !important;
    }

    /* Floating Ambient Background Layer with Soft Glowing Orbs & Kannada Watermark */
    .ambient-background-canvas {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        pointer-events: none;
        z-index: 0;
        overflow: hidden;
    }
    
    @keyframes orbFloat1 {
        0%, 100% { transform: translate(0px, 0px) scale(1); }
        33% { transform: translate(50px, -40px) scale(1.12); }
        66% { transform: translate(-30px, 30px) scale(0.92); }
    }
    @keyframes orbFloat2 {
        0%, 100% { transform: translate(0px, 0px) scale(1); }
        33% { transform: translate(-60px, 50px) scale(1.08); }
        66% { transform: translate(40px, -30px) scale(1.15); }
    }
    @keyframes orbFloat3 {
        0%, 100% { transform: translate(0px, 0px) scale(1); }
        50% { transform: translate(45px, 35px) scale(1.1); }
    }
    @keyframes orbFloat4 {
        0%, 100% { transform: translate(0px, 0px) scale(1); }
        50% { transform: translate(-50px, -45px) scale(1.14); }
    }

    .ambient-orb {
        position: absolute;
        border-radius: 50%;
        filter: blur(90px);
        opacity: 0.38;
        will-change: transform;
    }
    .orb-indigo {
        top: -6%;
        left: 6%;
        width: 480px;
        height: 480px;
        background: radial-gradient(circle, rgba(99, 102, 241, 0.45) 0%, rgba(99, 102, 241, 0) 70%);
        animation: orbFloat1 24s ease-in-out infinite;
    }
    .orb-peach {
        top: 30%;
        right: -5%;
        width: 540px;
        height: 540px;
        background: radial-gradient(circle, rgba(234, 88, 12, 0.35) 0%, rgba(234, 88, 12, 0) 70%);
        animation: orbFloat2 28s ease-in-out infinite;
    }
    .orb-sage {
        bottom: 5%;
        left: 12%;
        width: 480px;
        height: 480px;
        background: radial-gradient(circle, rgba(16, 185, 129, 0.32) 0%, rgba(16, 185, 129, 0) 70%);
        animation: orbFloat3 32s ease-in-out infinite;
    }
    .orb-amber {
        bottom: 22%;
        right: 15%;
        width: 420px;
        height: 420px;
        background: radial-gradient(circle, rgba(245, 158, 11, 0.35) 0%, rgba(245, 158, 11, 0) 70%);
        animation: orbFloat4 26s ease-in-out infinite;
    }

    /* Subtle Authentic Kannada Glyph Watermark Background Grid */
    .kannada-glyph-watermark {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        opacity: 0.038;
        background-image: url("data:image/svg+xml,%3Csvg width='140' height='140' viewBox='0 0 140 140' xmlns='http://www.w3.org/2000/svg'%3E%3Ctext x='20' y='40' font-family='serif' font-size='22' fill='%23FFFFFF'%3Eಅ%3C/text%3E%3Ctext x='85' y='40' font-family='serif' font-size='22' fill='%23F59E0B'%3Eಕ%3C/text%3E%3Ctext x='20' y='105' font-family='serif' font-size='24' font-weight='bold' fill='%23E2E8F0'%3Eನು%3C/text%3E%3Ctext x='85' y='105' font-family='serif' font-size='22' fill='%2334D399'%3Eರ%3C/text%3E%3C/svg%3E");
        background-repeat: repeat;
    }

    /* High-Impact Hero Section */
    .brand-hero-section {
        text-align: center;
        padding: 1.2rem 1rem 0.4rem 1rem;
        position: relative;
        z-index: 2;
    }
    
    .brand-title-row {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 20px;
        position: relative;
        margin-bottom: 0.25rem;
    }

    /* 360-DEGREE ROTATING LOGO ANIMATION */
    @keyframes rotateLogo360 {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    .brand-crest-container {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 78px;
        height: 78px;
        position: relative;
        filter: drop-shadow(0 8px 22px rgba(0, 0, 0, 0.6)); /* Static shadow: zero wobble */
        cursor: pointer;
        transition: transform 0.4s var(--ease-spring);
    }
    .brand-crest-container:hover {
        transform: scale(1.1);
    }
    .floral-crest-svg {
        width: 78px;
        height: 78px;
        display: block;
        animation: rotateLogo360 12s linear infinite;
        transform-origin: 50% 50% !important;
        transform-box: fill-box !important;
    }
    .brand-crest-container:hover .floral-crest-svg {
        animation-duration: 4.5s; /* Smooth acceleration on hover */
    }

    /* Radiant Gold-Glow Brand Title */
    .brand-title-text {
        font-family: 'Tiro Kannada', serif;
        font-size: 3.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #FFFFFF 0%, #FDE68A 45%, #F59E0B 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        line-height: 1.08;
        letter-spacing: -0.025em;
        filter: drop-shadow(0 4px 20px rgba(0, 0, 0, 0.55));
    }
    
    .brand-sub-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        margin-top: 6px;
        padding: 6px 20px;
        border-radius: 9999px;
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(14px);
        border: 1px solid rgba(255, 255, 255, 0.16);
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.25);
        font-size: 1.02rem;
        font-weight: 600;
        color: #E2E8F0;
    }
    .brand-sub-badge b {
        color: #FBA04B;
        font-weight: 700;
    }

    /* Glassmorphic 3-Pill Navigation Switcher */
    div[data-testid="stRadio"] > div[role="radiogroup"] {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 12px;
        background: rgba(18, 24, 44, 0.75) !important;
        backdrop-filter: blur(16px) !important;
        -webkit-backdrop-filter: blur(16px) !important;
        padding: 8px 12px !important;
        border-radius: 9999px !important;
        width: fit-content !important;
        margin: 0.8rem auto 1.5rem auto !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.35), inset 0 1px 1px rgba(255, 255, 255, 0.15) !important;
        border: 1.5px solid rgba(255, 255, 255, 0.14) !important;
        position: relative;
        z-index: 2;
    }
    div[data-testid="stRadio"] label,
    div[data-testid="stRadio"] label p,
    div[data-testid="stRadio"] label span,
    div[data-testid="stRadio"] div[role="radiogroup"] label {
        background: transparent !important;
        border-radius: 9999px !important;
        padding: 10px 24px !important;
        font-size: 1.05rem !important;
        font-weight: 700 !important;
        color: #FFFFFF !important; /* Bold White Color */
        opacity: 1 !important;
        cursor: pointer !important;
        border: none !important;
        transition: all 0.3s var(--ease-spring) !important;
    }
    div[data-testid="stRadio"] label:hover {
        color: #FFFFFF !important;
        background: rgba(255, 255, 255, 0.1) !important;
        transform: translateY(-2px) scale(1.02) !important;
    }
    div[data-testid="stRadio"] label[data-checked="true"] {
        background: linear-gradient(135deg, #EA580C 0%, #D97706 100%) !important;
        color: #FFFFFF !important;
        box-shadow: 0 4px 18px rgba(234, 88, 12, 0.45), 0 1px 3px rgba(0,0,0,0.1) !important;
    }

    /* Universal Buttons with Spring & Hover Tint */
    .stButton > button,
    button[kind="secondary"],
    button[data-testid="baseButton-secondary"],
    .stDownloadButton > button {
        border-radius: 12px !important;
        font-size: 1.04rem !important;
        font-family: 'Tiro Kannada', 'Plus Jakarta Sans', serif !important;
        font-weight: 600 !important;
        padding: 0.72rem 1.1rem !important;
        background: rgba(255, 255, 255, 0.96) !important;
        border: 1.5px solid rgba(255, 255, 255, 0.25) !important;
        color: #0F172A !important;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.2) !important;
        transition: all 0.35s var(--ease-spring) !important;
        width: 100% !important;
    }
    .stButton > button:hover,
    button[kind="secondary"]:hover,
    button[data-testid="baseButton-secondary"]:hover,
    .stDownloadButton > button:hover {
        background: rgba(254, 215, 170, 0.98) !important;
        border-color: #EA580C !important;
        color: #9A3412 !important;
        transform: translateY(-4px) scale(1.02) !important;
        box-shadow: 0 14px 28px -4px rgba(234, 88, 12, 0.3), 0 0 0 1px rgba(234, 88, 12, 0.25) !important;
    }
    .stButton > button:active,
    button[kind="secondary"]:active,
    button[data-testid="baseButton-secondary"]:active {
        transform: translateY(-1px) scale(0.99) !important;
    }

    /* High-Impact Primary Action Button */
    button[kind="primary"],
    button[data-testid="baseButton-primary"] {
        background: linear-gradient(135deg, #EA580C 0%, #D97706 60%, #B45309 100%) !important;
        border: none !important;
        color: #FFFFFF !important;
        font-weight: 800 !important;
        font-size: 1.15rem !important;
        border-radius: 12px !important;
        padding: 0.85rem 1.6rem !important;
        box-shadow: 0 6px 20px rgba(234, 88, 12, 0.45) !important;
        transition: all 0.35s var(--ease-spring) !important;
    }
    button[kind="primary"]:hover,
    button[data-testid="baseButton-primary"]:hover {
        background: linear-gradient(135deg, #F97316 0%, #EA580C 55%, #C2410C 100%) !important;
        box-shadow: 0 14px 34px -4px rgba(234, 88, 12, 0.55) !important;
        transform: translateY(-4px) scale(1.025) !important;
    }

    /* Starters Container Ribbon */
    .starters-container {
        margin-bottom: 0.75rem;
    }
    .starters-label {
        font-size: 1.05rem;
        font-weight: 700;
        color: #F8FAFC;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* Workspace Panel Header */
    .panel-header-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.75rem;
        padding-bottom: 0.55rem;
        border-bottom: 1.5px solid rgba(255, 255, 255, 0.14);
    }
    .panel-title {
        font-size: 1.18rem;
        font-weight: 700;
        color: #F8FAFC;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .counter-pill {
        font-size: 0.88rem;
        font-weight: 700;
        color: #E2E8F0;
        background: rgba(255, 255, 255, 0.12);
        padding: 4px 12px;
        border-radius: 9999px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
    }

    /* Textarea & Inputs with Clean Card Surface & Glow */
    textarea, .stTextArea textarea, .stTextInput input {
        font-family: 'Tiro Kannada', serif !important;
        font-size: 1.25rem !important;
        line-height: 1.7 !important;
        color: #0F172A !important;
        border-radius: 14px !important;
        background: rgba(255, 255, 255, 0.96) !important;
        border: 1.5px solid rgba(255, 255, 255, 0.25) !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.18) !important;
        transition: all 0.35s var(--ease-smooth) !important;
    }
    textarea:hover, .stTextArea textarea:hover, .stTextInput input:hover {
        background: #FFFFFF !important;
        border-color: rgba(234, 88, 12, 0.75) !important;
        box-shadow: 0 6px 20px rgba(234, 88, 12, 0.15) !important;
    }
    textarea:focus, .stTextArea textarea:focus, .stTextInput input:focus {
        background: #FFFFFF !important;
        border-color: #EA580C !important;
        box-shadow: 0 0 0 3px rgba(234, 88, 12, 0.22) !important;
    }

    /* Luminous Textbook Kannada Output Display */
    .output-kannada-display {
        font-family: 'Tiro Kannada', serif;
        font-size: 1.92rem;
        line-height: 2.0;
        color: #065F46;
        background: linear-gradient(180deg, #FFFFFF 0%, #F0FDF4 100%);
        border: 2px solid #86EFAC;
        border-radius: 14px;
        padding: 1.4rem 1.6rem;
        min-height: 155px;
        box-shadow: 0 6px 22px rgba(6, 95, 70, 0.15);
        transition: all 0.35s var(--ease-spring);
    }
    .output-kannada-display:hover {
        background: rgba(240, 253, 244, 0.98);
        border-color: #10B981;
        transform: translateY(-4px) scale(1.01);
        box-shadow: 0 16px 36px -6px rgba(16, 185, 129, 0.3), 0 0 0 2px rgba(16, 185, 129, 0.25);
    }
    .empty-kannada-placeholder {
        font-size: 1.15rem;
        color: #475569;
        background: rgba(255, 255, 255, 0.88);
        border: 2px dashed #94A3B8;
        border-radius: 14px;
        padding: 3rem 1.5rem;
        text-align: center;
        min-height: 155px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 10px;
        transition: all 0.35s var(--ease-spring);
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
    }
    .empty-kannada-placeholder:hover {
        background: rgba(255, 255, 255, 0.96);
        border-color: #EA580C;
        transform: translateY(-2px);
    }

    /* Morphological Transformation Flow Chips */
    .morph-chip {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(255, 255, 255, 0.95);
        border: 1.5px solid #FED7AA;
        color: #9A3412;
        border-radius: 10px;
        padding: 7px 16px;
        font-size: 1.12rem;
        font-family: 'Tiro Kannada', serif;
        font-weight: 700;
        margin: 5px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
        transition: all 0.35s var(--ease-spring);
        cursor: default;
    }
    .morph-chip:hover {
        background: rgba(254, 215, 170, 0.95);
        border-color: #EA580C;
        transform: translateY(-4px) scale(1.06);
        box-shadow: 0 12px 24px -3px rgba(234, 88, 12, 0.32);
    }
    .chip-arrow {
        color: #EA580C;
        font-weight: 900;
        font-size: 1rem;
    }

    /* Cultural Etymology Manuscript Card */
    .etym-card {
        background: #FFFBEB;
        border-left: 4.5px solid #D97706;
        border-radius: 10px;
        padding: 12px 18px;
        margin-top: 8px;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.15);
        transition: all 0.35s var(--ease-spring);
    }
    .etym-card:hover {
        background: rgba(254, 243, 199, 0.98);
        transform: translateY(-3px) scale(1.01);
        box-shadow: 0 10px 22px rgba(217, 119, 6, 0.22);
    }

    /* Semantic Translation Card */
    .semantic-card {
        background: #FFFFFF;
        border-left: 4.5px solid #4338CA;
        border-radius: 10px;
        padding: 14px 18px;
        font-style: italic;
        font-size: 1.08rem;
        color: #1E1B4B;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.15);
        transition: all 0.35s var(--ease-spring);
    }
    .semantic-card:hover {
        background: rgba(238, 242, 255, 0.95);
        transform: translateY(-3px) scale(1.01);
        box-shadow: 0 10px 22px rgba(67, 56, 202, 0.22);
    }

    /* Page 2: Dialect Cartography Studio Cards */
    .studio-card {
        background: #FFFFFF;
        border: 1.5px solid #E2E8F0;
        border-radius: 14px;
        padding: 1.4rem 1.5rem;
        margin-bottom: 1rem;
        transition: all 0.35s var(--ease-spring);
        position: relative;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.16);
    }
    .studio-card:hover {
        transform: translateY(-6px) scale(1.02);
    }
    .studio-card-hd { border-left: 5px solid #EA580C; }
    .studio-card-hd:hover {
        background: rgba(255, 247, 237, 0.95) !important;
        border-color: #EA580C !important;
        box-shadow: 0 18px 36px -6px rgba(234, 88, 12, 0.32), 0 0 0 1px rgba(234, 88, 12, 0.25) !important;
    }
    .studio-card-kk { border-left: 5px solid #7C3AED; }
    .studio-card-kk:hover {
        background: rgba(245, 243, 255, 0.95) !important;
        border-color: #7C3AED !important;
        box-shadow: 0 18px 36px -6px rgba(124, 58, 237, 0.32), 0 0 0 1px rgba(124, 58, 237, 0.25) !important;
    }
    .studio-card-co { border-left: 5px solid #0284C7; }
    .studio-card-co:hover {
        background: rgba(240, 249, 255, 0.95) !important;
        border-color: #0284C7 !important;
        box-shadow: 0 18px 36px -6px rgba(2, 132, 199, 0.32), 0 0 0 1px rgba(2, 132, 199, 0.25) !important;
    }
    .studio-card-uk { border-left: 5px solid #16A34A; }
    .studio-card-uk:hover {
        background: rgba(240, 253, 244, 0.95) !important;
        border-color: #16A34A !important;
        box-shadow: 0 18px 36px -6px rgba(22, 163, 74, 0.32), 0 0 0 1px rgba(22, 163, 74, 0.25) !important;
    }
    .studio-card-sm { border-left: 5px solid #D97706; }
    .studio-card-sm:hover {
        background: rgba(254, 252, 232, 0.95) !important;
        border-color: #D97706 !important;
        box-shadow: 0 18px 36px -6px rgba(217, 119, 6, 0.32), 0 0 0 1px rgba(217, 119, 6, 0.25) !important;
    }

    /* Page 3: Acoustic Field Audio Item Box */
    .audio-item-box {
        background: #FFFFFF;
        border: 1.5px solid #E2E8F0;
        border-radius: 14px;
        padding: 16px 20px;
        margin-bottom: 14px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.16);
        transition: all 0.35s var(--ease-spring);
    }
    .audio-item-box:hover {
        background: rgba(254, 243, 199, 0.65);
        border-color: #F59E0B;
        transform: translateY(-4px) scale(1.012);
        box-shadow: 0 14px 28px -4px rgba(245, 158, 11, 0.26), 0 0 0 1px rgba(245, 158, 11, 0.25);
    }

    /* History Card */
    .history-card {
        background: #FFFFFF;
        border: 1.5px solid #E2E8F0;
        border-radius: 12px;
        padding: 10px 16px;
        margin-bottom: 8px;
        transition: all 0.3s var(--ease-spring);
    }
    .history-card:hover {
        border-color: #EA580C;
        background: rgba(255, 247, 237, 0.9);
        transform: translateY(-2px);
        box-shadow: 0 8px 18px rgba(234, 88, 12, 0.16);
    }

    /* Editorial Footer */
    .editorial-footer {
        text-align: center;
        margin-top: 3.5rem;
        padding: 2.2rem 1rem 1.2rem 1rem;
        border-top: 1.5px solid rgba(255, 255, 255, 0.14);
        color: #94A3B8;
        position: relative;
        z-index: 2;
    }
    .footer-quote {
        font-family: 'Tiro Kannada', serif;
        font-size: 1.3rem;
        font-weight: 700;
        color: #F8FAFC;
        margin-bottom: 0.35rem;
    }

    @media (prefers-reduced-motion: reduce) {
        *, ::before, ::after {
            animation-duration: 0.01ms !important;
            animation-iteration-count: 1 !important;
            transition-duration: 0.01ms !important;
        }
    }

    /* Image 2: Streamlit Tabs - Change from Grey to Bold White Color */
    button[data-testid="stTab"],
    button[data-testid="stTab"] p,
    button[data-testid="stTab"] span,
    div[data-baseweb="tab-list"] button,
    div[data-baseweb="tab-list"] button p,
    div[data-baseweb="tab-list"] button span,
    div[data-baseweb="tab-list"] [role="tab"] {
        color: #FFFFFF !important; /* Bold White Color */
        font-weight: 700 !important;
        font-size: 1.05rem !important;
        opacity: 1 !important;
        background: transparent !important;
    }
    button[data-testid="stTab"]:hover,
    button[data-testid="stTab"]:hover p,
    div[data-baseweb="tab-list"] button:hover p {
        color: #FDE68A !important; /* Gold on hover */
    }
    button[data-testid="stTab"][aria-selected="true"],
    button[data-testid="stTab"][aria-selected="true"] p,
    div[data-baseweb="tab-list"] button[aria-selected="true"] p {
        color: #FFFFFF !important;
        font-weight: 800 !important;
        border-bottom-color: #EA580C !important;
    }
    div[data-baseweb="tab-highlight"] {
        background-color: #EA580C !important;
    }
    div[data-baseweb="tab-border"] {
        background-color: rgba(255, 255, 255, 0.2) !important;
    }

</style>
""", unsafe_allow_html=True)

# --- Floating Ambient Background Layer (DOM) ---
st.markdown("""
<div class="ambient-background-canvas" aria-hidden="true">
    <div class="ambient-orb orb-indigo"></div>
    <div class="ambient-orb orb-peach"></div>
    <div class="ambient-orb orb-sage"></div>
    <div class="ambient-orb orb-amber"></div>
    <div class="kannada-glyph-watermark"></div>
</div>
""", unsafe_allow_html=True)

# --- Backend Engine Initialization (100% Intact) ---
st.cache_resource.clear()

def get_normalizer():
    norm = DialectNormalizer(gemini_api_key=GEMINI_API_KEY)
    if not norm.ai_rewriter.is_available() and GEMINI_API_KEY:
        norm.ai_rewriter.api_key = GEMINI_API_KEY
    return norm

def get_generator():
    return DialectGenerator()

normalizer = get_normalizer()
generator = get_generator()
exec_mode = "hybrid" if normalizer.ai_rewriter.is_available() else "local"

# --- Session State Management ---
if "input_val" not in st.session_state:
    st.session_state["input_val"] = "ಅವನು ಇವ್ವತ್ ಬರಾಕತ್ತಾನ."

if "nav_tab" not in st.session_state:
    st.session_state["nav_tab"] = "📜 ಪರಿವರ್ತಕ (Live Converter)"

if "history" not in st.session_state:
    st.session_state["history"] = []

if "synth_text_val" not in st.session_state:
    st.session_state["synth_text_val"] = "ಅವನು ಇಂದು ಬರುತ್ತಿದ್ದಾನೆ."

# --- High-Impact Hero: Centered Branding with 360-Degree Rotating Royal Floral Emblem ---
st.markdown("""
<div class="brand-hero-section">
    <div class="brand-title-row">
        <div class="brand-crest-container" title="ನುಡಿ ಸೇತು 360° ತಿರುಗುವ ರಾಜಲಾಂಛನ (Click or hover to accelerate)">
            <svg class="floral-crest-svg" viewBox="0 0 120 120" fill="none" xmlns="http://www.w3.org/2000/svg">
                <defs>
                    <linearGradient id="goldGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stop-color="#FFFBEB" />
                        <stop offset="25%" stop-color="#FDE68A" />
                        <stop offset="55%" stop-color="#F59E0B" />
                        <stop offset="85%" stop-color="#D97706" />
                        <stop offset="100%" stop-color="#92400E" />
                    </linearGradient>
                    <linearGradient id="royalIndigo" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stop-color="#3730A3" />
                        <stop offset="50%" stop-color="#312E81" />
                        <stop offset="100%" stop-color="#1E1B4B" />
                    </linearGradient>
                    <linearGradient id="petalGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stop-color="#FFFBEB" />
                        <stop offset="50%" stop-color="#FDE68A" />
                        <stop offset="100%" stop-color="#F59E0B" />
                    </linearGradient>
                    <filter id="crestShadow" x="-25%" y="-25%" width="150%" height="150%">
                        <feDropShadow dx="0" dy="6" stdDeviation="6" flood-color="#000000" flood-opacity="0.55" />
                    </filter>
                </defs>
                <g>
                    <!-- 8-Petal Blooming Lotus/Jasmine Mandala (360° Rotating) -->
                    <g transform="origin: 60 60">
                        <path d="M60 12 C64 24, 72 32, 60 44 C48 32, 56 24, 60 12 Z" fill="url(#petalGrad)" stroke="#B45309" stroke-width="1.2"/>
                        <path d="M60 12 C64 24, 72 32, 60 44 C48 32, 56 24, 60 12 Z" transform="rotate(45 60 60)" fill="url(#petalGrad)" stroke="#B45309" stroke-width="1.2"/>
                        <path d="M60 12 C64 24, 72 32, 60 44 C48 32, 56 24, 60 12 Z" transform="rotate(90 60 60)" fill="url(#petalGrad)" stroke="#B45309" stroke-width="1.2"/>
                        <path d="M60 12 C64 24, 72 32, 60 44 C48 32, 56 24, 60 12 Z" transform="rotate(135 60 60)" fill="url(#petalGrad)" stroke="#B45309" stroke-width="1.2"/>
                        <path d="M60 12 C64 24, 72 32, 60 44 C48 32, 56 24, 60 12 Z" transform="rotate(180 60 60)" fill="url(#petalGrad)" stroke="#B45309" stroke-width="1.2"/>
                        <path d="M60 12 C64 24, 72 32, 60 44 C48 32, 56 24, 60 12 Z" transform="rotate(225 60 60)" fill="url(#petalGrad)" stroke="#B45309" stroke-width="1.2"/>
                        <path d="M60 12 C64 24, 72 32, 60 44 C48 32, 56 24, 60 12 Z" transform="rotate(270 60 60)" fill="url(#petalGrad)" stroke="#B45309" stroke-width="1.2"/>
                        <path d="M60 12 C64 24, 72 32, 60 44 C48 32, 56 24, 60 12 Z" transform="rotate(315 60 60)" fill="url(#petalGrad)" stroke="#B45309" stroke-width="1.2"/>
                    </g>
                    <!-- Outer Gold Filigree Ring -->
                    <circle cx="60" cy="60" r="41" fill="none" stroke="url(#goldGrad)" stroke-width="3" />
                    <circle cx="60" cy="60" r="37" fill="none" stroke="#FDE68A" stroke-width="1" stroke-dasharray="2.5 3.5" />
                    <!-- Deep Royal Indigo Medallion -->
                    <circle cx="60" cy="60" r="34" fill="url(#royalIndigo)" stroke="#B45309" stroke-width="1.8" />
                    <circle cx="60" cy="60" r="30.5" fill="none" stroke="url(#goldGrad)" stroke-width="1.2" />
                    <!-- Classical Embossed Letter "ನು" -->
                    <text x="60" y="72" font-family="'Tiro Kannada', serif" font-size="33" font-weight="800" text-anchor="middle" fill="url(#goldGrad)" filter="drop-shadow(0 2px 4px rgba(0,0,0,0.75))">ನು</text>
                </g>
            </svg>
        </div>
        <h1 class="brand-title-text">ನುಡಿ ಸೇತು</h1>
    </div>
    <div>
        <span class="brand-sub-badge">
            ಕರ್ನಾಟಕದ ಪ್ರಾದೇಶಿಕ ಆಡುಭಾಷೆಗಳಿಂದ ಪ್ರಮಾಣ ಗ್ರಾಂಥಿಕ ಕನ್ನಡಕ್ಕೆ • <b>Spoken Dialect ➔ Textbook Kannada</b>
        </span>
    </div>
</div>
""", unsafe_allow_html=True)

# --- Glassmorphic 3-Pill Navigation Switcher ---
nav_options = [
    "📜 ಪರಿವರ್ತಕ (Live Converter)",
    "🌐 ನುಡಿ ಸಂಶ್ಲೇಷಕ (Dialect Synthesizer)",
    "🎙️ ಧ್ವನಿ & ಕಾರ್ಪಸ್ (Audio & Corpus Hub)"
]

current_idx = 0
if "ಸಂಶ್ಲೇಷಕ" in st.session_state["nav_tab"]:
    current_idx = 1
elif "ಧ್ವನಿ" in st.session_state["nav_tab"] or "ಕಾರ್ಪಸ್" in st.session_state["nav_tab"]:
    current_idx = 2

nav_choice = st.radio(
    "Navigation",
    options=nav_options,
    index=current_idx,
    horizontal=True,
    label_visibility="collapsed",
    key="nav_selection_radio"
)
st.session_state["nav_tab"] = nav_choice


# ==============================================================================
# PAGE 1: 📜 ಪರಿವರ್ತಕ (LIVE DIALECT CONVERTER)
# ==============================================================================
if "ಪರಿವರ್ತಕ" in st.session_state["nav_tab"]:

    # --- Quick Test Starters Bar with Smooth Spring Hover Animations ---
    st.markdown("""
    <div class="starters-container">
        <div class="starters-label">
            <span>⚡</span> <b>ತ್ವರಿತ ಪರೀಕ್ಷಾ ವಾಕ್ಯಗಳು (Starter Dialect Sentences):</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_s1, col_s2, col_s3, col_s4, col_s5 = st.columns(5)
    with col_s1:
        if st.button("🌾 ಏನ್ರಿ, ಊಟ ಆತೇನ್ರಿ?", use_container_width=True, help="Hubballi-Dharwad honorific"):
            st.session_state["input_val"] = "ಏನ್ರಿ, ಊಟ ಆತೇನ್ರಿ?"
            st.rerun()
    with col_s2:
        if st.button("🌊 ಎಂತ ಮಾಡ್ತಾ ಇದ್ದೀರಿ?", use_container_width=True, help="Mangaluru coastal question"):
            st.session_state["input_val"] = "ಎಂತ ಮಾಡ್ತಾ ಇದ್ದೀರಿ?"
            st.rerun()
    with col_s3:
        if st.button("🌿 ಹೆಂಗಿದ್ದೀರಿ, ಊಟಕ್ಕೆ ಬರ್ತೀರಾ?", use_container_width=True, help="Uttara Kannada greeting"):
            st.session_state["input_val"] = "ಹೆಂಗಿದ್ದೀರಿ, ಊಟಕ್ಕೆ ಬರ್ತೀರಾ?"
            st.rerun()
    with col_s4:
        if st.button("🛒 ದೋಸ್ತ್, ರೊಕ್ಕ ಕೊಡತಿಯಾ?", use_container_width=True, help="Kalyana Karnataka market"):
            st.session_state["input_val"] = "ದೋಸ್ತ್, ರೊಕ್ಕ ಕೊಡತಿಯಾ?"
            st.rerun()
    with col_s5:
        if st.button("⚡ ಅವನು ಇವ್ವತ್ ಬರಾಕತ್ತಾನ.", use_container_width=True, help="Aspectual continuous"):
            st.session_state["input_val"] = "ಅವನು ಇವ್ವತ್ ಬರಾಕತ್ತಾನ."
            st.rerun()

    st.write("")

    # Dialect Selector Dropdown
    col_sel, col_mode_toggle = st.columns([2, 1])
    with col_sel:
        selected_dialect_choice = st.selectbox(
            "📍 ಪ್ರಾದೇಶಿಕ ಉಪಭಾಷೆ ಆಯ್ಕೆ (Dialect Selection):",
            options=[
                "🔍 ಸ್ವಯಂ ಪತ್ತೆ (Auto-Detect)",
                "🌾 Hubballi-Dharwad (ಹುಬ್ಬಳ್ಳಿ-ಧಾರವಾಡ)",
                "🌊 Mangaluru (ಮಂಗಳೂರು / ಕುಂದಗನ್ನಡ)",
                "🌿 Uttara Kannada (ಉತ್ತರ ಕನ್ನಡ / ಹವ್ಯಕ)"
            ],
            index=0,
            help="ಆಯ್ಕೆಮಾಡಿದ ಪ್ರಾಂತ್ಯದ ನಿಯಮಗಳನ್ನು ನಿರ್ದಿಷ್ಟವಾಗಿ ಅನ್ವಯಿಸುತ್ತದೆ."
        )
    with col_mode_toggle:
        st.write("")
        st.markdown("""
        <div style="text-align: right; margin-top: 10px; font-weight: 700; font-size: 0.95rem; color: #4ADE80;">
            ✅ 100% Offline Rule Engine + AI
        </div>
        """, unsafe_allow_html=True)

    region_mapping = {
        "🔍 ಸ್ವಯಂ ಪತ್ತೆ (Auto-Detect)": None,
        "🌾 Hubballi-Dharwad (ಹುಬ್ಬಳ್ಳಿ-ಧಾರವಾಡ)": "North Karnataka",
        "🌊 Mangaluru (ಮಂಗಳೂರು / ಕುಂದಗನ್ನಡ)": "Coastal / Kundagannada",
        "🌿 Uttara Kannada (ಉತ್ತರ ಕನ್ನಡ / ಹವ್ಯಕ)": "Uttara Kannada / Havyaka"
    }
    target_region = region_mapping.get(selected_dialect_choice)

    # --- Core Dual-Panel Workspace ---
    col_left, col_right = st.columns(2)

    raw_input = st.session_state.get("input_val", "")
    char_count = len(raw_input)
    word_count = len(raw_input.split()) if raw_input.strip() else 0

    is_kanglish = bool(re.search(r'[a-zA-Z]', raw_input))

    with col_left:
        st.markdown(f"""
        <div class="panel-header-row">
            <span class="panel-title">🗣️ ಪ್ರಾದೇಶಿಕ ಆಡುಮಾತು (Spoken Dialect)</span>
            <span class="counter-pill">{word_count} ಪದಗಳು • {char_count} ಅಕ್ಷರಗಳು</span>
        </div>
        """, unsafe_allow_html=True)

        user_input = st.text_area(
            "ಆಡುಮಾತಿನ ವಾಕ್ಯ:",
            value=st.session_state["input_val"],
            height=155,
            label_visibility="collapsed",
            placeholder="ಯಾವುದೇ ಪ್ರಾದೇಶಿಕ ಆಡುಮಾತಿನ ವಾಕ್ಯವನ್ನು ಇಲ್ಲಿ ಟೈಪ್ ಮಾಡಿ (ಅಥವಾ ಇಂಗ್ಲಿಷ್‌ನಲ್ಲಿ 'avanu bartana' ಎಂದೂ ಟೈಪ್ ಮಾಡಬಹುದು)..."
        )

        if is_kanglish and user_input.strip():
            st.caption("✨ Kanglish ಪತ್ತೆಯಾಗಿದೆ: ಸಿಸ್ಟಮ್ ಸ್ವಯಂಚಾಲಿತವಾಗಿ ಕನ್ನಡ ಲಿಪಿಗೆ ಪರಿವರ್ತಿಸಿ ಸಾಮಾನ್ಯೀಕರಿಸುತ್ತದೆ.")

        col_btn_run, col_btn_clear = st.columns([3, 1])
        with col_btn_run:
            convert_clicked = st.button("🚀 ಪ್ರಮಾಣ ಕನ್ನಡಕ್ಕೆ ಪರಿವರ್ತಿಸಿ (Convert)", type="primary", use_container_width=True)
        with col_btn_clear:
            if st.button("🔄 ತೆರವು (Clear)", use_container_width=True):
                st.session_state["input_val"] = ""
                st.rerun()

        # Collapsible Direct Kanglish Guide
        with st.expander("⌨️ ಲ್ಯಾಪ್ಟಾಪ್‌ನಲ್ಲಿ ನೇರವಾಗಿ ಟೈಪ್ ಮಾಡುವುದು ಹೇಗೆ? (Direct Kanglish)", expanded=False):
            st.markdown("""
            - **ಕನ್ನಡ ಕೀಬೋರ್ಡ್ ಇಲ್ಲದಿದ್ದರೂ ಚಿಂತೆ ಬೇಡ!**
            - ಮೇಲಿನ ಬಾಕ್ಸ್‌ನಲ್ಲಿ ಇಂಗ್ಲಿಷ್‌ನಲ್ಲಿ `avanu bartana`, `naale hogbeku`, `baralla` ಎಂದು ಟೈಪ್ ಮಾಡಿದರೆ ಸಾಕು, ಸಿಸ್ಟಮ್ ತಾನಾಗಿಯೇ ಕನ್ನಡಕ್ಕೆ ಬದಲಾಯಿಸಿ ಪರಿವರ್ತಿಸುತ್ತದೆ.
            """)

    with col_right:
        res = None
        if user_input and user_input.strip():
            with st.spinner("ಪರಿವರ್ತಿಸಲಾಗುತ್ತಿದೆ..."):
                res = normalizer.normalize(user_input.strip(), target_region=target_region, mode=exec_mode)

            if res and res.get("standard_text"):
                hist_item = {
                    "input": user_input.strip(),
                    "output": res["standard_text"],
                    "region": res.get("region_name_kn", "ಸಾಮಾನ್ಯ ಆಡುಮಾತು")
                }
                if not st.session_state["history"] or st.session_state["history"][0]["input"] != hist_item["input"]:
                    st.session_state["history"].insert(0, hist_item)
                    st.session_state["history"] = st.session_state["history"][:5]

        region_badge_text = ""
        if res and res.get("standard_text"):
            conf = res.get("confidence", 0.95)
            conf_percent = int(conf * 100) if conf else 95
            if target_region is None or res.get("is_auto_detected", True):
                region_badge_text = f"📍 {res.get('region_name_kn', 'ಸಾಮಾನ್ಯ ಆಡುಮಾತು')} ({conf_percent}% ಖಚಿತತೆ)"
            else:
                chosen_name = selected_dialect_choice.split("(")[0].strip()
                region_badge_text = f"🎯 {chosen_name}"

        st.markdown(f"""
        <div class="panel-header-row">
            <span class="panel-title">✍️ ಪ್ರಮಾಣ ಗ್ರಾಂಥಿಕ ಕನ್ನಡ (Standard Kannada)</span>
            <span class="counter-pill" style="color: #065F46; background: #DCFCE7;">{region_badge_text if region_badge_text else 'ಸಿದ್ಧವಾಗಿದೆ'}</span>
        </div>
        """, unsafe_allow_html=True)

        if res and res.get("standard_text"):
            st.markdown(f"""
            <div class="output-kannada-display">
                {res["standard_text"]}
            </div>
            """, unsafe_allow_html=True)

            clean_audio_text = res["standard_text"].replace("'", "\\'").replace('"', '\\"')
            audio_bar_html = f"""
            <style>
                .audio-action-btn {{
                    transition: all 0.35s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
                }}
                .audio-action-btn:hover {{
                    transform: translateY(-3px) scale(1.03) !important;
                    filter: brightness(1.12) !important;
                }}
                .audio-action-btn:active {{
                    transform: translateY(0px) scale(0.98) !important;
                }}
            </style>
            <div style="margin-top: 14px; display: flex; gap: 12px; align-items: center; flex-wrap: wrap; font-family: 'Plus Jakarta Sans', sans-serif;">
                <button onclick="playKannadaSpeech(0.9)" class="audio-action-btn" style="background: #15803D; color: white; border: none; padding: 10px 18px; border-radius: 10px; font-weight: 700; cursor: pointer; font-size: 0.98rem; display: flex; align-items: center; gap: 7px; box-shadow: 0 4px 12px rgba(21, 128, 61, 0.25);">
                    🔊 ಆಲಿಸಿ (Read Aloud)
                </button>
                <button onclick="playKannadaSpeech(0.75)" class="audio-action-btn" style="background: #166534; color: #DCFCE7; border: 1px solid #86EFAC; padding: 10px 14px; border-radius: 10px; font-weight: 700; cursor: pointer; font-size: 0.9rem;">
                    🐢 ನಿಧಾನ (0.75x)
                </button>
                <button onclick="copyOutputText()" id="copyBtn" class="audio-action-btn" style="background: #1E1B4B; color: white; border: none; padding: 10px 18px; border-radius: 10px; font-weight: 700; cursor: pointer; font-size: 0.98rem; display: flex; align-items: center; gap: 7px; box-shadow: 0 4px 12px rgba(30, 27, 75, 0.25);">
                    📋 ನಕಲಿಸಿ (Copy)
                </button>
                <span id="copyMsg" style="color: #4ADE80; font-weight: 700; font-size: 0.95rem;"></span>
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
                document.getElementById('copyMsg').innerText = '✅ ಯಶಸ್ವಿಯಾಗಿ ನಕಲಿಸಲಾಗಿದೆ!';
                setTimeout(function() {{
                    document.getElementById('copyMsg').innerText = '';
                }}, 2200);
            }}
            function playKannadaSpeech(rate) {{
                if ('speechSynthesis' in window) {{
                    window.speechSynthesis.cancel();
                    var utterance = new SpeechSynthesisUtterance('{clean_audio_text}');
                    utterance.lang = 'kn-IN';
                    utterance.rate = rate || 0.9;
                    window.speechSynthesis.speak(utterance);
                }} else {{
                    alert('Audio playback is not supported in this browser.');
                }}
            }}
            </script>
            """
            st.components.v1.html(audio_bar_html, height=60)
        else:
            st.markdown("""
            <div class="empty-kannada-placeholder">
                <div style="font-family: 'Tiro Kannada', serif; font-size: 2.2rem; font-weight: 800; color: #EA580C; margin-bottom: -4px;">ನು</div>
                <span style="font-weight: 700; color: #1E293B;">ಎಡಭಾಗದ ಬಾಕ್ಸ್‌ನಲ್ಲಿ ವಾಕ್ಯ ನಮೂದಿಸಿ <b>'ಪರಿವರ್ತಿಸಿ'</b> ಕ್ಲಿಕ್ ಮಾಡಿ.</span>
                <span style="font-size: 0.98rem; color: #475569;">ಶಿಷ್ಟ ಗ್ರಾಂಥಿಕ ಕನ್ನಡ ರೂಪಾಂತರವು ಸುಂದರವಾಗಿ ಇಲ್ಲಿ ಮೂಡಿಬರುತ್ತದೆ.</span>
            </div>
            """, unsafe_allow_html=True)

    # --- Linguistic Analysis Chips ---
    if res and res.get("standard_text"):
        st.markdown("<hr style='border: none; border-top: 1.5px solid rgba(255, 255, 255, 0.14); margin: 1.8rem 0 1.2rem 0;'>", unsafe_allow_html=True)
        col_m1, col_m2 = st.columns([3, 2])
        with col_m1:
            if res.get("transformations"):
                st.markdown("##### 🔍 ಬದಲಾದ ಪ್ರಾದೇಶಿಕ ಪದಗಳು (Morphological Transformations):")
                chips_html = ""
                for t in res["transformations"]:
                    chips_html += f'<span class="morph-chip"><b>{t.get("dialect", "")}</b> <span class="chip-arrow">➔</span> <b>{t.get("standard", "")}</b></span> '
                st.markdown(chips_html, unsafe_allow_html=True)
            elif res.get("rules_applied"):
                st.markdown("##### 📝 ಅನ್ವಯಿಸಲಾದ ವ್ಯಾಕರಣ ನಿಯಮಗಳು (Grammar Rules Applied):")
                for r in res["rules_applied"][:2]:
                    st.info(f"• {r.get('description', '')}")

            if res.get("etymology"):
                st.markdown("##### 💡 ಸಾಂಸ್ಕೃತಿಕ ಹಿನ್ನೆಲೆ (Cultural Etymology):")
                for et in res["etymology"]:
                    st.markdown(f"""
                    <div class="etym-card">
                        <span style="font-weight: 800; color: #92400E;">📖 '{et["word"]}' ➔ {et["standard"]} ({et["region"]})</span><br>
                        <span style="color: #78350F; font-size: 0.95rem;">{et["context"]}</span>
                    </div>
                    """, unsafe_allow_html=True)

        with col_m2:
            if res.get("english_meaning"):
                st.markdown("##### 🌐 English Semantic Translation:")
                st.markdown(f"""
                <div class="semantic-card">
                    "{res["english_meaning"]}"
                </div>
                """, unsafe_allow_html=True)

    # --- History Drawer ---
    if st.session_state["history"]:
        with st.expander("🕒 ಇತ್ತೀಚಿನ ಪರಿವರ್ತನೆಗಳು (Recent Conversion History)", expanded=False):
            for i, h in enumerate(st.session_state["history"]):
                col_h_text, col_h_btn = st.columns([4, 1])
                with col_h_text:
                    st.markdown(f"**{h['input']}** ➔ *{h['output']}* `{h['region']}`")
                with col_h_btn:
                    if st.button("ಪುನಃ ಬಳಸಿ", key=f"btn_hist_{i}"):
                        st.session_state["input_val"] = h["input"]
                        st.rerun()


# ==============================================================================
# PAGE 2: 🌐 ನುಡಿ ಸಂಶ್ಲೇಷಕ (CROSS-DIALECT SYNTHESIZER & RULE MATRIX)
# ==============================================================================
elif "ಸಂಶ್ಲೇಷಕ" in st.session_state["nav_tab"]:
    st.markdown("### 🌐 ಅಖಿಲ ಕರ್ನಾಟಕ ನುಡಿ ಸಂಶ್ಲೇಷಕ (Cross-Dialect Speech Synthesizer)")
    st.caption("ಯಾವುದೇ ಪ್ರಮಾಣ ವಾಕ್ಯವನ್ನು ಕರ್ನಾಟಕದ 5 ಪ್ರಮುಖ ಪ್ರಾದೇಶಿಕ ಆಡುಭಾಷೆಗಳಿಗೆ ಪರಿವರ್ತಿಸಿ ನೋಡಿ:")

    # Quick preset buttons for judges
    col_pr1, col_pr2, col_pr3, col_pr4 = st.columns(4)
    with col_pr1:
        if st.button("ಅವನು ಇಂದು ಬರುತ್ತಿದ್ದಾನೆ.", key="pr1"):
            st.session_state["synth_text_val"] = "ಅವನು ಇಂದು ಬರುತ್ತಿದ್ದಾನೆ."
            st.rerun()
    with col_pr2:
        if st.button("ನಾಳೆ ಶಾಲೆಗೆ ಹೋಗಬೇಕು.", key="pr2"):
            st.session_state["synth_text_val"] = "ನಾಳೆ ಶಾಲೆಗೆ ಹೋಗಬೇಕು."
            st.rerun()
    with col_pr3:
        if st.button("ನನಗೆ ಸ್ವಲ್ಪ ಹಣ ಕೊಡಿ.", key="pr3"):
            st.session_state["synth_text_val"] = "ನನಗೆ ಸ್ವಲ್ಪ ಹಣ ಕೊಡಿ."
            st.rerun()
    with col_pr4:
        if st.button("ನೀವು ಏನು ಮಾಡುತ್ತಿದ್ದೀರಿ?", key="pr4"):
            st.session_state["synth_text_val"] = "ನೀವು ಏನು ಮಾಡುತ್ತಿದ್ದೀರಿ?"
            st.rerun()

    col_synth_in, col_synth_act = st.columns([4, 1])
    with col_synth_in:
        synth_input = st.text_input(
            "ಪ್ರಮಾಣ ಗ್ರಾಂಥಿಕ ವಾಕ್ಯ ನಮೂದಿಸಿ:",
            value=st.session_state["synth_text_val"],
            placeholder="ಉದಾಹರಣೆಗೆ: ಅವನು ಇಂದು ಬರುತ್ತಿದ್ದಾನೆ."
        )
    with col_synth_act:
        st.write("")
        st.write("")
        if st.button("🔄 ಸಂಶ್ಲೇಷಿಸಿ (Generate)", use_container_width=True):
            st.session_state["synth_text_val"] = synth_input
            st.rerun()

    if synth_input:
        canonical_synth = synth_input.strip()
        norm_synth = normalizer.normalize(canonical_synth)
        if norm_synth and norm_synth.get("all_dialects"):
            synth_results = norm_synth["all_dialects"]
        else:
            if norm_synth and norm_synth.get("standard_text"):
                canonical_synth = norm_synth["standard_text"]
            synth_results = generator.generate_all_dialects(canonical_synth)

        # Row 1: North Karnataka, Coastal Kundagannada, Uttara Kannada
        col_d1, col_d2, col_d3 = st.columns(3)
        with col_d1:
            hd_data = synth_results.get("North Karnataka", {})
            hd_text = hd_data.get('text', synth_input)
            st.markdown(f"""
            <div class="studio-card studio-card-hd">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <span style="font-weight: 800; font-size: 1.15rem; color: #9A3412;">🌾 ಹುಬ್ಬಳ್ಳಿ-ಧಾರವಾಡ</span>
                    <span style="font-size: 0.8rem; font-weight: 700; background: #FFEDD5; color: #9A3412; padding: 2px 8px; border-radius: 6px;">ಉತ್ತರ ಕರ್ನಾಟಕ</span>
                </div>
                <div style="font-family: 'Tiro Kannada', serif; font-size: 1.55rem; font-weight: 700; color: #0F172A; margin: 12px 0;">
                    {hd_text}
                </div>
                <div style="font-size: 0.92rem; color: #64748B;">
                    ಪ್ರಮುಖ ಲಕ್ಷಣ: <b>{hd_data.get('accent_tag', '-ಆಕತ್ತ ಕ್ರಿಯಾಪದ')}</b>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("🚀 ಪರಿವರ್ತಕದಲ್ಲಿ ಪರೀಕ್ಷಿಸಿ", key="btn_hd_test"):
                st.session_state["input_val"] = hd_text
                st.session_state["nav_tab"] = "📜 ಪರಿವರ್ತಕ (Live Converter)"
                st.rerun()

        with col_d2:
            co_data = synth_results.get("Coastal / Kundagannada", {})
            co_text = co_data.get('text', synth_input)
            st.markdown(f"""
            <div class="studio-card studio-card-co">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <span style="font-weight: 800; font-size: 1.15rem; color: #0369A1;">🌊 ಮಂಗಳೂರು / ಕರಾವಳಿ</span>
                    <span style="font-size: 0.8rem; font-weight: 700; background: #E0F2FE; color: #0369A1; padding: 2px 8px; border-radius: 6px;">ಕುಂದಗನ್ನಡ</span>
                </div>
                <div style="font-family: 'Tiro Kannada', serif; font-size: 1.55rem; font-weight: 700; color: #0F172A; margin: 12px 0;">
                    {co_text}
                </div>
                <div style="font-size: 0.92rem; color: #64748B;">
                    ಪ್ರಮುಖ ಲಕ್ಷಣ: <b>{co_data.get('accent_tag', 'ಎಂತ ಮಾರೆ & ಕರಾವಳಿ ಕ್ರಿಯಾರೂಪ')}</b>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("🚀 ಪರಿವರ್ತಕದಲ್ಲಿ ಪರೀಕ್ಷಿಸಿ", key="btn_co_test"):
                st.session_state["input_val"] = co_text
                st.session_state["nav_tab"] = "📜 ಪರಿವರ್ತಕ (Live Converter)"
                st.rerun()

        with col_d3:
            uk_data = synth_results.get("Uttara Kannada / Havyaka", {})
            uk_text = uk_data.get('text', synth_input)
            st.markdown(f"""
            <div class="studio-card studio-card-uk">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <span style="font-weight: 800; font-size: 1.15rem; color: #166534;">🌿 ಉತ್ತರ ಕನ್ನಡ / ಹವ್ಯಕ</span>
                    <span style="font-size: 0.8rem; font-weight: 700; background: #DCFCE7; color: #166534; padding: 2px 8px; border-radius: 6px;">ಮಲೆನಾಡು</span>
                </div>
                <div style="font-family: 'Tiro Kannada', serif; font-size: 1.55rem; font-weight: 700; color: #0F172A; margin: 12px 0;">
                    {uk_text}
                </div>
                <div style="font-size: 0.92rem; color: #64748B;">
                    ಪ್ರಮುಖ ಲಕ್ಷಣ: <b>{uk_data.get('accent_tag', 'ಅನುನಾಸಿಕ ಸರ್ವನಾಮಗಳು')}</b>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("🚀 ಪರಿವರ್ತಕದಲ್ಲಿ ಪರೀಕ್ಷಿಸಿ", key="btn_uk_test"):
                st.session_state["input_val"] = uk_text
                st.session_state["nav_tab"] = "📜 ಪರಿವರ್ತಕ (Live Converter)"
                st.rerun()

        # Row 2: Kalyana Karnataka & Mysuru-Mandya
        col_d4, col_d5 = st.columns(2)
        with col_d4:
            kk_data = synth_results.get("Kalyana Karnataka", {})
            kk_text = kk_data.get('text', synth_input)
            st.markdown(f"""
            <div class="studio-card studio-card-kk">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <span style="font-weight: 800; font-size: 1.15rem; color: #6D28D9;">🕌 ಕಲ್ಯಾಣ ಕರ್ನಾಟಕ</span>
                    <span style="font-size: 0.8rem; font-weight: 700; background: #EDE9FE; color: #6D28D9; padding: 2px 8px; border-radius: 6px;">ಕಲಬುರಗಿ / ಬೀದರ್</span>
                </div>
                <div style="font-family: 'Tiro Kannada', serif; font-size: 1.55rem; font-weight: 700; color: #0F172A; margin: 12px 0;">
                    {kk_text}
                </div>
                <div style="font-size: 0.92rem; color: #64748B;">
                    ಪ್ರಮುಖ ಲಕ್ಷಣ: <b>{kk_data.get('accent_tag', '-ಲಿಕ್ಕತ್ತ ಪ್ರತ್ಯಯ')}</b>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("🚀 ಪರಿವರ್ತಕದಲ್ಲಿ ಪರೀಕ್ಷಿಸಿ", key="btn_kk_test"):
                st.session_state["input_val"] = kk_text
                st.session_state["nav_tab"] = "📜 ಪರಿವರ್ತಕ (Live Converter)"
                st.rerun()

        with col_d5:
            sm_data = synth_results.get("Mysuru-Mandya", {})
            sm_text = sm_data.get('text', synth_input)
            st.markdown(f"""
            <div class="studio-card studio-card-sm">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <span style="font-weight: 800; font-size: 1.15rem; color: #B45309;">🏛️ ಮೈಸೂರು-ಮಂಡ್ಯ</span>
                    <span style="font-size: 0.8rem; font-weight: 700; background: #FEF3C7; color: #B45309; padding: 2px 8px; border-radius: 6px;">ದಕ್ಷಿಣ ಕರ್ನಾಟಕ</span>
                </div>
                <div style="font-family: 'Tiro Kannada', serif; font-size: 1.55rem; font-weight: 700; color: #0F172A; margin: 12px 0;">
                    {sm_text}
                </div>
                <div style="font-size: 0.92rem; color: #64748B;">
                    ಪ್ರಮುಖ ಲಕ್ಷಣ: <b>{sm_data.get('accent_tag', '-ಆವನೆ & ಕಣ್ರೀ')}</b>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("🚀 ಪರಿವರ್ತಕದಲ್ಲಿ ಪರೀಕ್ಷಿಸಿ", key="btn_sm_test"):
                st.session_state["input_val"] = sm_text
                st.session_state["nav_tab"] = "📜 ಪರಿವರ್ತಕ (Live Converter)"
                st.rerun()

    st.markdown("<hr style='border: none; border-top: 1.5px solid rgba(255, 255, 255, 0.14); margin: 2rem 0 1.2rem 0;'>", unsafe_allow_html=True)
    st.markdown("##### 🧩 ನಿಯಮಾಧಾರಿತ ಎಂಜಿನ್‌ನ ರೂಪಾಂತರ ತರ್ಕ (Morphological Rule Matrix):")
    rules_data = [
        {"ವರ್ಗ (Category)": "ಆಸ್ಪೆಕ್ಚುವಲ್ ಕಂಟಿನ್ಯೂಯಸ್ (Aspectual Continuous)", "ಆಡುಮಾತಿನ ಪ್ರತ್ಯಯ (Dialect Suffix)": "-ಆಕತ್ತಾನ, -ಲಿಕ್ಕತ್ತಾನ", "ಪ್ರಮಾಣ ರೂಪ (Standard Kannada)": "-ಉತ್ತಿದ್ದಾನೆ / -ಉತ್ತಿದ್ದಾಳೆ", "ಪ್ರಾಂತ್ಯ (Region)": "ಉತ್ತರ / ಕಲ್ಯಾಣ ಕರ್ನಾಟಕ"},
        {"ವರ್ಗ (Category)": "ಕರಾವಳಿ ಭವಿಷ್ಯತ್ ಪ್ರತ್ಯಯ (Coastal Future)", "ಆಡುಮಾತಿನ ಪ್ರತ್ಯಯ (Dialect Suffix)": "-ಪೆ, -ವೆ (ಬರ್ಪೆ, ಪೋಪೆ)", "ಪ್ರಮಾಣ ರೂಪ (Standard Kannada)": "-ತ್ತೇನೆ / -ತ್ತೇವೆ", "ಪ್ರಾಂತ್ಯ (Region)": "ಮಂಗಳೂರು / ಕುಂದಗನ್ನಡ"},
        {"ವರ್ಗ (Category)": "ಹವ್ಯಕ ಹ್ಯಾಬಿಚುಯಲ್ (Habitual)", "ಆಡುಮಾತಿನ ಪ್ರತ್ಯಯ (Dialect Suffix)": "-ವುತ್ತೆ (ಸುರಿವುತ್ತೆ, ಬರ್ವುತ್ತೆ)", "ಪ್ರಮಾಣ ರೂಪ (Standard Kannada)": "-ತ್ತದೆ / -ತ್ತಿದೆ", "ಪ್ರಾಂತ್ಯ (Region)": "ಉತ್ತರ ಕನ್ನಡ / ಹವ್ಯಕ"},
        {"ವರ್ಗ (Category)": "ಗೌರವಾರ್ಥಕ ಪ್ರಶ್ನೆ (Honorific Inquiries)", "ಆಡುಮಾತಿನ ಪ್ರತ್ಯಯ (Dialect Suffix)": "-ಏನ್ರಿ, -ಐತ್ರಿ, -ಆತೇನ್ರಿ", "ಪ್ರಮಾಣ ರೂಪ (Standard Kannada)": "-ಆ? / -ಆಯಿತೇ?", "ಪ್ರಾಂತ್ಯ (Region)": "ಹುಬ್ಬಳ್ಳಿ-ಧಾರವಾಡ"},
        {"ವರ್ಗ (Category)": "ಮೋಡಲ್ ಸಂಕೋಚನ (Modal Contractions)", "ಆಡುಮಾತಿನ ಪ್ರತ್ಯಯ (Dialect Suffix)": "-್ಬೇಕು, -್ಬಾರ್ದು", "ಪ್ರಮಾಣ ರೂಪ (Standard Kannada)": "-ಬೇಕು, -ಬಾರದು", "ಪ್ರಾಂತ್ಯ (Region)": "ಅಖಿಲ ಕರ್ನಾಟಕ ಆಡುಮಾತು"},
        {"ವರ್ಗ (Category)": "ಅನುನಾಸಿಕ ಸರ್ವನಾಮಗಳು (Nasal Pronouns)", "ಆಡುಮಾತಿನ ಪ್ರತ್ಯಯ (Dialect Suffix)": "ನಾಂ, ನೀಂ, ಅವಂ, ಅವಳ್", "ಪ್ರಮಾಣ ರೂಪ (Standard Kannada)": "ನಾನು, ನೀನು, ಅವನು, ಅವಳು", "ಪ್ರಾಂತ್ಯ (Region)": "ಹವ್ಯಕ / ಕರಾವಳಿ"}
    ]
    st.dataframe(pd.DataFrame(rules_data), use_container_width=True, hide_index=True)


# ==============================================================================
# PAGE 3: 🎙️ ಧ್ವನಿ & ಕಾರ್ಪಸ್ (AUDIO BONUS & LINGUISTIC CORPUS HUB)
# ==============================================================================
else:
    st.markdown("### 🎙️ ಧ್ವನಿ & ಕಾರ್ಪಸ್ ಕೋಶ (Audio Bonus & Linguistic Corpus Hub)")

    c_tab1, c_tab2, c_tab3 = st.tabs([
        "🎧 ದೃಢೀಕರಿಸಿದ ಆಡಿಯೋ ರೆಕಾರ್ಡಿಂಗ್‌ಗಳು (16 kHz WAV Audio)",
        "📖 ಉಪಭಾಷಾ ಪದಕೋಶ (Glossary - 136 Terms)",
        "📜 ಪ್ಯಾರಲಲ್ ಕಾರ್ಪಸ್ (Parallel Corpus - 320 Pairs)"
    ])

    # --- TAB 1: 16 kHz Audio Bonus ---
    with c_tab1:
        st.write("")
        st.markdown("##### 🎙️ 16 kHz Mono WAV ದೃಢೀಕರಿಸಿದ ನೈಜ ಧ್ವನಿ ರೆಕಾರ್ಡಿಂಗ್‌ಗಳು (Field Audio Recordings):")
        manifest_path = "data/audio/audio_manifest.csv"
        if os.path.exists(manifest_path):
            df_audio = pd.read_csv(manifest_path)
            for idx, row in df_audio.iterrows():
                audio_file_path = os.path.join("data/audio", row["audio_filename"])
                with st.container():
                    st.markdown(f"""
                    <div class="audio-item-box">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                            <span style="font-weight: 800; font-size: 1.1rem; color: #1E1B4B;">
                                🎧 {row['audio_filename']} — {row['dialect']} ({row['town']})
                            </span>
                            <span style="font-size: 0.8rem; font-weight: 700; background: #FEF3C7; color: #92400E; padding: 3px 10px; border-radius: 9999px;">
                                {row['duration_sec']}s • 16 kHz WAV
                            </span>
                        </div>
                        <div style="font-family: 'Tiro Kannada', serif; font-size: 1.35rem; font-weight: 700; color: #9A3412; margin: 6px 0;">
                            🗣️ "{row['dialect_text']}"
                        </div>
                        <div style="font-size: 1rem; color: #065F46; font-weight: 600;">
                            ✍️ ಪ್ರಮಾಣ ರೂಪ: "{row['standard_text']}"
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    col_aud_play, col_aud_dl, col_aud_test = st.columns([3, 1, 1])
                    with col_aud_play:
                        if os.path.exists(audio_file_path):
                            st.audio(audio_file_path, format="audio/wav")
                    with col_aud_dl:
                        if os.path.exists(audio_file_path):
                            with open(audio_file_path, "rb") as f:
                                st.download_button("📥 WAV ಡೌನ್‌ಲೋಡ್", data=f.read(), file_name=row['audio_filename'], mime="audio/wav", key=f"dl_aud_{idx}")
                    with col_aud_test:
                        if st.button("🚀 ಪರಿವರ್ತಿಸಿ", key=f"btn_audio_{idx}", help="Load this spoken sentence into Live Converter"):
                            st.session_state["input_val"] = row["dialect_text"]
                            st.session_state["nav_tab"] = "📜 ಪರಿವರ್ತಕ (Live Converter)"
                            st.rerun()
                    st.write("")
        else:
            st.info("ಆಡಿಯೋ ಮ್ಯಾನಿಫೆಸ್ಟ್ ಲಭ್ಯವಿಲ್ಲ.")

    # --- TAB 2: Glossary ---
    with c_tab2:
        st.write("")
        col_sch_text1, col_sch_dialect1 = st.columns([3, 1])
        with col_sch_text1:
            search_query1 = st.text_input("ಪದಕೋಶ ಶೋಧಿಸಿ (Search in Kannada / English):", placeholder="ಉದಾ: ರೊಕ್ಕ, ಮಾರೆ, ಬರಾಕತ್ತಾನ...", key="sch_g1")
        with col_sch_dialect1:
            filter_dialect1 = st.selectbox("ಪ್ರಾಂತ್ಯ ಫಿಲ್ಟರ್:", ["ಎಲ್ಲವೂ (All)", "Hubballi-Dharwad", "Mangaluru", "Uttara Kannada"], key="flt_g1")

        glossary_path = "data/glossary.csv"
        if os.path.exists(glossary_path):
            df_glossary = pd.read_csv(glossary_path)
            if filter_dialect1 != "ಎಲ್ಲವೂ (All)":
                df_glossary = df_glossary[df_glossary["dialect"].astype(str).str.contains(filter_dialect1, case=False, na=False)]
            if search_query1:
                mask = df_glossary.astype(str).apply(lambda x: x.str.contains(search_query1, case=False, na=False)).any(axis=1)
                df_filtered = df_glossary[mask]
            else:
                df_filtered = df_glossary
            st.caption(f"ಒಟ್ಟು {len(df_filtered)} ಪದಗಳು ಕಂಡುಬಂದಿವೆ.")
            st.dataframe(df_filtered, use_container_width=True, hide_index=True)
            st.download_button("📥 Glossary CSV ಡೌನ್‌ಲೋಡ್", data=df_filtered.to_csv(index=False), file_name="glossary.csv", mime="text/csv", key="dl_gloss_csv")
        else:
            st.warning("Glossary file not found.")

    # --- TAB 3: Parallel Corpus ---
    with c_tab3:
        st.write("")
        col_sch_text2, col_sch_dialect2 = st.columns([3, 1])
        with col_sch_text2:
            search_query2 = st.text_input("ವಾಕ್ಯ ಶೋಧಿಸಿ (Search sentences):", placeholder="ಉದಾ: ಬರುತ್ತಿದ್ದಾನೆ, ರೊಕ್ಕ...", key="sch_c2")
        with col_sch_dialect2:
            filter_dialect2 = st.selectbox("ಪ್ರಾಂತ್ಯ ಫಿಲ್ಟರ್:", ["ಎಲ್ಲವೂ (All)", "Hubballi-Dharwad", "Mangaluru", "Uttara Kannada"], key="flt_c2")

        corpus_path = "data/dataset.csv"
        if os.path.exists(corpus_path):
            df_corpus = pd.read_csv(corpus_path)
            if filter_dialect2 != "ಎಲ್ಲವೂ (All)":
                df_corpus = df_corpus[df_corpus["dialect"].astype(str).str.contains(filter_dialect2, case=False, na=False)]
            if search_query2:
                mask2 = df_corpus.astype(str).apply(lambda x: x.str.contains(search_query2, case=False, na=False)).any(axis=1)
                df_filtered2 = df_corpus[mask2]
            else:
                df_filtered2 = df_corpus
            st.caption(f"ಒಟ್ಟು {len(df_filtered2)} ವಾಕ್ಯಗಳು ಕಂಡುಬಂದಿವೆ.")
            st.dataframe(df_filtered2, use_container_width=True, hide_index=True)
            st.download_button("📥 Dataset CSV ಡೌನ್‌ಲೋಡ್", data=df_filtered2.to_csv(index=False), file_name="dataset.csv", mime="text/csv", key="dl_corp_csv")
        else:
            st.warning("Dataset file not found.")

# --- Editorial Cultural Footer ---
st.markdown("""
<div class="editorial-footer">
    <div style="font-family: 'Tiro Kannada', serif; font-size: 1.5rem; font-weight: 800; color: #EA580C; margin-bottom: 0.3rem;">ನು</div>
    <div class="footer-quote">"ಕನ್ನಡವೇ ಸತ್ಯ, ಕನ್ನಡವೇ ನಿತ್ಯ • ಎಲ್ಲರ ನುಡಿಯ ಗೌರವಿಸೋಣ."</div>
    <div style="font-size: 0.92rem; color: #94A3B8; margin-top: 4px;">
        Modalapada 2.0 • Ramaiah Institute of Technology • Dept. of CSE
    </div>
</div>
""", unsafe_allow_html=True)
