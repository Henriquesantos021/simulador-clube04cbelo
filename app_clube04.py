import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Simulador Clube04 - Campo Belo", page_icon="🐾", layout="wide")

# --- CABEÇALHO E BRANDING ---
# Você deve substituir o link abaixo pelo link direto da sua logo hospedada (ex: Imgur, Dropbox)
LOGO_URL = "data:image/png;base64,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" # <--- SUBSTITUA AQUI

col_logo, col_info = st.columns([1, 4])

with col_logo:
    try:
        st.image(LOGO_URL, width=120)
    except:
        st.write("🐾 **CLUBE04**") # Fallback caso a imagem falhe

with col_info:
    st.title("Simulador de Planos Clube04")
    st.subheader("Unidade: **Campo Belo**")
    st.markdown("[@clube04.campobelo](https://instagram.com/clube04.campobelo)", help="Abrir Instagram da Loja")

st.markdown("---")

# --- CONEXÃO COM GOOGLE SHEETS ---
# Substitua pela URL da sua planilha 'Pública na Web'
sheet_url = "https://docs.google.com/spreadsheets/d/SUA_PLANILHA_ID_AQUI/export?format=csv" # <--- SUBSTITUA AQUI

@st.cache_data(ttl=600) # Mantém os preços em cache por 10 minutos
def load_data(url, worksheet_name):
    # Gambiarra para ler abas específicas via CSV export
    # Requer que você obtenha o gid=ID_DA_ABA na URL do Sheets
    return pd.read_csv(url) 

# Para simplicidade deste código, vamos assumir os preços direto aqui. 
# Para usar GSheets, requer configuração de secrets que é mais avançada.
# Vamos usar dados de exemplo baseados na estrutura que desenhei antes.

df_precos_base = pd.DataFrame([
    {"Porte": "Até 10kg", "Pelo": "Curto", "Preco": 89.00},
    {"Porte": "Até 10kg", "Pelo": "Médio / Longo", "Preco": 99.00},
    {"Porte": "Até 20kg", "Pelo": "Curto", "Preco": 149.00},
    {"Porte": "Até 50kg", "Pelo": "Curto", "Preco": 179.00}
])

dict_extras = {"Hidratação": 45.00, "Tosa Higiênica": 35.00, "Remoção Pelo Morto": 50.00}
dict_produtos = {"Bravecto 10-20kg": 220.00, "Tapete higiênico": 85.00}

# --- BARRA LATERAL (INPUTS DO VENDEDOR) ---
st.sidebar.header("📝 Dados do Atendimento")
nome_pet = st.sidebar.text_input("Nome do Pet", value="Nome")
whatsapp = st.sidebar.text_input("WhatsApp do Tutor (Opcional)")

st.sidebar.markdown("---")
st.sidebar.header("🛠️ Configuração do Pacote")

# Seleção do Banho Base
porte = st.sidebar.selectbox("Porte", df_precos_base["Porte"].unique())
pelo = st.sidebar.selectbox("Tipo de Pelo", df_precos_base[df_precos_base["Porte"] == porte]["Pelo"].unique())

# Frequência e Duração
qtd_banhos = st.sidebar.number_input("Quantidade de Banhos no Plano", min_value=1, value=4, step=1)
frequencia = st.sidebar.selectbox("Frequência", ["Semanal", "Quinzenal", "Mensal"])

# Extras e Produtos
extras_selecionados = st.sidebar.multiselect("Serviços Extras (Adicionar no plano)", list(dict_extras.keys()))
produtos_selecionados = st.sidebar.multiselect("Produtos (Itens de Balcão)", list(dict_produtos.keys()))

st.sidebar.markdown("---")
desconto_clube = st.sidebar.slider("Desconto Especial Clube04 (%)", min_value=0, max_value=30, value=15, step=5)

# --- CÁLCULOS LOGÍSTICOS E FINANCEIROS ---

