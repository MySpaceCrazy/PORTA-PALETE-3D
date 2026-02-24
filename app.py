import streamlit as st
import plotly.graph_objects as go
import numpy as np

st.set_page_config(layout="wide")

st.title("📦 Porta-Palete 3D - Simulação")

# ==============================
# PARAMETROS
# ==============================

st.sidebar.header("Configurações")

num_modulos = st.sidebar.slider("Módulos (largura)", 1, 10, 4)
num_niveis = st.sidebar.slider("Níveis", 1, 6, 3)

altura_nivel = st.sidebar.number_input("Altura entre níveis (m)", 1.0, 3.0, 1.8)
largura_modulo = st.sidebar.number_input("Largura módulo (m)", 1.5, 4.0, 2.7)
profundidade = st.sidebar.number_input("Profundidade (m)", 0.8, 2.0, 1.1)

altura_total = altura_nivel * num_niveis + 0.5

# espessuras estruturais
esp_coluna = 0.08
esp_viga = 0.12


# ==============================
# FUNÇÃO PARA CRIAR CAIXA 3D
# ==============================

def criar_caixa(x, y, z, dx, dy, dz, cor):
    return go.Mesh3d(
        x=[x, x+dx, x+dx, x, x, x+dx, x+dx, x],
        y=[y, y, y+dy, y+dy, y, y, y+dy, y+dy],
        z=[z, z, z, z, z+dz, z+dz, z+dz, z+dz],
        i=[0,0,0,1,1,2,4,5,6,4,5,6],
        j=[1,2,3,2,5,3,5,6,7,0,1,2],
        k=[2,3,1,5,6,7,6,7,4,1,2,3],
        color=cor,
        opacity=1.0,
        flatshading=True,
        showscale=False
    )


fig = go.Figure()

# ==============================
# COLUNAS (MONTANTES)
# ==============================

for m in range(num_modulos + 1):

    x_pos = m * largura_modulo

    # frente
    fig.add_trace(
        criar_caixa(
            x_pos, 0, 0,
            esp_coluna, esp_coluna, altura_total,
            "purple"
        )
    )

    # fundo
    fig.add_trace(
        criar_caixa(
            x_pos,
            profundidade - esp_coluna,
            0,
            esp_coluna,
            esp_coluna,
            altura_total,
            "purple"
        )
    )


# ==============================
# LONGARINAS (VIGAS)
# ==============================

for nivel in range(num_niveis):

    z = (nivel + 1) * altura_nivel

    for m in range(num_modulos):

        x = m * largura_modulo

        # viga frontal
        fig.add_trace(
            criar_caixa(
                x,
                0,
                z,
                largura_modulo,
                esp_viga,
                esp_viga,
                "orange"
            )
        )

        # viga traseira
        fig.add_trace(
            criar_caixa(
                x,
                profundidade - esp_viga,
                z,
                largura_modulo,
                esp_viga,
                esp_viga,
                "orange"
            )
        )


# ==============================
# CONFIGURAÇÃO VISUAL
# ==============================

fig.update_layout(
    scene=dict(
        xaxis_title="Largura",
        yaxis_title="Profundidade",
        zaxis_title="Altura",
        aspectmode="data"
    ),
    margin=dict(l=0, r=0, t=0, b=0),
)

st.plotly_chart(fig, use_container_width=True)