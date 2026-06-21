import os

import joblib
import numpy as np

MODEL_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "model", "quarantine_model.pkl"
)

FEATURE_NAMES = ["extension_risk", "entropy", "mismatch", "size_mb"]


def build_feature_vector(extension_risk, entropy, mismatch, size_mb):
    """
    Monta o vetor de features na ordem esperada pelo modelo.
    Função pura, sem dependência do modelo carregado — fácil de testar.
    """
    return np.array(
        [
            [
                float(extension_risk),
                float(entropy),
                1.0 if mismatch else 0.0,
                float(size_mb),
            ]
        ]
    )


def load_model():
    """
    Carrega o modelo treinado do disco.

    Levanta FileNotFoundError com uma mensagem clara se o modelo
    ainda não foi treinado.
    """
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            "Modelo de IA não encontrado em scanner/model/. "
            "Rode 'python scanner/train_model.py' para treiná-lo antes "
            "de usar o classificador."
        )
    return joblib.load(MODEL_PATH)


def predict_classification(extension_risk, entropy, mismatch, size_mb, model=None):
    """
    Usa o modelo treinado para prever a classificação de risco e a
    probabilidade (confiança) associada a cada classe possível.

    Parâmetro `model` opcional: permite injetar um modelo já
    carregado (ou um modelo de teste), evitando ler o disco de novo
    a cada chamada — também facilita testes automatizados.

    Retorna (classificacao_prevista: str, probabilidades: dict)
    """
    if model is None:
        model = load_model()

    features = build_feature_vector(extension_risk, entropy, mismatch, size_mb)

    prediction = str(model.predict(features)[0])
    probabilities = model.predict_proba(features)[0]

    prob_dict = {
        str(classe): round(float(prob), 3)
        for classe, prob in zip(model.classes_, probabilities)
    }

    return prediction, prob_dict
