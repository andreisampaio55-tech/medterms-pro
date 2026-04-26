import re
import streamlit as st
import random
from difflib import SequenceMatcher
from data.termos import termos

# Ícones por área médica
icones_areas = {
    "Cardiologia": "❤️",
    "Neurologia": "🧠",
    "Gastroenterologia": "🍽️",
    "Pneumologia": "🫁",
    "Clínica Médica": "🏥",
    "Infectologia": "🦠",
    "Nefrologia": "🧪",
    "Endocrinologia": "🧬",
    "Ortopedia": "🦴",
    "Obstetrícia/Ginecologia": "🤰"
}

st.set_page_config(page_title="MedTerms Pro", layout="centered")

# Carregar CSS personalizado
def load_css():
    css = """
/* Fundo geral médico com paleta suave e azul claro */
html, body, [data-testid="stAppViewContainer"], [data-testid="stAppViewContainer"] > div {
    background-color: #eef6fb !important;
    background-image:
        radial-gradient(circle at top left, rgba(255, 255, 255, 0.95), transparent 22%),
        radial-gradient(circle at bottom right, rgba(255, 255, 255, 0.95), transparent 24%),
        linear-gradient(135deg, #d4efff 0%, #c4f0ff 40%, #d1f8ff 70%, #f6fbff 100%);
    background-blend-mode: screen, screen, normal;
    background-size: cover;
    background-position: center;
    color: #333;
    min-height: 100vh;
}

.css-18e3th9, .css-14xtw13, .css-1v0mbdj {
    background: transparent !important;
}

body::after {
    content: "";
    position: fixed;
    inset: 0;
    background-image: radial-gradient(circle at center, rgba(255,255,255,0.18), transparent 25%), linear-gradient(45deg, rgba(255,255,255,0.10) 25%, transparent 25%, transparent 50%, rgba(255,255,255,0.10) 50%, rgba(255,255,255,0.10) 75%, transparent 75%, transparent);
    background-size: 120px 120px, 60px 60px;
    pointer-events: none;
    z-index: -1;
}

/* Título principal personalizado */
.hero-container {
    text-align: center;
    margin-bottom: 10px;
}

.hero-title {
    font-size: 3rem;
    margin: 0;
    background: linear-gradient(90deg, #ff0080, #00ff80, #0080ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-weight: 800;
    letter-spacing: 1px;
}

.hero-image {
    margin-top: 15px;
    max-width: 140px;
    border-radius: 18px;
    box-shadow: 0 12px 30px rgba(0,0,0,0.18);
}

/* Subtítulos */
h2, h3 {
    color: #ffffff;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
}

/* Cards modernos com cores vibrantes */
.card {
    background: rgba(255, 255, 255, 0.96);
    padding: 25px;
    border-radius: 18px;
    box-shadow: 0 10px 28px rgba(0,0,0,0.12);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(64, 190, 187, 0.22);
    margin-bottom: 20px;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    position: relative;
    overflow: hidden;
}

.card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 6px;
    background: linear-gradient(90deg, #23c3c0, #2bb4f4, #4fd7b6);
}

.card:hover {
    transform: translateY(-6px);
    box-shadow: 0 14px 46px rgba(0,0,0,0.18);
}

/* Botões estilizados */
.stButton > button {
    background: linear-gradient(45deg, #23c3c0, #2bb4f4);
    color: white;
    border: none;
    border-radius: 25px;
    padding: 12px 24px;
    font-weight: bold;
    font-size: 16px;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
}

.stButton > button:hover {
    background: linear-gradient(45deg, #2bb4f4, #23c3c0);
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0,0,0,0.3);
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: rgba(255, 255, 255, 0.9);
    backdrop-filter: blur(10px);
    border-right: 1px solid rgba(255, 255, 255, 0.2);
}

/* Inputs */
.stTextInput > div > div > input {
    border-radius: 10px;
    border: 2px solid #4ecdc4;
    padding: 10px;
    font-size: 16px;
    transition: border-color 0.3s ease;
}

.stTextInput > div > div > input:focus {
    border-color: #ff6b6b;
}

.stSelectbox > div > div > div {
    border-radius: 10px;
    border: 2px solid #4ecdc4;
}

/* Success e Error */
.stAlert {
    border-radius: 10px;
    border: none;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}
"""
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

load_css()

