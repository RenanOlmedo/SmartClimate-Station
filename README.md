# 🌤 SmartClimate AI

SmartClimate AI é uma estação meteorológica inteligente que combina sensores físicos, nuvem e inteligência artificial para gerar previsões climáticas e exibir tudo em um painel web interativo.

O projeto utiliza um **ESP8266** com sensores **DHT11** e **BMP180**, envia os dados para o **ThingSpeak** e, a partir desses dados, um sistema em **Python com IA (Prophet)** cria previsões e um **dashboard HTML interativo**.

---

## 🔥 Versão final do projeto


"dashboard_interativo_2_X_4_final.py"


Esse arquivo:
- Lê os dados do `climate.csv`
- Executa as previsões com IA
- Calcula tendências (subir / cair)
- Estima chance de chuva
- Gera o painel HTML interativo final

---

## 📊 O que o projeto faz

- Lê temperatura, umidade e pressão do ar
- Envia os dados automaticamente para a internet
- Usa inteligência artificial para prever o clima
- Mostra tudo em um painel moderno com indicadores, setas e gauges

---

## 🧠 Tecnologias usadas

- ESP8266 (NodeMCU)
- Sensor DHT11
- Sensor BMP180
- ThingSpeak API
- Python 3
- Prophet (Facebook)
- Pandas
- Plotly
- HTML interativo

---

## 🚀 Como funciona o sistema

1. O ESP8266 lê os sensores
2. Envia os dados para o ThingSpeak
3. O Python baixa os dados e cria `climate.csv`
4. O script `dashboard_interativo_2_X_4_final.py` gera:
   - Previsão por IA
   - Painel web interativo

---

## 🖥 Resultado final

O sistema gera um painel HTML que mostra:
- Temperatura atual
- Umidade atual
- Pressão atmosférica
- Chance de chuva
- Previsão da IA
- Tendência de subida ou queda

Tudo em tempo real, visual e interativo.

---

## 🔒 Segurança

As chaves de Wi-Fi e do ThingSpeak não estão no repositório, fazer a substituicao pela sua no campo do codigo (******).


---

## 🧑‍💻 Autor

Projeto desenvolvido por **Renan Ferreira**.
