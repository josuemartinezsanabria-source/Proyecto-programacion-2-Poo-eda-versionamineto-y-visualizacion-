import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


import Clases as cl
from Clases import GestorPartidos, EDA

st.title("Mundiales FIFA - Dashboard")


@st.cache_data
def cargar_todo():
    obj_carga = cl.CargarDatos("")
    obj_carga.descargar_datos()
    obj_carga.filtrar_mundiales()

    obj_eda = EDA(obj_carga.df)
    obj_eda.limpieza_datos()
    df_final = obj_eda.crear_columnas_derivadas()
    matriz_corr = obj_eda.matriz_correlacion()
    return df_final, matriz_corr


df, matriz_corr = cargar_todo()

anios = sorted(df["year"].unique().tolist())
anio_sel = st.sidebar.selectbox("Año", ["Todos"] + anios)

equipos = sorted(list(set(df["home_team"].unique().tolist() + df["away_team"].unique().tolist())))
equipo_sel = st.sidebar.selectbox("Selección", ["Todos"] + equipos)

df_f = df.copy()
if anio_sel != "Todos":
    df_f = df_f[df_f["year"] == anio_sel]
if equipo_sel != "Todos":
    df_f = df_f[(df_f["home_team"] == equipo_sel) | (df_f["away_team"] == equipo_sel)]

c1, c2, c3 = st.columns(3)
c1.metric("Partidos", len(df_f))
c2.metric("Goles Totales", int(df_f["total_goals"].sum()))
gestor = GestorPartidos(df_f)
c3.metric("Tasa Ventaja Local", f"{round(gestor.ventaja_local() * 100, 2)}%" if len(df_f) > 0 else "0%")


col_izq, col_der = st.columns(2)

with col_izq:
    st.subheader("Distribución de Ganadores")
    fig, ax = plt.subplots(figsize=(5, 4))
    sns.countplot(data=df_f, x="winner_type", order=["Local", "Visitante", "Empate"],
                  palette=["#FFAAA6", "#D6A2E8", "#836FA9"], ax=ax)
    st.pyplot(fig)

with col_der:
    st.subheader("Frecuencia de Goles")
    fig2, ax2 = plt.subplots(figsize=(5, 4))
    sns.histplot(data=df_f, x="total_goals", kde=True, color="#9EEAFB", ax=ax2)
    st.pyplot(fig2)


col_izq2, col_der2 = st.columns(2)

with col_izq2:
    st.subheader("Goles: Local vs. Visitante")
    fig3, ax3 = plt.subplots(figsize=(5, 4))
    sns.scatterplot(data=df_f, x="home_score", y="away_score", alpha=0.6, color="#1F77B4", s=100,
                    edgecolor="black", ax=ax3)
    ax3.plot([0, 10], [0, 10], color="#D62728", linestyle="--", linewidth=2)
    ax3.set_xlim(-0.5, 10.5)
    ax3.set_ylim(-0.5, 10.5)
    st.pyplot(fig3)

with col_der2:
    st.subheader("Matriz de Correlación")
    fig4, ax4 = plt.subplots(figsize=(5, 4))
    nombres_espanol = ["Goles Local", "Goles Visitante", "Total Goles", "Diferencia Goles"]


    columnas = ["home_score", "away_score", "total_goals", "goal_difference"]
    matriz_f = df_f[columnas].corr() if len(df_f) > 1 else matriz_corr
    matriz_f.index = nombres_espanol
    matriz_f.columns = nombres_espanol

    sns.heatmap(matriz_f, annot=True, cmap="coolwarm", fmt=".2f", linewidths=1,
                vmin=-1, vmax=1, ax=ax4, annot_kws={"size": 10, "weight": "bold"})
    st.pyplot(fig4)



st.markdown("---")
st.subheader(" Máximas Goles Históricas")
num_goleadas = st.slider("¿Cuántas goleadas querés desplegar?", min_value=3, max_value=15, value=5)

df_goleadas = gestor.top_goleadas(num_goleadas)

if not df_goleadas.empty:
    for idx, row in df_goleadas.iterrows():
        st.info(f" **{row['home_team']} {int(row['home_score'])} - {int(row['away_score'])} {row['away_team']}** | Año: {row['year']} (Diferencia de {int(row['goal_difference'])} goles)")
else:
    st.warning("No hay suficientes partidos con los filtros actuales para calcular el top de goleadas.")
st.markdown("---")


st.subheader("Partidos Registrados")
st.dataframe(df_f[["date", "home_team", "away_team", "home_score", "away_score", "winner_type"]],
             use_container_width=True)


#Para poder ejecutarlo se debe correr el comando streamlit run app.py  en la consola de pycharm
#si es necesario usar el comando pip install -r requirements.txt para instalar los requirements
