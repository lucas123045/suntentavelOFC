"""
ORION ENERGY MONITOR AI
Sistema Inteligente de Monitoramento Energético para Missão Espacial
Global Solution 2026-1 | FIAP | Lucas Klein - RM 570029
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import random
import time
from datetime import datetime

# ──────────────────────────────────────────────
# CONFIGURAÇÃO DA PÁGINA
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="ORION Energy Monitor AI",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────
# CSS PERSONALIZADO
# ──────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #0a0e1a; }
    .stApp { background: linear-gradient(135deg, #0a0e1a 0%, #0d1b2a 100%); }
    h1, h2, h3, h4 { color: #00d4ff !important; }
    .metric-card {
        background: linear-gradient(135deg, #0d1b2a, #1a2744);
        border: 1px solid #00d4ff33;
        border-radius: 12px;
        padding: 16px;
        margin: 8px 0;
    }
    .alert-critical {
        background: linear-gradient(135deg, #3d0000, #5c0000);
        border: 2px solid #ff4444;
        border-radius: 10px;
        padding: 12px;
        color: #ff8080;
        font-weight: bold;
    }
    .alert-warning {
        background: linear-gradient(135deg, #2d1a00, #4a2e00);
        border: 2px solid #ffa500;
        border-radius: 10px;
        padding: 12px;
        color: #ffcc66;
        font-weight: bold;
    }
    .alert-ok {
        background: linear-gradient(135deg, #001a0d, #002e1a);
        border: 2px solid #00cc66;
        border-radius: 10px;
        padding: 12px;
        color: #66ffaa;
        font-weight: bold;
    }
    .module-online  { color: #00ff88; font-weight: bold; }
    .module-offline { color: #ff4444; font-weight: bold; }
    .module-standby { color: #ffa500; font-weight: bold; }
    .ia-response {
        background: linear-gradient(135deg, #0d1b2a, #112233);
        border-left: 4px solid #00d4ff;
        border-radius: 0 10px 10px 0;
        padding: 16px;
        color: #cce8ff;
        font-family: 'Courier New', monospace;
        font-size: 0.9em;
    }
    .stButton>button {
        background: linear-gradient(135deg, #003d5c, #005580);
        color: #00d4ff;
        border: 1px solid #00d4ff;
        border-radius: 8px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #00d4ff, #0099cc);
        color: #000;
    }
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# ESTADO DA SESSÃO (histórico de dados)
# ──────────────────────────────────────────────
if "historico" not in st.session_state:
    st.session_state.historico = []
if "alertas_log" not in st.session_state:
    st.session_state.alertas_log = []
if "ciclo" not in st.session_state:
    st.session_state.ciclo = 0
if "modulos_status" not in st.session_state:
    st.session_state.modulos_status = {
        "Propulsão":       "ONLINE",
        "Comunicação":     "ONLINE",
        "Suporte de Vida": "ONLINE",
        "Navegação":       "ONLINE",
        "Lab. Científico": "ONLINE",
        "Armazenamento":   "ONLINE",
    }
if "modo_emergencia" not in st.session_state:
    st.session_state.modo_emergencia = False
if "cenario_ativo" not in st.session_state:
    st.session_state.cenario_ativo = "Normal"

# ──────────────────────────────────────────────
# FUNÇÕES DE SIMULAÇÃO DE DADOS
# ──────────────────────────────────────────────
MODULOS_ESSENCIAIS = {"Propulsão", "Comunicação", "Suporte de Vida"}

def simular_leitura(ciclo: int) -> dict:
    """Gera dados simulados realistas com variação suave."""
    base_temp      = 45 + 20 * abs((ciclo % 40) - 20) / 20
    base_energia   = max(10, 90 - (ciclo % 50) * 1.2)
    base_solar     = max(0, 80 - abs((ciclo % 60) - 30) * 2.5)
    base_bateria   = max(15, 95 - ciclo * 0.3)
    base_radiacao  = 15 + random.uniform(-5, 30)

    return {
        "timestamp":           datetime.now().strftime("%H:%M:%S"),
        "ciclo":               ciclo,
        "temperatura_casco":   round(base_temp   + random.uniform(-5, 5),  1),
        "temperatura_nucleo":  round(base_temp * 0.7 + random.uniform(-3, 3), 1),
        "energia_disponivel":  round(base_energia + random.uniform(-3, 3),  1),
        "painel_solar":        round(base_solar   + random.uniform(-5, 5),  1),
        "bateria":             round(min(100, base_bateria + random.uniform(-2, 2)), 1),
        "comunicacao":         random.choices(["ONLINE", "OFFLINE"], weights=[92, 8])[0],
        "fonte_energia":       random.choices(["Solar", "Bateria", "Híbrida"],
                                               weights=[60, 25, 15])[0],
        "velocidade_km_s":     round(7.8 + random.uniform(-0.3, 0.3), 2),
        "altitude_km":         round(400 + ciclo * 0.05 + random.uniform(-2, 2), 1),
        "radiacao_microsv":    round(base_radiacao, 1),
        "consumo_watts":       round(random.uniform(800, 1400), 0),
    }

def analisar_condicoes(dados: dict, modulos: dict) -> list[dict]:
    """Motor de alertas: retorna lista de alertas com severidade."""
    alertas = []

    # Temperatura
    if dados["temperatura_casco"] > 85:
        alertas.append({"nivel": "CRÍTICO", "msg": f" Temperatura do casco: {dados['temperatura_casco']}°C — LIMITE EXCEDIDO", "codigo": "TEMP_CRIT"})
    elif dados["temperatura_casco"] > 70:
        alertas.append({"nivel": "AVISO",   "msg": f" Temperatura do casco elevada: {dados['temperatura_casco']}°C",              "codigo": "TEMP_WARN"})

    # Energia
    if dados["energia_disponivel"] < 15:
        alertas.append({"nivel": "CRÍTICO", "msg": f" Energia crítica: {dados['energia_disponivel']}% — ACIONAR PROTOCOLO DE EMERGÊNCIA", "codigo": "ENER_CRIT"})
    elif dados["energia_disponivel"] < 30:
        alertas.append({"nivel": "AVISO",   "msg": f" Energia baixa: {dados['energia_disponivel']}%",                                      "codigo": "ENER_WARN"})

    # Comunicação
    if dados["comunicacao"] == "OFFLINE":
        alertas.append({"nivel": "CRÍTICO", "msg": " FALHA DE COMUNICAÇÃO — Sinal perdido com base terrestre", "codigo": "COM_FAIL"})

    # Bateria
    if dados["bateria"] < 20:
        alertas.append({"nivel": "CRÍTICO", "msg": f" Bateria crítica: {dados['bateria']}%",  "codigo": "BAT_CRIT"})
    elif dados["bateria"] < 40:
        alertas.append({"nivel": "AVISO",   "msg": f" Bateria baixa: {dados['bateria']}%",    "codigo": "BAT_WARN"})

    # Painel Solar
    if dados["painel_solar"] < 20:
        alertas.append({"nivel": "AVISO",   "msg": f" Geração solar reduzida: {dados['painel_solar']}%", "codigo": "SOLAR_LOW"})

    # Radiação
    if dados["radiacao_microsv"] > 35:
        alertas.append({"nivel": "CRÍTICO", "msg": f" Radiação elevada: {dados['radiacao_microsv']} µSv/h",  "codigo": "RAD_CRIT"})
    elif dados["radiacao_microsv"] > 25:
        alertas.append({"nivel": "AVISO",   "msg": f" Radiação acima do normal: {dados['radiacao_microsv']} µSv/h", "codigo": "RAD_WARN"})

    # Módulos offline
    for mod, status in modulos.items():
        if status == "OFFLINE":
            alertas.append({"nivel": "CRÍTICO", "msg": f" Módulo '{mod}' está OFFLINE", "codigo": f"MOD_{mod[:4].upper()}"})

    if not alertas:
        alertas.append({"nivel": "OK", "msg": " Todos os sistemas operando normalmente", "codigo": "ALL_OK"})

    return alertas

def tomada_de_decisao(alertas: list, dados: dict, modulos: dict) -> list[str]:
    """IA básica de tomada de decisão automatizada."""
    acoes = []
    codigos = {a["codigo"] for a in alertas}

    if "ENER_CRIT" in codigos or "BAT_CRIT" in codigos:
        st.session_state.modo_emergencia = True
        for mod in list(modulos.keys()):
            if mod not in MODULOS_ESSENCIAIS and modulos[mod] == "ONLINE":
                modulos[mod] = "STANDBY"
                acoes.append(f" Módulo '{mod}' colocado em STANDBY para economizar energia")
        acoes.append(" PROTOCOLO DE EMERGÊNCIA ENERGÉTICA ATIVADO")

    if "TEMP_CRIT" in codigos:
        acoes.append(" Sistema de resfriamento ativo acionado automaticamente")
        acoes.append(" Redução de 20% na carga de processamento do Lab. Científico")

    if "COM_FAIL" in codigos:
        acoes.append(" Tentativa de reconexão via antena de backup iniciada")
        acoes.append(" Log de missão sendo armazenado localmente até restauração")

    if "RAD_CRIT" in codigos:
        acoes.append(" Escudo de radiação magneticamente reforçado")
        acoes.append(" Tripulação instruída a permanecer no módulo blindado central")

    if not acoes:
        st.session_state.modo_emergencia = False
        # Reativar módulos em standby se energia OK
        if dados["energia_disponivel"] > 50:
            for mod in list(modulos.keys()):
                if modulos[mod] == "STANDBY":
                    modulos[mod] = "ONLINE"
                    acoes.append(f" Módulo '{mod}' reativado — energia normalizada")

    return acoes

def gerar_historico_inicial() -> list:
    """Pré-popula 30 ciclos de histórico para os gráficos."""
    historico = []
    for i in range(30):
        d = simular_leitura(i)
        historico.append(d)
    return historico

def aplicar_cenario(dados: dict, cenario: str) -> dict:
    """Aplica valores determinísticos para os cenários de teste."""
    if cenario == "Falha energética crítica":
        dados["energia_disponivel"] = 8.0
        dados["bateria"] = 12.0
    elif cenario == "Tempestade de radiação":
        dados["radiacao_microsv"] = 48.0
    elif cenario == "Perda de comunicação":
        dados["comunicacao"] = "OFFLINE"
    elif cenario == "Múltiplas falhas":
        dados["energia_disponivel"] = 8.0
        dados["bateria"] = 12.0
        dados["radiacao_microsv"] = 48.0
        dados["comunicacao"] = "OFFLINE"
    return dados

# ──────────────────────────────────────────────
# SIDEBAR — CONTROLES
# ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ORION CONTROL")
    st.markdown(f"**Missão:** GS-2026 Alpha")
    st.markdown(f"**Operador:** Lucas Klein — RM 570029")
    st.divider()

    auto_refresh = st.toggle("Atualização Automática", value=False)
    intervalo    = st.slider("Intervalo (segundos)", 1, 10, 3)

    st.divider()
    st.markdown("### Controle de Módulos")
    for mod in list(st.session_state.modulos_status.keys()):
        status = st.session_state.modulos_status[mod]
        col1, col2 = st.columns([2, 1])
        col1.write(mod)
        novo_status = col2.selectbox(
            f"Status de {mod}", ["ONLINE", "STANDBY", "OFFLINE"],
            index=["ONLINE", "STANDBY", "OFFLINE"].index(status),
            key=f"mod_{mod}",
            label_visibility="collapsed"
        )
        st.session_state.modulos_status[mod] = novo_status

    st.divider()
    st.markdown("### Cenário de Teste")
    cenario = st.selectbox("Simular situação:", [
        "Normal",
        "Falha energética crítica",
        "Tempestade de radiação",
        "Perda de comunicação",
        "Múltiplas falhas"
    ])

    aplicar_cenario_agora = st.button("Aplicar Cenário")
    if aplicar_cenario_agora:
        st.session_state.cenario_ativo = cenario
        if cenario == "Normal":
            for mod in st.session_state.modulos_status:
                st.session_state.modulos_status[mod] = "ONLINE"
        elif cenario == "Múltiplas falhas":
            st.session_state.modulos_status["Lab. Científico"] = "OFFLINE"
            st.session_state.modulos_status["Armazenamento"]   = "OFFLINE"

# ──────────────────────────────────────────────
# CABEÇALHO
# ──────────────────────────────────────────────
col_logo, col_titulo, col_status = st.columns([1, 4, 2])
with col_logo:
    st.markdown("# ORION")
with col_titulo:
    st.markdown("# ORION Energy Monitor AI")
    st.markdown("*Sistema Inteligente de Monitoramento Energético — Missão Espacial GS-2026*")
with col_status:
    modo = "EMERGÊNCIA" if st.session_state.modo_emergencia else "OPERACIONAL"
    st.markdown(f"### Status Geral\n## {modo}")

st.divider()

# ──────────────────────────────────────────────
# GERAR / ATUALIZAR DADOS
# ──────────────────────────────────────────────
if not st.session_state.historico:
    st.session_state.historico = gerar_historico_inicial()

if st.button("Atualizar Leitura") or auto_refresh or aplicar_cenario_agora:
    st.session_state.ciclo += 1
    nova_leitura = simular_leitura(st.session_state.ciclo)
    nova_leitura = aplicar_cenario(nova_leitura, st.session_state.cenario_ativo)

    st.session_state.historico.append(nova_leitura)
    if len(st.session_state.historico) > 60:
        st.session_state.historico = st.session_state.historico[-60:]
    if auto_refresh:
        time.sleep(intervalo)
        st.rerun()

dados_atuais = st.session_state.historico[-1]
df           = pd.DataFrame(st.session_state.historico)

# ──────────────────────────────────────────────
# MÉTRICAS PRINCIPAIS (linha 1)
# ──────────────────────────────────────────────
st.markdown("## Painel de Monitoramento em Tempo Real")

c1, c2, c3, c4, c5, c6 = st.columns(6)
c1.metric(" Temp. Casco",    f"{dados_atuais['temperatura_casco']}°C",
          delta=f"{round(dados_atuais['temperatura_casco'] - df['temperatura_casco'].iloc[-2], 1) if len(df)>1 else 0}°C")
c2.metric(" Energia",        f"{dados_atuais['energia_disponivel']}%",
          delta=f"{round(dados_atuais['energia_disponivel'] - df['energia_disponivel'].iloc[-2], 1) if len(df)>1 else 0}%")
c3.metric(" Bateria",        f"{dados_atuais['bateria']}%")
c4.metric(" Painel Solar",   f"{dados_atuais['painel_solar']}%")
c5.metric(" Radiação",       f"{dados_atuais['radiacao_microsv']} µSv/h")
c6.metric(" Comunicação",    dados_atuais["comunicacao"])

c7, c8, c9, c10, c11, c12 = st.columns(6)
c7.metric(" Velocidade",     f"{dados_atuais['velocidade_km_s']} km/s")
c8.metric(" Altitude",       f"{dados_atuais['altitude_km']} km")
c9.metric(" Consumo",        f"{int(dados_atuais['consumo_watts'])} W")
c10.metric(" Fonte",         dados_atuais["fonte_energia"])
c11.metric(" Temp. Núcleo",  f"{dados_atuais['temperatura_nucleo']}°C")
c12.metric(" Ciclo",         f"#{dados_atuais['ciclo']}")

st.divider()

# ──────────────────────────────────────────────
# ALERTAS E TOMADA DE DECISÃO
# ──────────────────────────────────────────────
alertas = analisar_condicoes(dados_atuais, st.session_state.modulos_status)
acoes   = tomada_de_decisao(alertas, dados_atuais, st.session_state.modulos_status)

# Log de alertas
for a in alertas:
    if a["nivel"] != "OK":
        entrada = {"hora": dados_atuais["timestamp"], "ciclo": dados_atuais["ciclo"], **a}
        if not st.session_state.alertas_log or st.session_state.alertas_log[-1]["codigo"] != a["codigo"]:
            st.session_state.alertas_log.append(entrada)

col_alertas, col_acoes = st.columns(2)

with col_alertas:
    st.markdown("##  Central de Alertas")
    for a in alertas:
        cls = "alert-critical" if a["nivel"] == "CRÍTICO" else ("alert-warning" if a["nivel"] == "AVISO" else "alert-ok")
        st.markdown(f'<div class="{cls}">{a["nivel"]} | {a["msg"]}</div>', unsafe_allow_html=True)
        st.write("")

with col_acoes:
    st.markdown("##  Ações Automáticas (IA)")
    if acoes:
        for acao in acoes:
            st.markdown(f'<div class="ia-response">▶ {acao}</div>', unsafe_allow_html=True)
            st.write("")
    else:
        st.markdown('<div class="ia-response"> Sistema estável. Nenhuma ação necessária no momento.</div>', unsafe_allow_html=True)

st.divider()

# ──────────────────────────────────────────────
# GRÁFICOS
# ──────────────────────────────────────────────
st.markdown("##  Histórico de Telemetria")

tab1, tab2, tab3, tab4 = st.tabs(["Energia", "Temperatura", "Solar & Bateria", "Radiação & Outros"])

with tab1:
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["ciclo"], y=df["energia_disponivel"], name="Energia Disponível",
                             line=dict(color="#00d4ff", width=2), fill="tozeroy", fillcolor="rgba(0,212,255,0.1)"))
    fig.add_hline(y=30, line_dash="dash", line_color="orange",  annotation_text="Limite Aviso (30%)")
    fig.add_hline(y=15, line_dash="dash", line_color="red",     annotation_text="Limite Crítico (15%)")
    fig.update_layout(template="plotly_dark", paper_bgcolor="#0d1b2a", plot_bgcolor="#0a0e1a",
                      title="Energia Disponível (%)", height=350)
    st.plotly_chart(fig, width="stretch")

with tab2:
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=df["ciclo"], y=df["temperatura_casco"],  name="Casco",  line=dict(color="#ff6b6b", width=2)))
    fig2.add_trace(go.Scatter(x=df["ciclo"], y=df["temperatura_nucleo"], name="Núcleo", line=dict(color="#ff9f43", width=2)))
    fig2.add_hline(y=85, line_dash="dash", line_color="red",    annotation_text="Crítico (85°C)")
    fig2.add_hline(y=70, line_dash="dash", line_color="orange", annotation_text="Aviso (70°C)")
    fig2.update_layout(template="plotly_dark", paper_bgcolor="#0d1b2a", plot_bgcolor="#0a0e1a",
                       title="Temperatura (°C)", height=350)
    st.plotly_chart(fig2, width="stretch")

with tab3:
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(x=df["ciclo"], y=df["painel_solar"], name="Painel Solar", line=dict(color="#ffd32a", width=2)))
    fig3.add_trace(go.Scatter(x=df["ciclo"], y=df["bateria"],      name="Bateria",      line=dict(color="#00ff88", width=2)))
    fig3.update_layout(template="plotly_dark", paper_bgcolor="#0d1b2a", plot_bgcolor="#0a0e1a",
                       title="Geração Solar e Nível de Bateria (%)", height=350)
    st.plotly_chart(fig3, width="stretch")

with tab4:
    fig4 = go.Figure()
    fig4.add_trace(go.Scatter(x=df["ciclo"], y=df["radiacao_microsv"], name="Radiação (µSv/h)", line=dict(color="#a29bfe", width=2)))
    fig4.add_trace(go.Scatter(x=df["ciclo"], y=df["consumo_watts"] / 20, name="Consumo (W÷20)", line=dict(color="#fd79a8", width=2, dash="dot")))
    fig4.add_hline(y=35, line_dash="dash", line_color="red",    annotation_text="Radiação Crítica (35)")
    fig4.add_hline(y=25, line_dash="dash", line_color="orange", annotation_text="Radiação Aviso (25)")
    fig4.update_layout(template="plotly_dark", paper_bgcolor="#0d1b2a", plot_bgcolor="#0a0e1a",
                       title="Radiação e Consumo", height=350)
    st.plotly_chart(fig4, width="stretch")

st.divider()

# ──────────────────────────────────────────────
# STATUS DOS MÓDULOS
# ──────────────────────────────────────────────
st.markdown("## Status dos Módulos Operacionais")
cols = st.columns(len(st.session_state.modulos_status))
for i, (mod, status) in enumerate(st.session_state.modulos_status.items()):
    cls   = "module-online" if status == "ONLINE" else ("module-standby" if status == "STANDBY" else "module-offline")
    with cols[i]:
        st.markdown(f"**{mod}**")
        st.markdown(f'<span class="{cls}">{status}</span>', unsafe_allow_html=True)
        essencial = "Essencial" if mod in MODULOS_ESSENCIAIS else ""
        st.caption(essencial)

st.divider()

# ──────────────────────────────────────────────
# LOG DE ALERTAS HISTÓRICO
# ──────────────────────────────────────────────
st.markdown("## Log de Ocorrências")
if st.session_state.alertas_log:
    df_log = pd.DataFrame(st.session_state.alertas_log[-20:][::-1])
    df_log = df_log[["hora", "ciclo", "nivel", "msg"]].rename(columns={
        "hora": "Hora", "ciclo": "Ciclo", "nivel": "Nível", "msg": "Mensagem"
    })
    st.dataframe(df_log, width="stretch", hide_index=True)
else:
    st.info("Nenhuma ocorrência registrada ainda.")

st.divider()

# ──────────────────────────────────────────────
# RESUMO ESTATÍSTICO
# ──────────────────────────────────────────────
st.markdown("## Resumo Estatístico da Missão")
if len(df) > 2:
    col_s1, col_s2, col_s3, col_s4 = st.columns(4)

    with col_s1:
        st.markdown("** Energia**")
        st.write(f"Média: {df['energia_disponivel'].mean():.1f}%")
        st.write(f"Mínima: {df['energia_disponivel'].min():.1f}%")
        st.write(f"Máxima: {df['energia_disponivel'].max():.1f}%")

    with col_s2:
        st.markdown("** Temperatura do Casco**")
        st.write(f"Média: {df['temperatura_casco'].mean():.1f}°C")
        st.write(f"Mínima: {df['temperatura_casco'].min():.1f}°C")
        st.write(f"Máxima: {df['temperatura_casco'].max():.1f}°C")

    with col_s3:
        st.markdown("** Painel Solar**")
        st.write(f"Média: {df['painel_solar'].mean():.1f}%")
        st.write(f"Eficiência total: {(df['painel_solar'] > 50).mean() * 100:.0f}% do tempo")

    with col_s4:
        st.markdown("** Alertas**")
        total_criticos = sum(1 for a in st.session_state.alertas_log if a["nivel"] == "CRÍTICO")
        total_avisos   = sum(1 for a in st.session_state.alertas_log if a["nivel"] == "AVISO")
        st.write(f"Críticos: {total_criticos}")
        st.write(f"Avisos: {total_avisos}")
        st.write(f"Total: {len(st.session_state.alertas_log)}")

st.divider()

# ──────────────────────────────────────────────
# RODAPÉ
# ──────────────────────────────────────────────
st.markdown("""
<div style='text-align:center; color:#334455; font-size:0.8em; padding:20px'>
     ORION Energy Monitor AI &nbsp;|&nbsp;
    Global Solution 2026-1 — FIAP &nbsp;|&nbsp;
    Lucas Klein — RM 570029 &nbsp;|&nbsp;
    Ciência da Computação — Turma 1CC
</div>
""", unsafe_allow_html=True)
