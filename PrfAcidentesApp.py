import pandas as pd
import streamlit as st
from spacy import load

nlp = load('pt_core_news_lg')

@st.cache_data #Otimiza carregamentos dos dados
def carregar_dados():
    dataset = pd.read_csv('Acidentes2023dadosPRF.csv')
    return dataset

with st.container():
    #menu
    bar = st.sidebar
    menu = bar.selectbox('MENU',['Escoha a opção para visualizar','Gráficos', 'Estatistica'])
    #checkbox tabela
    #st.sidebar.subheader('TABELA')
    #tabela = st.sidebar.empty()
    #checkbox mapa
    st.sidebar.subheader('MAPA')
    mapa = st.sidebar.empty()


    if menu == 'Gráficos':
        st.title("ACIDENTES DE TRANSITO NAS RODOVIAS FEDERAIS 2023")
        st.header('Dados abertos da PRF')
        st.subheader('Primeiro semestre 2023')
        with st.container():
            acidentes_dados = carregar_dados()
            var = acidentes_dados[
                ['feridos_leves', 'feridos_graves', 'mortos', 'pessoas', 'ilesos', 'ignorados', 'feridos', 'veiculos']]
            meses = {
                'Janeiro': ('2023-01-01', '2023-02-01'),
                'Fevereiro': ('2023-02-01', '2023-03-01'),
                'Março': ('2023-03-01', '2023-04-01'),
                'Abril': ('2023-04-01', '2023-05-01'),
                'Maio': ('2023-05-01', '2023-06-01'),
                'Junho': ('2023-06-01', '2023-07-01'),
                '1º Semestre geral': ('2023-01-01', '2023-07-01')
            }

            var = st.selectbox('Acidentes', list(var.keys()))
            meses_filter = st.selectbox('', list(meses.keys()))

            if meses_filter in meses:
                # Se o mês estiver na lista de meses, selecione os dados com base nas datas
                inicio, fim = meses[meses_filter]
                dados_filtrados = acidentes_dados[
                    (acidentes_dados['data_inversa'] >= inicio) & (acidentes_dados['data_inversa'] < fim)]

                # gráfico de área com base nos dados filtrados
                st.bar_chart(dados_filtrados, x='data_inversa', y=var)
            else:
                # Se o mês não estiver na lista de meses, exiba uma mensagem de erro
                st.error(f'O mês "{meses_filter}" não está disponível nos dados.')

        with st.container():
            dados_br = carregar_dados()
            var_br = acidentes_dados[
                ['feridos_leves', 'feridos_graves', 'mortos', 'pessoas', 'ilesos', 'ignorados', 'feridos', 'veiculos']]
            var_filtro = st.selectbox('Acidentes por Br', list(var_br.keys()))
            var_list_br = acidentes_dados[['br']]
            if var_filtro in var_br:
                st.bar_chart(dados_br, x='br', y=var_filtro)
            else:
                print('error')

    else:
        print('Escolha')

    if menu == 'Estatistica':
        st.header('Estatistica descritiva')
        estatistica = carregar_dados()
        st.table(estatistica.describe())
    else:
        print('error')

with st.container():
    if mapa.checkbox("Visualizar mapa geral de acidentes nas rodovias"):
        st.subheader("Mapa com pontos de acidentes")
        st.map(carregar_dados())
    else:
        print('Error')
'''
with st.container():
    if tabela.checkbox("Mostrar tabela de dados"):
        st.subheader('Base de dados geral')
        st.write(carregar_dados())
    else:
        print('error')
'''
