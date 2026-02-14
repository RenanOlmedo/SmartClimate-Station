import pandas as pd
from prophet import Prophet
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import os, webbrowser

# ----------------------------
# 1) Carregar os dados reais
# ----------------------------
df = pd.read_csv("climate.csv")  # substitua pelo seu CSV
df["created_at"] = pd.to_datetime(df["created_at"]).dt.tz_localize(None)
df = df.rename(columns={"created_at": "ds", "temp_dht": "temp_dht", "humidity": "humidity", "pressure": "pressure"})

# Função para treinar Prophet e gerar previsão
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
periods_ahead = 1  # previsão para próxima medição
forecast_temp = forecast_column(df, "temp_dht", periods=periods_ahead)
forecast_hum = forecast_column(df, "humidity", periods=periods_ahead)
forecast_pres = forecast_column(df, "pressure", periods=periods_ahead)

# Últimos valores reais
last_real_temp = df["temp_dht"].iloc[-1]
last_real_hum = df["humidity"].iloc[-1]
last_real_pres = df["pressure"].iloc[-1]

# Previsões IA
pred_temp = forecast_temp["yhat"].iloc[-1]
pred_hum = forecast_hum["yhat"].iloc[-1]
pred_pres = forecast_pres["yhat"].iloc[-1]

# Deltas
delta_temp = pred_temp - last_real_temp
delta_hum = pred_hum - last_real_hum
delta_pres = pred_pres - last_real_pres

# Setas
arrow_temp = "↑" if delta_temp > 0 else "↓"
arrow_hum = "↑" if delta_hum > 0 else "↓"
arrow_pres = "↑" if delta_pres > 0 else "↓"

# ----------------------------
# 3) Chance de chuva (simplificada)
# delta pressão + umidade
# ----------------------------
delta_pres_abs = abs(delta_pres)
chance_chuva = min(max((last_real_hum/100) * (delta_pres_abs/5) * 100, 0), 100)  # 0 a 100%
chance_chuva = round(chance_chuva, 1)

# ----------------------------
# 4) Criar painel digital com medidores lado a lado
# ----------------------------
fig = make_subplots(
    rows=1, cols=4,
    specs=[[{'type':'indicator'}, {'type':'indicator'}, {'type':'indicator'}, {'type':'indicator'}]],
    horizontal_spacing=0.1
)

# ------------------------------
# Medidor de Umidade
# ------------------------------
fig.add_trace(go.Indicator(
    mode="gauge+number+delta",
    value=last_real_hum,
    delta={'reference': pred_hum, 'position': "top", 'increasing': {'color':'green'}, 'decreasing': {'color':'red'}, 'valueformat':".1f"},
    title={'text': f"Umidade Real\nPrevisão {pred_hum:.1f}% {arrow_hum}", 'font': {'size': 18}},
    gauge={
        'axis': {'range':[0,100]},
        'bar': {'color': "blue"},
        'bgcolor': "lightgray",
        'steps': [
            {'range':[0,30], 'color':'lightblue'},
            {'range':[30,70], 'color':'blue'},
            {'range':[70,100], 'color':'darkblue'}
        ]
    }
), row=1, col=1)

# ------------------------------
# Medidor de Temperatura
# ------------------------------
fig.add_trace(go.Indicator(
    mode="gauge+number+delta",
    value=last_real_temp,
    delta={'reference': pred_temp, 'position': "top", 'increasing': {'color':'red'}, 'decreasing': {'color':'blue'}, 'valueformat':".1f"},
    title={'text': f"Temp Real (°C)\nPrevisão {pred_temp:.1f}°C {arrow_temp}", 'font': {'size': 18}},
    gauge={
        'axis': {'range':[0,50]},
        'bar': {'color': "orange"},
        'bgcolor': "lightgray",
        'steps': [
            {'range':[0,20], 'color':'lightyellow'},
            {'range':[20,35], 'color':'orange'},
            {'range':[35,50], 'color':'darkorange'}
        ]
    }
), row=1, col=2)

# ------------------------------
# Medidor de Pressão
# ------------------------------
fig.add_trace(go.Indicator(
    mode="gauge+number+delta",
    value=last_real_pres,
    delta={'reference': pred_pres, 'position': "top", 'increasing': {'color':'red'}, 'decreasing': {'color':'green'}, 'valueformat':".1f"},
    title={'text': f"Pressão Real (hPa)\nPrevisão {pred_pres:.1f} {arrow_pres}", 'font': {'size': 18}},
    gauge={
        'axis': {'range':[900,1050]},
        'bar': {'color': "purple"},
        'bgcolor': "lightgray",
        'steps': [
            {'range':[900,980], 'color':'violet'},
            {'range':[980,1020], 'color':'purple'},
            {'range':[1020,1050], 'color':'darkviolet'}
        ]
    }
), row=1, col=3)

# ------------------------------
# Medidor de Chance de Chuva
# ------------------------------
fig.add_trace(go.Indicator(
    mode="gauge+number",
    value=chance_chuva,
    title={'text': f"Chance de Chuva (%)", 'font': {'size': 18}},
    gauge={
        'axis': {'range':[0,100]},
        'bar': {'color': "skyblue"},
        'bgcolor': "lightgray",
        'steps': [
            {'range':[0,30], 'color':'lightblue'},
            {'range':[30,70], 'color':'deepskyblue'},
            {'range':[70,100], 'color':'blue'}
        ]
    }
), row=1, col=4)

# Layout geral
fig.update_layout(
    template=None,
    paper_bgcolor="white",
    font={'color':'black', 'family':'Arial'},
    title={'text': "SmartClimate AI - Painel Digital", 'x':0.5, 'xanchor':'center', 'yanchor':'top', 'font':{'size':28}}
)

# Salvar e abrir automaticamente
output_file = "painel_digital_medidores.html"
fig.write_html(output_file)
print(f"Painel digital interativo salvo: {output_file}")

def open_dashboard(file_path):
    full_path = os.path.abspath(file_path)
    webbrowser.open(f"file://{full_path}")

open_dashboard(output_file)
