import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import pandas as pd
import logging
from pathlib import Path
from datetime import datetime
import tempfile

from config_dialog import ConfigDialog
from excel_processor import validate_file, load_excel, apply_transformation
from printer import export_to_pdf, print_document
from utils import load_config, LOG_FILE

try:
    from sqlalchemy import create_engine
except ImportError:
    create_engine = None

class ExcelPrinterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Transformador Excel - Dashboard")
        self.geometry("1000x600")
        self.configure(bg="#F9FAFB")

        self.df = None
        self.transformed_df = None
        self.sheet = None
        self.mode = "listados"
        self.processing = False
        self.mode_vars = {
            "urbano": tk.BooleanVar(value=False),
            "fedex": tk.BooleanVar(value=False),
            "listados": tk.BooleanVar(value=True)
        }
        self.config_columns = load_config()

        self._setup_styles()
        self._setup_sidebar()
        self._setup_main_area()
        self._setup_status_bar()

    def _setup_styles(self):
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure("TButton", font=("Segoe UI", 11), padding=8)
        style.configure("TLabel", font=("Segoe UI", 11))
        style.configure("TCheckbutton", font=("Segoe UI", 11))

    def _setup_sidebar(self):
        sidebar = tk.Frame(self, bg="#111827", width=200)
        sidebar.pack(side="left", fill="y")

        tk.Label(sidebar, text="Menú", bg="#111827", fg="white",
                 font=("Segoe UI", 14, "bold")).pack(pady=20)

        ttk.Button(sidebar, text="Seleccionar Excel 📂", command=self._threaded_select_file).pack(pady=10, fill="x", padx=10)
        ttk.Button(sidebar, text="Configuración ⚙️", command=self._open_config_menu).pack(pady=10, fill="x", padx=10)
        ttk.Button(sidebar, text="Exportar PDF 📄", command=lambda: export_to_pdf(self.transformed_df, self)).pack(pady=10, fill="x", padx=10)
        ttk.Button(sidebar, text="Ver Logs 📋", command=self.view_logs).pack(pady=10, fill="x", padx=10)
        ttk.Button(sidebar, text="Salir ❌", command=self.quit).pack(side="bottom", pady=20, fill="x", padx=10)

    def _setup_main_area(self):
        self.main_frame = tk.Frame(self, bg="#F9FAFB")
        self.main_frame.pack(side="left", fill="both", expand=True)

        tk.Label(self.main_frame, text="Transformador Excel",
                 bg="#F9FAFB", fg="#111827", font=("Segoe UI", 18, "bold")).pack(pady=20)

        # Modo de operación
        mode_frame = ttk.LabelFrame(self.main_frame, text="Modo de Operación", padding=15)
        mode_frame.pack(pady=10)

        for m in self.mode_vars:
            ttk.Checkbutton(mode_frame, text=m.capitalize(),
                            variable=self.mode_vars[m],
                            command=lambda m=m: self._update_mode(m)).pack(side=tk.LEFT, padx=10)

    def _setup_status_bar(self):
        self.status_var = tk.StringVar()
        status_bar = ttk.Label(self, textvariable=self.status_var,
                               relief=tk.SUNKEN, anchor=tk.W, padding=5)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def _update_status(self, message):
        self.status_var.set(message)
        self.update_idletasks()
    def _update_mode(self, selected_mode: str):
        if self.mode_vars[selected_mode].get():
            for mode in self.mode_vars:
                if mode != selected_mode:
                    self.mode_vars[mode].set(False)
            self.mode = selected_mode
        else:
            if not any(var.get() for var in self.mode_vars.values()):
                self.mode_vars["listados"].set(True)
                self.mode = "listados"

    def _threaded_select_file(self):
        if self.processing:
            return
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
        if file_path and validate_file(file_path):
            self.processing = True
            threading.Thread(target=self._process_file, args=(file_path,), daemon=True).start()

    def _process_file(self, file_path: str):
        self._update_status("Procesando archivo...")
        try:
            df = load_excel(file_path)
            self.df = df
            self.transformed_df = apply_transformation(self.df, self.config_columns, self.mode)

            # Cargar hoja en Excel (para impresión)
            from win32com.client import Dispatch
            excel = Dispatch("Excel.Application")
            excel.Visible = False
            wb = excel.Workbooks.Open(str(Path(file_path).resolve()))
            self.sheet = wb.ActiveSheet

            # Mostrar vista previa elegante
            self.after(0, self._show_preview)

        except Exception as exc:
            messagebox.showerror("Error", f"Error al leer el archivo:\n{exc}")
            logging.error(f"Error: {exc}")
        finally:
            self.processing = False
            self._update_status("Listo")

    def _show_preview(self):
        if self.transformed_df is None or self.transformed_df.empty:
            messagebox.showerror("Error", "No hay datos para mostrar.")
            return

        preview_win = tk.Toplevel(self)
        preview_win.title("Vista Previa")
        preview_win.geometry("950x600")
        preview_win.configure(bg="#F9FAFB")

        tree_frame = ttk.Frame(preview_win, padding=10)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        columns = list(self.transformed_df.columns)
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120, minwidth=80, anchor=tk.CENTER)

        rows_per_page = 100
        total_rows = len(self.transformed_df)
        current_offset = 0

        def load_page(offset):
            for item in tree.get_children():
                tree.delete(item)
            page = self.transformed_df.iloc[offset:offset + rows_per_page]
            for row in page.itertuples(index=False):
                tree.insert("", "end", values=row)
            page_label.config(text=f"Filas {offset + 1}-{min(offset + rows_per_page, total_rows)} de {total_rows}")

        nav_frame = ttk.Frame(preview_win, padding=10)
        nav_frame.pack()

        btn_prev = ttk.Button(nav_frame, text="Anterior", state=tk.DISABLED)
        btn_prev.pack(side=tk.LEFT, padx=5)
        page_label = ttk.Label(nav_frame, text="")
        page_label.pack(side=tk.LEFT, padx=5)
        btn_next = ttk.Button(nav_frame, text="Siguiente")
        btn_next.pack(side=tk.LEFT, padx=5)

        def next_page():
            nonlocal current_offset
            if current_offset + rows_per_page < total_rows:
                current_offset += rows_per_page
                load_page(current_offset)
                btn_prev.config(state=tk.NORMAL)
            if current_offset + rows_per_page >= total_rows:
                btn_next.config(state=tk.DISABLED)

        def prev_page():
            nonlocal current_offset
            if current_offset - rows_per_page >= 0:
                current_offset -= rows_per_page
                load_page(current_offset)
                btn_next.config(state=tk.NORMAL)
            if current_offset == 0:
                btn_prev.config(state=tk.DISABLED)

        btn_next.config(command=next_page)
        btn_prev.config(command=prev_page)

        btn_frame = ttk.Frame(preview_win, padding=10)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Imprimir", command=lambda: self._threaded_print()).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cerrar", command=preview_win.destroy).pack(side=tk.LEFT, padx=5)

        load_page(current_offset)
    def _threaded_print(self):
        if self.processing or self.sheet is None:
            messagebox.showerror("Error", "Primero debe cargar un archivo Excel válido.")
            return
        threading.Thread(target=self._print_document, daemon=True).start()

    def _print_document(self):
        try:
            if self.transformed_df is None or self.transformed_df.empty:
                messagebox.showerror("Error", "No hay datos para imprimir.")
                return

            # Guardar temporalmente el archivo editado
            temp_path = Path(tempfile.gettempdir()) / f"excel_editado_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            self.transformed_df.to_excel(temp_path, index=False)

            # Abrir con win32com
            from win32com.client import Dispatch
            excel = Dispatch("Excel.Application")
            excel.Visible = False
            wb = excel.Workbooks.Open(str(temp_path.resolve()))
            sheet = wb.ActiveSheet

            from printer import print_document
            print_document(sheet, self.mode, self.config_columns, self.transformed_df)

            messagebox.showinfo("Impresión", "El documento editado se ha enviado a imprimir.")

            wb.Close(SaveChanges=False)
            excel.Quit()

        except Exception as e:
            messagebox.showerror("Error", f"Error al imprimir:\n{e}")

    def _open_config_menu(self):
        if self.df is None:
            messagebox.showerror("Error", "Primero cargue un archivo Excel.")
            return
        self.open_config_dialog(self.mode)

    def open_config_dialog(self, mode: str):
        dialog = ConfigDialog(self, mode, list(self.df.columns), self.config_columns)
        self.wait_window(dialog)
        self.transformed_df = apply_transformation(self.df, self.config_columns, self.mode)

    def view_logs(self):
        if not LOG_FILE.exists():
            messagebox.showinfo("Logs", "No hay logs para mostrar.")
            return
        log_win = tk.Toplevel(self)
        log_win.title("Logs de la Aplicación")
        log_win.geometry("600x400")
        txt = tk.Text(log_win)
        txt.pack(fill=tk.BOTH, expand=True)
        with LOG_FILE.open("r", encoding="utf-8", errors="replace") as f:
            txt.insert(tk.END, f.read())

    def connect_to_db(self):
        if create_engine is None:
            messagebox.showerror("Error", "SQLAlchemy no está instalado.")
            return
        try:
            engine = create_engine("sqlite:///:memory:")
            connection = engine.connect()
            messagebox.showinfo("Conexión a BD", "Conexión exitosa a la base de datos SQLite.")
            logging.info("Conexión a BD exitosa.")
            connection.close()
        except Exception as e:
            messagebox.showerror("Error", f"Error al conectar a la BD:\n{e}")

if __name__ == "__main__":
    app = ExcelPrinterApp()
    app.mainloop()

