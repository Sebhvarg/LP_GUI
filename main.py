import sys
import os
import io
import datetime
import subprocess
from contextlib import redirect_stdout
from PySide6.QtWidgets import (
    QApplication, QWidget, QPushButton, QPlainTextEdit, QVBoxLayout, QHBoxLayout, 
    QLabel, QListWidget, QInputDialog, QMessageBox, QFileDialog, QSplitter, QTextEdit
)
from PySide6.QtGui import QIcon, QFont, QColor, QPalette, QPainter, QTextFormat
from PySide6.QtCore import Qt, QRect, QSize

sys.path.append(os.path.abspath("Analizadores"))

# Función para obtener la ruta correcta de los recursos y construir la ruta completa
def resource_path(relative_path):
    
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def get_git_user():
    try:
        result = subprocess.run(['git', 'config', 'user.name'], capture_output=True, text=True)
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
        else:
            return "unknown_user"
    except Exception:
        return "unknown_user"

def generate_log(type_name, content, filename):
    usuario_git = get_git_user()
    fecha_hora = datetime.datetime.now().strftime("%d-%m-%Y-%Hh%M")
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    
    # Limpiar nombre del tipo para el archivo (quitar acentos si es necesario, aunque el sistema de archivos moderno suele aguantar)
    # Pero para seguir el formato pedido: semántico -> semantico
    type_clean = type_name.lower().replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')
    
    log_file_path = os.path.join(log_dir, f"{type_clean}-{usuario_git}-{fecha_hora}.txt")
    
    with open(log_file_path, 'a', encoding='utf-8') as log_file:
        # Primera línea con usuario y archivo
        log_file.write(f"Usuario: {usuario_git} | Archivo: {filename}\n")
        log_file.write(content + "\n")

try:
    import Analizadores.Lexicon.lexer as lex_module
    import Analizadores.Syntax.syntax as syn_module
    import Analizadores.Semantic.semantic as sem_module
except ImportError as e:
    print(f"Error importando módulos: {e}")

