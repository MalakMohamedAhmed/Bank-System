import streamlit as st
import json
import os
from datetime import datetime
from bank_system import *
 
# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Welcome to our Bank",
    page_icon="🏦",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');
 
:root {
    --navy:   #0a1628;
    --gold:   #c9a84c;
    --gold2:  #e8c97a;
    --cream:  #f5f0e8;
    --white:  #ffffff;
    --slate:  #4a5568;
    --light:  #edf2f7;
    --red:    #c0392b;
    --green:  #27ae60;
}
 
/* ── Global ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--cream);
    color: var(--navy);
}
 
/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem; padding-bottom: 3rem; max-width: 720px; }
 
/* ── Hero Banner ── */
.hero {
    background: linear-gradient(135deg, var(--navy) 0%, #1a2d4f 60%, #0f2240 100%);
    border-radius: 20px;
    padding: 3rem 2.5rem 2.5rem;
    text-align: center;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
    box-shadow: 0 20px 60px rgba(10,22,40,0.3);
}
.hero::before {
    content: "";
    position: absolute;
    top: -60px; right: -60px;
    width: 200px; height: 200px;
    border-radius: 50%;
    background: rgba(201,168,76,0.12);
}
.hero::after {
    content: "";
    position: absolute;
    bottom: -40px; left: -40px;
    width: 150px; height: 150px;
    border-radius: 50%;
    background: rgba(201,168,76,0.08);
}
.hero-icon { font-size: 3rem; margin-bottom: 0.5rem; }
.hero h1 {
    font-family: 'Playfair Display', serif;
    color: var(--white);
    font-size: 2.4rem;
    margin: 0 0 0.3rem;
    letter-spacing: -0.5px;
}
.hero-sub {
    color: var(--gold2);
    font-size: 0.95rem;
    font-weight: 300;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 0.2rem;
}
.hero-tagline { color: rgba(255,255,255,0.6); font-size: 0.9rem; margin-top: 0.5rem; }
 
/* ── Section Header ── */
.section-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.6rem;
    color: var(--navy);
    margin-bottom: 0.2rem;
}
.gold-bar {
    width: 48px; height: 3px;
    background: var(--gold);
    border-radius: 2px;
    margin-bottom: 1.5rem;
}
 
/* ── Cards ── */
.card {
    background: var(--white);
    border-radius: 16px;
    padding: 2rem;
    box-shadow: 0 4px 24px rgba(10,22,40,0.08);
    border: 1px solid rgba(201,168,76,0.15);
    margin-bottom: 1.5rem;
}
 
/* ── Info box ── */
.info-box {
    background: linear-gradient(135deg, var(--navy), #1a2d4f);
    border-radius: 14px;
    padding: 1.6rem;
    color: var(--white);
    margin-bottom: 1.2rem;
}
.info-box .label { color: var(--gold2); font-size: 0.75rem; letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 0.2rem; }
.info-box .value { font-size: 1.05rem; font-weight: 500; }
.balance-amount {
    font-family: 'Playfair Display', serif;
    font-size: 2.2rem;
    color: var(--gold);
}
 
/* ── Alert Boxes ── */
.alert-success {
    background: #eafaf1; border-left: 4px solid var(--green);
    padding: 1rem 1.2rem; border-radius: 8px;
    color: #1e8449; font-weight: 500; margin: 1rem 0;
}
.alert-error {
    background: #fdedec; border-left: 4px solid var(--red);
    padding: 1rem 1.2rem; border-radius: 8px;
    color: var(--red); font-weight: 500; margin: 1rem 0;
}
.alert-info {
    background: #eaf0fb; border-left: 4px solid #2980b9;
    padding: 1rem 1.2rem; border-radius: 8px;
    color: #1a5276; font-weight: 500; margin: 1rem 0;
}
 
/* ── Divider ── */
.gold-divider {
    border: none;
    border-top: 1px solid rgba(201,168,76,0.3);
    margin: 1.5rem 0;
}
 
/* ── Buttons ── */
.stButton > button {
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    border-radius: 10px !important;
    padding: 0.6rem 1.5rem !important;
    transition: all 0.2s ease !important;
}
.stButton > button:first-child {
    background: linear-gradient(135deg, var(--navy), #1a2d4f) !important;
    color: var(--white) !important;
    border: none !important;
}
.stButton > button:first-child:hover {
    background: linear-gradient(135deg, #1a2d4f, var(--navy)) !important;
    box-shadow: 0 6px 20px rgba(10,22,40,0.25) !important;
    transform: translateY(-1px) !important;
}
 
/* ── Inputs ── */
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stSelectbox > div > div {
    border-radius: 10px !important;
    border: 1.5px solid #dde3ec !important;
    font-family: 'DM Sans', sans-serif !important;
}
.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus {
    border-color: var(--gold) !important;
    box-shadow: 0 0 0 3px rgba(201,168,76,0.15) !important;
}
 
/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: var(--light);
    border-radius: 12px;
    padding: 4px;
    gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 9px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    color: var(--slate) !important;
}
.stTabs [aria-selected="true"] {
    background: var(--navy) !important;
    color: var(--white) !important;
}
 
/* ── Transaction History ── */
.txn-row {
    display: flex; justify-content: space-between; align-items: center;
    padding: 0.7rem 0;
    border-bottom: 1px solid var(--light);
}
.txn-row:last-child { border-bottom: none; }
.txn-type { font-weight: 500; color: var(--navy); }
.txn-date { font-size: 0.8rem; color: var(--slate); }
.txn-amount-pos { color: var(--green); font-weight: 600; }
.txn-amount-neg { color: var(--red); font-weight: 600; }
</style>
""", unsafe_allow_html=True)

