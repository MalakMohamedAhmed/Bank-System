import streamlit as st
import pandas as pd
import os
from bank_system import User_account

# ─── Page Config ──────────────────────────────────────────────────────────
st.set_page_config(
    page_title="NexaBank",
    page_icon="🏦",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ─── File Paths ────────────────────────────────────────────────────────────
FILE_PATH         = "bank_data.csv"
TRANSACTIONS_FILE = "transactions.csv"

# ─── Custom CSS ───────────────────────────────────────────────────────────
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
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--cream);
    color: var(--navy);
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem; padding-bottom: 3rem; max-width: 720px; }

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
.gold-divider {
    border: none;
    border-top: 1px solid rgba(201,168,76,0.3);
    margin: 1.5rem 0;
}
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
.txn-row {
    display: flex; justify-content: space-between; align-items: center;
    padding: 0.7rem 0;
    border-bottom: 1px solid var(--light);
}
.txn-row:last-child { border-bottom: none; }
.txn-type { font-weight: 500; color: var(--navy); }
.txn-amount-pos { color: var(--green); font-weight: 600; }
.txn-amount-neg { color: var(--red); font-weight: 600; }
</style>
""", unsafe_allow_html=True)

# ─── Helper Functions ────────────────────────────────────────────────────────
def load_user_row(user_id: str):
    """Fetch a single user's row from bank_data.csv."""
    if not os.path.exists(FILE_PATH):
        return None
    data = pd.read_csv(FILE_PATH)
    match = data[data['user_id'] == user_id]
    return match.iloc[0] if not match.empty else None

def get_next_id() -> str:
    """Generate the next sequential account number."""
    if not os.path.exists(FILE_PATH):
        return "NX-100001"
    data = pd.read_csv(FILE_PATH)
    if data.empty:
        return "NX-100001"
    nums = [int(str(uid).split("-")[1]) for uid in data['user_id'] if str(uid).startswith("NX-")]
    return f"NX-{max(nums)+1}" if nums else "NX-100001"

def restore_user(row) -> User_account:
    """
    Rebuild a User_account object from a CSV row
    WITHOUT calling _add_to_csv again (bypasses __init__).
    """
    u = object.__new__(User_account)
    u.user_id       = row['user_id']
    u.name          = row['name']
    u.password      = str(row['password'])
    u.phone_number  = str(row['phone_number'])
    u.balance       = float(row['balance'])
    u.transaction_history = {
        "Current Balance": [u.balance],
        "Operation":       ["Session Start"],
        "Amount":          ["—"]
    }
    return u

