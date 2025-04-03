import streamlit as st
import requests
import pandas as pd
import folium
from streamlit_folium import st_folium

st.title("Consulta de Países")

# Entrada de dados pelo usuário: nome do país (em inglês) com exemplo "Brazil"
pais_input = st.text_input("Insira o nome do país (em inglês):", value="Brazil")

if pais_input:
    url = f"https://restcountries.com/v3.1/name/{pais_input}"
    response = requests.get(url)
    
    if response.status_code == 200:
        dados = response.json()
        if dados:
            # Consideramos o primeiro resultado da busca
            pais = dados[0]
            nome = pais.get("name", {}).get("common", "Não disponível")
            capital = pais.get("capital", ["Não disponível"])[0]
            regiao = pais.get("region", "Não disponível")
            populacao = pais.get("population", "Não disponível")
            
            st.subheader(nome)
            st.write("**Capital:**", capital)
            st.write("**Região:**", regiao)
            st.write("**População:**", populacao)
            
            # Tenta usar as coordenadas da capital, se disponíveis
            if "capitalInfo" in pais and pais["capitalInfo"].get("latlng"):
                cap_lat, cap_lon = pais["capitalInfo"]["latlng"]
                # Cria um mapa com o centro na capital
                mapa = folium.Map(location=[cap_lat, cap_lon], zoom_start=6)
                
                # Adiciona um marcador com tooltip e popup personalizados
                folium.Marker(
                    location=[cap_lat, cap_lon],
                    tooltip="Clique para mais detalhes",
                    popup=f"Capital: {capital}",
                    icon=folium.Icon(icon="flag", color="blue")  # Ícone de bandeira azul
                ).add_to(mapa)
                
                st.subheader("Localização da Capital")
                st_folium(mapa, width=700)
            elif "latlng" in pais:
                # Caso não haja informações específicas da capital, usa as coordenadas do país
                lat, lon = pais["latlng"]
                mapa_data = pd.DataFrame({"lat": [lat], "lon": [lon]})
                st.subheader("Localização aproximada")
                st.map(mapa_data)
            else:
                st.write("Coordenadas não disponíveis para este país.")
        else:
            st.error("País não encontrado.")
    else:
        st.error("Erro ao acessar a API. Verifique se o país informado está correto.")
