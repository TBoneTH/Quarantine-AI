EXTENSION_RISK_TABLE = {
    ".exe": 30,
    ".msi": 25,
    ".bat": 40,
    ".cmd": 40,
    ".ps1": 40,
    ".vbs": 40,
    ".scr": 35,

    ".html": 5,
    ".js": 15,

    ".zip": 10,
    ".rar": 10,
    ".7z": 10,

    ".docm": 20,
    ".xlsm": 20,
    ".pptm": 20,

    ".txt": 0,
    ".pdf": 0,
    ".docx": 0,
    ".xlsx": 0,
    ".pptx": 0,
    ".jpg": 0,
    ".jpeg": 0,
    ".png": 0,
    ".gif": 0,
    ".mp4": 0,
    ".mp3": 0,
}

# Pontos somados quando a extensão declarada não bate com o tipo
# real detectado pela assinatura binária do arquivo.
MISMATCH_PENALTY = 35


def calculate_score(extension, entropy_points=0, mismatch=False):
    """
    Calcula o score final de risco e a classificação textual.

    Parâmetros:
    - extension: extensão declarada do arquivo (ex: ".exe")
    - entropy_points: pontos vindos da análise de entropia
      (ver scanner.entropy_scanner.classify_entropy)
    - mismatch: True se a extensão não bate com a assinatura real
      do arquivo (ver scanner.signature_scanner.check_extension_mismatch)

    Retorna (score: int, classificacao: str)
    """
    extension = extension.lower()

    score = EXTENSION_RISK_TABLE.get(extension, 0)
    score += entropy_points

    if mismatch:
        score += MISMATCH_PENALTY

    # Limita o score a 100 pontos
    score = min(score, 100)

    if score >= 40:
        classification = "Perigoso"
    elif score >= 20:
        classification = "Suspeito"
    else:
        classification = "Seguro"

    return score, classification