# ─── Session State Init ──────────────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "home"
if "user" not in st.session_state:
    st.session_state.user = None   # holds the User_account object

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
#  CREATE ACCOUNT  ── uses User_account.__init__ → _add_to_csv
# ════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "create_account":
    st.markdown('<div class="section-title">Open an Account</div><div class="gold-bar"></div>', unsafe_allow_html=True)

    with st.form("create_form"):
        col1, col2 = st.columns(2)
        with col1:
            name     = st.text_input("Full Name")
            phone    = st.text_input("Phone Number")
        with col2:
            password = st.text_input("Password", type="password")
            deposit  = st.number_input("Initial Deposit (EGP)", min_value=0.0, step=100.0, format="%.2f")
        submitted = st.form_submit_button("Create My Account", use_container_width=True)

    if submitted:
        if not all([name, phone, password]):
            st.markdown('<div class="alert-error">❌ Please fill in all fields.</div>', unsafe_allow_html=True)
        else:
            new_id = get_next_id()
            # __init__ automatically calls _add_to_csv(FILE_PATH)
            User_account(
                user_id      = new_id,
                name         = name,
                password     = password,
                phone_number = phone,
                balance      = deposit,
                file_path    = FILE_PATH
            )
            st.markdown(f"""
            <div class="alert-success">
                ✅ Account created successfully!<br>
                Your Account Number is <strong>{new_id}</strong> — please save it.
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
        acc_input  = st.text_input("Account Number (e.g. NX-100001)")
        pass_input = st.text_input("Password", type="password")
        login_btn  = st.form_submit_button("Sign In", use_container_width=True)

    if login_btn:
        row = load_user_row(acc_input.strip())
        if row is None:
            st.markdown('<div class="alert-error">❌ Account not found.</div>', unsafe_allow_html=True)
        elif str(row['password']) != pass_input:
            st.markdown('<div class="alert-error">❌ Incorrect password.</div>', unsafe_allow_html=True)
        else:
            # Restore User_account object from CSV row
            st.session_state.user = restore_user(row)
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
    user: User_account = st.session_state.user

    if user is None:
        st.session_state.page = "home"
        st.rerun()

    # Always refresh balance/name/phone from CSV on every rerun
    fresh = load_user_row(user.user_id)
    if fresh is not None:
        user.balance      = float(fresh['balance'])
        user.name         = str(fresh['name'])
        user.phone_number = str(fresh['phone_number'])
        user.password     = str(fresh['password'])

    # ── Account Summary Card ──────────────────────────────────────────────
    st.markdown(f"""
    <div class="info-box">
        <div style="display:flex; justify-content:space-between; align-items:flex-start;">
            <div>
                <div class="label">Account Holder</div>
                <div class="value" style="font-size:1.3rem;">{user.name}</div>
                <div style="color:rgba(255,255,255,0.5); font-size:0.82rem; margin-top:4px;">
                    {user.user_id} &nbsp;·&nbsp; {user.phone_number}
                </div>
            </div>
            <div style="text-align:right;">
                <div class="label">Available Balance</div>
                <div class="balance-amount">EGP {user.balance:,.2f}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    tabs = st.tabs(["💳 Deposit", "💸 Withdraw", "✏️ Update Info", "📋 History", "🗑️ Delete Account"])

    # ── DEPOSIT ── user.Deposite(amount, FILE_PATH, TRANSACTIONS_FILE) ────
    with tabs[0]:
        st.markdown("### Deposit Funds")
        with st.form("deposit_form"):
            amount  = st.number_input("Amount to Deposit (EGP)", min_value=0.01, step=100.0, format="%.2f")
            dep_btn = st.form_submit_button("Deposit", use_container_width=True)
        if dep_btn:
            user.Deposite(amount, FILE_PATH, TRANSACTIONS_FILE)
            st.markdown(f'<div class="alert-success">✅ EGP {amount:,.2f} deposited. New balance: <strong>EGP {user.balance:,.2f}</strong></div>', unsafe_allow_html=True)
            st.rerun()

    # ── WITHDRAW ── user.Withdraw(amount, FILE_PATH, TRANSACTIONS_FILE) ───
    with tabs[1]:
        st.markdown("### Withdraw Funds")
        with st.form("withdraw_form"):
            amount  = st.number_input("Amount to Withdraw (EGP)", min_value=0.01, step=100.0, format="%.2f")
            wit_btn = st.form_submit_button("Withdraw", use_container_width=True)
        if wit_btn:
            if amount > user.balance:
                st.markdown(f'<div class="alert-error">❌ Insufficient balance. Available: EGP {user.balance:,.2f}</div>', unsafe_allow_html=True)
            else:
                user.Withdraw(amount, FILE_PATH, TRANSACTIONS_FILE)
                st.markdown(f'<div class="alert-success">✅ EGP {amount:,.2f} withdrawn. Remaining: <strong>EGP {user.balance:,.2f}</strong></div>', unsafe_allow_html=True)
                st.rerun()

    # ── UPDATE INFO ── user.Update_username / Update_number / Update_password
    with tabs[2]:
        st.markdown("### Update Personal Information")
        with st.form("update_form"):
            new_name  = st.text_input("Full Name",    value=user.name)
            new_phone = st.text_input("Phone Number", value=user.phone_number)
            new_pass  = st.text_input("New Password *(leave blank to keep current)*", type="password")
            upd_btn   = st.form_submit_button("Save Changes", use_container_width=True)
        if upd_btn:
            if new_name != user.name:
                user.Update_username(new_name, FILE_PATH)
            if new_phone != user.phone_number:
                user.Update_number(new_phone, FILE_PATH)
            if new_pass:
                user.Update_password(new_pass, FILE_PATH)
            st.markdown('<div class="alert-success">✅ Information updated successfully.</div>', unsafe_allow_html=True)
            st.rerun()

    # ── HISTORY ── reads user.transaction_history + transactions.csv ──────
    with tabs[3]:
        st.markdown("### Transaction History")

        # Show full history from transactions.csv for this user
        if os.path.exists(TRANSACTIONS_FILE):
            txn_data = pd.read_csv(TRANSACTIONS_FILE)
            user_txns = txn_data[txn_data['user_id'] == user.user_id]
            if user_txns.empty:
                st.markdown('<div class="alert-info">ℹ️ No transactions recorded yet.</div>', unsafe_allow_html=True)
            else:
                for _, row in user_txns.iloc[::-1].iterrows():
                    amt    = str(row['amount'])
                    is_pos = amt.startswith("+")
                    color  = "txn-amount-pos" if is_pos else "txn-amount-neg"
                    st.markdown(f"""
                    <div class="txn-row">
                        <div>
                            <div class="txn-type">{row['operation']}</div>
                        </div>
                        <div style="text-align:right;">
                            <div class="{color}">{amt} EGP</div>
                            <div style="font-size:0.8rem;color:#4a5568;">Balance: EGP {float(row['balance']):,.2f}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.markdown('<div class="alert-info">ℹ️ No transactions recorded yet.</div>', unsafe_allow_html=True)

    # ── DELETE ACCOUNT ── user.Delete_account(FILE_PATH) ─────────────────
    with tabs[4]:
        st.markdown("### Delete Account")
        st.markdown('<div class="alert-error">⚠️ This action is permanent and cannot be undone.</div>', unsafe_allow_html=True)
        with st.form("delete_form"):
            confirm_pass = st.text_input("Enter your password to confirm", type="password")
            confirm_txt  = st.text_input('Type "DELETE" to confirm')
            del_btn      = st.form_submit_button("🗑️ Permanently Delete Account", use_container_width=True)
        if del_btn:
            if confirm_pass != user.password:
                st.markdown('<div class="alert-error">❌ Incorrect password.</div>', unsafe_allow_html=True)
            elif confirm_txt != "DELETE":
                st.markdown('<div class="alert-error">❌ Please type DELETE to confirm.</div>', unsafe_allow_html=True)
            else:
                user.Delete_account(FILE_PATH)
                st.session_state.user = None
                st.session_state.page = "home"
                st.rerun()

    # ── Sign Out ──────────────────────────────────────────────────────────
    st.markdown('<hr class="gold-divider">', unsafe_allow_html=True)
    if st.button("🔓 Sign Out"):
        st.session_state.user = None
        st.session_state.page = "home"
        st.rerun()
