import streamlit as st
import math
from datetime import datetime, timedelta

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Simulador Clube04 - Campo Belo", page_icon="🐾", layout="wide")

# --- ESTILIZAÇÃO CSS (Corrigindo cores de input e visual) ---
st.markdown("""
    <style>
        /* Fundo e textos gerais da barra lateral */
        [data-testid="stSidebar"] { background-color: #FF8A00; }
        [data-testid="stSidebar"] .stMarkdown p, 
        [data-testid="stSidebar"] .stMarkdown h3,
        [data-testid="stSidebar"] label { color: #FFFFFF !important; font-weight: bold; }
        
        /* Corrigindo o texto dentro das caixas de input (fundo branco, letra preta) */
        [data-testid="stSidebar"] input { color: #000000 !important; background-color: #FFFFFF !important; }
        [data-testid="stSidebar"] div[data-baseweb="select"] div { color: #000000 !important; }
        
        /* Cor dos títulos dos expansores */
        div[data-testid="stExpander"] div[role="button"] p { color: #FF8A00 !important; font-weight: bold; }
        
        /* Estilo da caixa de proposta final */
        .proposta-box {
            background-color: #FFFFFF;
            padding: 25px;
            border-radius: 10px;
            border: 1px solid #E0E0E0;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
            font-family: sans-serif;
            color: #333333;
        }
    </style>
""", unsafe_allow_html=True)

# URL da Logo
LOGO_URL = ""https://www.kalaes.com.br/22/wp-content/uploads/2023/08/CB04LOGO.png""

# --- TABELAS DE PREÇOS UNITÁRIOS REAIS DO CLUBE04 ---
precos_banho_avulso = {
    "Até 10 kg": {"Curto": 85.0, "Médio": 99.0, "Longo": 99.0},
    "Até 20 kg": {"Curto": 105.0, "Médio": 139.0, "Longo": 139.0},
    "Até 50 kg": {"Curto": 149.0, "Médio": 179.0, "Longo": 179.0},
    "+ 50 kg": {"Curto": 239.0, "Médio": 279.0, "Longo": 279.0}
}

precos_tosa_avulso = { "Até 10 kg": 209.0, "Até 20 kg": 279.0, "Até 50 kg": 489.0, "+ 50 kg": 699.0 }

precos_mascaras_avulso = {
    "Senses/Detox": {"Até 10 kg": 69.0, "Até 20 kg": 79.0, "Até 50 kg": 89.0, "+ 50 kg": 109.0},
    "Luxo/Máx. Volume/Liso Intenso": {"Até 10 kg": 59.0, "Até 20 kg": 69.0, "Até 50 kg": 79.0, "+ 50 kg": 99.0},
    "Argan": {"Até 10 kg": 49.0, "Até 20 kg": 59.0, "Até 50 kg": 69.0, "+ 50 kg": 89.0},
    "Matização": {"Até 10 kg": 69.0, "Até 20 kg": 79.0, "Até 50 kg": 89.0, "+ 50 kg": 99.0}
}

precos_adicionais_avulso = {
    "Remoção de Pelos Mortos": {"Até 10 kg": 79.0, "Até 20 kg": 89.0, "Até 50 kg": 99.0, "+ 50 kg": 109.0},
    "Tosa Higiênica": {"Até 10 kg": 39.0, "Até 20 kg": 49.0, "Até 50 kg": 59.0, "+ 50 kg": 69.0},
    "Ozônio": {"Até 10 kg": 39.0, "Até 20 kg": 49.0, "Até 50 kg": 59.0, "+ 50 kg": 79.0},
    "Desembolo": {"Até 10 kg": 99.0, "Até 20 kg": 149.0, "Até 50 kg": 189.0, "+ 50 kg": 299.0},
    "Extra Soft": {"Até 10 kg": 19.0, "Até 20 kg": 29.0, "Até 50 kg": 39.0, "+ 50 kg": 49.0},
    "X-treme (Limpeza Profunda)": {"Até 10 kg": 39.0, "Até 20 kg": 39.0, "Até 50 kg": 39.0, "+ 50 kg": 39.0}
}

# --- BARRA LATERAL (INPUTS) ---
st.sidebar.image(LOGO_URL, width=150)
st.sidebar.markdown("### 👤 Atendimento")
vendedor = st.sidebar.text_input("Nome do vendedor(a)", value="Amanda")
nome_tutor = st.sidebar.text_input("Nome do tutor(a)")
nome_pet = st.sidebar.text_input("Nome do doguinho", value="Buda")

