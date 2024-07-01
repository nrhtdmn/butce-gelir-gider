import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QMessageBox,uic
from PyQt5.uic import loadUi
import sqlite3
import datetime

class BudgetTracker(QMainWindow):
    def __init__(self):
        super(BudgetTracker, self).__init__()
        loadUi('ui/main_window.ui', self)
        self.initUI()

    def initUI(self):
        self.loadCategories()
        self.loadTransactions()
        self.add_income_expense_btn.clicked.connect(self.showAddIncomeExpenseDialog)
        self.create_category_btn.clicked.connect(self.showCreateCategoryDialog)
        self.view_analysis_btn.clicked.connect(self.showAnalysisDialog)

    def loadCategories(self):
        conn = sqlite3.connect('database/budget.db')
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

    def showCreateCategoryDialog(self):
        dialog = CreateCategoryDialog(self)
        dialog.exec_()
        self.loadCategories()

    def showAnalysisDialog(self):
        dialog = AnalysisDialog(self)
        dialog.exec_()

class AddIncomeExpenseDialog(QDialog):
    def __init__(self, parent=None):
        super(AddIncomeExpenseDialog, self).__init__(parent)
        loadUi('ui/add_income_expense.ui', self)
        self.add_btn.clicked.connect(self.addTransaction)

    def addTransaction(self):
        # İşlem ekleme mantığı
        pass

class CreateCategoryDialog(QDialog):
    def __init__(self, parent=None):
        super(CreateCategoryDialog, self).__init__(parent)
        loadUi('ui/create_category.ui', self)
        self.add_btn.clicked.connect(self.addCategory)

    def addCategory(self):
        category_name = self.category_name_input.text()
        if category_name:
            conn = sqlite3.connect('database/budget.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO categories (name) VALUES (?)", (category_name,))
            conn.commit()
            conn.close()
            self.accept()
        else:
            QMessageBox.warning(self, 'Hata', 'Kategori adı boş olamaz')

class AnalysisDialog(QDialog):
    def __init__(self, parent=None):
        super(AnalysisDialog, self).__init__(parent)
        loadUi('ui/view_analysis.ui', self)
        self.loadAnalysis()

    def loadAnalysis(self):
        # Analiz ve grafik oluşturma mantığı
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BudgetTracker()
    window.show()
    sys.exit(app.exec_())
