import customtkinter as ctk
from tkinter import filedialog
from datetime import datetime

from scanner.file_scanner import get_file_info
from scanner.hash_scanner import calculate_sha256
from scanner.score_engine import calculate_score, EXTENSION_RISK_TABLE
from scanner.file_types import get_file_type
from scanner.entropy_scanner import calculate_entropy, classify_entropy
from scanner.signature_scanner import check_extension_mismatch
from scanner.ml_classifier import predict_classification
from database.history_manager import save_analysis
from ui.history_window import HistoryWindow


class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Quarantine AI")
        self.geometry("700x560")

        # Titulo
        self.title_label = ctk.CTkLabel(
            self,
            text="Quarantine AI",
            font=("Arial", 28, "bold")
        )
        self.title_label.pack(pady=20)

        # Descrição
        self.description = ctk.CTkLabel(
            self,
            text="Análise de arquivos suspeitos",
            font=("Arial", 14)
        )
        self.description.pack()

        # Botão selecionar arquivo
        self.select_button = ctk.CTkButton(
            self,
            text="Selecionar Arquivo",
            command=self.select_file
        )
        self.select_button.pack(pady=(30, 10))

        # Botão ver histórico
        self.history_button = ctk.CTkButton(
            self,
            text="📜 Ver Histórico",
            command=self.open_history,
            fg_color="transparent",
            border_width=1,
            width=160,
        )
        self.history_button.pack(pady=(0, 20))

        # Informações de arquivos
        self.file_label = ctk.CTkLabel(
            self,
            text="Nenhum arquivo selecionado",
            justify="left",
            anchor="w",
            font=("Consolas", 13)
        )
        self.file_label.pack(padx=20)

    def select_file(self):
        filepath = filedialog.askopenfilename()

        if not filepath:
            return

        info = get_file_info(filepath)
        sha256 = calculate_sha256(filepath)
        file_type = get_file_type(info["extension"])

        # --- Análise de entropia ---
        entropy = calculate_entropy(filepath)
        entropy_level, entropy_points = classify_entropy(entropy)

        # --- Verificação de assinatura (extensão real x declarada) ---
        mismatch, real_type = check_extension_mismatch(
            filepath, info["extension"]
        )

        # --- Score final combinando os três sinais (motor de regras) ---
        score, classification = calculate_score(
            info["extension"],
            entropy_points=entropy_points,
            mismatch=mismatch,
        )

        # --- Classificação por IA (modelo treinado, scikit-learn) ---
        extension_risk = EXTENSION_RISK_TABLE.get(info["extension"].lower(), 0)
        try:
            ai_classification, ai_probabilities = predict_classification(
                extension_risk, entropy, mismatch, info["size_mb"]
            )
            ai_confidence = ai_probabilities.get(ai_classification, 0) * 100
        except FileNotFoundError:
            ai_classification = None
            ai_confidence = 0

        save_analysis({
            "arquivo": info["filename"],
            "tipo": file_type,
            "extensao": info["extension"],
            "tamanho_mb": info["size_mb"],
            "sha256": sha256,
            "entropia": entropy,
            "nivel_entropia": entropy_level,
            "assinatura_divergente": mismatch,
            "tipo_real_detectado": real_type,
            "score": score,
            "classificacao": classification,
            "classificacao_ia": ai_classification,
            "confianca_ia": round(ai_confidence, 1),
            "data_hora": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        })

        mismatch_line = ""
        if mismatch:
            mismatch_line = (
                f"\n⚠ Extensão suspeita! Conteúdo real detectado: "
                f"{real_type}"
            )

        if ai_classification:
            ai_line = (
                f"\nIA (modelo treinado): {ai_classification} "
                f"({ai_confidence:.0f}% confiança)"
            )
        else:
            ai_line = (
                "\nIA: modelo não treinado ainda "
                "(rode scanner/train_model.py)"
            )

        self.file_label.configure(
            text=(
                f"Arquivo: {info['filename']}\n\n"
                f"Tipo: {file_type}\n"
                f"Extensão: {info['extension']}\n"
                f"Tamanho: {info['size_mb']} MB\n\n"
                f"SHA256:\n{sha256[:16]}...\n\n"
                f"Entropia: {entropy} ({entropy_level})\n"
                f"{mismatch_line}\n"
                f"Score (regras): {score}\n"
                f"Classificação (regras): {classification}\n"
                f"{ai_line}"
            )
        )

    def open_history(self):
        """Abre a tela de histórico de análises numa janela separada."""
        HistoryWindow(self)
