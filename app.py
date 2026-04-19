import streamlit as st
import pandas as pd
import numpy as np
import pickle
import json
import os

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="NaijaHousePrice AI",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Premium CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; }

.stApp { background: #080b14; color: #c8d0e0; }

[data-testid="stSidebar"] {
    background: #0d1120 !important;
    border-right: 1px solid rgba(255,255,255,0.06);
}
[data-testid="stSidebar"] label {
    color: #6b7a99 !important;
    font-size: 0.72rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.1em !important;
}
[data-testid="stSidebar"] [data-testid="stSelectbox"] > div > div {
    background: #131929 !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 10px !important;
    color: #e0e8f5 !important;
}
.stButton > button {
    background: linear-gradient(135deg, #f59e0b 0%, #ef4444 100%);
    color: #fff;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-weight: 700;
    font-size: 0.95rem;
    letter-spacing: 0.04em;
    border: none;
    border-radius: 14px;
    padding: 0.85rem 1.5rem;
    width: 100%;
    cursor: pointer;
    box-shadow: 0 4px 24px rgba(245,158,11,0.25);
    transition: all 0.25s;
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 32px rgba(245,158,11,0.4);
}

.hero-eyebrow { font-size:0.72rem; font-weight:600; letter-spacing:0.2em; text-transform:uppercase; color:#f59e0b; margin-bottom:0.75rem; }
.hero-title { font-size:clamp(2rem,4vw,3.2rem); font-weight:800; line-height:1.05; color:#f0f4ff; margin-bottom:0.75rem; }
.hero-title span { background:linear-gradient(90deg,#f59e0b,#ef4444); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }
.hero-desc { font-size:1rem; color:#4a5570; max-width:580px; line-height:1.7; margin-bottom:1.5rem; }

.stats-row { display:flex; gap:1rem; margin:0 0 2rem; flex-wrap:wrap; }
.stat-card { flex:1; min-width:130px; background:#0d1120; border:1px solid rgba(255,255,255,0.06); border-radius:16px; padding:1.25rem 1.4rem; position:relative; overflow:hidden; }
.stat-card::before { content:''; position:absolute; top:0; left:0; right:0; height:2px; background:linear-gradient(90deg,#f59e0b,#ef4444); opacity:0.7; }
.stat-label { font-size:0.68rem; font-weight:600; letter-spacing:0.12em; text-transform:uppercase; color:#3d4a66; margin-bottom:0.5rem; }
.stat-value { font-size:1.7rem; font-weight:800; color:#e8eeff; line-height:1; }
.stat-sub { font-size:0.72rem; color:#3d4a66; margin-top:0.3rem; }

.result-card { background:linear-gradient(135deg,#0f1a2e,#0d1120); border:1px solid rgba(245,158,11,0.25); border-radius:24px; padding:2.5rem; margin:0.5rem 0 1.5rem; animation:slideUp 0.4s ease; }
@keyframes slideUp { from{opacity:0;transform:translateY(16px)} to{opacity:1;transform:translateY(0)} }
.result-eyebrow { font-size:0.72rem; font-weight:600; letter-spacing:0.15em; text-transform:uppercase; color:#f59e0b; margin-bottom:0.6rem; }
.result-price { font-size:clamp(1.8rem,3.5vw,2.8rem); font-weight:800; color:#f0f4ff; line-height:1; margin-bottom:0.5rem; }
.result-range { font-size:0.85rem; color:#3d4a66; margin-bottom:1.5rem; }
.result-range strong { color:#6b7a99; }
.tags-row { display:flex; flex-wrap:wrap; gap:0.5rem; }
.tag { background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.08); border-radius:999px; padding:0.3rem 0.85rem; font-size:0.78rem; color:#6b7a99; }
.tag.hi { background:rgba(245,158,11,0.1); border-color:rgba(245,158,11,0.3); color:#f59e0b; }

.placeholder-box { background:#0d1120; border:1px dashed rgba(255,255,255,0.07); border-radius:24px; padding:3rem; text-align:center; margin:0.5rem 0 1.5rem; }
.placeholder-icon { font-size:3rem; margin-bottom:1rem; opacity:0.25; }
.placeholder-text { color:#3d4a66; font-size:0.9rem; line-height:1.7; }

.section-title { font-size:1rem; font-weight:700; color:#e0e8f5; margin:1.5rem 0 1rem; display:flex; align-items:center; gap:0.6rem; }
.section-title::after { content:''; flex:1; height:1px; background:rgba(255,255,255,0.06); }

.acc-wrap { background:#131929; border:1px solid rgba(255,255,255,0.05); border-radius:14px; padding:1.1rem 1.3rem; margin-bottom:1rem; }
.acc-lbl { font-size:0.68rem; font-weight:600; letter-spacing:0.12em; text-transform:uppercase; color:#3d4a66; margin-bottom:0.5rem; }
.acc-bg { background:#0d1120; border-radius:999px; height:6px; }
.acc-fill { height:6px; border-radius:999px; background:linear-gradient(90deg,#f59e0b,#ef4444); }
.acc-num { font-size:1.4rem; font-weight:800; color:#e8eeff; margin-top:0.45rem; }

.divider { height:1px; background:rgba(255,255,255,0.06); margin:1.2rem 0; }
.sb-brand { font-size:1.1rem; font-weight:800; color:#e0e8f5; margin-bottom:0.2rem; }
.sb-brand span { color:#f59e0b; }
.sb-tag { font-size:0.72rem; color:#3d4a66; margin-bottom:1.3rem; }
.sb-sec { font-size:0.65rem; font-weight:700; letter-spacing:0.14em; text-transform:uppercase; color:#2d3a55; margin-bottom:0.7rem; }

[data-testid="stExpander"] { background:#0d1120 !important; border:1px solid rgba(255,255,255,0.06) !important; border-radius:14px !important; }
</style>
""", unsafe_allow_html=True)

# ── Load assets ───────────────────────────────────────────────────────────────
@st.cache_resource
def load_assets():
    base = os.path.dirname(__file__)
    with open(os.path.join(base, 'model_xgb.pkl'), 'rb') as f: xgb_m = pickle.load(f)
    with open(os.path.join(base, 'model_lgb.pkl'), 'rb') as f: lgb_m = pickle.load(f)
    with open(os.path.join(base, 'encoders.pkl'),  'rb') as f: enc   = pickle.load(f)
    with open(os.path.join(base, 'meta.json'))          as f: meta  = json.load(f)
    return xgb_m, lgb_m, enc, meta

xgb_model, lgb_model, encoders, meta = load_assets()

@st.cache_data
def load_data():
    base = os.path.dirname(__file__)
    df = pd.read_csv(os.path.join(base, 'nigeria_houses_data.csv'))
    return df[df['price'].between(df['price'].quantile(0.005), df['price'].quantile(0.995))]

df = load_data()

def predict(bedrooms, bathrooms, toilets, parking_space, prop_type, town, state):
    title_enc = encoders['title'].transform([prop_type])[0]
    town_enc  = encoders['town'].transform([town])[0]
    state_enc = encoders['state'].transform([state])[0]
    total_rooms  = bedrooms + bathrooms + toilets
    luxury_score = bedrooms * bathrooms * (parking_space + 1)
    is_duplex    = 1 if 'Duplex'    in prop_type else 0
    is_detached  = 1 if 'Detached'  in prop_type else 0
    state_med = meta['state_median'].get(state, np.median(list(meta['state_median'].values())))
    town_med  = meta['town_median'].get(town, state_med)
    row = pd.DataFrame([[bedrooms, bathrooms, toilets, parking_space,
                          title_enc, town_enc, state_enc,
                          total_rooms, luxury_score, is_duplex, is_detached,
                          state_med, town_med]], columns=meta['features'])
    p_xgb = np.expm1(xgb_model.predict(row)[0])
    p_lgb = np.expm1(lgb_model.predict(row)[0])
    return (p_xgb + p_lgb) / 2

# ═══════════════════════════════════════════════════════════════════════════════
#  SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown('<div class="sb-brand">Naija<span>House</span>Price</div>', unsafe_allow_html=True)
    st.markdown('<div class="sb-tag">AI-powered · 25 states · 24K+ listings</div>', unsafe_allow_html=True)

    r2_pct = meta['r2'] * 100
    st.markdown(f"""
    <div class="acc-wrap">
        <div class="acc-lbl">Model Accuracy (R²)</div>
        <div class="acc-bg"><div class="acc-fill" style="width:{r2_pct:.1f}%"></div></div>
        <div class="acc-num">{r2_pct:.1f}%</div>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="sb-sec">📍 Location</div>', unsafe_allow_html=True)
    state    = st.selectbox("State", sorted(meta['states']))
    towns_in = sorted(df[df['state'] == state]['town'].unique().tolist())
    town     = st.selectbox("Town / Area", towns_in)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="sb-sec">🏡 Property Type</div>', unsafe_allow_html=True)
    prop_type = st.selectbox("Type", meta['titles'])

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="sb-sec">📐 Specifications</div>', unsafe_allow_html=True)
    bedrooms      = st.slider("Bedrooms",       1, 9, 3)
    bathrooms     = st.slider("Bathrooms",      1, 9, 2)
    toilets       = st.slider("Toilets",        1, 9, 2)
    parking_space = st.slider("Parking Spaces", 0, 6, 1)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    predict_btn = st.button("🔮  Predict House Price")

# ═══════════════════════════════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero-eyebrow">CSC 309 · Mini Project #7 · House Price Prediction</div>
<div class="hero-title">Nigeria's <span>Smartest</span> Property Valuator</div>
<div class="hero-desc">
    Enter any property specification and get an instant AI-powered price estimate —
    trained on 24,000+ real listings across 25 Nigerian states using an
    XGBoost + LightGBM ensemble model.
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="stats-row">
    <div class="stat-card">
        <div class="stat-label">Training Records</div>
        <div class="stat-value">24K+</div>
        <div class="stat-sub">real listings</div>
    </div>
    <div class="stat-card">
        <div class="stat-label">States Covered</div>
        <div class="stat-value">25</div>
        <div class="stat-sub">nationwide</div>
    </div>
    <div class="stat-card">
        <div class="stat-label">Model R² Score</div>
        <div class="stat-value">{meta['r2']*100:.1f}%</div>
        <div class="stat-sub">accuracy</div>
    </div>
    <div class="stat-card">
        <div class="stat-label">Algorithm</div>
        <div class="stat-value" style="font-size:1rem;padding-top:0.3rem">XGB + LGB</div>
        <div class="stat-sub">ensemble</div>
    </div>
    <div class="stat-card">
        <div class="stat-label">Features Used</div>
        <div class="stat-value">13</div>
        <div class="stat-sub">engineered</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Prediction ────────────────────────────────────────────────────────────────
if predict_btn:
    try:
        price = predict(bedrooms, bathrooms, toilets, parking_space, prop_type, town, state)
        lo, hi = price * 0.85, price * 1.15
        def f(n): return f"₦{n/1e6:.1f}M" if n >= 1e6 else f"₦{n:,.0f}"
        def ff(n): return f"₦{n:,.0f}"
        st.markdown(f"""
        <div class="result-card">
            <div class="result-eyebrow">✦ Estimated Market Value</div>
            <div class="result-price">{ff(price)}</div>
            <div class="result-range">Confidence range: <strong>{f(lo)}</strong> → <strong>{f(hi)}</strong> &nbsp;(±15%)</div>
            <div class="tags-row">
                <span class="tag hi">{prop_type}</span>
                <span class="tag hi">{town}, {state}</span>
                <span class="tag">{bedrooms} Bed</span>
                <span class="tag">{bathrooms} Bath</span>
                <span class="tag">{toilets} Toilet</span>
                <span class="tag">{parking_space} Parking</span>
            </div>
        </div>""", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"⚠️ Prediction error: {e}")
else:
    st.markdown("""
    <div class="placeholder-box">
        <div class="placeholder-icon">🏠</div>
        <div class="placeholder-text">
            Set property details in the sidebar<br>
            then click <strong style="color:#f59e0b">Predict House Price</strong>
        </div>
    </div>""", unsafe_allow_html=True)

# ── Analytics ─────────────────────────────────────────────────────────────────
st.markdown('<div class="section-title"> Dataset Analytics</div>', unsafe_allow_html=True)
c1, c2 = st.columns(2)
with c1:
    st.markdown("**Avg Price by State — Top 10 (₦M)**")
    sa = df.groupby('state')['price'].mean().sort_values(ascending=False).head(10).reset_index()
    sa.columns = ['State','Avg (₦M)']; sa['Avg (₦M)'] = (sa['Avg (₦M)']/1e6).round(1)
    st.bar_chart(sa.set_index('State'), color="#f59e0b")
with c2:
    st.markdown("**Property Type Distribution**")
    td = df['title'].value_counts().reset_index(); td.columns=['Type','Count']
    st.bar_chart(td.set_index('Type'), color="#ef4444")

c3, c4 = st.columns(2)
with c3:
    st.markdown("**Median Price by Bedrooms (₦M)**")
    bp = df.groupby('bedrooms')['price'].median().reset_index()
    bp.columns=['Bedrooms','Median (₦M)']; bp['Median (₦M)']=(bp['Median (₦M)']/1e6).round(1)
    st.bar_chart(bp.set_index('Bedrooms'), color="#10b981")
with c4:
    st.markdown("**Price vs Bedrooms — 2K sample**")
    smp = df.sample(min(2000,len(df)), random_state=7)[['bedrooms','price']].copy()
    smp.columns=['Bedrooms','Price (₦M)']; smp['Price (₦M)']=(smp['Price (₦M)']/1e6).round(2)
    st.scatter_chart(smp, x='Bedrooms', y='Price (₦M)', color="#6366f1")

# ── Feature importance ────────────────────────────────────────────────────────
st.markdown('<div class="section-title">🧠 What Drives Price Most</div>', unsafe_allow_html=True)
fi_df = pd.DataFrame({'Feature': meta['features'],
                       'Importance %': (xgb_model.feature_importances_*100).round(2)})
fi_df = fi_df.sort_values('Importance %', ascending=False).reset_index(drop=True)
fi_df['Visual'] = fi_df['Importance %'].apply(lambda x: '█'*max(1,int(x/2)))
st.dataframe(fi_df, use_container_width=True, hide_index=True)

with st.expander("📂 Raw Dataset Preview (50 rows)"):
    st.dataframe(df.head(50), use_container_width=True)

with st.expander("🤖 Model Architecture"):
    st.markdown("""
| Detail | Value |
|--------|-------|
| **Algorithms** | XGBoost + LightGBM (ensemble average) |
| **Target transform** | log1p(price) → expm1 on output |
| **Outlier handling** | Removed bottom & top 0.5% of prices |
| **Engineered features** | total_rooms, luxury_score, is_duplex, is_detached, state_price_median, town_price_median |
| **R² Score** | 67.05% |
| **Records trained on** | 24,000+ |
| **Dataset** | Kaggle — abdullahiyunus/nigeria-houses-and-prices-dataset |
    """)

st.markdown("""
<div style="text-align:center;color:#1e2740;font-size:0.78rem;margin-top:3rem;padding-bottom:1rem;">
    NaijaHousePrice AI · CSC 309 Mini Project · XGBoost + LightGBM + Streamlit
</div>""", unsafe_allow_html=True)
