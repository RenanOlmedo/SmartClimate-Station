🧠🌦️ SmartClimateAI — CHANGELOG
v2.0 — Atmospheric Intelligence Upgrade

Data: 2026-02-18

Esta versão marca a transição do SmartClimateAI de um painel meteorológico para um sistema de análise atmosférica científica em tempo real.

🚀 O que foi adicionado
1️⃣ Arquitetura em Múltiplos Módulos

O projeto agora está dividido em quatro sistemas independentes, aumentando confiabilidade, escalabilidade e clareza de desenvolvimento.

Módulo	Função
download.py	Baixa e atualiza dados do ThingSpeak
dashboard_interativo_final.py	Gera o painel interativo com previsão e histórico
tela_cientifica.py	Gera o painel científico de instabilidade atmosférica
main.py	Orquestra tudo automaticamente

O sistema agora roda com:

main.py → download.py → (delay) → dashboards

🌩️ 2️⃣ Novo Modelo Físico: Índice de Instabilidade Atmosférica (IAI)

Foi criado um índice baseado em meteorologia real, usando apenas sensores locais:

Variável	Função
Temperatura	Energia térmica disponível
Umidade	Conteúdo de vapor d’água
Pressão	Movimento vertical do ar
Tendência da pressão	Aproximação de sistemas instáveis
Ponto de orvalho	Saturação do ar
🔬 O IAI representa

A energia da atmosfera para formar nuvens, chuva e tempestades.

Não é um chute — é baseado em física atmosférica.

🌡️ 3️⃣ Ponto de Orvalho Integrado

O sistema agora calcula o ponto de orvalho a partir de:

Temperatura

Umidade

Isso permite medir:

“O quão perto o ar está de virar nuvem ou chuva”

📉 4️⃣ Tendência de Pressão Atmosférica

O sistema agora analisa variação da pressão no tempo, permitindo detectar:

Aproximação de frentes

Formação de nuvens

Queda de estabilidade

🧪 5️⃣ Tela Científica Profissional

Foi criada uma nova interface:

tela_cientifica.py

Ela mostra:

Índice IAI (gauge)

Temperatura

Umidade

Pressão

Ponto de orvalho

Tendência de pressão

Estado atmosférico (Estável / Atenção / Instável / Tempestade)

Em layout 1x2:

Gauge

Dados físicos lado a lado

Isso transforma o projeto em um instrumento científico de monitoramento do clima local.

📊 6️⃣ Painel Digital Mantido e Integrado

O painel interativo existente:

Continua intacto

Continua com Prophet e previsões

Agora usa os dados atualizados pelo sistema unificado

Nada foi quebrado — só expandido.

🧠 7️⃣ SmartClimateAI agora prevê formação de nuvens antes da chuva

O sistema agora detecta:

Sinal físico	Interpretação
Pressão caindo	Ar subindo
Umidade subindo	Saturação
Temperatura caindo	Condensação
Ponto de orvalho se aproximando	Nuvens se formando

O IAI sobe antes da chuva cair, exatamente como meteorologia profissional.