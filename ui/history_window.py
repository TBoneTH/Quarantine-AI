import customtkinter as ctk
from tkinter import messagebox

from database.history_manager import load_history, clear_history
from ui.history_formatting import get_classification_color, format_entry_details


class HistoryWindow(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)

        self.title("Histórico de Análises - Quarantine AI")
        self.geometry("650x520")

        self.header_label = ctk.CTkLabel(
            self,
            text="Histórico de Análises",
            font=("Arial", 20, "bold"),
        )
        self.header_label.pack(pady=(20, 5))

        self.subtitle_label = ctk.CTkLabel(
            self,
            text="Análises mais recentes aparecem primeiro",
            font=("Arial", 12),
            text_color="gray",
        )
        self.subtitle_label.pack(pady=(0, 10))

        self.scroll_frame = ctk.CTkScrollableFrame(self, width=600, height=350)
        self.scroll_frame.pack(padx=20, pady=10, fill="both", expand=True)

        button_row = ctk.CTkFrame(self, fg_color="transparent")
        button_row.pack(pady=15)

        self.refresh_button = ctk.CTkButton(
            button_row, text="🔄 Atualizar", command=self.load_entries, width=140
        )
        self.refresh_button.pack(side="left", padx=8)

        self.clear_button = ctk.CTkButton(
            button_row,
            text="🗑 Limpar Histórico",
            command=self.confirm_clear_history,
            width=160,
            fg_color="#E74C3C",
            hover_color="#C0392B",
        )
        self.clear_button.pack(side="left", padx=8)

        self.load_entries()

    def load_entries(self):
        """Recarrega a lista de análises a partir do JSON salvo."""
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        history = load_history()

        if not history:
            empty_label = ctk.CTkLabel(
                self.scroll_frame,
                text="Nenhuma análise registrada ainda.\n"
                     "Selecione um arquivo na tela inicial pra começar.",
                font=("Arial", 13),
                text_color="gray",
            )
            empty_label.pack(pady=30)
            return

        # Mostra do mais recente para o mais antigo
        for record in reversed(history):
            self._add_entry_row(record)

    def _add_entry_row(self, record):
        classificacao = record.get("classificacao", "Indefinido")
        color = get_classification_color(classificacao)

        row = ctk.CTkFrame(self.scroll_frame)
        row.pack(fill="x", pady=4, padx=4)

        info_frame = ctk.CTkFrame(row, fg_color="transparent")
        info_frame.pack(side="left", fill="x", expand=True, padx=10, pady=8)

        name_label = ctk.CTkLabel(
            info_frame,
            text=record.get("arquivo", "Arquivo desconhecido"),
            font=("Arial", 13, "bold"),
            anchor="w",
        )
        name_label.pack(anchor="w")

        detail_label = ctk.CTkLabel(
            info_frame,
            text=format_entry_details(record),
            font=("Arial", 11),
            text_color="gray",
            anchor="w",
        )
        detail_label.pack(anchor="w")

        status_label = ctk.CTkLabel(
            row,
            text=f"{classificacao}\n{record.get('score', 0)} pts",
            font=("Arial", 13, "bold"),
            text_color=color,
            justify="right",
        )
        status_label.pack(side="right", padx=15)

    def confirm_clear_history(self):
        """Pede confirmação antes de apagar o histórico permanentemente."""
        confirmed = messagebox.askyesno(
            "Limpar Histórico",
            "Tem certeza que deseja apagar todo o histórico de análises?\n"
            "Essa ação não pode ser desfeita.",
        )
        if confirmed:
            clear_history()
            self.load_entries()
