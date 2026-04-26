import streamlit as st
import random

st.set_page_config(page_title="MedTerms Pro", layout="centered")

st.title("🧠 MedTerms Pro — Nível Residência")

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
            st.markdown(f"## 📌 {t['termo']}")
            st.write(f"**Área:** {t['area']}")
            st.write(f"**Significado:** {t['significado']}")
            st.write(f"**Exemplo clínico:** {t['exemplo']}")

# =========================
# 🧪 MODO PROVA
# =========================

elif modo == "Prova":

    if "score" not in st.session_state:
        st.session_state.score = 0

    termo = random.choice(termos_filtrados)

    st.markdown(f"### ❓ O que significa: **{termo['termo']}** ?")

    resposta = st.text_input("Digite sua resposta")

    if st.button("Responder"):
        if termo["significado"].lower() in resposta.lower():
            st.success("✅ Correto!")
            st.session_state.score += 1
        else:
            st.error("❌ Errado")
            st.write(f"✔ Resposta: {termo['significado']}")

    st.write(f"🏆 Pontuação: {st.session_state.score}")

# =========================
# 🎲 MODO ALEATÓRIO
# =========================

elif modo == "Aleatório":
    if st.button("Gerar termo"):
        t = random.choice(termos_filtrados)
        st.markdown(f"## 🎲 {t['termo']}")
        st.write(f"**Área:** {t['area']}")
        st.write(f"**Significado:** {t['significado']}")
        st.write(f"**Exemplo:** {t['exemplo']}")
