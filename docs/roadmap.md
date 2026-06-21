# Roadmap

## ✅ Implementado

- [x] Seleção de arquivo via interface gráfica (customtkinter)
- [x] Cálculo de hash SHA-256
- [x] Identificação de tipo de arquivo por extensão
- [x] Análise de entropia de Shannon (detecção de compactação/ofuscação)
- [x] Verificação de assinatura binária (magic bytes) vs. extensão declarada
- [x] Motor de pontuação de risco combinando os três sinais acima
- [x] Classificador de Machine Learning (RandomForest, scikit-learn)
- [x] Histórico de análises (JSON) com tela dedicada na interface
- [x] Suíte de testes automatizados (pytest)

## 🚧 Planejado

- [ ] Exportação de relatório individual em PDF
- [ ] Tela de progresso/etapas durante a análise (UX mais próxima do
      pré-projeto acadêmico original)
- [ ] Configuração de pesos do score via arquivo externo (JSON/YAML),
      em vez de valores fixos no código
- [ ] Re-treinar o modelo de ML com dados reais (ex: hashes
      consultados via API pública de reputação de arquivos), em vez do
      dataset sintético atual
- [ ] CI no GitHub Actions rodando a suíte de testes a cada push
- [ ] Extensão de navegador para analisar downloads automaticamente
      (visão original do pré-projeto acadêmico)

## ❌ Fora de escopo (por design)

- Execução real de arquivos suspeitos em sandbox/VM. O projeto opera
  inteiramente por **análise estática** (hash, entropia, assinatura
  binária), sem nunca rodar o conteúdo do arquivo analisado. Essa é
  uma decisão de segurança consciente: executar arquivos
  potencialmente maliciosos exigiria isolamento via VM/Docker que
  foge do escopo de um projeto de portfólio.
