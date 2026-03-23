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
        .reference-text {
            color: #555;
            font-size: 0.9em;
            font-style: italic;
        }
    </style>
""", unsafe_allow_html=True)

# URL da Logo (Para o WhatsApp e Menu)
LOGO_URL = "https://www.kalaes.com.br/22/wp-content/uploads/2023/08/CB04LOGO.png" # <- Substitua pelo link da sua logo real

# --- TABELAS DE PREÇOS UNITÁRIOS REAIS DO CLUBE04 (AVULSO) ---

# Tabela 1: Banhos (Avulso Unitário) - image_2.png
# Atualizado com nomes de peso exatos
precos_banho_avulso = {
    "Até 10 kg": {"Curto": 85.0, "Médio": 99.0, "Longo": 99.0},
    "Até 20 kg": {"Curto": 105.0, "Médio": 139.0, "Longo": 139.0},
    "Até 50 kg": {"Curto": 149.0, "Médio": 179.0, "Longo": 179.0},
    "+ 50 kg": {"Curto": 239.0, "Médio": 279.0, "Longo": 279.0}
}

# Tabela 1: Tosa (Avulso Unitário - Tabela de Base) - image_2.png
# Tratada como extra, aplicando o desconto geral do pacote escolhido
precos_tosa_avulso = {
    "Até 10 kg": 209.0,
    "Até 20 kg": 279.0,
    "Até 50 kg": 489.0,
    "+ 50 kg": 699.0
}

# Tabela 2: Máscaras (Avulso Unitário) - image_3.png
precos_mascaras_avulso = {
    "Senses/Detox": {"Até 10 kg": 69.0, "Até 20 kg": 79.0, "Até 50 kg": 89.0, "+ 50 kg": 109.0},
    "Luxo/Máx. Volume/Liso Intenso": {"Até 10 kg": 59.0, "Até 20 kg": 69.0, "Até 50 kg": 79.0, "+ 50 kg": 99.0},
    "Argan": {"Até 10 kg": 49.0, "Até 20 kg": 59.0, "Até 50 kg": 69.0, "+ 50 kg": 89.0},
    "Matização": {"Até 10 kg": 69.0, "Até 20 kg": 79.0, "Até 50 kg": 89.0, "+ 50 kg": 99.0}
}

# Tabela 2: Adicionais (Avulso Unitário) - image_3.png
precos_adicionais_avulso = {
    "Remoção de Pelos Mortos": {"Até 10 kg": 79.0, "Até 20 kg": 89.0, "Até 50 kg": 99.0, "+ 50 kg": 109.0},
    "Tosa Higiênica": {"Até 10 kg": 39.0, "Até 20 kg": 49.0, "Até 50 kg": 59.0, "+ 50 kg": 69.0},
    "Ozônio": {"Até 10 kg": 39.0, "Até 20 kg": 49.0, "Até 50 kg": 59.0, "+ 50 kg": 79.0},
    "Desembolo": {"Até 10 kg": 99.0, "Até 20 kg": 149.0, "Até 50 kg": 189.0, "+ 50 kg": 299.0},
    "Extra Soft": {"Até 10 kg": 19.0, "Até 20 kg": 29.0, "Até 50 kg": 39.0, "+ 50 kg": 49.0},
    "X-treme (Limpeza Profunda)": {"Até 10 kg": 39.0, "Até 20 kg": 39.0, "Até 50 kg": 39.0, "+ 50 kg": 39.0}
}

# Tabela 3: Bravecto (Avulso Unitário) - image_4.png
# Atualizado com nomes de peso exatos da planilha
precos_bravecto_avulso = {
    "4.5 - 10 kg": 238.90,
    "10 - 20 kg": 294.90,
    "20 - 40 kg": 352.90,
    "40 - 56 kg": 344.90
}

# --- BARRA LATERAL (INPUTS) ---
st.sidebar.image(LOGO_URL, width=150)
st.sidebar.markdown("### 👤 Atendimento")
vendedor = st.sidebar.text_input("Nome do vendedor(a)")
nome_tutor = st.sidebar.text_input("Nome do tutor(a)")
nome_pet = st.sidebar.text_input("Nome do doguinho")

st.sidebar.markdown("---")
st.sidebar.markdown("### 🐾 Perfil do Doguinho")
porte = st.sidebar.selectbox("Porte do Doguinho", list(precos_banho_avulso.keys()))
pelo = st.sidebar.selectbox("Tipo de pelo", ["Curto", "Médio", "Longo"])

st.sidebar.markdown("---")
st.sidebar.markdown("### 🛠️ Estrutura do Plano")
# Atualizado conforme image_2.png
pacote_opcoes = {"Unitário": 1, "4 unidades": 4, "8 unidades": 8, "12 unidades": 12, "24 unidades": 24, "48 unidades": 48}
escolha_pacote = st.sidebar.selectbox("Pacote de Banhos", list(pacote_opcoes.keys()))
qtd_banhos = pacote_opcoes[escolha_pacote]
frequencia = st.sidebar.selectbox("Frequência", ["Semanal", "Quinzenal", "Mensal"])

st.sidebar.markdown("---")
st.sidebar.markdown("### ✨ 1) Extras: Beleza (Qtd)")

# Coletor dinâmico de Extras
selecao_mascaras = {}
selecao_adicionais = {}

with st.sidebar.expander("🧴 Selecionar Máscaras"):
    for mascara in precos_mascaras_avulso.keys():
        qtd = st.number_input(f"{mascara}", min_value=0, max_value=qtd_banhos, value=0, key=f"m_{mascara}")
        if qtd > 0: selecao_mascaras[mascara] = qtd

with st.sidebar.expander("✂️ Selecionar Adicionais"):
    # Inclui a Tosa Geral como Adicional dinâmico
    for adicional in list(precos_adicionais_avulso.keys()) + ["Tosa Geral"]:
        qtd = st.number_input(f"{adicional}", min_value=0, max_value=qtd_banhos, value=0, key=f"a_{adicional}")
        if qtd > 0: selecao_adicionais[adicional] = qtd

st.sidebar.markdown("---")
st.sidebar.markdown("### 🛒 2) Extras: Consumo")
quer_bravecto = st.sidebar.checkbox("Incluir Bravecto?")
if quer_bravecto:
    peso_bravecto = st.sidebar.selectbox("Peso para Bravecto", list(precos_bravecto_avulso.keys()))
else:
    peso_bravecto = None

# --- MOTOR DE CÁLCULO E LOGÍSTICA ---
# Estrutura de descontos fixos conforme image_2.png
descontos_fixos = {1: 0.0, 4: 0.05, 8: 0.07, 12: 0.10, 24: 0.15, 48: 0.20}

def calcular_simulacao(q_banhos, freq, sel_masc, sel_adic, p_bravecto_peso):
    # Duração
    if freq == "Semanal": semanas_duracao = q_banhos
    elif freq == "Quinzenal": semanas_duracao = q_banhos * 2
    else: semanas_duracao = q_banhos * 4 # Mensal
    
    meses_duracao = semanas_duracao / 4
    dias_duracao = semanas_duracao * 7
    
    # Consumo
    q_bravecto = math.ceil(meses_duracao / 3) if p_bravecto_peso and meses_duracao > 0 else 0

    # 1. Recuperar Preços Unitários Padrão (Avulso)
    banho_avulso_un = precos_banho_avulso[porte][pelo]
    tosa_avulso_un = precos_tosa_avulso[porte] if "Tosa Geral" in sel_adic else 0.0
    bravecto_avulso_un = precos_bravecto_avulso[p_bravecto_peso] if p_bravecto_peso else 0.0

    # 2. Formação do Valor Avulso Padrão (Sem Desconto)
    total_banhos_avulso_padrao = banho_avulso_un * q_banhos
    
    # Cálculo das Máscaras e Adicionais (Baseado no Porte)
    total_mascaras_avulso_padrao = sum([qtd * precos_mascaras_avulso[item][porte] for item, qtd in sel_masc.items()])
    
    # Adicionais normais + Tosa Geral
    adic_normal = sum([qtd * precos_adicionais_avulso[item][porte] for item, qtd in sel_adic.items() if item != "Tosa Geral"])
    qtd_tosa_geral = sel_adic["Tosa Geral"] if "Tosa Geral" in sel_adic else 0
    adic_tosa_geral = qtd_tosa_geral * tosa_avulso_un
    total_adicionais_avulso_padrao = adic_normal + adic_tosa_geral
    
    total_beleza_avulso_padrao = total_mascaras_avulso_padrao + total_adicionais_avulso_padrao
    total_consumo_avulso_padrao = q_bravecto * bravecto_avulso_un
    
    # TOTAL GERAL AVULSO (Tabela Padrão como referência)
    total_avulso_geral = total_banhos_avulso_padrao + total_beleza_avulso_padrao + total_consumo_avulso_padrao
    
    # 3. Formação do Valor Clube04 (Aplicando Desconto Fixo em TUDO)
    desc_percentual = descontos_fixos[q_banhos]
    
    total_com_desconto = total_avulso_geral * (1 - desc_percentual)
    
    # 4. Preços Unitários e Totais Detalhados (Para referência Padrão vs Clube)
    return {
        "avulso_un": banho_avulso_un,
        "banho_clube_un": banho_avulso_un * (1 - desc_percentual),
        "total_avulso_apenas_banhos": total_banhos_avulso_padrao,
        "total_clube_apenas_banhos": total_banhos_avulso_padrao * (1 - desc_percentual),
        
        "total_avulso_geral": total_avulso_geral,
        "total_clube_geral": total_com_desconto,
        "economia": total_avulso_geral - total_com_desconto,
        "desc_perc": desc_percentual,
        
        "q_bravecto": q_bravecto,
        "bravecto_avulso_un": bravecto_avulso_un,
        "bravecto_clube_un": bravecto_avulso_un * (1 - desc_percentual),
        "total_avulso_apenas_consumo": total_consumo_avulso_padrao,
        
        "total_avulso_apenas_beleza": total_beleza_avulso_padrao,
        
        "meses": round(meses_duracao, 1),
        "dias": dias_duracao
    }

plano_atual = calcular_simulacao(qtd_banhos, frequencia, selecao_mascaras, selecao_adicionais, peso_bravecto)

# --- TELA PRINCIPAL ---
st.title(f"🐾 Proposta de Bem-Estar: **{nome_pet or 'Doguinho'}** do(a) **{nome_tutor or 'Tutor(a)'}**")
st.markdown(f"**Atendimento:** {vendedor or 'Equipe Clube04'} | **Unidade:** Campo Belo")
st.markdown("---")

st.header("📊 Comparativo de Valor")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Tabela Padrão (Sem Desconto)", f"R$ {plano_atual['total_avulso_geral']:.2f}")

with col2:
    st.metric(
        f"Preço CLUBE04 ({int(plano_atual['desc_perc']*100)}% OFF)", 
        f"R$ {plano_atual['total_clube_geral']:.2f}", 
        delta=f"- R$ {plano_atual['economia']:.2f} economizados!"
    )

with col3:
    if qtd_banhos > 1:
        economia_mes = plano_atual['economia'] / (plano_atual['meses'] if plano_atual['meses'] > 0 else 1)
        st.metric("Economia Média por Mês", f"R$ {economia_mes:.2f}")
    else:
        st.metric("Economia", "R$ 0,00 (Plano Unitário)")

# --- MOTOR DE UPSELL ---
niveis = [1, 4, 8, 12, 24, 48] # Atualizado conforme image_2.png
try:
    indice_atual = niveis.index(qtd_banhos)
except ValueError:
    indice_atual = len(niveis) # Caso seja unitário e não tenha próximo pacote

if indice_atual < len(niveis) - 1:
    proximo_nivel = niveis[indice_atual + 1]
    plano_upsell = calcular_simulacao(proximo_nivel, frequencia, selecao_mascaras, selecao_adicionais, peso_bravecto)
    desc_upsell = int(plano_upsell['desc_perc'] * 100)
    
    st.success(f"🚀 **Oportunidade de Ouro:** Se você levar o pacote de **{proximo_nivel} unidades**, seu desconto sobe para **{desc_upsell}%** em TODOS os itens (banho, beleza e consumo) e você economiza um total de **R$ {plano_upsell['economia']:.2f}**!")

st.markdown("---")

# --- DETALHAMENTO DA REFERÊNCIA PADRÃO ---
st.subheader("🏁 Detalhamento (Padrão vs. Clube04)")
st.markdown(f"Planos Clube04 são calculados com base na nossa tabela de preços unitários avulsos.")

# Resumo exemplificado conforme solicitação do usuário
st.markdown(f"""
<div style="background-color:#fef6eb; padding:15px; border-radius:10px; border: 1px solid #FF8A00">
    <h4 style="margin-top:0">Exemplo de Cálculo: Banhos</h4>
    <p style="margin-bottom:0px" class="reference-text">
        Pacote {qtd_banhos}x Banho ({porte}/{pelo}) - unitário R$ {plano_atual['avulso_un']:.2f} e total sem desconto R$ {plano_atual['total_avulso_apenas_banhos']:.2f}.
    </p>
    <p style="margin-bottom:0px">
        ✅ <b>No pacote Clube04 fica:</b> desconto de {int(plano_atual['desc_perc']*100)}%, saindo por <b>R$ {plano_atual['banho_clube_un']:.2f} unitário</b> e <b>R$ {plano_atual['total_clube_apenas_banhos']:.2f} no total</b>.
    </p>