st.sidebar.markdown("---")
st.sidebar.markdown("### 🐾 Perfil do Doguinho")
porte = st.sidebar.selectbox("Porte do Doguinho", list(precos_banho_avulso.keys()))
pelo = st.sidebar.selectbox("Tipo de pelo", ["Curto", "Médio", "Longo"])

st.sidebar.markdown("---")
st.sidebar.markdown("### 🛠️ Estrutura do Plano Base")
pacote_opcoes = {4: "4 banhos", 8: "8 banhos", 12: "12 banhos", 24: "24 banhos", 48: "48 banhos"}
escolha_qtd = st.sidebar.selectbox("Pacote (Opção 1)", list(pacote_opcoes.keys()), format_func=lambda x: pacote_opcoes[x], index=2)
frequencia = st.sidebar.selectbox("Frequência", ["Semanal", "Quinzenal", "Mensal"])

st.sidebar.markdown("---")
st.sidebar.markdown("### ✨ Extras (Cobrados)")
sel_masc_pagas = {}
sel_adic_pagos = {}

with st.sidebar.expander("🪄 Máscaras (Pagas)"):
    for item in precos_mascaras_avulso.keys():
        qtd = st.number_input(f"{item} (Paga)", min_value=0, max_value=48, value=0, key=f"mp_{item}")
        if qtd > 0: sel_masc_pagas[item] = qtd

with st.sidebar.expander("✂️ Adicionais (Pagos)"):
    for item in list(precos_adicionais_avulso.keys()) + ["Tosa Geral"]:
        qtd = st.number_input(f"{item} (Pago)", min_value=0, max_value=48, value=0, key=f"ap_{item}")
        if qtd > 0: sel_adic_pagos[item] = qtd

st.sidebar.markdown("---")
st.sidebar.markdown("### 🎁 Brindes (Presentes)")
st.sidebar.caption("Soma na economia do cliente, mas zera o custo.")
sel_brindes = {}

with st.sidebar.expander("🎁 Adicionar Brindes"):
    for item in list(precos_mascaras_avulso.keys()) + list(precos_adicionais_avulso.keys()) + ["Tosa Geral"]:
        qtd = st.number_input(f"{item} (Brinde)", min_value=0, max_value=48, value=0, key=f"br_{item}")
        if qtd > 0: sel_brindes[item] = qtd

st.sidebar.markdown("---")
st.sidebar.markdown("### 🛒 Consumo")
itens_consumo = st.sidebar.text_input("Itens com desconto (Ex: bravecto, shampoo)", value="bravecto, shampoo e petisco")

# --- MOTOR DE CÁLCULO ---
descontos_fixos = {4: 0.05, 8: 0.07, 12: 0.10, 24: 0.15, 48: 0.20}

def obter_preco_unitario(item):
    if item in precos_mascaras_avulso: return precos_mascaras_avulso[item][porte]
    if item in precos_adicionais_avulso: return precos_adicionais_avulso[item][porte]
    if item == "Tosa Geral": return precos_tosa_avulso[porte]
    return 0.0

def calcular_opcao(qtd_banhos, freq, masc_pagas, adic_pagos, brindes):
    # Duração
    semanas = qtd_banhos if freq == "Semanal" else (qtd_banhos * 2 if freq == "Quinzenal" else qtd_banhos * 4)
    meses = int(semanas / 4) if semanas >= 4 else 1
    parcelas = meses
    
    # Preços Base
    banho_un = precos_banho_avulso[porte][pelo]
    desc_perc = descontos_fixos.get(qtd_banhos, 0.0)
    
    # Cálculos Pagos
    total_banhos = banho_un * qtd_banhos
    total_extras = sum([qtd * obter_preco_unitario(i) for i, qtd in masc_pagas.items()]) + \
                   sum([qtd * obter_preco_unitario(i) for i, qtd in adic_pagos.items()])
    
    subtotal = total_banhos + total_extras
    total_final = subtotal * (1 - desc_perc)
    
    # Cálculos Brindes (Somam no valor avulso percebido para aumentar a "Economia")
    valor_brindes = sum([qtd * obter_preco_unitario(i) for i, qtd in brindes.items()])
    
    economia = (subtotal + valor_brindes) - total_final
    banho_com_desconto = banho_un * (1 - desc_perc)
    parcela_valor = total_final / parcelas
    
    return {
        "qtd": qtd_banhos, "meses": meses, "parcelas": parcelas, "parcela_valor": parcela_valor,
        "banho_un": banho_un, "banho_desc_un": banho_com_desconto, "total_final": total_final,
        "economia": economia, "desc_perc": int(desc_perc * 100),
        "masc_pagas": masc_pagas, "adic_pagos": adic_pagos, "brindes": brindes
    }

