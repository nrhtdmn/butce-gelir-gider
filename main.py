import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QMessageBox
import sqlite3
import datetime

# Dönüştürülmüş UI dosyalarını import edin
from Ui_main_window import Ui_MainWindow
from Ui_add_income_expense import Ui_AddIncomeExpenseDialog
from Ui_create_category import Ui_CreateCategoryDialog
from Ui_view_analysis import Ui_AnalysisDialog

# Veritabanı bağlantısı ve tablo oluşturma
def initialize_database():
    db_path = os.path.join(os.path.dirname(__file__), 'database', 'budget.db')
    if not os.path.exists(db_path):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount REAL NOT NULL,
        category TEXT NOT NULL,
        type TEXT NOT NULL,
        date TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

class BudgetTracker(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(BudgetTracker, self).__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.loadCategories()
        self.loadTransactions()
        self.add_income_expense_btn.clicked.connect(self.showAddIncomeExpenseDialog)
        self.create_category_btn.clicked.connect(self.showCreateCategoryDialog)
        self.view_analysis_btn.clicked.connect(self.showAnalysisDialog)

    def loadCategories(self):
        db_path = os.path.join(os.path.dirname(__file__), 'database', 'budget.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM categories")
        categories = cursor.fetchall()
        conn.close()

        self.categories_list.clear()
        for category in categories:
            self.categories_list.addItem(category[0])

    def loadTransactions(self):
        # İşlem yükleme mantığı
        pass

    def showAddIncomeExpenseDialog(self):
        dialog = AddIncomeExpenseDialog(self)
        dialog.exec_()
        self.loadTransactions()  # Yeni işlemleri yüklemek için

    def showCreateCategoryDialog(self):
        dialog = CreateCategoryDialog(self)
        dialog.exec_()
        self.loadCategories()

    def showAnalysisDialog(self):
        dialog = AnalysisDialog(self)
        dialog.exec_()

class AddIncomeExpenseDialog(QDialog, Ui_AddIncomeExpenseDialog):
    def __init__(self, parent=None):
        super(AddIncomeExpenseDialog, self).__init__(parent)
        self.setupUi(self)
        self.loadCategories()
        self.add_btn.clicked.connect(self.addTransaction)

    def loadCategories(self):
        db_path = os.path.join(os.path.dirname(__file__), 'database', 'budget.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM categories")
        categories = cursor.fetchall()
        conn.close()

        self.category_combobox.clear()
        for category in categories:
            self.category_combobox.addItem(category[0])

    def addTransaction(self):
        amount = self.amount_input.text()
        category = self.category_combobox.currentText()
        transaction_type = self.type_combobox.currentText()
        date = datetime.datetime.now().strftime("%Y-%m-%d")  # Anlık zaman alınıp istenen formata dönüştürülüyor
        
        if amount and category and transaction_type and date:
            db_path = os.path.join(os.path.dirname(__file__), 'database', 'budget.db')
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO transactions (amount, category, type, date) VALUES (?, ?, ?, ?)",
                           (amount, category, transaction_type, date))
            conn.commit()
            conn.close()
            self.accept()
        else:
            QMessageBox.warning(self, 'Hata', 'Tüm alanlar doldurulmalıdır!')

class CreateCategoryDialog(QDialog, Ui_CreateCategoryDialog):
    def __init__(self, parent=None):
        super(CreateCategoryDialog, self).__init__(parent)
        self.setupUi(self)
        self.add_btn.clicked.connect(self.addCategory)

    def addCategory(self):
        category_name = self.category_name_input.text()
        if category_name:
            db_path = os.path.join(os.path.dirname(__file__), 'database', 'budget.db')
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO categories (name) VALUES (?)", (category_name,))
            conn.commit()
            conn.close()
            self.accept()
        else:
            QMessageBox.warning(self, 'Hata', 'Kategori adı boş olamaz')

class AnalysisDialog(QDialog, Ui_AnalysisDialog):
    def __init__(self, parent=None):
        super(AnalysisDialog, self).__init__(parent)
        self.setupUi(self)
        self.loadAnalysis()

    def loadAnalysis(self):
        db_path = os.path.join(os.path.dirname(__file__), 'database', 'budget.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT SUM(amount) FROM transactions WHERE type = 'Gelir'")
        income = cursor.fetchone()[0] or 0
        
        cursor.execute("SELECT SUM(amount) FROM transactions WHERE type = 'Gider'")
        expense = cursor.fetchone()[0] or 0
        
        conn.close()
        
        balance = income - expense
        
        self.analysis_result.setText(f"Toplam Gelir: {income} TL\nToplam Gider: {expense} TL\nBakiye: {balance} TL")

if __name__ == "__main__":
    initialize_database()  # Veritabanını başlatma
    app = QApplication(sys.argv)
    window = BudgetTracker()
    window.show()
    sys.exit(app.exec_())