</div>
""", unsafe_allow_html=True)
st.write("")

# Expander detalhando tudo
with st.expander("Clique para ver o detalhamento completo de Extras & Consumo"):
    # Detalhamento de Beleza
    if plano_atual["total_avulso_apenas_beleza"] > 0:
        st.markdown("**Extras de Beleza (Matérias-Primas e Adicionais):**")
        
        for item, qtd in selecao_mascaras.items():
            avulso_un = precos_mascaras_avulso[item][porte]
            desc_percentual = plano_atual['desc_perc']
            clube_un = avulso_un * (1 - desc_percentual)
            st.markdown(f"- {qtd}x {item}: Un. Padrão R$ {avulso_un:.2f} ➔ **Un. Clube04 R$ {clube_un:.2f}**")
            
        for item, qtd in selecao_adicionais.items():
            if item == "Tosa Geral":
                avulso_un = precos_tosa_avulso[porte]
            else:
                avulso_un = precos_adicionais_avulso[item][porte]
            
            desc_percentual = plano_atual['desc_perc']
            clube_un = avulso_un * (1 - desc_percentual)
            st.markdown(f"- {qtd}x {item}: Un. Padrão R$ {avulso_un:.2f} ➔ **Un. Clube04 R$ {clube_un:.2f}**")
            
        st.write("")
        
    # Detalhamento de Consumo
    if plano_atual["total_avulso_apenas_consumo"] > 0:
        st.markdown("**Consumo (Medicamentos):**")
        
        st.markdown(f"- {plano_atual['q_bravecto']}x Bravecto ({peso_bravecto}): Un. Padrão R$ {plano_atual['bravecto_avulso_un']:.2f} ➔ **Un. Clube04 R$ {plano_atual['bravecto_clube_un']:.2f}**")
        st.write("")

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
            
        # Formatando listas de extras para o resumo
        lista_masc = []
        for item, qtd in selecao_mascaras.items():
            avulso_un = precos_mascaras_avulso[item][porte]
            lista_masc.append(f"{qtd}x {item} (avulso un. R$ {avulso_un:.2f})")
            
        lista_adic = []
        for item, qtd in selecao_adicionais.items():
            if item == "Tosa Geral":
                avulso_un = precos_tosa_avulso[porte]
            else:
                avulso_un = precos_adicionais_avulso[item][porte]
            lista_adic.append(f"{qtd}x {item} (avulso un. R$ {avulso_un:.2f})")
            
        todos_extras = lista_masc + lista_adic
        texto_extras = "\n- ".join(todos_extras) if todos_extras else "Nenhum"
        
        texto_consumo = []
        if plano_atual['q_bravecto'] > 0: 
            texto_consumo.append(f"{plano_atual['q_bravecto']}x Bravecto ({peso_bravecto} | avulso un. R$ {plano_atual['bravecto_avulso_un']:.2f})")
        texto_consumo_str = "\n- ".join(texto_consumo) if texto_consumo else "Nenhum"

        st.markdown(f"""
        **📋 Detalhes do Plano Clube04:**
        - **Banhos:** {qtd_banhos} unidades ({porte} - Pelo {pelo})
        - **Referência (Unitário Padrão):** R$ {plano_atual['avulso_un']:.2f}
        - **Frequência:** {frequencia}
        - **Duração Estimada:** {plano_atual['meses']} meses ({plano_atual['dias']} dias)
        
        **✨ Extras de Beleza Inclusos com {int(plano_atual['desc_perc']*100)}% de desconto:**
        - {texto_extras}
        
        **🛒 Consumo Incluso com {int(plano_atual['desc_perc']*100)}% de desconto:**
        - {texto_consumo_str}
        
        ---
        ❌ Valor Total Avulso (Sem Clube): ~~R$ {plano_atual['total_avulso_geral']:.2f}~~
        ✅ **VALOR NO CLUBE04 HOJE: R$ {plano_atual['total_clube_geral']:.2f}** *(Desconto aplicado de {int(plano_atual['desc_perc']*100)}%)*
        
        *Atendente: {vendedor}*
        """)