st.markdown(
    """
    <div class="hero-container">
        <h1 class="hero-title">🧠 MedTerms Pro — Nível Residência</h1>
        <img class="hero-image" src="https://img.icons8.com/fluency/120/000000/medical-doctor.png" alt="MedTerms Pro" />
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("---")

if "user_terms" not in st.session_state:
    st.session_state.user_terms = []

with st.sidebar.expander("Adicionar termo", expanded=True):
    with st.form("add_term_form"):
        novo_termo = st.text_input("Termo", key="novo_termo")
        nova_area = st.text_input("Área", key="nova_area")
        novo_significado = st.text_area("Significado", key="novo_significado")
        novo_exemplo = st.text_area("Exemplo clínico", key="novo_exemplo")
        enviar_termo = st.form_submit_button("Adicionar termo")

        if enviar_termo:
            if novo_termo.strip() and nova_area.strip() and novo_significado.strip():
                st.session_state.user_terms.append({
                    "termo": novo_termo.strip(),
                    "area": nova_area.strip(),
                    "significado": novo_significado.strip(),
                    "exemplo": novo_exemplo.strip() or "Sem exemplo fornecido."
                })
                st.success(f"✅ Termo '{novo_termo.strip()}' adicionado com sucesso.")
                st.session_state.novo_termo = ""
                st.session_state.nova_area = ""
                st.session_state.novo_significado = ""
                st.session_state.novo_exemplo = ""
            else:
                st.error("Preencha Termo, Área e Significado para adicionar.")

# =========================
# 📚 BANCO DE TERMOS
# =========================

# O banco de termos agora é carregado de data/termos.py para facilitar crescimento


def normalize_text(text):
    text = str(text).lower()
    text = re.sub(r"[^a-z0-9áâàãéêíóôõúçñ\s]+", " ", text)
    return " ".join(text.split())


def meaning_matches(answer: str, expected: str) -> bool:
    normalized_answer = normalize_text(answer)
    normalized_expected = normalize_text(expected)
    if not normalized_answer or not normalized_expected:
        return False

    if normalized_expected in normalized_answer:
        return True

    expected_words = set(normalized_expected.split())
    answer_words = set(normalized_answer.split())
    common = expected_words.intersection(answer_words)
    if len(common) >= max(1, int(len(expected_words) * 0.55)):
        return True

    similarity = SequenceMatcher(None, normalized_expected, normalized_answer).ratio()
    return similarity >= 0.65

# =========================
# 🎯 MENU
# =========================

modo = st.sidebar.radio("Modo", ["Estudo", "Prova", "Aleatório"])

termos = termos + st.session_state.user_terms
areas = sorted(set([t["area"] for t in termos]))
filtro_area = st.sidebar.selectbox("Filtrar por área", ["Todas"] + areas)

if filtro_area != "Todas":
    termos_filtrados = [t for t in termos if t["area"] == filtro_area]
else:
    termos_filtrados = termos

# =========================
# 📖 MODO ESTUDO
# =========================

if modo == "Estudo":
    nomes = [t["termo"] for t in termos_filtrados]
    escolha = st.selectbox("Escolha um termo:", nomes)

    for t in termos_filtrados:
        if t["termo"] == escolha:
            icone = icones_areas.get(t['area'], "🏥")
            st.markdown(f"""
            <div class="card">
                <h2>{icone} {t['termo']}</h2>
                <p><strong>Área:</strong> {t['area']}</p>
                <p><strong>Significado:</strong> {t['significado']}</p>
                <p><strong>Exemplo clínico:</strong> {t['exemplo']}</p>
            </div>
            """, unsafe_allow_html=True)

# =========================
# 🧪 MODO PROVA
# =========================

elif modo == "Prova":

    if "score" not in st.session_state:
        st.session_state.score = 0

    if "prova_index" not in st.session_state or st.session_state.prova_index >= len(termos_filtrados):
        st.session_state.prova_index = random.randrange(len(termos_filtrados))
        st.session_state.resposta_prova = ""

    if st.button("Novo termo"):
        st.session_state.prova_index = random.randrange(len(termos_filtrados))
        st.session_state.resposta_prova = ""

    termo = termos_filtrados[st.session_state.prova_index]

    st.markdown(f"""
    <div class="card">
        <h3>❓ O que significa: <strong>{termo['termo']}</strong>?</h3>
    </div>
    """, unsafe_allow_html=True)

    if "resposta_prova" not in st.session_state:
        st.session_state.resposta_prova = ""

    with st.form("prova_form"):
        resposta = st.text_input("Digite sua resposta", key="resposta_prova")
        submit = st.form_submit_button("Responder")

    if submit:
        if meaning_matches(resposta, termo["significado"]):
            st.success("✅ Correto!")
            st.session_state.score += 1
        else:
            st.error("❌ Errado")

        st.markdown(f"""
        <div class="card">
            <h4>📘 Definição de {termo['termo']}</h4>
            <p><strong>Significado:</strong> {termo['significado']}</p>
            <p><strong>Exemplo:</strong> {termo['exemplo']}</p>
        </div>
        """, unsafe_allow_html=True)

    st.write(f"🏆 Pontuação: {st.session_state.score}")

# =========================
# 🎲 MODO ALEATÓRIO
# =========================

elif modo == "Aleatório":
    if st.button("Gerar termo"):
        t = random.choice(termos_filtrados)
        icone = icones_areas.get(t['area'], "🏥")
        st.markdown(f"""
        <div class="card">
            <h2>{icone} {t['termo']}</h2>
            <p><strong>Área:</strong> {t['area']}</p>
            <p><strong>Significado:</strong> {t['significado']}</p>
            <p><strong>Exemplo:</strong> {t['exemplo']}</p>
        </div>
        """, unsafe_allow_html=True)
