import streamlit as st
import math
from datetime import datetime, timedelta

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Simulador Clube04 - Campo Belo", page_icon="🐾", layout="wide")

st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            background-color: #FF8A00; 
        }
        [data-testid="stSidebar"] * {
            color: #FFFFFF !important; 
        }
        .stSelectbox label, .stNumberInput label, .stTextInput label, .stCheckbox label {
            font-weight: bold;
        }
        div[data-testid="stExpander"] div[role="button"] p {
            color: #FF8A00 !important;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# URL da Logo (Para o WhatsApp e Menu)
# Hospede a sua logo da primeira imagem no Imgur ou Poste no próprio GitHub para gerar um link direto e cole aqui:
LOGO_URL = "https://www.kalaes.com.br/22/wp-content/uploads/2023/08/CB04LOGO.png" # <- Substitua pelo link da sua logo

# --- TABELAS DE PREÇOS REAIS DO CLUBE04 ---
precos_banho = {
    "Até 10kg": {"Curto": 85.0, "Médio": 99.0, "Longo": 99.0},
    "Até 20kg": {"Curto": 105.0, "Médio": 139.0, "Longo": 139.0},
    "Até 50kg": {"Curto": 149.0, "Médio": 179.0, "Longo": 179.0},
    "Acima de 50kg": {"Curto": 239.0, "Médio": 279.0, "Longo": 279.0}
}

precos_mascaras = {
    "Senses/Detox": {"Até 10kg": 69.0, "Até 20kg": 79.0, "Até 50kg": 89.0, "Acima de 50kg": 109.0},
    "Luxo/Máx. Volume/Liso Intenso": {"Até 10kg": 59.0, "Até 20kg": 69.0, "Até 50kg": 79.0, "Acima de 50kg": 99.0},
    "Argan": {"Até 10kg": 49.0, "Até 20kg": 59.0, "Até 50kg": 69.0, "Acima de 50kg": 89.0},
    "Matização": {"Até 10kg": 69.0, "Até 20kg": 79.0, "Até 50kg": 89.0, "Acima de 50kg": 99.0}
}

precos_adicionais = {
    "Remoção de Pelos Mortos": {"Até 10kg": 79.0, "Até 20kg": 89.0, "Até 50kg": 99.0, "Acima de 50kg": 109.0},
    "Tosa Higiênica": {"Até 10kg": 39.0, "Até 20kg": 49.0, "Até 50kg": 59.0, "Acima de 50kg": 69.0},
    "Ozônio": {"Até 10kg": 39.0, "Até 20kg": 49.0, "Até 50kg": 59.0, "Acima de 50kg": 79.0},
    "Desembolo": {"Até 10kg": 99.0, "Até 20kg": 149.0, "Até 50kg": 189.0, "Acima de 50kg": 299.0},
    "Extra Soft": {"Até 10kg": 19.0, "Até 20kg": 29.0, "Até 50kg": 39.0, "Acima de 50kg": 49.0},
    "X-treme (Limpeza Profunda)": {"Até 10kg": 39.0, "Até 20kg": 39.0, "Até 50kg": 39.0, "Acima de 50kg": 39.0}
}

# Preços base para itens de balcão (Ajuste conforme sua loja)
preco_bravecto = 250.0 
preco_pacote_tapete = 89.0 # Pacote com 30 unidades

# --- BARRA LATERAL (INPUTS) ---
st.sidebar.image(LOGO_URL, width=150)
st.sidebar.markdown("### 👤 Atendimento")
vendedor = st.sidebar.text_input("Nome do vendedor(a)")
nome_tutor = st.sidebar.text_input("Nome do tutor(a)")
nome_pet = st.sidebar.text_input("Nome do doguinho")

st.sidebar.markdown("---")
st.sidebar.markdown("### 🐾 Perfil do Doguinho")
porte = st.sidebar.selectbox("Porte do Doguinho", ["Até 10kg", "Até 20kg", "Até 50kg", "Acima de 50kg"])
pelo = st.sidebar.selectbox("Tipo de pelo", ["Curto", "Médio", "Longo"])

st.sidebar.markdown("---")
st.sidebar.markdown("### 🛠️ Estrutura do Plano")
pacote_opcoes = {"Unitário": 1, "4 unidades": 4, "12 unidades": 12, "24 unidades": 24, "48 unidades": 48}
escolha_pacote = st.sidebar.selectbox("Pacote de Banhos", list(pacote_opcoes.keys()))
qtd_banhos = pacote_opcoes[escolha_pacote]
frequencia = st.sidebar.selectbox("Frequência", ["Semanal", "Quinzenal", "Mensal"])

st.sidebar.markdown("---")
st.sidebar.markdown("### ✨ 1) Extras: Beleza (Qtd)")

# Coletor dinâmico de Extras
selecao_mascaras = {}
selecao_adicionais = {}

with st.sidebar.expander("🧴 Selecionar Máscaras"):
    for mascara in precos_mascaras.keys():
        qtd = st.number_input(f"{mascara}", min_value=0, max_value=qtd_banhos, value=0, key=f"m_{mascara}")
        if qtd > 0: selecao_mascaras[mascara] = qtd

with st.sidebar.expander("✂️ Selecionar Adicionais"):
    for adicional in precos_adicionais.keys():
        qtd = st.number_input(f"{adicional}", min_value=0, max_value=qtd_banhos, value=0, key=f"a_{adicional}")
        if qtd > 0: selecao_adicionais[adicional] = qtd

st.sidebar.markdown("---")
st.sidebar.markdown("### 🛒 2) Extras: Consumo")
quer_bravecto = st.sidebar.checkbox("Incluir Bravecto?")
tapetes_semana = st.sidebar.number_input("Tapete Higiênico (Unidades usadas por SEMANA)", min_value=0, max_value=50, value=0)

# --- MOTOR DE CÁLCULO ---
descontos_fixos = {1: 0.0, 4: 0.05, 12: 0.08, 24: 0.10, 48: 0.20}

def calcular_simulacao(q_banhos, freq, sel_masc, sel_adic, flag_bravecto, tap_semana):
    if freq == "Semanal": semanas_duracao = q_banhos
    elif freq == "Quinzenal": semanas_duracao = q_banhos * 2
    else: semanas_duracao = q_banhos * 4 # Mensal
    
    meses_duracao = semanas_duracao / 4
    dias_duracao = semanas_duracao * 7
    
    q_bravecto = math.ceil(meses_duracao / 3) if flag_bravecto and meses_duracao > 0 else 0
    total_tapetes_unidade = semanas_duracao * tap_semana
    q_pacotes_tapete = math.ceil(total_tapetes_unidade / 30)

    # Cálculo dos Banhos
    valor_banho_un = precos_banho[porte][pelo]
    total_banhos = valor_banho_un * q_banhos
    
    # Cálculo das Máscaras e Adicionais (Baseado no Porte)
    total_mascaras = sum([qtd * precos_mascaras[item][porte] for item, qtd in sel_masc.items()])
    total_adicionais = sum([qtd * precos_adicionais[item][porte] for item, qtd in sel_adic.items()])
    total_beleza = total_mascaras + total_adicionais
    
    # Cálculo de Consumo
    total_consumo = (q_bravecto * preco_bravecto) + (q_pacotes_tapete * preco_pacote_tapete)
    
    total_avulso = total_banhos + total_beleza + total_consumo
    desc_percentual = descontos_fixos[q_banhos]
    total_com_desconto = total_avulso * (1 - desc_percentual)
    
    return {
        "avulso": total_avulso,
        "final": total_com_desconto,
        "economia": total_avulso - total_com_desconto,
        "desc_perc": desc_percentual,
        "q_bravecto": q_bravecto,
        "q_tapetes": q_pacotes_tapete,
        "meses": round(meses_duracao, 1),
        "dias": dias_duracao,
        "valor_banho_un": valor_banho_un
    }

plano_atual = calcular_simulacao(qtd_banhos, frequencia, selecao_mascaras, selecao_adicionais, quer_bravecto, tapetes_semana)

# --- TELA PRINCIPAL ---
st.title(f"🐾 Proposta de Bem-Estar: **{nome_pet or 'Doguinho'}** do(a) **{nome_tutor or 'Tutor(a)'}**")
st.markdown(f"**Atendimento:** {vendedor or 'Equipe Clube04'} | **Unidade:** Campo Belo")
st.markdown("---")

st.header("📊 Comparativo de Valor")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Preço Avulso (Sem Desconto)", f"R$ {plano_atual['avulso']:.2f}")

with col2:
    st.metric(
        f"Preço CLUBE04 ({int(plano_atual['desc_perc']*100)}% OFF)", 
        f"R$ {plano_atual['final']:.2f}", 
        delta=f"- R$ {plano_atual['economia']:.2f} economizados!"
    )

with col3:
    if qtd_banhos > 1:
        economia_mes = plano_atual['economia'] / (plano_atual['meses'] if plano_atual['meses'] > 0 else 1)
        st.metric("Economia Média por Mês", f"R$ {economia_mes:.2f}")
    else:
        st.metric("Economia", "R$ 0,00 (Plano Unitário)")

# --- MOTOR DE UPSELL ---
niveis = [1, 4, 12, 24, 48]
indice_atual = niveis.index(qtd_banhos)

if indice_atual < len(niveis) - 1:
    proximo_nivel = niveis[indice_atual + 1]
    plano_upsell = calcular_simulacao(proximo_nivel, frequencia, selecao_mascaras, selecao_adicionais, quer_bravecto, tapetes_semana)
    desc_upsell = int(plano_upsell['desc_perc'] * 100)
    
    st.success(f"🚀 **Oportunidade de Ouro:** Se você levar o pacote de **{proximo_nivel} unidades**, seu desconto sobe para **{desc_upsell}%** em TODOS os itens (banho, beleza e consumo) e você economiza um total de **R$ {plano_upsell['economia']:.2f}**!")

st.markdown("---")

# --- RESUMO WHATSAPP ---
st.subheader("📱 Resumo para Envio")
if st.checkbox("Montar Resumo para o WhatsApp"):
    with st.container(border=True):
        col_logo, col_texto = st.columns([1, 4])
        with col_logo:
            try:
                st.image(LOGO_URL, width=80)
            except:
                pass
        with col_texto:
            st.markdown(f"### CLUBE04 - Unidade Campo Belo")
            st.markdown(f"**Proposta exclusiva para o(a) {nome_pet}**")
            
        # Formatando listas de extras
        lista_masc = [f"{qtd}x {item} (R$ {precos_mascaras[item][porte]:.2f}/un)" for item, qtd in selecao_mascaras.items()]
        lista_adic = [f"{qtd}x {item} (R$ {precos_adicionais[item][porte]:.2f}/un)" for item, qtd in selecao_adicionais.items()]
        todos_extras = lista_masc + lista_adic
        texto_extras = "\n- ".join(todos_extras) if todos_extras else "Nenhum"
        
        texto_consumo = []
        if plano_atual['q_bravecto'] > 0: texto_consumo.append(f"{plano_atual['q_bravecto']}x Bravecto(s) (Cobertura do período)")
        if plano_atual['q_tapetes'] > 0: texto_consumo.append(f"{plano_atual['q_tapetes']}x Pct Tapete Higiênico (30 un/cada)")
        texto_consumo_str = "\n- ".join(texto_consumo) if texto_consumo else "Nenhum"

        st.markdown(f"""
        **📋 Detalhes do Plano:**
        - **Banhos:** {qtd_banhos} unidades ({porte} - Pelo {pelo})
        - **Valor Base do Banho:** R$ {plano_atual['valor_banho_un']:.2f}
        - **Frequência:** {frequencia}
        - **Duração Estimada:** {plano_atual['meses']} meses ({plano_atual['dias']} dias)
        
        **✨ Extras de Beleza Inclusos:**
        - {texto_extras}
        
        **🛒 Consumo Incluso:**
        - {texto_consumo_str}
        
        ---
        ❌ Valor Avulso (Sem Clube): ~~R$ {plano_atual['avulso']:.2f}~~
        ✅ **Valor no CLUBE04: R$ {plano_atual['final']:.2f}** *(Desconto aplicado de {int(plano_atual['desc_perc']*100)}%)*
        
        *Atendente: {vendedor}*
        """)
