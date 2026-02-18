import pandas as pd
from prophet import Prophet
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import webbrowser

# ----------------------------
# 1) Carregar os dados
# ----------------------------
df = pd.read_csv("climate.csv")  # substitua pelo seu CSV
df["created_at"] = pd.to_datetime(df["created_at"]).dt.tz_localize(None)
df = df.rename(columns={"created_at": "ds", "temp_dht": "temp_dht", "humidity": "humidity", "pressure": "pressure"})

# Função de previsão
def forecast_column(df, column_name, periods=1):
    train = df[["ds", column_name]].copy()
    train = train.rename(columns={column_name: "y"})
    model = Prophet(daily_seasonality=True, weekly_seasonality=True)
    model.fit(train)
    future = model.make_future_dataframe(periods=periods, freq='30min')
    forecast = model.predict(future)
    return forecast[["ds", "yhat"]].tail(periods)

# ----------------------------
# 2) Gerar previsões
# ----------------------------
periods_ahead = 1
forecast_temp = forecast_column(df, "temp_dht", periods=periods_ahead)
forecast_hum = forecast_column(df, "humidity", periods=periods_ahead)
forecast_pres = forecast_column(df, "pressure", periods=periods_ahead)

# Últimos valores reais
last_temp = df["temp_dht"].iloc[-1]
last_hum = df["humidity"].iloc[-1]
last_pres = df["pressure"].iloc[-1]

# Previsões IA
pred_temp = forecast_temp["yhat"].iloc[-1]
pred_hum = forecast_hum["yhat"].iloc[-1]
pred_pres = forecast_pres["yhat"].iloc[-1]

# Deltas
delta_temp = pred_temp - last_temp
delta_hum = pred_hum - last_hum
delta_pres = pred_pres - last_pres

# Setas
arrow_temp = "↑" if delta_temp > 0 else "↓"
arrow_hum = "↑" if delta_hum > 0 else "↓"
arrow_pres = "↑" if delta_pres > 0 else "↓"

# ----------------------------
# 3) Chance de chuva (simplificada)
# ----------------------------
delta_pres_abs = abs(delta_pres)
chance_chuva = min(max((last_hum/100) * (delta_pres_abs/10) * 100, 0), 100)
chance_chuva = round(chance_chuva, 1)

# ----------------------------
# 4) Criar painel 2x4 (1 gauge + 1 previsão por coluna)
# ----------------------------
fig = make_subplots(
    rows=2, cols=4,
    specs=[[{'type':'indicator'}]*4,
           [{'type':'indicator'}]*4],
    horizontal_spacing=0.05, vertical_spacing=0.2
)

# ----------------------------
# Linha 1: Gauges
# ----------------------------
fig.add_trace(go.Indicator(
    mode="gauge+number",
    value=last_temp,
    title={'text': "Temp Real (°C)", 'font': {'size': 20}},
    gauge={'axis': {'range':[0,50]}, 'bar': {'color':'orange'}, 'bgcolor':'lightgray'},
), row=1, col=1)

fig.add_trace(go.Indicator(
    mode="gauge+number",
    value=last_hum,
    title={'text': "Umidade Real (%)", 'font': {'size': 20}},
    gauge={'axis': {'range':[0,100]}, 'bar': {'color':'blue'}, 'bgcolor':'lightgray'},
), row=1, col=2)

fig.add_trace(go.Indicator(
    mode="gauge+number",
    value=last_pres,
    title={'text': "Pressão Real (hPa)", 'font': {'size': 20}},
    gauge={'axis': {'range':[900,1050]}, 'bar': {'color':'purple'}, 'bgcolor':'lightgray'},
), row=1, col=3)

fig.add_trace(go.Indicator(
    mode="gauge+number",
    value=chance_chuva,
    title={'text': "Chance de Chuva (%)", 'font': {'size': 20}},
    gauge={'axis': {'range':[0,100]}, 'bar': {'color':'deepskyblue'}, 'bgcolor':'lightgray'},
), row=1, col=4)

# ----------------------------
# Linha 2: Previsões
# ----------------------------
fig.add_trace(go.Indicator(
    mode="number+delta",
    value=pred_temp,
    delta={'reference': last_temp, 'position': "bottom", 'increasing': {'color':'red'}, 'decreasing': {'color':'blue'}},
    title={'text': f"Temp Prev. {arrow_temp}", 'font': {'size':16}}
), row=2, col=1)

fig.add_trace(go.Indicator(
    mode="number+delta",
    value=pred_hum,
    delta={'reference': last_hum, 'position': "bottom", 'increasing': {'color':'green'}, 'decreasing': {'color':'red'}},
    title={'text': f"Umid Prev. {arrow_hum}", 'font': {'size':16}}
), row=2, col=2)

fig.add_trace(go.Indicator(
    mode="number+delta",
    value=pred_pres,
    delta={'reference': last_pres, 'position': "bottom", 'increasing': {'color':'red'}, 'decreasing': {'color':'green'}},
    title={'text': f"Pressão Prev. {arrow_pres}", 'font': {'size':16}}
), row=2, col=3)

fig.add_trace(go.Indicator(
    mode="number",
    value=chance_chuva,
    title={'text': "Chance Prev. (%)", 'font': {'size':16}}
), row=2, col=4)

# ----------------------------
# Layout
# ----------------------------
fig.update_layout(
    template=None,
    paper_bgcolor="white",
    font={'color':'black','family':'Arial'},
    title={'text': "SmartClimate AI - Painel Digital", 'x':0.5, 'xanchor':'center', 'yanchor':'top', 'font':{'size':28}}
)

# ----------------------------
# Salvar e abrir
# ----------------------------
output_file = "painel_digital_2x4.html"
fig.write_html(output_file)
print(f"Painel digital interativo salvo: {output_file}")

def open_dashboard(file_path):
    full_path = os.path.abspath(file_path)
    webbrowser.open(f"file://{full_path}")

open_dashboard(output_file)
