import sys
from PySide6.QtWidgets import QApplication
from UIFormula import Form

if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    form = Form()
    availableGeometry = form.screen().availableGeometry()
    form.resize(availableGeometry.width()*2/3, availableGeometry.height()*2/3)
    form.setWindowTitle("i-Formula")
    form.show()
    # Run the main Qt loop
    sys.exit(app.exec())
