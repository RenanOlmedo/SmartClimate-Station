
# forecast_dashboard_painel.py
import pandas as pd
from prophet import Prophet
import plotly.graph_objs as go

# --- CONFIGURAÇÕES ---
csv_file = "climate.csv"  # seu CSV real do ThingSpeak
output_html = "previsao_painel_interativo.html"

# --- LENDO DADOS ---
df = pd.read_csv(csv_file)
df['ds'] = pd.to_datetime(df['created_at']).dt.tz_localize(None)  # remove timezone

# --- SENSORES ---
sensors = {
    "humidity": "Umidade (%)",
    "temp_dht": "Temp DHT11 (°C)",
    "temp_bmp": "Temp BMP180 (°C)",
    "pressure": "Pressão (hPa)"
}

# --- TREINA MODELO E FAZ PREVISÃO ---
forecasts = {}
for col, label in sensors.items():
    print(f"Treinando e prevendo: {col}")
    sensor_df = df[['ds', col]].rename(columns={col: 'y'})
    sensor_df = sensor_df.dropna()  # remove NaN antes de treinar
    model = Prophet(daily_seasonality=True)
    model.fit(sensor_df)
    future = model.make_future_dataframe(periods=24, freq='H')
    forecast = model.predict(future)
    forecasts[col] = forecast

# --- CONFIGURAÇÃO DOS MEDIDORES ---
card_colors = {
    "humidity": "royalblue",
    "temp_dht": "orange",
    "temp_bmp": "crimson",
    "pressure": "green"
}

x_positions = {
    "humidity": [0.0, 0.25],
    "temp_dht": [0.25, 0.5],
    "temp_bmp": [0.5, 0.75],
    "pressure": [0.75, 1.0]
}

fig = go.Figure()

# --- ADICIONA MEDIDORES DIGITAIS ---
for col, label in sensors.items():
    forecast = forecasts[col]
    last_val = round(forecast['yhat'].iloc[-1], 2)
    
    # Último valor real, mas ignora NaN
    last_real = df[col].dropna().iloc[-1] if not df[col].dropna().empty else last_val

    fig.add_trace(go.Indicator(
        mode="gauge+number+delta",
        value=last_val,
        delta={
            'reference': last_real,
            'relative': False,
            'position': "top",
            'increasing': {'color': "green"},
            'decreasing': {'color': "red"}
        },
        title={"text": label, "font": {"size": 20}},
        gauge={
            'axis': {'range': [min(df[col].min(), last_val - 5), max(df[col].max(), last_val + 5)]},
            'bar': {'color': card_colors[col]},
            'bgcolor': "lightgray",
            'borderwidth': 2,
            'bordercolor': "gray",
        },
        number={'font': {"size": 40, "color": card_colors[col]}},
        domain={'x': x_positions[col], 'y': [0, 1]}
    ))

# --- LAYOUT ---
fig.update_layout(
    paper_bgcolor="white",
    height=450,
    margin=dict(l=20, r=20, t=50, b=20),
    title={
        "text": "SmartClimate AI - Painel Digital IoT",
        "font": {"size": 28},
        "x": 0.5
    }
)

# --- SALVA E ABRE ---
fig.write_html(output_html, auto_open=True)
print(f"Painel digital interativo salvo: {output_html}")
