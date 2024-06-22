import streamlit as st
import pandas as pd

def show_page(df):
    st.title("Qualys Page")

    colonna_selezionata = st.sidebar.selectbox("Seleziona una tipologia", df.columns)
    filtro_opzioni = df[colonna_selezionata].unique()
    categoria_selezionata = st.sidebar.selectbox("Seleziona un filtro", filtro_opzioni)
    data_filtrati = df[df[colonna_selezionata] == categoria_selezionata]

    tab = st.selectbox("Scegli una scheda", ["🗃 Data 🧬", "📈📉 Chart", "📊 Grafico🔬"])

    if tab == "🗃 Data 🧬":
        st.subheader("A tab with data")
        st.dataframe(data_filtrati)
    elif tab == "📈📉 Chart":
        st.subheader("A tab with the chart")
        x_variable = st.sidebar.selectbox('Seleziona variabile X', df.columns)
        y_variable = st.sidebar.selectbox('Seleziona variabile Y', df.columns)
        st.line_chart(df[[x_variable, y_variable]], use_container_width=True)
    elif tab == "📊 Grafico🔬":
        st.subheader("A tab with chart and info")
        st.line_chart(data_filtrati)
        st.write(f"Numero di righe per la categoria '{categoria_selezionata}': {len(data_filtrati)}")
        st.write(categoria_selezionata)
