from scanner.score_engine import calculate_score


def test_safe_extension_with_no_extra_risk_is_seguro():
    score, classification = calculate_score(".pdf")

    assert score == 0
    assert classification == "Seguro"


def test_exe_extension_alone_is_suspeito():
    # .exe sozinho vale 30 pontos -> ainda não chega em "Perigoso" (40+)
    score, classification = calculate_score(".exe")

    assert score == 30
    assert classification == "Suspeito"


def test_bat_extension_alone_is_perigoso():
    # .bat vale 40 pontos -> já cruza o limiar de "Perigoso"
    score, classification = calculate_score(".bat")

    assert score == 40
    assert classification == "Perigoso"


def test_entropy_points_increase_score():
    score, classification = calculate_score(".zip", entropy_points=25)

    # .zip vale 10 + entropia "Muito Alta" vale 25 = 35
    assert score == 35
    assert classification == "Suspeito"


def test_mismatch_alone_pushes_safe_extension_to_suspeito():
    # Um .txt comum (0 pontos) com extensão divergente já vira Suspeito
    # (35 pontos), mas sozinho ainda não cruza o limiar de Perigoso (40)
    score, classification = calculate_score(".txt", mismatch=True)

    assert score == 35
    assert classification == "Suspeito"


def test_combined_signals_reach_perigoso():
    score, classification = calculate_score(
        ".txt", entropy_points=10, mismatch=True
    )

    assert score == 45
    assert classification == "Perigoso"


def test_score_is_capped_at_100():
    score, classification = calculate_score(
        ".bat", entropy_points=25, mismatch=True
    )

    # 40 + 25 + 35 = 100 exatamente, mas testamos o teto de qualquer forma
    assert score == 100
    assert classification == "Perigoso"


def test_unknown_extension_defaults_to_zero_base_score():
    score, classification = calculate_score(".xyz123")

    assert score == 0
    assert classification == "Seguro"


def test_extension_is_case_insensitive():
    score_lower, _ = calculate_score(".exe")
    score_upper, _ = calculate_score(".EXE")

    assert score_lower == score_upper
