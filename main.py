import sys

from PyQt6.QtWidgets import QApplication

from MainWindow import MainWindow


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    result = app.exec()

    if result == 100:  # Custom restart code
        main()  # Call main again to restart
    else:
        sys.exit(result)


if __name__ == "__main__":
    main()