# --- PROCESSANDO AS OPÇÕES ---
opcao1 = calcular_opcao(escolha_qtd, frequencia, sel_masc_pagas, sel_adic_pagos, sel_brindes)

niveis = [4, 8, 12, 24, 48]
idx = niveis.index(escolha_qtd)
tem_opcao2 = idx < len(niveis) - 1
if tem_opcao2:
    # A Opção 2 puxa o próximo nível de pacote, dobrando os extras para fazer sentido na proporção (opcional)
    fator_multiplicador = niveis[idx+1] / escolha_qtd
    masc_pagas_op2 = {k: int(v * fator_multiplicador) for k, v in sel_masc_pagas.items()}
    adic_pagos_op2 = {k: int(v * fator_multiplicador) for k, v in sel_adic_pagos.items()}
    brindes_op2 = {k: int(v * fator_multiplicador) for k, v in sel_brindes.items()}
    
    opcao2 = calcular_opcao(niveis[idx+1], frequencia, masc_pagas_op2, adic_pagos_op2, brindes_op2)

# --- GERADOR DE TEXTO WHATSAPP ---
data_validade = (datetime.now() + timedelta(days=5)).strftime('%d/%m/%Y')

def formatar_bloco_opcao(op, numero):
    texto = f"Opção {numero}:\n"
    texto += f"🛁 **{op['qtd']} banhos** de: R$ {op['banho_un']:.2f} por: R$ {op['total_final']:.0f} (R$ {op['banho_desc_un']:.2f} cada banho);\n"
    
    for item, qtd in op['masc_pagas'].items():
        texto += f"🪄 {qtd} {item} com {op['desc_perc']}% de desconto;\n"
    for item, qtd in op['adic_pagos'].items():
        texto += f"🪄 {qtd} {item} com {op['desc_perc']}% de desconto;\n"
        
    for item, qtd in op['brindes'].items():
        texto += f"+ 🎁 {qtd} {item} de presente;\n"
        
    texto += f"Duração do plano: {op['meses']} meses\n"
    texto += f"Total: R$ {op['total_final']:.2f} (Economia de R$ {op['economia']:.2f})\n"
    texto += f"💳 {op['parcelas']}x de R$ {op['parcela_valor']:.2f}\n"
    return texto

texto_op1 = formatar_bloco_opcao(opcao1, 1)
texto_op2 = formatar_bloco_opcao(opcao2, 2) if tem_opcao2 else ""

# --- TELA PRINCIPAL (VISUALIZAÇÃO IDÊNTICA AO ANEXO) ---
st.title("📱 Proposta Pronta para WhatsApp")
st.write("Você pode tirar um print ou simplesmente selecionar o texto abaixo, copiar e colar no WhatsApp. As formatações de negrito já irão funcionar perfeitamente.")

st.markdown("""<hr style="height:2px;border:none;color:#FF8A00;background-color:#FF8A00;" />""", unsafe_allow_html=True)

# Renderizando como a imagem
with st.container():
    st.markdown(f"""
    <div class="proposta-box">
        <div style="display: flex; align-items: center; margin-bottom: 20px;">
            <img src="{LOGO_URL}" width="70" style="margin-right: 15px;">
            <div>
                <strong>CLUBE04 - Unidade Campo Belo</strong><br>
                <strong>Proposta exclusiva para o(a) doguinho {nome_pet}</strong>
            </div>
        </div>
        <p>📋 <strong>Detalhes do Plano Clube04:</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Usando st.markdown puro para que o usuário possa grifar e copiar facilmente
    proposta_texto = f"""
{texto_op1}
{texto_op2}

🛒 Consumo:
**{opcao1['desc_perc']}% desconto:** {itens_consumo}

**Atendimento: {vendedor}**
Prazo de validade da proposta: **{data_validade}**
    """
    st.markdown(proposta_texto)

st.markdown("""<hr style="height:2px;border:none;color:#FF8A00;background-color:#FF8A00;" />""", unsafe_allow_html=True)
