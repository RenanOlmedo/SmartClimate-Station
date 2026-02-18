import subprocess
import sys
import os
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def run(script):
    path = os.path.join(BASE_DIR, script)
    print(f"\nExecutando: {script}")
    subprocess.run([sys.executable, path], check=True)

print("\nSmartClimateAI – Sistema Unificado Iniciado\n")

# 1️⃣ Baixar dados do ThingSpeak
run("download.py")

# Aguarda o CSV ser atualizado
print("\nAguardando dados do ThingSpeak...")
time.sleep(5)

# 2️⃣ Dashboard Interativo
run("dashboard_interativo_final.py")

# 3️⃣ Tela Científica (IAI, ponto de orvalho, tendência)
run("tela_cientifica.py")

print("\nSistema SmartClimateAI em execução!")
