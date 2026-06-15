%%writefile app.py
import streamlit as st
import pandas as pd
from pyvis.network import Network
from wordcloud import WordCloud
import streamlit.components.v1 as components
from streamlit_autorefresh import st_autorefresh
from datetime import datetime
from collections import Counter
import matplotlib.pyplot as plt
import base64
import re
import os
import html
import random

st.set_page_config(
    page_title="Innovation Pulse | HERMES",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

DATA_FILE = "responses.csv"
LOGO_FILE = "hermes_logo.png"
COLUMNS = ["timestamp", "ambito", "problema", "rapporto", "frase", "sentiment", "parole_chiave"]

if not os.path.exists(DATA_FILE):
    pd.DataFrame(columns=COLUMNS).to_csv(DATA_FILE, index=False)

def img_to_base64(path):
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

logo_b64 = img_to_base64(LOGO_FILE)

st.markdown("""
<style>
.stApp {
    background:
        radial-gradient(circle at 12% 10%, rgba(37, 99, 235, 0.18), transparent 28%),
        radial-gradient(circle at 86% 18%, rgba(14, 165, 233, 0.20), transparent 30%),
        radial-gradient(circle at 50% 90%, rgba(59, 130, 246, 0.10), transparent 36%),
        linear-gradient(135deg, #ffffff 0%, #f5f9ff 45%, #eaf4ff 100%);
    color: #0f172a;
}

html, body, [class*="css"] {
    font-family: 'Inter', 'Segoe UI', sans-serif;
}

[data-testid="stSidebar"] {
    display: none;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1400px;
}

.hero {
    background: rgba(255,255,255,0.96);
    border: 1px solid rgba(37,99,235,0.22);
    border-radius: 34px;
    padding: 2.4rem;
    box-shadow: 0 26px 65px rgba(15, 23, 42, 0.10);
    margin-bottom: 1.5rem;
}

.logo-img {
    max-width: 280px;
    margin-bottom: 1rem;
}

.badge {
    display: inline-block;
    padding: 0.45rem 0.85rem;
    border-radius: 999px;
    background: linear-gradient(90deg, #0b4f8a, #0284c7);
    color: white;
    font-size: 0.78rem;
    font-weight: 850;
    letter-spacing: 0.08em;
    margin-bottom: 0.9rem;
}

.main-title {
    font-size: clamp(2.6rem, 6vw, 5.8rem);
    font-weight: 950;
    color: #0f172a;
    line-height: 0.95;
    margin-bottom: 0.8rem;
}

.subtitle {
    font-size: clamp(1.05rem, 2vw, 1.45rem);
    color: #334155;
    max-width: 1000px;
}

.card {
    background: rgba(255,255,255,0.96);
    border: 1px solid rgba(148,163,184,0.35);
    border-radius: 28px;
    padding: 1.5rem;
    box-shadow: 0 18px 42px rgba(15, 23, 42, 0.07);
    margin-bottom: 1rem;
}

.blue-card {
    background: linear-gradient(135deg, #ffffff, #eff6ff);
    border-left: 7px solid #0b4f8a;
}

.cyan-card {
    background: linear-gradient(135deg, #ffffff, #ecfeff);
    border-left: 7px solid #0284c7;
}

.big-button-card {
    background: white;
    border: 1px solid #dbeafe;
    border-radius: 28px;
    padding: 1.7rem;
    box-shadow: 0 18px 42px rgba(15,23,42,0.07);
    min-height: 210px;
}

.metric-card {
    background: white;
    border-radius: 24px;
    padding: 1.15rem;
    border: 1px solid #dbeafe;
    text-align: center;
    box-shadow: 0 10px 24px rgba(15, 23, 42, 0.06);
    min-height: 115px;
}

.metric-number {
    font-size: 2.15rem;
    font-weight: 950;
    color: #0b4f8a;
}

.metric-label {
    color: #475569;
    font-size: 0.92rem;
}

.highlight {
    font-size: clamp(1.2rem, 2vw, 1.8rem);
    font-weight: 850;
    color: #0b4f8a;
}

.quote-box {
    background: linear-gradient(135deg, #0b4f8a, #0284c7);
    color: white;
    border-radius: 28px;
    padding: 1.6rem;
    box-shadow: 0 18px 42px rgba(2,132,199,0.23);
    margin-bottom: 1rem;
}

.quote-text {
    font-size: clamp(1.2rem, 2.2vw, 2rem);
    font-weight: 750;
    line-height: 1.25;
}

.result-box {
    background: linear-gradient(135deg, #eff6ff, #ffffff);
    border-left: 7px solid #0284c7;
    padding: 1.15rem;
    border-radius: 20px;
    margin-top: 1rem;
}

.stButton > button {
    width: 100%;
    border-radius: 18px;
    padding: 1rem 1rem;
    font-weight: 900;
    font-size: 1.02rem;
    background: linear-gradient(90deg, #0b4f8a, #0284c7);
    color: white !important;
    border: none;
    box-shadow: 0 14px 30px rgba(2,132,199,0.25);
}

.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 18px 38px rgba(2,132,199,0.32);
}

label, .stRadio label, .stTextArea label {
    color: #0f172a !important;
    font-weight: 700 !important;
}

textarea, input {
    color: #0f172a !important;
    background-color: #ffffff !important;
}

div[role="radiogroup"] label {
    background: white;
    border: 1px solid #dbeafe;
    border-radius: 14px;
    padding: 0.45rem 0.75rem;
    margin-bottom: 0.35rem;
}

.nav-row {
    display: flex;
    gap: 0.7rem;
    margin-bottom: 1.2rem;
    flex-wrap: wrap;
}

.nav-pill {
    padding: 0.55rem 0.9rem;
    border-radius: 999px;
    background: white;
    border: 1px solid #bfdbfe;
    color: #0b4f8a;
    font-weight: 800;
}

@media (max-width: 768px) {
    .hero { padding: 1.25rem; border-radius: 24px; }
    .card { padding: 1rem; border-radius: 22px; }
    .logo-img { max-width: 220px; }
}
</style>
""", unsafe_allow_html=True)

STOPWORDS = set("""
a ad al allo ai agli all alla alle con col come da dal dallo dai dagli dall dalla dalle
di del dello dei degli dell della delle e ed è essere sono sei siamo siete era erano
in il lo la i gli le un uno una per tra fra su sul sulla sui sulle che chi cui non
più meno anche o oppure ma però quindi questo questa questi queste quello quella quelli quelle
nel nella nei nelle mi ti ci vi si io tu lui lei noi voi loro
innovazione futuro mondo anni grazie cosa quale secondo te
""".split())

POSITIVE_WORDS = {"fiducia","speranza","migliore","migliorare","opportunità","crescita","progresso","cura","benessere","sostenibile","sostenibilità","aiuto","collaborazione","accessibile","qualità","vita","soluzioni","pace"}
NEGATIVE_WORDS = {"paura","rischio","rischi","crisi","problema","problemi","ansia","disuguaglianze","pericolo","insicurezza","sostituire","perdere","controllo","climatica","guerra","povertà"}

def get_query_param():
    try:
        return st.query_params.get("page", "home")
    except Exception:
        return "home"

def set_page(page):
    st.query_params["page"] = page
    st.rerun()

def clean_words(text):
    text = str(text).lower()
    text = re.sub(r"[^a-zàèéìòóùç\s]", " ", text)
    words = [w.strip() for w in text.split() if len(w.strip()) > 2]
    return [w for w in words if w not in STOPWORDS]

def extract_keywords(text, top_n=5):
    words = clean_words(text)
    if not words:
        return []
    return [w for w, c in Counter(words).most_common(top_n)]

def simple_sentiment(text, rapporto):
    words = clean_words(text)
    score = 0
    for w in words:
        if w in POSITIVE_WORDS:
            score += 1
        if w in NEGATIVE_WORDS:
            score -= 1
    if rapporto in ["Entusiasmo", "Curiosità"]:
        score += 1
    elif rapporto in ["Paura", "Scetticismo"]:
        score -= 1
    if score > 0:
        return "positivo"
    if score < 0:
        return "critico"
    return "neutro"

def load_data():
    return pd.read_csv(DATA_FILE)

def save_response(ambito, problema, rapporto, frase, sentiment, keywords):
    df = load_data()
    new = pd.DataFrame([{
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "ambito": ambito,
        "problema": problema,
        "rapporto": rapporto,
        "frase": frase,
        "sentiment": sentiment,
        "parole_chiave": ", ".join(keywords)
    }])
    pd.concat([df, new], ignore_index=True).to_csv(DATA_FILE, index=False)

def logo_html():
    if logo_b64:
        return f'<img class="logo-img" src="data:image/png;base64,{logo_b64}">'
    return '<div class="badge">HERMES LAB</div>'

def top_value(df, col):
    if df.empty:
        return "-"
    return df[col].value_counts().idxmax()

def frase_momento(df):
    if df.empty or df["frase"].dropna().empty:
        return "La mappa collettiva prenderà forma con le prime risposte dei partecipanti."
    frasi = [f for f in df["frase"].dropna().astype(str).tolist() if len(f.strip()) > 20]
    if not frasi:
        return "Ogni contributo aggiunge un nodo alla mappa dell’innovazione."
    return random.choice(frasi)

def build_network(df, height="720px"):
    if df.empty:
        st.info("Il grafo si genererà dopo le prime risposte.")
        return

    net = Network(height=height, width="100%", bgcolor="#ffffff", font_color="#0f172a", directed=False)
    net.barnes_hut(gravity=-6200, central_gravity=0.25, spring_length=180)

    center = "Innovation Pulse"
    net.add_node(center, label=center, size=44, color="#0b4f8a")

    category_nodes = {
        "Ambiti": "#2563eb",
        "Problemi": "#0284c7",
        "Emozioni": "#0f766e",
        "Parole": "#64748b"
    }

    for cat, color in category_nodes.items():
        net.add_node(cat, label=cat, size=28, color=color)
        net.add_edge(center, cat)

    for _, row in df.iterrows():
        ambito = str(row["ambito"])
        problema = str(row["problema"])
        rapporto = str(row["rapporto"])
        sentiment = str(row["sentiment"])
        keywords = [k.strip() for k in str(row["parole_chiave"]).split(",") if k.strip()]

        net.add_node(ambito, label=ambito, size=27, color="#2563eb")
        net.add_node(problema, label=problema, size=25, color="#0284c7")
        net.add_node(rapporto, label=rapporto, size=22, color="#38bdf8")
        net.add_node(sentiment, label=sentiment, size=20, color="#0f766e")

        net.add_edge("Ambiti", ambito)
        net.add_edge("Problemi", problema)
        net.add_edge("Emozioni", rapporto)
        net.add_edge(rapporto, sentiment)
        net.add_edge(ambito, problema)

        for kw in keywords[:3]:
            net.add_node(kw, label=kw, size=16, color="#64748b")
            net.add_edge("Parole", kw)
            net.add_edge(problema, kw)

    net.save_graph("innovation_graph.html")
    with open("innovation_graph.html", "r", encoding="utf-8") as f:
        graph_html = f.read()
    components.html(graph_html, height=int(height.replace("px","")) + 40, scrolling=True)

def plot_bar(df, column, title):
    if df.empty:
        st.info("Ancora nessuna risposta raccolta.")
        return
    counts = df[column].value_counts()
    fig, ax = plt.subplots(figsize=(8, 4.3))
    counts.plot(kind="bar", ax=ax)
    ax.set_title(title)
    ax.set_xlabel("")
    ax.set_ylabel("Risposte")
    ax.tick_params(axis="x", rotation=30)
    st.pyplot(fig)

def show_wordcloud(df):
    if df.empty:
        st.info("La nuvola apparirà dopo le prime risposte.")
        return
    text = " ".join(df["frase"].dropna().astype(str).tolist())
    words = clean_words(text)
    if not words:
        st.info("Servono più parole per generare la nuvola.")
        return
    wc = WordCloud(width=1100, height=430, background_color="white", colormap="Blues").generate(" ".join(words))
    fig, ax = plt.subplots(figsize=(11, 4.5))
    ax.imshow(wc, interpolation="bilinear")
    ax.axis("off")
    st.pyplot(fig)

page = get_query_param()

st.markdown("""
<div class="nav-row">
    <div class="nav-pill">HERMES LAB</div>
    <div class="nav-pill">Innovation Day</div>
    <div class="nav-pill">NLP · Sentiment · Semantic Graph</div>
</div>
""", unsafe_allow_html=True)

if page == "home":
    df = load_data()

    st.markdown(f"""
    <div class="hero">
        {logo_html()}
        <div class="badge">POWERED BY HERMES LAB</div>
        <div class="main-title">Innovation Pulse</div>
        <div class="subtitle">
            Costruire il futuro attraverso linguaggio, dati e innovazione.
            Una web app interattiva per raccogliere, analizzare e visualizzare in tempo reale
            idee, bisogni ed emozioni legate all’innovazione.
        </div>
    </div>
    """, unsafe_allow_html=True)

    b1, b2 = st.columns(2)
    with b1:
        st.markdown('<div class="big-button-card"><h2>Partecipa</h2><p>Compila il questionario e genera il tuo profilo dell’innovazione.</p></div>', unsafe_allow_html=True)
        if st.button("Apri questionario"):
            set_page("participate")
    with b2:
        st.markdown('<div class="big-button-card"><h2>Innovation Pulse</h2><p>Visualizza il grafo collettivo che si aggiorna live durante l’evento.</p></div>', unsafe_allow_html=True)
        if st.button("Apri mappa live"):
            set_page("wall")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f'<div class="metric-card"><div class="metric-number">{len(df)}</div><div class="metric-label">partecipanti</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="metric-card"><div class="metric-number">6</div><div class="metric-label">ambiti monitorati</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="metric-card"><div class="metric-number">AI</div><div class="metric-label">analisi testuale</div></div>', unsafe_allow_html=True)

