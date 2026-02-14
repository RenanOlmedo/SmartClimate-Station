import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt

# 1️⃣ Carregar dados
df = pd.read_csv("climate.csv")
df["ds"] = pd.to_datetime(df["created_at"]).dt.tz_localize(None)

# 2️⃣ Sensores e cores
sensors = ["humidity", "temp_dht", "temp_bmp", "pressure"]
colors = {"humidity":"blue", "temp_dht":"green", "temp_bmp":"red", "pressure":"orange"}

# 3️⃣ DataFrame para salvar previsões
forecast_all = pd.DataFrame()
forecast_all["ds"] = df["ds"]

# 4️⃣ Criar figura com 4 subplots (um por sensor)
fig, axs = plt.subplots(len(sensors), 1, figsize=(12, 10), sharex=True)

for i, sensor in enumerate(sensors):
    print(f"Treinando e prevendo: {sensor}")
    
    # Preparar dados
    df_model = df[["ds", sensor]].rename(columns={sensor: "y"})
    
    # Criar e treinar modelo
    model = Prophet(daily_seasonality=True)
    model.fit(df_model)
    
    # Criar futuro (24 horas)
    future = model.make_future_dataframe(periods=24, freq="H")
    
    # Prever
    forecast = model.predict(future)
    
    # Adicionar previsões ao dataframe final
    forecast_all[sensor+"_forecast"] = forecast["yhat"]
    
    # Plotar histórico
    axs[i].plot(df_model["ds"], df_model["y"], label=f"{sensor} Real", color=colors[sensor], linestyle="solid")
    
    # Plotar previsão
    axs[i].plot(forecast["ds"], forecast["yhat"], label=f"{sensor} Previsto", color=colors[sensor], linestyle="dashed")
    
    # Faixa de incerteza
    axs[i].fill_between(forecast["ds"], forecast["yhat_lower"], forecast["yhat_upper"], color=colors[sensor], alpha=0.1)
    
    axs[i].set_ylabel(sensor)
    axs[i].legend()
    axs[i].grid(True)

# 5️⃣ Ajustes finais
plt.xlabel("Data/Hora")
plt.tight_layout()
plt.savefig("previsao_completa_subplots.png", dpi=150)
plt.show()

# 6️⃣ Salvar previsões em CSV
forecast_all.to_csv("previsao_completa.csv", index=False)
print("Previsões salvas em previsao_completa.csv e gráfico em previsao_completa_subplots.png")
