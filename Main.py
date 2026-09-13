
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, BOLD


class DataAnalyzerApp(toga.App):

    def startup(self):
        # Lista para armazenar os caminhos dos arquivos selecionados
        self.selected_files = []

        # 1. Container Principal (Layout em Coluna)
        main_box = toga.Box(style=Pack(direction=COLUMN, padding=20))

        # 2. Cabeçalho
        title_label = toga.Label(
            "📊 Data Analyzer Pro",
            style=Pack(font_weight=BOLD, font_size=18, padding_bottom=5),
        )

        subtitle_label = toga.Label(
            "Select CSV, XLS, or XLSX files to analyze",
            style=Pack(font_size=10, padding_bottom=15),
        )

        # 3. Label de Status da Seleção
        self.status_label = toga.Label(
            "No files selected.",
            style=Pack(padding_bottom=10),
        )

        # 4. Botões de Ação
        btn_choose = toga.Button(
            "📁 Choose Files",
            on_press=self.action_choose_files,
            style=Pack(padding=5),
        )

        btn_run = toga.Button(
            "▶️ Run Analysis",
            on_press=self.action_run_analysis,
            style=Pack(padding=5),
        )

        # 5. Área de Saída (Log / Relatório estilo Terminal)
        self.output_multiline = toga.MultilineTextInput(
            value="Waiting for files...\n",
            readonly=True,
            style=Pack(flex=1, padding_top=15, font_family="monospace"),
        )

        # Adiciona os elementos ao container principal
        main_box.add(title_label)
        main_box.add(subtitle_label)
        main_box.add(btn_choose)
        main_box.add(self.status_label)
        main_box.add(btn_run)
        main_box.add(self.output_multiline)

        # Janela Principal
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

    # Evento: Selecionar Arquivos Nativamente
    async def action_choose_files(self, widget):
        try:
            files = await self.main_window.open_file_dialog(
                title="Select Data Files",
                multiple_select=True,
                file_types=["csv", "xls", "xlsx"],
            )

            if files:
                self.selected_files = [str(f) for f in files]
                self.status_label.text = f"✅ {len(self.selected_files)} file(s) selected."
            else:
                self.selected_files = []
                self.status_label.text = "❌ Selection cancelled."
        except Exception as e:
            self.selected_files = []
            self.status_label.text = f"Error selecting files: {e}"

    # Evento: Rodar Análise
    def action_run_analysis(self, widget):
        if len(self.selected_files) < 2:
            self.output_multiline.value = (
                "Error: Please select at least 2 files to cross-reference.\n"
            )
            return

        self.output_multiline.value = "Reading and processing files... Please wait.\n"

        try:
            # Ponto de conexão futuro com o analisador.py
            report = (
                "=== ANALYSIS REPORT ===\n\n"
                f"Ready to process {len(self.selected_files)} selected database(s)!\n\n"
                "(The engine analisador.py will be connected in the next step)."
            )
            self.output_multiline.value = report
        except Exception as error:
            self.output_multiline.value = f"An error occurred:\n{str(error)}"


def main():
    return DataAnalyzerApp("Data Analyzer Pro", "org.example.dataanalyzer")


if __name__ == "__main__":
    main().main_loop()
