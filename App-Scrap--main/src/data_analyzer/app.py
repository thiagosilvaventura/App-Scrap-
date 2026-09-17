import toga
import os
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, BOLD, CENTER
from . import analyzerpy  # Connects to data analysis engine


class DataAnalyzerApp(toga.App):

    def startup(self):
        self.selected_files = []

        # ============================================================
        # MAIN CONTAINER (Minimalist Apple Space)
        # ============================================================
        self.main_box = toga.Box(
            style=Pack(
                direction=COLUMN,
                padding=35,
                background_color="#f5f5f7"  # Apple light gray background
            )
        )

        # ============================================================
        # 1. HEADER (Clean Typography)
        # ============================================================
        self.banner_box = toga.Box(
            style=Pack(
                direction=COLUMN,
                padding_bottom=30,
                alignment=CENTER,
                background_color="#f5f5f7"
            )
        )

        self.title_label = toga.Label(
            "APP SCRAP",
            style=Pack(
                font_weight=BOLD,
                font_size=22,
                alignment=CENTER,
                color="#1d1d1f",  # Apple dark gray text
                background_color="#f5f5f7"
            ),
        )

        self.subtitle_label = toga.Label(
            "developed by Thiago Ventura",
            style=Pack(
                font_size=10,
                alignment=CENTER,
                color="#86868b",  # Apple subtitle gray
                padding_top=4,
                background_color="#f5f5f7"
            ),
        )

        self.banner_box.add(self.title_label)
        self.banner_box.add(self.subtitle_label)

        # ============================================================
        # 2. STATUS & ACTIONS (Centered & Uniform)
        # ============================================================
        self.status_label = toga.Label(
            "No datasets selected.",
            style=Pack(
                alignment=CENTER,
                padding_bottom=15,
                font_size=11,
                color="#1d1d1f",
                background_color="#f5f5f7"
            ),
        )

        # Wrapper box to center the button nicely
        btn_choose_box = toga.Box(
            style=Pack(
                direction=ROW, 
                alignment=CENTER, 
                padding_bottom=10, 
                background_color="#f5f5f7"
            )
        )
        
        btn_choose = toga.Button(
            "Select Datasets...",
            on_press=self.action_choose_files,
            style=Pack(width=200, padding=6),
        )
        btn_choose_box.add(btn_choose)

        # Wrapper box for the run button
        btn_run_box = toga.Box(
            style=Pack(
                direction=ROW, 
                alignment=CENTER, 
                padding_bottom=25, 
                background_color="#f5f5f7"
            )
        )
        
        btn_run = toga.Button(
            "Run Analysis",
            on_press=self.action_run_analysis,
            style=Pack(width=200, padding=6),
        )
        btn_run_box.add(btn_run)

        # ============================================================
        # 3. TEXT OUTPUT CONSOLE
        # ============================================================
        self.output_multiline = toga.MultilineTextInput(
            value="Ready to process.\nWaiting for user input...",
            readonly=True,
            style=Pack(
                flex=1,
                padding=10,
                font_size=11
            ),
        )

        # ============================================================
        # ASSEMBLE LAYOUT
        # ============================================================
        self.main_box.add(self.banner_box)
        self.main_box.add(self.status_label)
        self.main_box.add(btn_choose_box)
        self.main_box.add(btn_run_box)
        self.main_box.add(self.output_multiline)

        # ============================================================
        # MAIN WINDOW
        # ============================================================
        self.main_window = toga.MainWindow(
            title="APP SCRAP",
            size=(550, 480)
        )
        
        self.main_window.content = self.main_box
        self.main_window.show()

    # ================================================================
    # FILE SELECTION
    # ================================================================
    async def action_choose_files(self, widget):
        try:
            files = await self.main_window.open_file_dialog(
                title="Select Datasets",
                multiple_select=True,
                file_types=["csv", "xls", "xlsx"],
            )

            if files:
                self.selected_files = [str(f) for f in files]
                
                self.status_label.text = (
                    f"{len(self.selected_files)} file(s) ready for analysis."
                )
                
                self.output_multiline.value = (
                    "Files loaded:\n\n"
                    + "\n".join(f" • {os.path.basename(file)}" for file in self.selected_files)
                    + "\n"
                )
            else:
                self.status_label.text = "Selection cancelled."

        except Exception as e:
            self.selected_files = []
            self.status_label.text = "Error selecting files."
            self.output_multiline.value = str(e)

    # ================================================================
    # ANALYSIS ENGINE
    # ================================================================
    def action_run_analysis(self, widget):
        if len(self.selected_files) < 2:
            self.output_multiline.value = (
                "Error: Insufficient datasets.\n"
                "Please select at least 2 files to run the correlation."
            )
            return

        self.output_multiline.value = "Analyzing datasets... Please wait.\n"

        try:
            report = analyzerpy.process_datasets(self.selected_files)
            self.output_multiline.value = f"Analysis Complete:\n\n{report}"
            
        except Exception as error:
            self.output_multiline.value = f"An error occurred:\n{str(error)}"


# ====================================================================
# APPLICATION ENTRY POINT
# ====================================================================
def main():
    return DataAnalyzerApp("APP SCRAP", "org.example.appscrap")


if __name__ == "__main__":
    main().main_loop()