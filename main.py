import sys
import os
import traceback

# PyInstaller windowed build: redireciona stdout/stderr para arquivo de log
_log_path = os.path.join(os.path.dirname(sys.executable), 'dnd_companion.log')
if sys.stdout is None:
    sys.stdout = open(_log_path, 'w', encoding='utf-8')
if sys.stderr is None:
    sys.stderr = sys.stdout

from gui.main_window import MainWindow
from PyQt6.QtWidgets import QApplication

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("D&D 5e Character Builder")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    try:
        main()
    except Exception:
        traceback.print_exc()
        sys.stderr.flush()
