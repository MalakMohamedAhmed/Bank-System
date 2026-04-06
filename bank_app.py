import streamlit as st
import json
import os
from datetime import datetime

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="NexaBank",
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

# ─── Data Persistence ────────────────────────────────────────────────────────
DATA_FILE = "bank_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_next_account_number(data):
    if not data:
        return "NX-100001"
    nums = [int(k.split("-")[1]) for k in data.keys()]
    return f"NX-{max(nums)+1}"

# ─── Session State Init ──────────────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "home"
if "account_id" not in st.session_state:
    st.session_state.account_id = None

bank_data = load_data()

# ─── Hero ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-icon">🏦</div>
  <div class="hero-sub">Private Banking</div>
  <h1>NexaBank</h1>
  <div class="hero-tagline">Your wealth, thoughtfully managed.</div>
</div>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
#  HOME PAGE
# ════════════════════════════════════════════════════════════════════════════
if st.session_state.page == "home":
    st.markdown('<div class="section-title">Welcome</div><div class="gold-bar"></div>', unsafe_allow_html=True)
    st.markdown("Are you a **new customer** or do you already have an account with us?")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🆕  New Customer", use_container_width=True):
            st.session_state.page = "create_account"
            st.rerun()
    with col2:
        if st.button("🔐  Existing Customer", use_container_width=True):
            st.session_state.page = "login"
            st.rerun()

