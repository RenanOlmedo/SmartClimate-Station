import pandas as pd
from prophet import Prophet
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import webbrowser

# =========================
# 1️⃣ Ler dados do CSV
# =========================
df = pd.read_csv("climate.csv")
df['created_at'] = pd.to_datetime(df['created_at']).dt.tz_localize(None)  # remove timezone

sensor_map = {
    "humidity": {"col": "humidity", "title": "Umidade (%)", "color": "blue", "alert": (30, 80)},
    "temp_dht": {"col": "temp_dht", "title": "Temperatura DHT11 (°C)", "color": "green", "alert": (15, 40)},
    "temp_bmp": {"col": "temp_bmp", "title": "Temperatura BMP180 (°C)", "color": "red", "alert": (15, 40)},
    "pressure": {"col": "pressure", "title": "Pressão (hPa)", "color": "orange", "alert": (950, 1050)}
}

# =========================
# 2️⃣ Prever todos os sensores
# =========================
forecast_all = pd.DataFrame()

for sensor, info in sensor_map.items():
    print(f"Treinando e prevendo: {sensor}")
    df_sensor = pd.DataFrame()
    df_sensor['ds'] = df['created_at']
    df_sensor['y'] = df[info["col"]].astype(float)

    model = Prophet()
    model.fit(df_sensor)

    future = model.make_future_dataframe(periods=0, freq='H')
    forecast = model.predict(future)
    forecast = forecast[['ds','yhat']]
    forecast = forecast.rename(columns={'yhat': sensor})

    if forecast_all.empty:
        forecast_all = forecast
    else:
        forecast_all = forecast_all.merge(forecast, on='ds')

# =========================
# 3️⃣ Criar dashboard com 4 cards separados + destaques
# =========================
fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=[info["title"] for info in sensor_map.values()],
    vertical_spacing=0.15,
    horizontal_spacing=0.1
)

row_col_map = {
    "humidity": (1,1),
    "temp_dht": (1,2),
    "temp_bmp": (2,1),
    "pressure": (2,2)
}

color_rgba = {
    "blue": "rgba(0,0,255,0.2)",
    "green": "rgba(0,255,0,0.2)",
    "red": "rgba(255,0,0,0.2)",
    "orange": "rgba(255,165,0,0.2)"
}

for sensor, info in sensor_map.items():
    r, c = row_col_map[sensor]
    last_val = df[info["col"]].iloc[-1]
    alert_min, alert_max = info["alert"]
    alert_color = "red" if (last_val < alert_min or last_val > alert_max) else info["color"]

    # Gráfico da previsão
    fig.add_trace(
        go.Scatter(
            x=forecast_all['ds'],
            y=forecast_all[sensor],
            mode='lines',
            name=sensor,
            line=dict(color=info["color"], width=3),
            fill='tozeroy',
            fillcolor=color_rgba[info["color"]]
        ),
        row=r, col=c
    )

    # Última medição em destaque como marcador
    fig.add_trace(
        go.Scatter(
            x=[df['created_at'].iloc[-1]],
            y=[last_val],
            mode='markers+text',
            marker=dict(color=alert_color, size=15, symbol='circle'),
            text=[f"Último: {last_val:.2f}"],
            textposition="top center",
            showlegend=False
        ),
        row=r, col=c
    )

# =========================
# 4️⃣ Layout e estilo
# =========================
fig.update_layout(
    title=dict(
        text="SmartClimate AI - Painel Interativo Premium",
        x=0.5, y=0.95,
        font=dict(size=28, color="black")
    ),
    template="plotly_white",
    hovermode="x unified",
    height=900
)

# =========================
# 5️⃣ Salvar e abrir no navegador
# =========================
fig.write_html("dashboard_interativo_premium.html")
print("Dashboard interativo salvo: dashboard_interativo_premium.html")
webbrowser.open("dashboard_interativo_premium.html")

# =========================
# 6️⃣ Salvar CSV de previsões
# =========================
forecast_all.to_csv("previsao_dashboard_interativo_premium.csv", index=False)
print("CSV de previsões salvo: previsao_dashboard_interativo_premium.csv")
