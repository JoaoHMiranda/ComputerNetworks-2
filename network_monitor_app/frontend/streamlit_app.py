import os
import requests
import pandas as pd
import streamlit as st
import altair as alt

API_URL = os.getenv('API_URL', 'http://localhost:5000/devices')

st.set_page_config(page_title='Network Monitor', layout='wide')
st.title('📡 Monitoramento de Tráfego de Rede')

# ✚ Formulário: Endereço IP (4 octetos) e demais campos
st.subheader('➕ Adicionar Dispositivo')
st.write('**Endereço IP**')
col1, col2, col3, col4 = st.columns(4)
oct1 = col1.number_input('Octeto 1', min_value=0, max_value=255, step=1)
oct2 = col2.number_input('Octeto 2', min_value=0, max_value=255, step=1)
oct3 = col3.number_input('Octeto 3', min_value=0, max_value=255, step=1)
oct4 = col4.number_input('Octeto 4', min_value=0, max_value=255, step=1)
name = st.text_input('Nome do Dispositivo')
traffic = st.number_input('Taxa de Tráfego (Mbps)', min_value=0.0, step=0.1)
if st.button('➕ Adicionar'):
    ip = f"{oct1}.{oct2}.{oct3}.{oct4}"
    if not name.strip():
        st.error('❌ Nome do dispositivo é obrigatório.')
    else:
        r = requests.post(API_URL, json={'ip': ip, 'name': name.strip(), 'traffic': traffic})
        if r.status_code == 201:
            st.success('✅ Dispositivo adicionado! Atualize a página.')
        else:
            st.error(f"❌ {r.json().get('error', r.text)}")

# 🔍 Listagem e gráfico
res = requests.get(API_URL)
if res.ok:
    devices = res.json()
    df = pd.DataFrame(devices)
    if not df.empty:
        st.subheader('📈 Gráfico de Tráfego')
        chart = alt.Chart(df).mark_bar().encode(
            x=alt.X('ip:N', title='Endereço IP'),
            y=alt.Y('traffic:Q', title='Taxa (Mbps)'),
            color=alt.condition(
                alt.datum.traffic < 50,
                alt.value('green'),
                alt.value('red')
            ),
            tooltip=['name:N', 'ip:N', 'traffic:Q', 'status:N']
        )
        st.altair_chart(chart, use_container_width=True)
    st.subheader('🔍 Dispositivos Cadastrados')
    for d in devices:
        cols = st.columns([1,2,3,3,1])
        cols[0].write(d['id'])
        cols[1].write(d['ip'])
        cols[2].write(d['name'])
        bg = 'lightgreen' if d['status']=='Normal' else 'lightcoral'
        cols[3].markdown(
            f"<div style='background:{bg};padding:6px;border-radius:4px'>{d['traffic']} Mbps ({d['status']})</div>",
            unsafe_allow_html=True
        )
        if cols[4].button('🗑️', key=d['id']):
            rd = requests.delete(f"{API_URL}/{d['id']}")
            if rd.ok:
                st.success('🗑️ Removido. Atualize a página.')
            else:
                st.error('❌ Falha ao remover')
else:
    st.error('❌ Não foi possível carregar dispositivos.')