# ════════════════════════════════════════════════════════════════════════════
#  CREATE ACCOUNT
# ════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "create_account":
    st.markdown('<div class="section-title">Open an Account</div><div class="gold-bar"></div>', unsafe_allow_html=True)

    with st.form("create_form"):
        col1, col2 = st.columns(2)
        with col1:
            first = st.text_input("First Name")
            email = st.text_input("Email Address")
            pin   = st.text_input("Create PIN (4 digits)", type="password", max_chars=4)
        with col2:
            last    = st.text_input("Last Name")
            phone   = st.text_input("Phone Number")
            deposit = st.number_input("Initial Deposit (EGP)", min_value=0.0, step=100.0, format="%.2f")

        submitted = st.form_submit_button("Create My Account", use_container_width=True)

    if submitted:
        # Validation
        if not all([first, last, email, phone, pin]):
            st.markdown('<div class="alert-error">❌ Please fill in all fields.</div>', unsafe_allow_html=True)
        elif not pin.isdigit() or len(pin) != 4:
            st.markdown('<div class="alert-error">❌ PIN must be exactly 4 digits.</div>', unsafe_allow_html=True)
        elif deposit < 0:
            st.markdown('<div class="alert-error">❌ Initial deposit cannot be negative.</div>', unsafe_allow_html=True)
        else:
            acc_id = get_next_account_number(bank_data)
            bank_data[acc_id] = {
                "first": first, "last": last,
                "email": email, "phone": phone,
                "pin": pin, "balance": deposit,
                "created": datetime.now().strftime("%d %b %Y"),
                "transactions": [
                    {"type": "Initial Deposit", "amount": deposit,
                     "date": datetime.now().strftime("%d %b %Y, %H:%M")}
                ] if deposit > 0 else []
            }
            save_data(bank_data)
            st.markdown(f"""
            <div class="alert-success">
                ✅ Account created successfully!<br>
                Your Account Number is <strong>{acc_id}</strong> — please save it.
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<hr class="gold-divider">', unsafe_allow_html=True)
    if st.button("← Back to Home"):
        st.session_state.page = "home"
        st.rerun()

# ════════════════════════════════════════════════════════════════════════════
#  LOGIN
# ════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "login":
    st.markdown('<div class="section-title">Sign In</div><div class="gold-bar"></div>', unsafe_allow_html=True)

    with st.form("login_form"):
        acc_input = st.text_input("Account Number (e.g. NX-100001)")
        pin_input = st.text_input("PIN", type="password", max_chars=4)
        login_btn = st.form_submit_button("Sign In", use_container_width=True)

    if login_btn:
        acc_input = acc_input.strip().upper()
        if acc_input not in bank_data:
            st.markdown('<div class="alert-error">❌ Account not found.</div>', unsafe_allow_html=True)
        elif bank_data[acc_input]["pin"] != pin_input:
            st.markdown('<div class="alert-error">❌ Incorrect PIN.</div>', unsafe_allow_html=True)
        else:
            st.session_state.account_id = acc_input
            st.session_state.page = "dashboard"
            st.rerun()

    st.markdown('<hr class="gold-divider">', unsafe_allow_html=True)
    if st.button("← Back to Home"):
        st.session_state.page = "home"
        st.rerun()

# ════════════════════════════════════════════════════════════════════════════
#  DASHBOARD
# ════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "dashboard":
    acc_id = st.session_state.account_id
    if acc_id not in bank_data:
        st.session_state.page = "home"
        st.rerun()

    acct = bank_data[acc_id]

    # ── Account Summary Card ──────────────────────────────────────────────
    st.markdown(f"""
    <div class="info-box">
        <div style="display:flex; justify-content:space-between; align-items:flex-start;">
            <div>
                <div class="label">Account Holder</div>
                <div class="value" style="font-size:1.3rem;">{acct['first']} {acct['last']}</div>
                <div style="color:rgba(255,255,255,0.5); font-size:0.82rem; margin-top:4px;">{acc_id} &nbsp;·&nbsp; Member since {acct['created']}</div>
            </div>
            <div style="text-align:right;">
                <div class="label">Available Balance</div>
                <div class="balance-amount">EGP {acct['balance']:,.2f}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Tabs ──────────────────────────────────────────────────────────────
    tabs = st.tabs(["💳 Deposit", "💸 Withdraw", "✏️ Update Info", "📋 History", "🗑️ Delete Account"])

    # ── DEPOSIT ──────────────────────────────────────────────────────────
    with tabs[0]:
        st.markdown("### Deposit Funds")
        with st.form("deposit_form"):
            amount = st.number_input("Amount to Deposit (EGP)", min_value=0.01, step=100.0, format="%.2f")
            dep_btn = st.form_submit_button("Deposit", use_container_width=True)
        if dep_btn:
            bank_data[acc_id]["balance"] += amount
            bank_data[acc_id]["transactions"].append({
                "type": "Deposit", "amount": amount,
                "date": datetime.now().strftime("%d %b %Y, %H:%M")
            })
            save_data(bank_data)
            st.markdown(f'<div class="alert-success">✅ EGP {amount:,.2f} deposited successfully. New balance: <strong>EGP {bank_data[acc_id]["balance"]:,.2f}</strong></div>', unsafe_allow_html=True)
            st.rerun()

    # ── WITHDRAW ─────────────────────────────────────────────────────────
    with tabs[1]:
        st.markdown("### Withdraw Funds")
        with st.form("withdraw_form"):
            amount = st.number_input("Amount to Withdraw (EGP)", min_value=0.01, step=100.0, format="%.2f")
            wit_btn = st.form_submit_button("Withdraw", use_container_width=True)
        if wit_btn:
            if amount > bank_data[acc_id]["balance"]:
                st.markdown(f'<div class="alert-error">❌ Insufficient balance. Available: EGP {bank_data[acc_id]["balance"]:,.2f}</div>', unsafe_allow_html=True)
            else:
                bank_data[acc_id]["balance"] -= amount
                bank_data[acc_id]["transactions"].append({
                    "type": "Withdrawal", "amount": -amount,
                    "date": datetime.now().strftime("%d %b %Y, %H:%M")
                })
                save_data(bank_data)
                st.markdown(f'<div class="alert-success">✅ EGP {amount:,.2f} withdrawn. Remaining balance: <strong>EGP {bank_data[acc_id]["balance"]:,.2f}</strong></div>', unsafe_allow_html=True)
                st.rerun()

    # ── UPDATE INFO ──────────────────────────────────────────────────────
    with tabs[2]:
        st.markdown("### Update Personal Information")
        with st.form("update_form"):
            new_first = st.text_input("First Name", value=acct["first"])
            new_last  = st.text_input("Last Name",  value=acct["last"])
            new_email = st.text_input("Email",      value=acct["email"])
            new_phone = st.text_input("Phone",      value=acct["phone"])
            st.markdown("**Change PIN** *(leave blank to keep current)*")
            new_pin   = st.text_input("New PIN (4 digits)", type="password", max_chars=4)
            upd_btn   = st.form_submit_button("Save Changes", use_container_width=True)
        if upd_btn:
            if new_pin and (not new_pin.isdigit() or len(new_pin) != 4):
                st.markdown('<div class="alert-error">❌ PIN must be exactly 4 digits.</div>', unsafe_allow_html=True)
            else:
                bank_data[acc_id]["first"] = new_first
                bank_data[acc_id]["last"]  = new_last
                bank_data[acc_id]["email"] = new_email
                bank_data[acc_id]["phone"] = new_phone
                if new_pin:
                    bank_data[acc_id]["pin"] = new_pin
                save_data(bank_data)
                st.markdown('<div class="alert-success">✅ Your information has been updated.</div>', unsafe_allow_html=True)
                st.rerun()

    # ── HISTORY ──────────────────────────────────────────────────────────
    with tabs[3]:
        st.markdown("### Transaction History")
        txns = acct.get("transactions", [])
        if not txns:
            st.markdown('<div class="alert-info">ℹ️ No transactions recorded yet.</div>', unsafe_allow_html=True)
        else:
            for t in reversed(txns):
                amt   = t["amount"]
                color = "txn-amount-pos" if amt >= 0 else "txn-amount-neg"
                sign  = "+" if amt >= 0 else ""
                st.markdown(f"""
                <div class="txn-row">
                    <div>
                        <div class="txn-type">{t['type']}</div>
                        <div class="txn-date">{t['date']}</div>
                    </div>
                    <div class="{color}">{sign}EGP {abs(amt):,.2f}</div>
                </div>
                """, unsafe_allow_html=True)

    # ── DELETE ACCOUNT ───────────────────────────────────────────────────
    with tabs[4]:
        st.markdown("### Delete Account")
        st.markdown('<div class="alert-error">⚠️ This action is permanent and cannot be undone. All your data and balance will be erased.</div>', unsafe_allow_html=True)
        with st.form("delete_form"):
            confirm_pin = st.text_input("Enter your PIN to confirm", type="password", max_chars=4)
            confirm_txt = st.text_input('Type "DELETE" to confirm')
            del_btn     = st.form_submit_button("🗑️ Permanently Delete Account", use_container_width=True)
        if del_btn:
            if confirm_pin != bank_data[acc_id]["pin"]:
                st.markdown('<div class="alert-error">❌ Incorrect PIN.</div>', unsafe_allow_html=True)
            elif confirm_txt != "DELETE":
                st.markdown('<div class="alert-error">❌ Please type DELETE to confirm.</div>', unsafe_allow_html=True)
            else:
                del bank_data[acc_id]
                save_data(bank_data)
                st.session_state.account_id = None
                st.session_state.page = "home"
                st.markdown('<div class="alert-success">Account deleted.</div>', unsafe_allow_html=True)
                st.rerun()

    # ── Sign Out ──────────────────────────────────────────────────────────
    st.markdown('<hr class="gold-divider">', unsafe_allow_html=True)
    if st.button("🔓 Sign Out"):
        st.session_state.account_id = None
        st.session_state.page = "home"
        st.rerun()
