import json
import os

# Caminho absoluto, baseado na localização deste arquivo (não no
# diretório de onde o script foi chamado). Isso evita o bug clássico
# de "FileNotFoundError" quando o app é executado de outra pasta.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HISTORY_FILE = os.path.join(BASE_DIR, "history.json")


def save_analysis(data):
    """
    Adiciona um novo registro de análise ao histórico em JSON.
    Cria o arquivo automaticamente se ele ainda não existir.
    """
    if not os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "w", encoding="utf-8") as file:
            json.dump([], file)

    with open(HISTORY_FILE, "r", encoding="utf-8") as file:
        history = json.load(file)

    history.append(data)

    with open(HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(history, file, indent=4, ensure_ascii=False)


def load_history():
    """
    Retorna a lista completa de análises já registradas.
    Retorna uma lista vazia se o histórico ainda não existir.
    """
    if not os.path.exists(HISTORY_FILE):
        return []

    with open(HISTORY_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def clear_history():
    """
    Apaga permanentemente todo o histórico de análises salvo.
    """
    with open(HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump([], file)
