📄 ExcelPrinter v0.3.0
¡Bienvenido a ExcelPrinter! 🖨️✨
Una herramienta multiplataforma poderosa para transformar, visualizar, imprimir y exportar archivos Excel personalizados para tu flujo de trabajo diario.

🚀 Características Principales
Funcionalidad	Descripción
📊 Estadísticas Dinámicas	Muestra estadísticas instantáneas del archivo Excel: filas, columnas, bultos, clientes únicos y fechas envío.
📁 Exportación Avanzada (CSV, PDF, XLSX)	Exporta el archivo transformado en múltiples formatos de manera sencilla.
🎨 Editor Visual de Columnas	Elimina columnas no deseadas, renombra dinámicamente y guarda configuraciones.
🔍 Búsqueda Avanzada	Busca registros específicos dentro de la vista previa (cliente, ciudad, tracking).
🌙 Modo Oscuro / Claro Toggle	Alterna entre modo claro y oscuro para mayor comodidad visual.
🖨️ Compatibilidad Multiplataforma de Impresión	Imprime en Windows (Win32) y Linux/macOS (LibreOffice + lp).
🖥️ Gestión de Modo Urbano / FedEx / Listados	Transforma y limpia automáticamente los archivos según modo seleccionado.
💾 Historial de Archivos Procesados	Guarda un registro de los últimos archivos procesados (nombre, fecha, modo usado).
📧 Envío Directo por Email (SMTP)	Envía el Excel o PDF directamente desde la app.
🔐 Gestión de Usuarios (Login Previo para Herramientas Avanzadas)	Sistema de login básico para proteger configuraciones y accesos.
⏰ Programación de Impresión Automática (Opcional)	Permite programar impresión diaria/semanal (mediante cron o tareas programadas).

📥 Instalación

1. Clonar el proyecto:
bash
Copiar código
git clone https://github.com/stredes/conversorv.0.3.0.git
cd conversorv.0.3.0

2. Crear entorno virtual:
bash
Copiar código
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

3. Instalar dependencias:
bash
Copiar código
pip install -r requirements.txt

⚙️ Uso Básico
bash
Copiar código
python main_app.py

🏷️ Modos Disponibles
Flag UI (checkbox)	Modo	Descripción
🟢 Urbano	Urbano	Lee archivos desde fila 3. Ideal para listados urbanos.
🟣 FedEx	FedEx	Limpia columnas, agrupa bultos, renombra y suma total de bultos al final según plantilla.
🔵 Listados	Listados	Limpieza general para listados personalizados.

🔥 Comandos y Funcionalidades Clave:
Comando / Botón en GUI	Descripción
Seleccionar Excel 📂	Carga archivo Excel desde tu sistema.
Configuración ⚙️	Permite seleccionar/eliminar columnas según modo actual.
Exportar PDF 📄, Exportar CSV, Exportar XLSX	Exporta el archivo transformado en el formato elegido.
Ver Logs 📋	Visualiza el historial y registros detallados de uso.
Herramientas Avanzadas 🔥	Acceso a estadísticas, editor, búsqueda, envío email, configuraciones (requiere login previo).
Imprimir	Envía el documento transformado directamente a la impresora configurada.
Modo Oscuro / Claro 🌙	Alterna entre temas visuales para la GUI.
Salir ❌	Cierra la aplicación.


✉️ Configuración SMTP para Envío de Emails
Modifica tu archivo herramientas.py:

python
Copiar código
msg['From'] = 'tuemail@dominio.com'
with smtplib.SMTP('smtp.dominio.com', 587) as server:
    server.login('tuemail@dominio.com', 'tupassword')



📜 Requisitos
Python 3.8+
tkinter, pandas, openpyxl, reportlab, smtplib
(Linux) LibreOffice + CUPS configurado
(Windows) Win32com instalado

🌎 Multiplataforma
✔️ Windows
✔️ Linux
✔️ macOS

📦 Empaquetado (Opcional)
Para distribuir como ejecutable:

bash
Copiar código
pyinstaller --onefile --noconsole main_app.py
🛡️ Licencia
MIT License

👤 Autor
Desarrollado por Stredes 🚀

