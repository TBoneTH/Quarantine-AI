import math
from collections import Counter

# Lê só os primeiros 1 MB por padrão: suficiente pra ter uma amostra
# estatisticamente relevante sem precisar carregar arquivos grandes
# inteiros na memória.
DEFAULT_SAMPLE_SIZE = 1024 * 1024


def calculate_entropy(filepath, sample_size=DEFAULT_SAMPLE_SIZE):
    """
    Calcula a entropia de Shannon (em bits por byte) de uma amostra
    do arquivo. Retorna um valor entre 0.0 e 8.0.
    """
    try:
        with open(filepath, "rb") as file:
            data = file.read(sample_size)
    except (OSError, IOError):
        return 0.0

    if not data:
        return 0.0

    byte_counts = Counter(data)
    total_bytes = len(data)
    entropy = 0.0

    for count in byte_counts.values():
        probability = count / total_bytes
        entropy -= probability * math.log2(probability)

    return round(entropy, 2)


def classify_entropy(entropy):
    """
    Traduz o valor numérico de entropia em uma categoria de risco
    e um valor de pontos a somar no score final.

    Retorna (nivel: str, pontos: int)
    """
    if entropy >= 7.5:
        return "Muito Alta", 25
    elif entropy >= 6.5:
        return "Alta", 10
    elif entropy >= 4.0:
        return "Normal", 0
    else:
        return "Baixa", 0
