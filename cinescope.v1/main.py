import sys
import csv
import mysql.connector
from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QFileDialog
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

class MovieApp(QMainWindow):
    def __init__(self):
        super().__init__()
        loader = QUiLoader()
        ui_file = QFile("cinescope.ui")
        ui_file.open(QFile.ReadOnly)
        self.ui = loader.load(ui_file, self)
        ui_file.close()
        self.ui.loadButton.clicked.connect(self.load_movies)
        self.ui.searchButton.clicked.connect(self.search_movies)
        self.ui.exportButton.clicked.connect(self.export_csv)

    def connect_db(self):
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="cinescope"
        )

    def load_movies(self):
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT title, genre, year, rating FROM movies")
        data = cursor.fetchall()
        conn.close()
        self.display_data(data)

    def search_movies(self):
        keyword = self.ui.searchInput.text()
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT title, genre, year, rating FROM movies WHERE title LIKE %s",
            (f"%{keyword}%",)
        )
        data = cursor.fetchall()
        conn.close()
        self.display_data(data)

    def display_data(self, data):
        self.ui.tableWidget.setRowCount(len(data))
        self.ui.tableWidget.setColumnCount(4)
        for row, row_data in enumerate(data):
            for col, value in enumerate(row_data):
                self.ui.tableWidget.setItem(row, col, QTableWidgetItem(str(value)))

    def export_csv(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save CSV", "", "CSV Files (*.csv)")
        if not path:
            return
        row_count = self.ui.tableWidget.rowCount()
        col_count = self.ui.tableWidget.columnCount()
        with open(path, "w", newline="") as file:
            writer = csv.writer(file)
            for row in range(row_count):
                writer.writerow([
                    self.ui.tableWidget.item(row, col).text() if self.ui.tableWidget.item(row, col) else ""
                    for col in range(col_count)
                ])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MovieApp()
    window.show()
    sys.exit(app.exec())
