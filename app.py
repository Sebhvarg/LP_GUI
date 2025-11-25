from PySide6.QtWidgets import (
    QApplication, QWidget, QPushButton, QTextEdit, QVBoxLayout, QLabel
)
import sys

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Analizador de Lenguajes")

        # ----- Widgets -----
        self.label = QLabel("Ingresa tu código:")
        self.text_input = QTextEdit()

        self.button = QPushButton("Analizar")
        self.button.clicked.connect(self.on_analyze)

        self.output = QTextEdit()
        self.output.setReadOnly(True)

        # ----- Layout -----
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.text_input)
        layout.addWidget(self.button)
        layout.addWidget(self.output)

        self.setLayout(layout)

    # ----- Acción del botón -----
    def on_analyze(self):
        texto = self.text_input.toPlainText()
        self.output.setText(f"Procesando...\n\n{texto}")

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(500, 600)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