# --- Clase para el área de números de línea ---
class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.codeEditor = editor

    def sizeHint(self):
        return QSize(self.codeEditor.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        self.codeEditor.lineNumberAreaPaintEvent(event)

# --- Editor de código con números de línea ---
class CodeEditor(QPlainTextEdit):
    def __init__(self):
        super().__init__()
        self.lineNumberArea = LineNumberArea(self)

        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)

        self.updateLineNumberAreaWidth(0)
        self.highlightCurrentLine()

    def lineNumberAreaWidth(self):
        digits = 1
        max_value = max(1, self.blockCount())
        while max_value >= 10:
            max_value //= 10
            digits += 1
        
        space = 3 + self.fontMetrics().horizontalAdvance('9') * digits
        return space

    def updateLineNumberAreaWidth(self, _):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def updateLineNumberArea(self, rect, dy):
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height())

        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height()))

    def lineNumberAreaPaintEvent(self, event):
        painter = QPainter(self.lineNumberArea)
        painter.fillRect(event.rect(), QColor(40, 40, 40))  # Fondo oscuro para números

        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(blockNumber + 1)
                painter.setPen(QColor(150, 150, 150)) # Color de los números
                painter.setFont(self.font())
                painter.drawText(0, int(top), self.lineNumberArea.width(), self.fontMetrics().height(),
                                 Qt.AlignRight, number)

            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            blockNumber += 1

    def highlightCurrentLine(self):
        extraSelections = []

        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            lineColor = QColor(60, 60, 60) # Color de la línea actual
            selection.format.setBackground(lineColor)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extraSelections.append(selection)

        self.setExtraSelections(extraSelections)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ARust - Analizador de código Rust")
        self.setWindowIcon(QIcon(resource_path("assets/img/logo.png")))
        self.resize(1200, 800)
        
        # Configuración del tema
        self.setup_theme()

        # Layout principal
        main_layout = QHBoxLayout()
        
        # --- Panel de archivos ---
        left_layout = QVBoxLayout()
        
        self.file_list_label = QLabel("Archivos Rust (.rs)")
        self.file_list_label.setFont(QFont("Arial", 12, QFont.Bold))
        
        self.file_list = QListWidget()
        self.file_list.itemClicked.connect(self.load_file_content)
        
        self.btn_create_file = QPushButton("Crear Archivo")
        self.btn_create_file.clicked.connect(self.create_file)
        
        self.btn_delete_file = QPushButton("Eliminar Archivo")
        self.btn_delete_file.clicked.connect(self.delete_file)
        
        self.btn_refresh_files = QPushButton("Recargar Lista")
        self.btn_refresh_files.clicked.connect(self.refresh_file_list)

        left_layout.addWidget(self.file_list_label)
        left_layout.addWidget(self.file_list)
        left_layout.addWidget(self.btn_create_file)
        left_layout.addWidget(self.btn_delete_file)
        left_layout.addWidget(self.btn_refresh_files)
        
        left_widget = QWidget()
        left_widget.setLayout(left_layout)
        left_widget.setMaximumWidth(250)

        # --- Panel central ---
        center_splitter = QSplitter(Qt.Vertical)
        
        # Editor
        editor_widget = QWidget()
        editor_layout = QVBoxLayout()
        self.editor_label = QLabel("Editor de Código")
        self.editor_label.setFont(QFont("Arial", 12, QFont.Bold))
        
        # Usamos el nuevo CodeEditor
        self.text_input = CodeEditor()
        self.text_input.setFont(QFont("Consolas", 11))
        self.text_input.setPlaceholderText("Escribe tu código Rust aquí...")
        
        self.btn_save_file = QPushButton("Guardar Cambios")
        self.btn_save_file.clicked.connect(self.save_file)
        
        editor_layout.addWidget(self.editor_label)
        editor_layout.addWidget(self.text_input)
        editor_layout.addWidget(self.btn_save_file)
        editor_widget.setLayout(editor_layout)
        
        # Errors
        error_widget = QWidget()
        error_layout = QVBoxLayout()
        self.error_label = QLabel("Errores / Consola")
        self.error_label.setFont(QFont("Arial", 10, QFont.Bold))
        self.error_output = QTextEdit()
        self.error_output.setReadOnly(True)
        self.error_output.setMaximumHeight(150)
        self.error_output.setStyleSheet("color: #ff5555; background-color: #1e1e1e;") 
        
        error_layout.addWidget(self.error_label)
        error_layout.addWidget(self.error_output)
        error_widget.setLayout(error_layout)
        
        center_splitter.addWidget(editor_widget)
        center_splitter.addWidget(error_widget)
        center_splitter.setStretchFactor(0, 4)
        center_splitter.setStretchFactor(1, 1)

        # --- Panel derecho botones de análisis y Resultados ---
        right_layout = QVBoxLayout()
        
        self.analysis_label = QLabel("Herramientas de Análisis")
        self.analysis_label.setFont(QFont("Arial", 12, QFont.Bold))
        
        self.btn_lexico = QPushButton("Análisis Léxico")
        self.btn_lexico.clicked.connect(lambda: self.run_analysis("Léxico"))
        
        self.btn_sintactico = QPushButton("Análisis Sintáctico")
        self.btn_sintactico.clicked.connect(lambda: self.run_analysis("Sintáctico"))
        
        self.btn_semantico = QPushButton("Análisis Semántico")
        self.btn_semantico.clicked.connect(lambda: self.run_analysis("Semántico"))
        
        self.btn_todos = QPushButton("Analizar todo")
        self.btn_todos.clicked.connect(lambda: self.run_analysis("Todos"))
        
        self.output_label = QLabel("Resultado del Análisis")
        self.output_area = QTextEdit()
        self.output_area.setReadOnly(True)
        self.output_area.setFont(QFont("Consolas", 10))
        
        right_layout.addWidget(self.analysis_label)
        right_layout.addWidget(self.btn_lexico)
        right_layout.addWidget(self.btn_sintactico)
        right_layout.addWidget(self.btn_semantico)
        right_layout.addWidget(self.btn_todos)
        right_layout.addSpacing(20)
        right_layout.addWidget(self.output_label)
        right_layout.addWidget(self.output_area)
        
        right_widget = QWidget()
        right_widget.setLayout(right_layout)
        right_widget.setMaximumWidth(300)

        
        main_layout.addWidget(left_widget)
        main_layout.addWidget(center_splitter)
        main_layout.addWidget(right_widget)

        self.setLayout(main_layout)
        
        # Inicialización
        self.ensure_rust_dir()
        self.refresh_file_list()
        self.current_file = None

    def setup_theme(self):
        # Tema oscuro
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ToolTipBase, Qt.white)
        palette.setColor(QPalette.ToolTipText, Qt.white)
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.BrightText, Qt.red)
        palette.setColor(QPalette.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.HighlightedText, Qt.black)
        self.setPalette(palette)
        
        # Hojas de estilo adicionales
        self.setStyleSheet("""
            QToolTip { 
                color: #ffffff; 
                background-color: #2a82da; 
                border: 1px solid white; 
            }
            QPushButton {
                background-color: #2b2b2b;
                border: 1px solid #3c3c3c;
                padding: 5px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #3c3c3c;
            }
            QPushButton:pressed {
                background-color: #505050;
            }
            QListWidget {
                background-color: #1e1e1e;
                border: 1px solid #3c3c3c;
                color: #d4d4d4;
            }
            QPlainTextEdit, QTextEdit {
                background-color: #1e1e1e;
                border: 1px solid #3c3c3c;
                color: #d4d4d4;
            }
        """)

    def ensure_rust_dir(self):
        if not os.path.exists("rust_files"):
            os.makedirs("rust_files")

    def refresh_file_list(self):
        self.file_list.clear()
        if os.path.exists("rust_files"):
            files = [f for f in os.listdir("rust_files") if f.endswith(".rs")]
            self.file_list.addItems(files)

    def create_file(self):
        name, ok = QInputDialog.getText(self, "Crear Archivo", "Nombre del archivo (sin .rs):")
        if ok and name:
            if not name.endswith(".rs"):
                name += ".rs"
            path = os.path.join("rust_files", name)
            if os.path.exists(path):
                QMessageBox.warning(self, "Error", "El archivo ya existe.")
            else:
                with open(path, "w") as f:
                    f.write("// Archivo Rust nuevo\nfn main() {\n    println!(\"Hola Mundo\");\n}")
                self.refresh_file_list()

    def delete_file(self):
        item = self.file_list.currentItem()
        if item:
            name = item.text()
            reply = QMessageBox.question(self, "Confirmar", f"¿Eliminar {name}?", QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                os.remove(os.path.join("rust_files", name))
                self.refresh_file_list()
                self.text_input.clear()
                self.current_file = None

    def load_file_content(self, item):
        name = item.text()
        self.current_file = name
        path = os.path.join("rust_files", name)
        if os.path.exists(path):
            with open(path, "r") as f:
                content = f.read()
            self.text_input.setPlainText(content)
            self.error_output.clear()
            self.output_area.clear()

    def save_file(self):
        if self.current_file:
            path = os.path.join("rust_files", self.current_file)
            content = self.text_input.toPlainText()
            with open(path, "w") as f:
                f.write(content)
            self.error_output.setText(f"Guardado: {self.current_file}")
        else:
            QMessageBox.warning(self, "Aviso", "Selecciona o crea un archivo primero.")

    def run_analysis(self, type_name):
        code = self.text_input.toPlainText()
        if not code.strip():
            self.error_output.setText("Error: El editor está vacío.")
            return

        self.output_area.clear()
        self.error_output.clear()
        
        # Nombre del archivo actual para el log
        current_filename = self.current_file if self.current_file else "sin_titulo.rs"
        
        # Captura de salida global para la GUI
        global_output = io.StringIO()
        
        try:
            # Flags
            run_lexico = type_name == "Léxico" or type_name == "Todos"
            run_sintactico = type_name == "Sintáctico" or type_name == "Todos"
            run_semantico = type_name == "Semántico" or type_name == "Todos"

            if run_lexico:
                lex_output = io.StringIO()
                with redirect_stdout(lex_output):
                    if type_name == "Todos":
                        print("=== ANÁLISIS LÉXICO ===")
                    # Resetear lexer
                    lex_module.lexer.lineno = 1
                    lex_module.lexer.input(code)
                    while True:
                        tok = lex_module.lexer.token()
                        if not tok:
                            break
                        print(f"Línea {tok.lineno}: {tok.type} -> {tok.value}")
                    if type_name == "Todos":
                        print("\n")
                
                # Escribir a salida global y generar log
                lex_content = lex_output.getvalue()
                global_output.write(lex_content)
                generate_log("Léxico", lex_content, current_filename)
                    
            if run_sintactico:
                syn_output = io.StringIO()
                with redirect_stdout(syn_output):
                    if type_name == "Todos":
                        print("=== ANÁLISIS SINTÁCTICO ===")
                    # Resetear mensajes
                    syn_module.mensajes.clear()
                    # Resetear lexer
                    lex_module.lexer.lineno = 1
                    syn_module.parser.parse(code, lexer=lex_module.lexer)
                    if not syn_module.mensajes:
                        print("Análisis sintáctico completado sin errores.")
                    else:
                        for msg in syn_module.mensajes:
                            print(msg)
                    if type_name == "Todos":
                        print("\n")
                
                # Escribir a salida global y generar log
                syn_content = syn_output.getvalue()
                global_output.write(syn_content)
                generate_log("Sintáctico", syn_content, current_filename)
                        
            if run_semantico:
                sem_output = io.StringIO()
                with redirect_stdout(sem_output):
                    if type_name == "Todos":
                        print("=== ANÁLISIS SEMÁNTICO ===")
                    
                    sem_module.mensajes.clear()
                    # Resetear tabla de símbolos
                    sem_module.tabla_simbolos["variables"] = {}
                    sem_module.tabla_simbolos["funciones"] = {}
                    
                    # Resetear lexer
                    lex_module.lexer.lineno = 1
                    sem_module.parser.parse(code, lexer=lex_module.lexer)
                    
                    if not sem_module.mensajes:
                        print("Análisis semántico completado.")
                        
                        print("\n=== TABLA DE SÍMBOLOS ===")
                        print("\n--- Variables ---")
                        for var, info in sem_module.tabla_simbolos["variables"].items():
                            if isinstance(info, dict):
                                tipo = info.get("tipo", "unknown")
                                const = "const" if info.get("const") else ("mut" if info.get("mutable") else "let")
                                usado = "✓" if info.get("usado") else "✗ (no usada)"
                                print(f"  {var}: {const} {tipo} - Usado: {usado}")
                            else:
                                print(f"  {var}: {info}")
                        
                        print("\n--- Funciones ---")
                        for func, info in sem_module.tabla_simbolos["funciones"].items():
                            retorno = info.get("retorno", "void")
                            params = len(info.get("params", []))
                            print(f"  {func}({params} params) -> {retorno}")
                            
                        # Advertencias
                        print("\n--- Advertencias ---")
                        for var, info in sem_module.tabla_simbolos["variables"].items():
                            if isinstance(info, dict) and not info.get("usado", False):
                                print(f"Advertencia: Variable '{var}' declarada pero no usada.")
                    else:
                        for msg in sem_module.mensajes:
                            print(msg)
                
                # Escribir a salida global y generar log
                sem_content = sem_output.getvalue()
                global_output.write(sem_content)
                generate_log("Semántico", sem_content, current_filename)

            output = global_output.getvalue()
            self.output_area.setText(output)
            
            # Verificar errores en la salida para actualizar la consola de errores
            if "Error" in output or "error" in output:
                 self.error_output.setText("Se encontraron errores. Ver detalles en el panel de resultados.")
                 # Extraer líneas con Error
                 errors = [line for line in output.split('\n') if "Error" in line or "error" in line]
                 self.error_output.setText("\n".join(errors))
            else:
                 self.error_output.setText("Análisis finalizado sin errores críticos.")

        except Exception as e:
            self.error_output.setText(f"Excepción durante el análisis: {str(e)}")
            self.output_area.setText(global_output.getvalue())

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