elif page == "participate":
    st.markdown(f"""
    <div class="hero">
        {logo_html()}
        <div class="badge">QUESTIONARIO INTERATTIVO</div>
        <div class="main-title">Partecipa</div>
        <div class="subtitle">
            La tua risposta diventa parte del grafo collettivo dell’innovazione.
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("← Torna alla homepage"):
        set_page("home")

    left, right = st.columns([1, 1])

    with left:
        st.markdown('<div class="card blue-card">', unsafe_allow_html=True)
        st.subheader("Il tuo profilo")

        ambito = st.radio("Secondo te, quale ambito cambierà di più il mondo nei prossimi anni?", [
            "Intelligenza artificiale", "Energia", "Salute", "Ambiente", "Industria", "Cultura"
        ])

        problema = st.radio("Quale problema dovrebbe risolvere prima l’innovazione?", [
            "Crisi climatica", "Disuguaglianze", "Lavoro e automazione", "Sanità",
            "Sicurezza", "Sostenibilità produttiva", "Qualità della vita"
        ])

        rapporto = st.radio("Che rapporto hai con l’innovazione?", [
            "Entusiasmo", "Curiosità", "Fiducia cauta", "Paura", "Scetticismo"
        ])

        frase = st.text_area(
            "In una frase, racconta quale futuro immagini grazie all’innovazione.",
            placeholder="Immagino un futuro in cui la tecnologia aiuta la ricerca e migliora la vita delle persone.",
            height=120
        )

        if st.button("Genera profilo e aggiorna la mappa"):
            if len(frase.strip()) < 8:
                st.warning("Scrivi almeno una frase breve.")
            else:
                keywords = extract_keywords(frase)
                sentiment = simple_sentiment(frase, rapporto)
                save_response(ambito, problema, rapporto, frase, sentiment, keywords)

                st.success("Risposta aggiunta alla mappa collettiva.")
                st.markdown(f"""
                <div class="result-box">
                    <h3>Il tuo profilo dell’innovazione</h3>
                    <p><b>Ambito:</b> {html.escape(ambito)}</p>
                    <p><b>Priorità:</b> {html.escape(problema)}</p>
                    <p><b>Rapporto:</b> {html.escape(rapporto)}</p>
                    <p><b>Orientamento emotivo:</b> {html.escape(sentiment)}</p>
                    <p><b>Parole chiave:</b> {html.escape(", ".join(keywords))}</p>
                </div>
                """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        df = load_data()
        st.markdown('<div class="card cyan-card">', unsafe_allow_html=True)
        st.subheader("Anteprima Innovation Pulse")

        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f'<div class="metric-card"><div class="metric-number">{len(df)}</div><div class="metric-label">partecipanti</div></div>', unsafe_allow_html=True)
        with c2:
            top = top_value(df, "ambito")
            st.markdown(f'<div class="metric-card"><div class="metric-number" style="font-size:1rem;">{html.escape(str(top))}</div><div class="metric-label">ambito più scelto</div></div>', unsafe_allow_html=True)

        build_network(df, height="520px")
        st.markdown('</div>', unsafe_allow_html=True)

elif page == "wall":
    st_autorefresh(interval=5000, key="refresh_live")
    df = load_data()

    st.markdown(f"""
    <div class="hero">
        {logo_html()}
        <div class="badge">LIVE SEMANTIC MAP</div>
        <div class="main-title">Innovation Pulse</div>
        <div class="subtitle">
            Il grafo si aggiorna automaticamente ogni 5 secondi con le risposte dei partecipanti.
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("← Torna alla homepage"):
        set_page("home")

    top_ambito = top_value(df, "ambito")
    top_prob = top_value(df, "problema")
    top_sent = top_value(df, "sentiment")
    frase = frase_momento(df)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'<div class="metric-card"><div class="metric-number">{len(df)}</div><div class="metric-label">partecipanti</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="metric-card"><div class="metric-number" style="font-size:1rem;">{html.escape(str(top_ambito))}</div><div class="metric-label">tema emergente</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="metric-card"><div class="metric-number" style="font-size:1rem;">{html.escape(str(top_prob))}</div><div class="metric-label">priorità collettiva</div></div>', unsafe_allow_html=True)
    with c4:
        st.markdown(f'<div class="metric-card"><div class="metric-number" style="font-size:1rem;">{html.escape(str(top_sent))}</div><div class="metric-label">sentiment prevalente</div></div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="quote-box">
        <div style="font-weight:900; opacity:.85; margin-bottom:.5rem;">FRASE DEL MOMENTO</div>
        <div class="quote-text">“{html.escape(frase)}”</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="card cyan-card">', unsafe_allow_html=True)
    build_network(df, height="760px")
    st.markdown('</div>', unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["Ambiti", "Problemi", "Rapporto", "Parole"])
    with tab1:
        plot_bar(df, "ambito", "Ambiti che cambieranno di più il mondo")
    with tab2:
        plot_bar(df, "problema", "Problemi prioritari")
    with tab3:
        plot_bar(df, "rapporto", "Rapporto con l’innovazione")
    with tab4:
        show_wordcloud(df)
