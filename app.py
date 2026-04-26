import streamlit as st
import random

# Ícones por área médica
icones_areas = {
    "Cardiologia": "❤️",
    "Neurologia": "🧠",
    "Gastroenterologia": "🍽️",
    "Pneumologia": "🫁",
    "Clínica Médica": "🏥"
}

st.set_page_config(page_title="MedTerms Pro", layout="centered")

# Carregar CSS personalizado
def load_css():
    with open("styles/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

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

# =========================
# 📚 BANCO DE TERMOS
# =========================

# =========================
# 📚 BANCO DE TERMOS
# =========================

termos = [
    # CARDIO
    {"termo": "Taquicardia", "area": "Cardiologia",
     "significado": "Frequência cardíaca >100 bpm",
     "exemplo": "Paciente séptico com FC 130 bpm."},

    {"termo": "Bradicardia", "area": "Cardiologia",
     "significado": "Frequência cardíaca <60 bpm",
     "exemplo": "Atleta com bradicardia fisiológica."},

    {"termo": "Angina", "area": "Cardiologia",
     "significado": "Dor torácica por isquemia miocárdica",
     "exemplo": "Dor ao esforço que melhora com repouso."},

    {"termo": "Ortopneia", "area": "Cardiologia",
     "significado": "Dispneia ao deitar",
     "exemplo": "Paciente dorme com 3 travesseiros."},

    # NEURO
    {"termo": "Parestesia", "area": "Neurologia",
     "significado": "Sensação anormal (formigamento)",
     "exemplo": "Formigamento em mãos e pés."},

    {"termo": "Síncope", "area": "Neurologia",
     "significado": "Perda súbita de consciência",
     "exemplo": "Desmaio após dor intensa."},

    {"termo": "Convulsão", "area": "Neurologia",
     "significado": "Atividade elétrica cerebral anormal",
     "exemplo": "Crise tônico-clônica generalizada."},

    {"termo": "Afasia", "area": "Neurologia",
     "significado": "Alteração da linguagem",
     "exemplo": "Paciente não consegue nomear objetos."},

    # GASTRO
    {"termo": "Hematêmese", "area": "Gastroenterologia",
     "significado": "Vômito com sangue",
     "exemplo": "Úlcera gástrica sangrante."},

    {"termo": "Melena", "area": "Gastroenterologia",
     "significado": "Fezes negras com sangue digerido",
     "exemplo": "Sangramento digestivo alto."},

    {"termo": "Icterícia", "area": "Gastroenterologia",
     "significado": "Pele amarelada por bilirrubina",
     "exemplo": "Hepatite viral."},

    {"termo": "Ascite", "area": "Gastroenterologia",
     "significado": "Líquido na cavidade abdominal",
     "exemplo": "Cirrose hepática."},

    # RESP
    {"termo": "Dispneia", "area": "Pneumologia",
     "significado": "Falta de ar",
     "exemplo": "Paciente com DPOC."},

    {"termo": "Hemoptise", "area": "Pneumologia",
     "significado": "Expectoração com sangue",
     "exemplo": "Tuberculose pulmonar."},

    {"termo": "Sibilos", "area": "Pneumologia",
     "significado": "Ruído respiratório tipo chiado",
     "exemplo": "Crise asmática."},

    {"termo": "Crepitações", "area": "Pneumologia",
     "significado": "Estertores pulmonares",
     "exemplo": "Edema agudo de pulmão."},

    # GERAL
    {"termo": "Astenia", "area": "Clínica Médica",
     "significado": "Fraqueza generalizada",
     "exemplo": "Infecção viral."},

    {"termo": "Adinamia", "area": "Clínica Médica",
     "significado": "Perda de força",
     "exemplo": "Paciente acamado."},

    {"termo": "Anasarca", "area": "Clínica Médica",
     "significado": "Edema generalizado",
     "exemplo": "Síndrome nefrótica."},

    {"termo": "Cianose", "area": "Clínica Médica",
     "significado": "Coloração azulada por hipóxia",
     "exemplo": "Extremidades frias e azuladas."},
]

# =========================
# 🎯 MENU
# =========================

modo = st.sidebar.radio("Modo", ["Estudo", "Prova", "Aleatório"])

areas = list(set([t["area"] for t in termos]))
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
        if termo["significado"].strip().lower() in resposta.strip().lower():
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
