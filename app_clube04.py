import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Simulador Clube04 - Campo Belo", page_icon="🐾", layout="wide")

# --- CABEÇALHO E BRANDING ---
# Você deve substituir o link abaixo pelo link direto da sua logo hospedada (ex: Imgur, Dropbox)
LOGO_URL = "https://i.imgur.com/your_logo_here.png" # <--- SUBSTITUA AQUI

col_logo, col_info = st.columns([1, 4])

with col_logo:
    try:
        st.image(LOGO_URL, width=120)
    except:
        st.write("🐾 **CLUBE04**") # Fallback caso a imagem falhe

with col_info:
    st.title("Simulador de Planos Clube04")
    st.subheader("Unidade: **Campo Belo**")
    st.markdown("[@clube04_petshop](https://instagram.com/clube04_petshop)", help="Abrir Instagram da Loja")

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
    {"Porte": "Pequeno", "Pelo": "Curto", "Preco": 60.00},
    {"Porte": "Pequeno", "Pelo": "Longo/Dificultoso", "Preco": 85.00},
    {"Porte": "Médio", "Pelo": "Curto", "Preco": 90.00},
    {"Porte": "Grande", "Pelo": "Curto", "Preco": 130.00}
])

dict_extras = {"Hidratação": 45.00, "Tosa Higiênica": 35.00, "Remoção Pelo Morto": 50.00}
dict_produtos = {"Bravecto 10-20kg": 220.00, "Ração SP 1kg": 85.00}

# --- BARRA LATERAL (INPUTS DO VENDEDOR) ---
st.sidebar.header("📝 Dados do Atendimento")
nome_pet = st.sidebar.text_input("Nome do Pet", value="Fiel")
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
            label=f"Preço no CLUBE04 ({desconto_clube}% off)", 
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
