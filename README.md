#  ORION Energy Monitor AI

> Sistema Inteligente de Monitoramento Energético para Missão Espacial  
> **Global Solution 2026-1 — FIAP | Ciência da Computação — Turma 1CC**

---

##  Integrante

| Nome | RM |
|------|----|
| Lucas Klein | 570029 |
| Rafael Ferreirinha | 571949 |
---

##  Objetivo

Desenvolver um sistema inteligente de monitoramento para controle operacional de uma missão espacial experimental, aplicando conceitos de **energia**, **potência**, **energias renováveis** e **sustentabilidade** na análise de dados simulados dos módulos da missão.

---

##  Sobre o Projeto

O **ORION Energy Monitor AI** é uma plataforma de monitoramento em tempo real dos sistemas energéticos de uma missão espacial. O sistema simula dados operacionais e aplica lógica de inteligência artificial para:

-  **Monitorar** temperatura, energia, comunicação e status dos módulos
-  **Gerar alertas automáticos** diante de condições críticas
-  **Tomar decisões automatizadas** para proteger a missão
-  **Visualizar** o histórico completo da telemetria com gráficos interativos

---

##  Funcionalidades

###  Monitoramento em Tempo Real
- Temperatura do casco e núcleo da nave
- Nível de energia disponível e bateria
- Geração de energia solar (renovável)
- Radiação cósmica
- Velocidade e altitude orbital
- Status de comunicação com a base terrestre
- Consumo energético dos módulos

###  Sistema de Alertas
| Nível | Condição | Ação |
|-------|----------|------|
|  CRÍTICO | Temp > 85°C | Acionar resfriamento |
|  CRÍTICO | Energia < 15% | Protocolo de emergência |
|  CRÍTICO | Comunicação OFFLINE | Antena de backup |
|  AVISO | Temp > 70°C | Monitoramento intensificado |
|  AVISO | Energia < 30% | Redução de carga |
|  CRÍTICO | Radiação > 35 µSv/h | Reforço de blindagem |

###  Tomada de Decisão Automatizada (IA)
- **Protocolo de emergência energética**: desliga automaticamente módulos não essenciais em standby quando a energia atinge nível crítico
- **Reativação inteligente**: reativa módulos quando a energia se normaliza
- **Resposta a falhas de comunicação**: ativa antena de backup e modo de armazenamento local
- **Proteção contra radiação**: reforça escudos e posiciona tripulação em área segura

###  Módulos Operacionais
-  **Propulsão** *(Essencial)*
-  **Comunicação** *(Essencial)*
-  **Suporte de Vida** *(Essencial)*
-  Navegação
-  Lab. Científico
-  Armazenamento

###  Visualizações
- Gráfico de energia disponível com limites de alerta
- Gráfico de temperatura (casco e núcleo)
- Gráfico de geração solar e nível de bateria
- Gráfico de radiação e consumo
- Log histórico de alertas
- Resumo estatístico da missão

---

##  Sustentabilidade e Energias Renováveis

O sistema monitora e prioriza o uso de **energia solar** como fonte primária (renovável), alternando para bateria e modo híbrido conforme necessário. Os conceitos aplicados incluem:

- **Eficiência energética**: desligamento automático de módulos não essenciais
- **Energia solar**: monitoramento da geração fotovoltaica dos painéis da nave
- **Gestão de carga**: balanceamento inteligente entre fontes (solar, bateria, híbrida)
- **Sustentabilidade operacional**: prolongar a vida útil da missão com uso otimizado dos recursos

---

##  Tecnologias Utilizadas

| Tecnologia | Uso |
|------------|-----|
| Python 3.10+ | Linguagem principal |
| Streamlit | Interface web interativa |
| Pandas | Manipulação de dados históricos |
| Plotly | Gráficos interativos |

---

## ▶ Como Executar

### Pré-requisitos
- Python 3.10 ou superior
- pip

### Instalação

```bash
# Clone o repositório
git clone https://github.com/lucas123045/suntentavelOFC
cd suntentavelOFC

# Instale as dependências
pip install -r requirements.txt

# Execute a aplicação
streamlit run app.py
```

A aplicação abrirá automaticamente em `http://localhost:8501`

---

##  Como Usar

1. **Acesse o painel** após executar o comando acima
2. Clique em **" Atualizar Leitura"** para simular uma nova leitura de dados
3. Ative **"Atualização Automática"** na barra lateral para modo contínuo
4. Use os **Cenários de Teste** para simular situações críticas:
   - *Falha energética crítica*
   - *Tempestade de radiação*
   - *Perda de comunicação*
   - *Múltiplas falhas*
5. **Controle os módulos** individualmente na barra lateral
6. Analise os **gráficos de telemetria** nas 4 abas disponíveis
7. Acompanhe o **Log de Ocorrências** e o **Resumo Estatístico**

---

##  Estrutura do Projeto

```
orion-energy-monitor/
├── app.py              # Aplicação principal
├── requirements.txt    # Dependências
└── README.md           # Este arquivo
```

---

##  Critérios Atendidos

| Critério | Implementação |
|----------|---------------|
|  Monitoramento de dados simulados | 12 variáveis monitoradas em tempo real |
|  Geração de alertas | 8 tipos de alerta com 3 níveis de severidade |
|  Tomada de decisão básica | 6 respostas automatizadas por tipo de falha |
|  Visualização dos dados | 4 gráficos interativos + métricas + log |
|  Organização do código | Funções modulares e comentadas |
|  Aplicação de IA introdutória | Motor de decisão por regras com estado |
|  Energias renováveis | Monitoramento de geração solar e gestão de carga |

---

*FIAP — Faculdade de Informática e Administração Paulista*  
*Global Solution 2026-1 | Soluções em Energias Renováveis e Sustentáveis*
