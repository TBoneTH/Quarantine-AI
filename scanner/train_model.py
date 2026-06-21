import os

import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split

RANDOM_SEED = 42
SAMPLES_PER_CLASS = 500

MODEL_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "model")
MODEL_PATH = os.path.join(MODEL_DIR, "quarantine_model.pkl")

FEATURE_NAMES = ["extension_risk", "entropy", "mismatch", "size_mb"]
CLASS_LABELS = ["Seguro", "Suspeito", "Perigoso"]


def generate_synthetic_dataset(samples_per_class=SAMPLES_PER_CLASS, seed=RANDOM_SEED):
    """
    Gera exemplos sintéticos rotulados para as três classes de risco.

    Cada exemplo tem 4 features, na mesma ordem usada pelo app real:
    [extension_risk, entropy, mismatch, size_mb]

    As distribuições de cada classe se sobrepõem nas bordas de
    propósito — um arquivo .zip legítimo pode ter entropia alta sem
    ser malicioso, por exemplo, então o modelo precisa aprender
    padrões, não só decorar limiares fixos.
    """
    rng = np.random.default_rng(seed)

    X = []
    y = []

    # --- Classe: Seguro ---
    for _ in range(samples_per_class):
        extension_risk = rng.uniform(0, 8)
        entropy = float(np.clip(rng.normal(3.2, 1.0), 0, 8))
        mismatch = 1 if rng.random() < 0.02 else 0
        size_mb = float(abs(rng.lognormal(mean=1.0, sigma=1.2)))
        X.append([extension_risk, entropy, mismatch, size_mb])
        y.append("Seguro")

    # --- Classe: Suspeito ---
    for _ in range(samples_per_class):
        extension_risk = rng.uniform(5, 28)
        entropy = float(np.clip(rng.normal(5.5, 1.1), 0, 8))
        mismatch = 1 if rng.random() < 0.18 else 0
        size_mb = float(abs(rng.lognormal(mean=0.8, sigma=1.3)))
        X.append([extension_risk, entropy, mismatch, size_mb])
        y.append("Suspeito")

    # --- Classe: Perigoso ---
    for _ in range(samples_per_class):
        extension_risk = rng.uniform(18, 40)
        entropy = float(np.clip(rng.normal(7.0, 0.9), 0, 8))
        mismatch = 1 if rng.random() < 0.5 else 0
        size_mb = float(abs(rng.lognormal(mean=0.3, sigma=1.5)))
        X.append([extension_risk, entropy, mismatch, size_mb])
        y.append("Perigoso")

    X = np.array(X)
    y = np.array(y)

    # Embaralha pra não deixar os exemplos agrupados por classe
    indices = rng.permutation(len(X))
    return X[indices], y[indices]


def train_and_evaluate(
    model_path=None, samples_per_class=SAMPLES_PER_CLASS, save=True, verbose=True
):
    """
    Treina o RandomForestClassifier, avalia num conjunto de teste
    separado e (opcionalmente) salva o modelo treinado em disco.

    Parâmetros pensados pra permitir testes automatizados isolados:
    - model_path: caminho customizado pra salvar o modelo (útil em
      testes, pra não sobrescrever o modelo "de produção")
    - samples_per_class: dataset menor deixa os testes mais rápidos
    - save: permite treinar sem persistir nada em disco

    Retorna (modelo_treinado, acuracia_no_teste)
    """
    X, y = generate_synthetic_dataset(samples_per_class=samples_per_class)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_SEED, stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=150,
        max_depth=8,
        random_state=RANDOM_SEED,
    )
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)

    if verbose:
        print("=== Avaliação do modelo (conjunto de teste sintético) ===")
        print(f"Acurácia: {accuracy:.2%}\n")
        print(classification_report(y_test, predictions))

    if save:
        target_path = model_path or MODEL_PATH
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        joblib.dump(model, target_path)
        if verbose:
            print(f"Modelo salvo em: {target_path}")

    return model, accuracy


if __name__ == "__main__":
    train_and_evaluate()
