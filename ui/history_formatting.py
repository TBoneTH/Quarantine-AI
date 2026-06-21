CLASSIFICATION_COLORS = {
    "Seguro": "#2ECC71",
    "Suspeito": "#F39C12",
    "Perigoso": "#E74C3C",
}

DEFAULT_COLOR = "#AAAAAA"


def get_classification_color(classificacao):
    """Retorna a cor hexadecimal associada a uma classificação de risco."""
    return CLASSIFICATION_COLORS.get(classificacao, DEFAULT_COLOR)


def format_entry_summary(record):
    """
    Monta a linha de resumo textual de um registro do histórico.
    Usado tanto para exibição quanto para futura exportação em texto.
    """
    arquivo = record.get("arquivo", "Arquivo desconhecido")
    classificacao = record.get("classificacao", "Indefinido")
    score = record.get("score", 0)
    data_hora = record.get("data_hora", "data não registrada")

    return f"{arquivo}  |  {classificacao} ({score} pts)  |  {data_hora}"


def format_entry_details(record):
    """
    Monta a linha de detalhes secundários (data, entropia, IA, alerta
    de assinatura divergente) exibida abaixo do nome do arquivo.
    """
    detail_text = (
        f"{record.get('data_hora', 'data não registrada')}  •  "
        f"Entropia: {record.get('entropia', '-')}"
    )

    ai_classification = record.get("classificacao_ia")
    if ai_classification:
        detail_text += f"  •  IA: {ai_classification}"

    if record.get("assinatura_divergente"):
        detail_text += "  •  ⚠ Assinatura divergente"

    return detail_text
