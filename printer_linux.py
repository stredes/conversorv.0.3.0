import os
import platform
import subprocess
from pathlib import Path
from datetime import datetime
from tkinter import messagebox

def print_document_linux(temp_excel_path):
    try:
        if platform.system().lower() != "linux":
            messagebox.showerror("Error", "Este método solo es compatible con Linux.")
            return

        output_dir = Path(temp_excel_path).parent
        pdf_output = output_dir / f"converted_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

        # Convertir Excel a PDF usando LibreOffice
        convert_cmd = [
            "libreoffice",
            "--headless",
            "--convert-to", "pdf",
            "--outdir", str(output_dir),
            str(temp_excel_path)
        ]
        result = subprocess.run(convert_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if result.returncode != 0:
            raise Exception(f"Error al convertir a PDF:\n{result.stderr.decode()}")

        # Imprimir usando lp
        print_cmd = ["lp", str(pdf_output)]
        subprocess.run(print_cmd)

        messagebox.showinfo("Impresión", f"PDF enviado a imprimir: {pdf_output.name}")

    except Exception as e:
        messagebox.showerror("Error", f"Error impresión Linux:\n{e}")
