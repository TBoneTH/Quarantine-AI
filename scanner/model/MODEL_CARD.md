# Model Card — Quarantine AI Classifier

## O que é

Um `RandomForestClassifier` (scikit-learn) treinado para classificar
arquivos em **Seguro**, **Suspeito** ou **Perigoso**, complementando o
motor de regras determinístico (`scanner/score_engine.py`).

## Features usadas

| Feature           | Descrição                                                          |
|--------------------|---------------------------------------------------------------------|
| `extension_risk`  | Pontuação de risco da extensão do arquivo (tabela fixa)            |
| `entropy`         | Entropia de Shannon do conteúdo (0 a 8 bits/byte)                  |
| `mismatch`        | 1 se a extensão declarada diverge da assinatura binária real, 0 c.c.|
| `size_mb`         | Tamanho do arquivo em megabytes                                    |

## Dados de treino

⚠️ **Dataset sintético**, gerado por `scanner/train_model.py`
(`generate_synthetic_dataset`). Não usamos malware real — os exemplos
são amostrados de distribuições estatísticas plausíveis para cada
classe, com sobreposição proposital nas bordas (uma boa parte dos
"Suspeitos" se parece estatisticamente com "Perigosos", por exemplo),
pra evitar um problema trivialmente separável.

Isso significa que o modelo aprende um **padrão estatístico
plausível**, não o comportamento real de malware. Pra evoluir o
projeto de forma honesta, o próximo passo seria treinar com exemplos
reais rotulados (ex: hashes consultados em APIs públicas de reputação
de arquivos).

## Desempenho (no conjunto de teste sintético)

- Acurácia: **95%**
- F1-score por classe: Seguro 0.99 · Suspeito 0.92 · Perigoso 0.94

(Reproduzível rodando `python scanner/train_model.py` — usa
`random_state` fixo.)

## Limitações conhecidas

- O modelo nunca viu um arquivo real, só vetores numéricos sintéticos.
- Não captura nenhum comportamento dinâmico (rede, processos, registro
  do sistema) — só características estáticas do arquivo.
- Pode performar mal em combinações de features fora da distribuição
  sintética usada no treino (ex: arquivos muito grandes, > algumas
  centenas de MB).
- Não deve ser tratado como veredito definitivo — está integrado na
  interface lado a lado com a classificação por regras, exatamente
  para deixar claro que são dois métodos diferentes e nenhum dos dois
  é infalível.