# 1. Recuperar Preço Base (PROCV)
row = df_precos_base[(df_precos_base["Porte"] == porte) & (df_precos_base["Pelo"] == pelo)]
preco_banho_unitario = row["Preco"].values[0]

# 2. Somar Extras Unitários
preco_extras_unitario = sum([dict_extras[item] for item in extras_selecionados])
total_servicos_unitario = preco_banho_unitario + preco_extras_unitario

# 3. Calcular Totais Avulsos (Sem Desconto)
total_servicos_avulso = total_servicos_unitario * qtd_banhos
total_produtos = sum([dict_produtos[item] for item in produtos_selecionados])
preco_total_avulso = total_servicos_avulso + total_produtos

# 4. Calcular Totais Clube04 (Com Desconto nos SERVIÇOS)
total_servicos_clube = total_servicos_avulso * (1 - (desconto_clube / 100))
preco_total_clube = total_servicos_clube + total_produtos

# 5. Cálculo de Duração
dias_frequencia = {"Semanal": 7, "Quinzenal": 14, "Mensal": 30}
total_dias = (qtd_banhos - 1) * dias_frequencia[frequencia]
data_final = datetime.now() + timedelta(days=total_dias)
meses_duracao = round(total_dias / 30, 1)

# --- TELA PRINCIPAL (O PITCH DE VENDA) ---
st.header(f"Proposta de Bem-Estar: **{nome_pet}**")

# Container customizado para o print
with st.container(border=True):
    st.markdown(f"""
    <div style="background-color:#f9f9f9; padding:15px; border-radius:10px; border: 1px solid #ddd">
        <h3 style="margin-top:0">📊 Comparativo de Valor</h3>
        <p style="margin-bottom:5px">Plano de {qtd_banhos} banhos ({frequencia}) + {len(extras_selecionados)} Extras + {len(produtos_selecionados)} Produtos.</p>
    </div>
    """, unsafe_allow_html=True)
    st.write("")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(label="Preço Avulso (Normal)", value=f"R$ {preco_total_avulso:.2f}")

    with col2:
        # Mostra o desconto de forma agressiva
        st.metric(
            label=f"Preço no Pacote do CLUBE04 ({desconto_clube}% off)", 
            value=f"R$ {preco_total_clube:.2f}", 
            delta=f"-{preco_total_avulso - preco_total_clube:.2f} economizados"
        )

    with col3:
        # Argumento RevOps: Economia por Banho
        economia_banho = (total_servicos_avulso - total_servicos_clube) / qtd_banhos
        st.metric(label="Economia POR BANHO", value=f"R$ {economia_banho:.2f}")

    st.markdown("---")
    st.subheader("🕒 Duração e Planejamento")
    c1, c2, c3 = st.columns([1,1,1])
    c1.info(f"🗓️ Duração total: **{total_dias} dias** (~{meses_duracao} meses)")
    c2.info(f"📅 Término estimado: **{data_final.strftime('%d/%m/%Y')}**")
    c3.success(f"💡 Você trava o preço de hoje por {meses_duracao} meses!")

    # Área de resumo para print limpo
    if st.checkbox("Gerar Resumo para Screenshot"):
        st.markdown("---")
        st.markdown(f"""
        **🛒 Resumo do Plano Clube04 - {nome_pet}**
        - **Serviço Base:** {qtd_banhos} Banhos ({porte}/{pelo}) - {frequencia}
        - **Incluso:** {', '.join(extras_selecionados) if extras_selecionados else 'Apenas Banho'}
        - **Produtos:** {', '.join(produtos_selecionados) if produtos_selecionados else 'Nenhum'}
        ---
        - ❌ Preço total avulso: ~~R$ {preco_total_avulso:.2f}~~
        - ✅ **Preço Clube04 hoje: R$ {preco_total_clube:.2f}**
        - 🔥 **Duração:** {total_dias} dias ({meses_duracao} meses)
        ---
        *Atendimento Unidade Campo Belo.*
        """)
