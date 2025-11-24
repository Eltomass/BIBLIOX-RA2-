"""
Dashboard de Monitoreo y Observabilidad - BiblioX
IE5: Dashboard visual que muestra el comportamiento del agente según las métricas implementadas
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import os
from datetime import datetime, timedelta
import sys

# Agregar path para imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from monitoring.metrics import get_metrics_collector

# Configuración de la página
st.set_page_config(
    page_title="BiblioX - Dashboard de Observabilidad",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado con animaciones
st.markdown("""
<style>
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes slideInLeft {
    from {
        opacity: 0;
        transform: translateX(-50px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}

@keyframes pulse {
    0%, 100% {
        transform: scale(1);
    }
    50% {
        transform: scale(1.05);
    }
}

@keyframes shimmer {
    0% {
        background-position: -1000px 0;
    }
    100% {
        background-position: 1000px 0;
    }
}

/* Animaciones para elementos */
.main > div {
    animation: fadeInUp 0.8s ease-out;
}

.stMetric {
    animation: fadeInUp 0.6s ease-out;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.stMetric:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 16px rgba(0,0,0,0.2);
}

[data-testid="stMetricValue"] {
    font-size: 2rem !important;
    font-weight: 700;
    background: linear-gradient(90deg, #1f77b4, #ff7f0e);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: shimmer 3s infinite linear;
    background-size: 2000px 100%;
}

.stPlotlyChart {
    animation: fadeInUp 0.8s ease-out;
    transition: transform 0.2s ease;
}

.stPlotlyChart:hover {
    transform: scale(1.02);
}

.stExpander {
    animation: slideInLeft 0.6s ease-out;
    transition: all 0.3s ease;
}

.stExpander:hover {
    border-left: 4px solid #1f77b4;
    padding-left: 10px;
}

.stDataFrame {
    animation: fadeInUp 0.7s ease-out;
}

h1 {
    animation: slideInLeft 0.8s ease-out;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 800;
}

h2 {
    animation: slideInLeft 0.7s ease-out;
    color: #2c3e50;
    border-left: 5px solid #3498db;
    padding-left: 15px;
    margin-top: 20px;
}

.stButton > button {
    transition: all 0.3s ease;
    border-radius: 8px;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 12px rgba(0,0,0,0.15);
}

/* Sidebar animations */
.css-1d391kg {
    animation: slideInLeft 0.6s ease-out;
}

/* Header gradiente animado */
.animated-header {
    background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
    background-size: 400% 400%;
    animation: gradient 15s ease infinite;
    padding: 20px;
    border-radius: 10px;
    color: white;
    text-align: center;
    margin-bottom: 30px;
}

@keyframes gradient {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
</style>
""", unsafe_allow_html=True)

# Header principal con animación
st.markdown("""
<div class="animated-header">
    <h1 style="margin:0; color: white; -webkit-text-fill-color: white;">Dashboard de Observabilidad BiblioX</h1>
    <p style="margin:5px 0 0 0; color: rgba(255,255,255,0.9);">Sistema de Monitoreo en Tiempo Real del Agente Funcional</p>
</div>
""", unsafe_allow_html=True)

# Obtener el collector de métricas
metrics = get_metrics_collector()

# Sidebar para controles
st.sidebar.header("Configuración")

# Botón para recargar métricas desde archivo
if st.sidebar.button("Recargar Métricas desde Archivo"):
    metrics_file = 'logs/metrics.json'
    if os.path.exists(metrics_file):
        st.sidebar.success("Métricas recargadas exitosamente")
    else:
        st.sidebar.warning("No hay archivo de métricas disponible")

# Botón para limpiar métricas
if st.sidebar.button("Limpiar Métricas", help="Resetea todas las métricas acumuladas"):
    metrics.reset()
    st.sidebar.success("Métricas limpiadas correctamente")
    st.rerun()

st.sidebar.divider()

# Filtros
st.sidebar.subheader("Filtros")
show_errors_only = st.sidebar.checkbox("Solo mostrar errores", value=False)
min_latency = st.sidebar.slider("Latencia mínima (s)", 0.0, 10.0, 0.0, 0.1)

# Obtener estadísticas
stats = metrics.get_summary_stats()

# ============================================================
# SECCIÓN 1: KPIs PRINCIPALES
# ============================================================
st.header("KPIs Principales")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        label="Total Requests",
        value=stats['total_requests'],
        delta=None
    )

with col2:
    successful = stats['total_requests'] - stats['total_errors'] if stats['total_requests'] > 0 else 0
    success_rate = (successful / stats['total_requests'] * 100) if stats['total_requests'] > 0 else 0
    st.metric(
        label="Tasa de Éxito",
        value=f"{success_rate:.1f}%",
        delta=f"{successful}/{stats['total_requests']}"
    )

with col3:
    st.metric(
        label="Latencia Promedio",
        value=f"{stats['avg_latency']:.2f}s",
        delta=None
    )

with col4:
    st.metric(
        label="Total Errores",
        value=stats['total_errors'],
        delta=None,
        delta_color="inverse"
    )

with col5:
    st.metric(
        label="Herramientas Usadas",
        value=stats['total_tools_used'],
        delta=f"{stats['unique_tools']} únicas"
    )

st.divider()

# ============================================================
# SECCIÓN 2: GRÁFICOS DE LATENCIA (IE2)
# ============================================================
st.header("Análisis de Latencia")

if stats['total_requests'] > 0:
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de distribución de latencias
        st.subheader("Distribución de Latencia")
        
        requests = metrics.metrics_data['requests']
        latencies = [r['total_latency'] for r in requests if r['total_latency'] >= min_latency]
        
        if latencies:
            fig_hist = px.histogram(
                latencies,
                nbins=20,
                labels={'value': 'Latencia (s)', 'count': 'Frecuencia'},
                title="Distribución de Tiempos de Respuesta"
            )
            fig_hist.add_vline(x=stats['avg_latency'], line_dash="dash", line_color="red", 
                              annotation_text=f"Promedio: {stats['avg_latency']:.2f}s")
            fig_hist.add_vline(x=stats['p95_latency'], line_dash="dash", line_color="orange",
                              annotation_text=f"P95: {stats['p95_latency']:.2f}s")
            st.plotly_chart(fig_hist, use_container_width=True)
    
    with col2:
        # Percentiles
        st.subheader("Percentiles de Latencia")
        
        percentiles_data = {
            'Percentil': ['P50 (Mediana)', 'P95', 'P99', 'Mínimo', 'Máximo'],
            'Latencia (s)': [
                stats['p50_latency'],
                stats['p95_latency'],
                stats['p99_latency'],
                stats['min_latency'],
                stats['max_latency']
            ]
        }
        
        fig_percentiles = px.bar(
            percentiles_data,
            x='Percentil',
            y='Latencia (s)',
            title="Latencia por Percentiles",
            color='Latencia (s)',
            color_continuous_scale='Reds'
        )
        st.plotly_chart(fig_percentiles, use_container_width=True)
    
    # Evolución temporal de latencia
    st.subheader("Evolución Temporal de Latencia")
    
    requests_df = pd.DataFrame([
        {
            'timestamp': r['start_timestamp'],
            'latencia': r['total_latency'],
            'status': r['status']
        }
        for r in requests
    ])
    
    if not requests_df.empty:
        fig_timeline = px.line(
            requests_df,
            x='timestamp',
            y='latencia',
            color='status',
            title="Latencia de Requests a lo Largo del Tiempo",
            labels={'latencia': 'Latencia (s)', 'timestamp': 'Tiempo'}
        )
        st.plotly_chart(fig_timeline, use_container_width=True)

else:
    st.info("No hay datos de latencia aún. Ejecuta algunos requests para ver métricas.")

st.divider()

# ============================================================
# SECCIÓN 3: USO DE HERRAMIENTAS (IE1, IE4)
# ============================================================
st.header("Análisis de Herramientas del Agente")

if stats['total_tools_used'] > 0:
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de pie - Distribución de uso de herramientas
        st.subheader("Distribución de Uso de Herramientas")
        
        tool_usage_df = pd.DataFrame([
            {'Herramienta': tool, 'Uso': count}
            for tool, count in stats['tool_usage'].items()
        ])
        
        fig_pie = px.pie(
            tool_usage_df,
            values='Uso',
            names='Herramienta',
            title="Proporción de Uso por Herramienta"
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # Tabla de estadísticas por herramienta
        st.subheader("Estadísticas por Herramienta")
        
        tool_stats = []
        for tool_name, tool_data in metrics.metrics_data['tools'].items():
            if tool_data:
                latencies = [d['latency'] for d in tool_data]
                success_count = sum(1 for d in tool_data if d['success'])
                
                tool_stats.append({
                    'Herramienta': tool_name,
                    'Llamadas': len(tool_data),
                    'Éxito': success_count,
                    'Tasa Éxito': f"{success_count/len(tool_data)*100:.1f}%",
                    'Latencia Avg': f"{sum(latencies)/len(latencies):.3f}s"
                })
        
        if tool_stats:
            tools_df = pd.DataFrame(tool_stats)
            st.dataframe(tools_df, use_container_width=True, hide_index=True)
    
    # Gráfico de barras - Latencia por herramienta
    st.subheader("Latencia Promedio por Herramienta")
    
    tool_latency_data = []
    for tool_name, tool_data in metrics.metrics_data['tools'].items():
        if tool_data:
            latencies = [d['latency'] for d in tool_data]
            tool_latency_data.append({
                'Herramienta': tool_name,
                'Latencia Promedio': sum(latencies) / len(latencies),
                'Llamadas': len(tool_data)
            })
    
    if tool_latency_data:
        fig_bar = px.bar(
            tool_latency_data,
            x='Herramienta',
            y='Latencia Promedio',
            color='Llamadas',
            title="Comparación de Latencia entre Herramientas",
            labels={'Latencia Promedio': 'Latencia Promedio (s)'}
        )
        st.plotly_chart(fig_bar, use_container_width=True)

else:
    st.info("No se han ejecutado herramientas aún.")

st.divider()

# ============================================================
# SECCIÓN 4: USO DE RECURSOS (IE2)
# ============================================================
st.header("Uso de Recursos del Sistema")

if stats['total_requests'] > 0:
    col1, col2 = st.columns(2)
    
    with col1:
        # Gauge para CPU
        fig_cpu = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=stats['avg_cpu_percent'],
            title={'text': "CPU Promedio (%)"},
            delta={'reference': 20},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 30], 'color': "lightgreen"},
                    {'range': [30, 70], 'color': "yellow"},
                    {'range': [70, 100], 'color': "red"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 80
                }
            }
        ))
        st.plotly_chart(fig_cpu, use_container_width=True)
    
    with col2:
        # Gauge para Memoria
        fig_mem = go.Figure(go.Indicator(
            mode="gauge+number",
            value=stats['avg_memory_mb'],
            title={'text': "Memoria Promedio (MB)"},
            gauge={
                'axis': {'range': [0, 1024]},
                'bar': {'color': "darkred"},
                'steps': [
                    {'range': [0, 256], 'color': "lightgreen"},
                    {'range': [256, 512], 'color': "yellow"},
                    {'range': [512, 1024], 'color': "red"}
                ]
            }
        ))
        st.plotly_chart(fig_mem, use_container_width=True)

st.divider()

# ============================================================
# SECCIÓN 5: ERRORES Y ANOMALÍAS (IE3, IE4)
# ============================================================
st.header("Errores y Anomalías")

col1, col2 = st.columns(2)

with col1:
    # Lista de errores
    st.subheader("Errores Recientes")
    
    errors = metrics.metrics_data['errors']
    if errors:
        errors_df = pd.DataFrame([
            {
                'Timestamp': e['timestamp'],
                'Componente': e['component'],
                'Tipo': e['type'],
                'Mensaje': e['message'][:100]
            }
            for e in errors[-10:]  # Últimos 10 errores
        ])
        st.dataframe(errors_df, use_container_width=True, hide_index=True)
    else:
        st.success("No hay errores registrados")

with col2:
    # Anomalías de latencia
    st.subheader("Anomalías Detectadas (Latencia > 2x Promedio)")
    
    if stats['total_requests'] > 0:
        threshold = stats['avg_latency'] * 2
        anomalies = [
            r for r in metrics.metrics_data['requests']
            if r['total_latency'] > threshold
        ]
        
        if anomalies:
            anomalies_df = pd.DataFrame([
                {
                    'Trace ID': a['trace_id'],
                    'Query': a['query'][:50] + '...',
                    'Latencia': f"{a['total_latency']:.2f}s"
                }
                for a in anomalies
            ])
            st.dataframe(anomalies_df, use_container_width=True, hide_index=True)
        else:
            st.success("No se detectaron anomalías de latencia")

st.divider()

# ============================================================
# SECCIÓN 6: LOGS Y TRAZABILIDAD (IE3)
# ============================================================
st.header("Logs y Trazabilidad")

# Mostrar últimos requests con detalles
st.subheader("Últimos 10 Requests")

requests = metrics.metrics_data['requests'][-10:]

if requests:
    for req in reversed(requests):
        with st.expander(f"{req['trace_id']} - {req['query'][:60]}... ({req['status']})"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Detalles del Request:**")
                st.write(f"- **Timestamp:** {req['start_timestamp']}")
                st.write(f"- **Session ID:** {req['session_id']}")
                st.write(f"- **Status:** {req['status']}")
                st.write(f"- **Latencia Total:** {req['total_latency']:.3f}s")
                st.write(f"- **Query:** {req['query']}")
            
            with col2:
                st.write("**Herramientas Ejecutadas:**")
                if req.get('tools_used'):
                    for tool in req['tools_used']:
                        success_icon = "[OK]" if tool['success'] else "[FAIL]"
                        st.write(f"{success_icon} `{tool['tool_name']}` - {tool['latency']:.3f}s")
                else:
                    st.write("_No se usaron herramientas_")
                
                st.write("**Recursos:**")
                st.write(f"- CPU: {req['resource_usage']['cpu_percent']:.1f}%")
                st.write(f"- Memoria: {req['resource_usage']['memory_mb']:.1f} MB")
else:
    st.info("No hay requests registrados aún")

st.divider()

# ============================================================
# FOOTER CON INFORMACIÓN DEL SISTEMA
# ============================================================
st.caption("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.caption(f"Total de Requests: **{stats['total_requests']}**")

with col2:
    st.caption(f"Herramientas Únicas: **{stats['unique_tools']}**")

with col3:
    if stats['total_requests'] > 0:
        st.caption(f"Herramienta Más Usada: **{stats.get('most_used_tool', 'N/A')}**")
    else:
        st.caption("Herramienta Más Usada: **N/A**")

st.caption("**BiblioX - Sistema de Observabilidad y Monitoreo** | Evaluación Parcial N°3 - RA3")
