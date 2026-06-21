# 🛡️ Quarantine AI

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Tests](https://img.shields.io/badge/tests-50%20passing-brightgreen)

Aplicativo desktop em Python que analisa arquivos suspeitos **antes**
de você abri-los, combinando heurísticas clássicas de segurança com
um classificador de Machine Learning treinado.

> Projeto nascido a partir de um pré-projeto acadêmico (Análise e
> Desenvolvimento de Sistemas) e evoluído individualmente como projeto
> de portfólio. A versão acadêmica original descrevia uma arquitetura
> web (React/Node/PostgreSQL) com sandbox de execução real — este
> repositório é uma implementação desktop, com escopo conscientemente
> reduzido para **análise estática** (sem executar arquivos). Veja a
> seção [Decisões de Projeto](#-decisões-de-projeto) pra entender o porquê.

<!--
📸 Adicione aqui um screenshot ou GIF do app rodando!
Exemplo: ![Demo](assets/demo.gif)
-->

##  Funcionalidades

- **Hash SHA-256** de qualquer arquivo selecionado
- **Análise de entropia de Shannon** — detecta indícios de
  compactação, criptografia ou ofuscação (técnica comum em malware)
- **Verificação de assinatura binária (magic bytes)** — flagra
  arquivos com extensão disfarçada (ex: um `.exe` renomeado para `.txt`)
- **Motor de pontuação por regras**, combinando os três sinais acima
  numa classificação: `Seguro` / `Suspeito` / `Perigoso`
- **Classificador de Machine Learning** (RandomForest, scikit-learn),
  treinado de forma independente do motor de regras e exibido lado a
  lado — pra deixar claro que são dois métodos diferentes
- **Histórico de análises**, com tela dedicada, cor por classificação
  e opção de limpar o histórico
- **Suíte de testes automatizados** (pytest), incluindo testes que
  rodam sem precisar de interface gráfica instalada

##  Como funciona

```
Arquivo selecionado
        │
        ├──► Hash SHA-256
        ├──► Tipo/extensão
        ├──► Entropia de Shannon ───────┐
        ├──► Assinatura binária (magic) ┤
        │                               ▼
        │                    Motor de regras (score 0-100)
        │                               │
        └──► Features numéricas ──► Modelo de IA (RandomForest)
                                         │
                                         ▼
                    Classificação por regras + Classificação por IA
                         exibidas lado a lado na interface
```

O motor de regras e o classificador de IA são **independentes** e
podem discordar entre si — isso é intencional. Veja o
[Model Card](scanner/model/MODEL_CARD.md) pra entender exatamente como
o modelo foi treinado, com quais dados e quais as limitações dele.

##  Tecnologias

- Python 3.10+
- [customtkinter](https://github.com/TomSchimansky/CustomTkinter) — interface gráfica
- [scikit-learn](https://scikit-learn.org/) — classificador de Machine Learning
- [pytest](https://pytest.org/) — testes automatizados

##  Estrutura do projeto

```
QUARANTINE_PROTOTIPO/
├── app.py                      # ponto de entrada do aplicativo
├── ui/
│   ├── main_window.py          # tela principal
│   ├── history_window.py       # tela de histórico
│   └── history_formatting.py   # formatação (sem dependência de GUI)
├── scanner/
│   ├── file_scanner.py         # metadados básicos do arquivo
│   ├── hash_scanner.py         # cálculo de SHA-256
│   ├── entropy_scanner.py      # entropia de Shannon
│   ├── signature_scanner.py    # verificação de magic bytes
│   ├── score_engine.py         # motor de pontuação por regras
│   ├── ml_classifier.py        # carrega e usa o modelo treinado
│   ├── train_model.py          # script de treino do modelo
│   └── model/
│       ├── quarantine_model.pkl  # modelo já treinado
│       └── MODEL_CARD.md         # documentação do modelo
├── database/
│   └── history_manager.py      # persistência do histórico (JSON)
├── tests/                      # suíte de testes (pytest)
├── docs/
│   └── roadmap.md
├── requirements.txt
└── LICENSE
```

##  Instalação e uso

```bash
# Clone o repositório
git clone https://github.com/TBoneTH/Quarantine-AI
cd QUARANTINE_PROTOTIPO

# Instale as dependências
pip install -r requirements.txt

# Rode o aplicativo
python app.py
```

O modelo de IA já vem treinado e versionado no repositório
(`scanner/model/quarantine_model.pkl`), então o app funciona direto
após a instalação. Se quiser re-treinar com outros parâmetros:

```bash
python scanner/train_model.py
```

### Rodando os testes

```bash
pytest -v
```

São 50 testes cobrindo os módulos de análise (entropia, assinatura,
score, histórico) e o pipeline de Machine Learning (geração de
dataset, treino, predição).

##  Decisões de projeto

- **Sem execução real de arquivos.** O app nunca abre ou executa o
  conteúdo do arquivo analisado — toda a análise é estática (hash,
  entropia, cabeçalho binário). Um sandbox de execução real exigiria
  isolamento via VM/Docker, fora do escopo deste projeto de portfólio.
- **Modelo de IA treinado com dados sintéticos.** Não existe, aqui,
  uma base real de malware rotulada. O classificador foi treinado com
  exemplos gerados estatisticamente (com sobreposição proposital entre
  classes), documentado em detalhe no
  [Model Card](scanner/model/MODEL_CARD.md). Trocar por dados reais é
  o próximo passo natural de evolução.
- **Diferente da arquitetura do pré-projeto acadêmico original**
  (React/Node/PostgreSQL + sandbox). Esta implementação prioriza algo
  que funciona de ponta a ponta, com testes e um pipeline de ML real,
  em vez de uma stack maior só no papel.

##  Roadmap

Veja [docs/roadmap.md](docs/roadmap.md) para o que já foi feito e o
que está planejado.

##  Licença

Distribuído sob a licença MIT. Veja [LICENSE](LICENSE) para mais detalhes.

##  Origem acadêmica

Este projeto nasceu como pré-projeto de sistemas para a disciplina de
Interface e Jornada do Usuário, desenvolvido originalmente em grupo.
A implementação neste repositório é uma evolução individual, para
fins de portfólio.
