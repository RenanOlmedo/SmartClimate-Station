import requests
import pandas as pd

CHANNEL_ID = "2420345"
READ_KEY = "MTKXHOTLMKL75UV4"

url = f"https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds.json?api_key={READ_KEY}&results=8000"

r = requests.get(url)
data = r.json()

df = pd.DataFrame(data["feeds"])

df["created_at"] = pd.to_datetime(df["created_at"])
df["humidity"] = df["field1"].astype(float)
df["temp_dht"] = df["field2"].astype(float)
df["temp_bmp"] = df["field3"].astype(float)
df["pressure"] = df["field4"].astype(float)

df = df[["created_at","humidity","temp_dht","temp_bmp","pressure"]]

df.to_csv("climate.csv", index=False)

print(df.tail())
