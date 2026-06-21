import numpy as np

from scanner.ml_classifier import build_feature_vector, predict_classification
from scanner.train_model import generate_synthetic_dataset, train_and_evaluate


def test_build_feature_vector_shape_and_values():
    features = build_feature_vector(
        extension_risk=30, entropy=7.2, mismatch=True, size_mb=1.5
    )

    assert features.shape == (1, 4)
    assert list(features[0]) == [30.0, 7.2, 1.0, 1.5]


def test_build_feature_vector_mismatch_false_is_zero():
    features = build_feature_vector(
        extension_risk=0, entropy=1.0, mismatch=False, size_mb=0.1
    )

    assert features[0][2] == 0.0


def test_generate_synthetic_dataset_shapes():
    X, y = generate_synthetic_dataset(samples_per_class=20, seed=1)

    assert X.shape == (60, 4)
    assert y.shape == (60,)
    assert set(y) == {"Seguro", "Suspeito", "Perigoso"}


def test_generate_synthetic_dataset_is_reproducible_with_seed():
    X1, y1 = generate_synthetic_dataset(samples_per_class=10, seed=7)
    X2, y2 = generate_synthetic_dataset(samples_per_class=10, seed=7)

    assert np.allclose(X1, X2)
    assert list(y1) == list(y2)


def test_generate_synthetic_dataset_features_stay_in_plausible_ranges():
    X, _ = generate_synthetic_dataset(samples_per_class=200, seed=3)

    extension_risk, entropy, mismatch, size_mb = X[:, 0], X[:, 1], X[:, 2], X[:, 3]

    assert extension_risk.min() >= 0
    assert entropy.min() >= 0 and entropy.max() <= 8
    assert set(np.unique(mismatch)).issubset({0.0, 1.0})
    assert size_mb.min() >= 0


def test_train_and_evaluate_reaches_reasonable_accuracy(tmp_path):
    model_path = tmp_path / "modelo_teste.pkl"

    model, accuracy = train_and_evaluate(
        model_path=str(model_path),
        samples_per_class=80,
        save=True,
        verbose=False,
    )

    assert model_path.exists()
    # As classes têm sobreposição proposital, então não esperamos
    # 100%, mas um classificador minimamente útil deve passar de 70%
    assert accuracy > 0.70


def test_train_and_evaluate_without_save_does_not_create_file(tmp_path):
    model_path = tmp_path / "nao_deveria_existir.pkl"

    train_and_evaluate(
        model_path=str(model_path),
        samples_per_class=50,
        save=False,
        verbose=False,
    )

    assert not model_path.exists()


def test_predict_classification_returns_native_python_types():
    model, _ = train_and_evaluate(samples_per_class=80, save=False, verbose=False)

    prediction, probabilities = predict_classification(
        extension_risk=10, entropy=4.0, mismatch=False, size_mb=1.0, model=model
    )

    # Garante tipos nativos (não np.str_/np.float64), pra serialização
    # em JSON funcionar de forma previsível em qualquer contexto
    assert type(prediction) is str
    assert all(type(key) is str for key in probabilities)
    assert all(type(value) is float for value in probabilities.values())


def test_predict_classification_returns_valid_label_and_probabilities():
    model, _ = train_and_evaluate(samples_per_class=80, save=False, verbose=False)

    prediction, probabilities = predict_classification(
        extension_risk=35, entropy=7.5, mismatch=True, size_mb=0.5, model=model
    )

    assert prediction in {"Seguro", "Suspeito", "Perigoso"}
    assert set(probabilities.keys()) == {"Seguro", "Suspeito", "Perigoso"}
    assert abs(sum(probabilities.values()) - 1.0) < 0.01


def test_predict_classification_safe_looking_file_leans_seguro():
    model, _ = train_and_evaluate(samples_per_class=200, save=False, verbose=False)

    # Vetor bem característico de "Seguro": baixo risco de extensão,
    # entropia normal, sem mismatch, tamanho moderado
    prediction, _ = predict_classification(
        extension_risk=0, entropy=3.0, mismatch=False, size_mb=2.0, model=model
    )

    assert prediction == "Seguro"


def test_predict_classification_dangerous_looking_file_leans_perigoso():
    model, _ = train_and_evaluate(samples_per_class=200, save=False, verbose=False)

    # Vetor bem característico de "Perigoso": alto risco de extensão,
    # entropia muito alta, com mismatch de assinatura
    prediction, _ = predict_classification(
        extension_risk=38, entropy=7.8, mismatch=True, size_mb=0.2, model=model
    )

    assert prediction == "Perigoso"
