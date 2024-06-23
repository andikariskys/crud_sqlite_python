import sqlite3
from PyQt5.QtWidgets import QMainWindow, QGridLayout, QApplication, QLabel, QLineEdit, QPushButton, QMessageBox, QWidget, QTableView, QHeaderView
from PyQt5.QtGui import QStandardItemModel, QStandardItem

class MainApplication(QMainWindow):
    def __init__(self):
        super().__init__()
        # Membuat tata letak menggunakan Grid Layout
        layout = QGridLayout()

        # Formulir Daftar Menu
        # keterangan: addWidget(widget, row , column, row span, col span)
        layout.addWidget(QLabel("Daftar Menu"), 0 , 0, 1, 4)

        self.input_id_menu = QLineEdit()
        layout.addWidget(QLabel("ID Menu"), 1 , 0,)
        layout.addWidget(self.input_id_menu, 1 , 1, 1, 3)

        self.input_nama_menu = QLineEdit()
        layout.addWidget(QLabel("Nama Menu"), 2 , 0)
        layout.addWidget(self.input_nama_menu, 2 , 1, 1, 3)
        
        self.input_harga_menu = QLineEdit()
        layout.addWidget(QLabel("Harga Menu"), 3 , 0)
        layout.addWidget(self.input_harga_menu, 3 , 1, 1, 3)

        self.button_create_menu = QPushButton("Create")
        layout.addWidget(self.button_create_menu, 4, 0)
        self.button_read_menu = QPushButton("Read")
        layout.addWidget(self.button_read_menu, 4, 1)
        self.button_update_menu = QPushButton("Update")
        layout.addWidget(self.button_update_menu, 4, 2)
        self.button_delete_menu = QPushButton("Delete")
        layout.addWidget(self.button_delete_menu, 4, 3)

        self.table_menu = QTableView()
        layout.addWidget(self.table_menu, 5, 0, 1, 4)

        # Formulir Transaksi
        layout.addWidget(QLabel("Transaksi"), 6 , 0, 1, 4)

        self.input_id_transaksi = QLineEdit()
        layout.addWidget(QLabel("ID Transaksi"), 7 , 0,)
        layout.addWidget(self.input_id_transaksi, 7 , 1, 1, 3)

        self.input_menu_transaksi = QLineEdit()
        layout.addWidget(QLabel("ID Menu"), 8 , 0)
        layout.addWidget(self.input_menu_transaksi, 8 , 1, 1, 3)
        
        self.input_jumlah_transaksi = QLineEdit()
        layout.addWidget(QLabel("Jumlah Pembelian"), 9 , 0)
        layout.addWidget(self.input_jumlah_transaksi, 9 , 1, 1, 3)

        self.button_create_transaksi = QPushButton("Create")
        layout.addWidget(self.button_create_transaksi, 10, 0)
        self.button_read_transaksi = QPushButton("Read")
        layout.addWidget(self.button_read_transaksi, 10, 1)
        self.button_update_transaksi = QPushButton("Update")
        layout.addWidget(self.button_update_transaksi, 10, 2)
        self.button_delete_transaksi = QPushButton("Delete")
        layout.addWidget(self.button_delete_transaksi, 10, 3)

        self.table_transaksi = QTableView()
        layout.addWidget(self.table_transaksi, 11, 0, 1, 4)

        # menerapkan tata letak yang telah dibuat
        widget = QWidget()
        widget.setLayout(layout)
        # Menambahkan style pada formulir
        self.setStyleSheet("""
                QLineEdit { font-size: 15px }
                QLabel { 
                           font-size: 15px;
                           font-weight: bold;
                        }
        """)
        # Memberikan warna pada button
        self.button_create_menu.setStyleSheet("background-color: SpringGreen")
        self.button_read_menu.setStyleSheet("background-color: DeepSkyBlue")
        self.button_update_menu.setStyleSheet("background-color: Orange")
        self.button_delete_menu.setStyleSheet("background-color: Red")

        self.button_create_transaksi.setStyleSheet("background-color: SpringGreen")
        self.button_read_transaksi.setStyleSheet("background-color: DeepSkyBlue")
        self.button_update_transaksi.setStyleSheet("background-color: Orange")
        self.button_delete_transaksi.setStyleSheet("background-color: Red")

        # Memberikan Judul aplikasi
        self.setWindowTitle("Kasir Sederhana Rumah Makan")
        # Mengatur posisi ketika pertama kali dijalankan
        self.setCentralWidget(widget)
        # Mengatur ukuran minimal lebar & tinggi
        self.setMinimumSize(700, 200)

        self.button_create_menu.clicked.connect(self.create_menu)
        self.button_read_menu.clicked.connect(self.read_menu)
        self.button_update_menu.clicked.connect(self.update_menu)
        self.button_delete_menu.clicked.connect(self.delete_menu)
        
        self.button_create_transaksi.clicked.connect(self.create_transaksi)
        self.button_read_transaksi.clicked.connect(self.read_transaksi)
        self.button_update_transaksi.clicked.connect(self.update_transaksi)
        self.button_delete_transaksi.clicked.connect(self.delete_transaksi)

        self.conn = sqlite3.connect('data_cashier.db')
        self.create_table()
        self.load_data()
        
    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS menu (
                id_menu TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                price INT NOT NULL
            )
        """)
                       
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id_transaction TEXT PRIMARY KEY,
                id_menu TEXT NOT NULL,
                count INT NOT NULL
            )
        """)
        self.conn.commit()
    
    def load_data(self):
        self.read_menu()
        self.read_transaksi()

    def create_menu(self):
        id_menu = self.input_id_menu.text()
        nama_menu = self.input_nama_menu.text()
        harga_menu = self.input_harga_menu.text()
        if not id_menu or not nama_menu or not harga_menu:
            QMessageBox.warning(self, "Error", "Kolom ID Menu/Nama Menu/Harga Menu tidak boleh kosong.")
            return

        try:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO menu (id_menu, name, price) VALUES (?, ?, ?)", (id_menu, nama_menu, harga_menu))
            self.conn.commit()
            QMessageBox.information(self, "Success", "Menu berhasil ditambahkan.")
            self.clear_inputs()
            self.read_menu()  # Refresh the table view
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "Error", "ID Menu sudah ada, buat yang lain.")
        
    def read_menu(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM menu")
        rows = cursor.fetchall()
        
        # Membuat model tabel
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(['ID Menu', 'Nama Menu', 'Harga'])

        for row in rows:
            items = [
                QStandardItem(str(row[0])),
                QStandardItem(str(row[1])),
                QStandardItem(str(row[2]))
            ]
            model.appendRow(items)

        # Menampilkan model dalam QTableView
        self.table_menu.setModel(model)
        self.table_menu.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        
    def update_menu(self):
        id_menu = self.input_id_menu.text()
        nama_menu = self.input_nama_menu.text()
        harga_menu = self.input_harga_menu.text()
        if not id_menu or not nama_menu or not harga_menu:
            QMessageBox.warning(self, "Error", "Kolom ID Menu/Nama Menu/Harga Menu tidak boleh kosong.")
            return

        cursor = self.conn.cursor()
        cursor.execute("UPDATE menu SET name=?, price=? WHERE id_menu=?", (nama_menu, harga_menu, id_menu))
        self.conn.commit()
        if cursor.rowcount > 0:
            QMessageBox.information(self, "Success", "Menu berhasil diupdate.")
            self.clear_inputs()
            self.read_menu()  # Refresh the table view
        else:
            QMessageBox.warning(self, "Error", "ID Menu tidak ditemukan.")
        
    def delete_menu(self):
        id_menu = self.input_id_menu.text()
        if not id_menu:
            QMessageBox.warning(self, "Error", "Kolom ID Menu tidak boleh kosong")
            return

        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM menu WHERE id_menu=?", (id_menu,))
        self.conn.commit()
        if cursor.rowcount > 0:
            QMessageBox.information(self, "Success", "Menu berhasil dihapus.")
            self.clear_inputs()
            self.read_menu()  # Refresh the table view
        else:
            QMessageBox.warning(self, "Error", "ID Menu tidak ditemukan.")
    
    def create_transaksi(self):
        id_transaksi = self.input_id_transaksi.text()
        id_menu = self.input_menu_transaksi.text()
        jumlah = self.input_jumlah_transaksi.text()
        if not id_transaksi or not id_menu or not jumlah:
            QMessageBox.warning(self, "Error", "Kolom ID Transaksi/ID Menu/Jumlah Pembelian tidak boleh kosong.")
            return
        
        # Melakukan pengecekan apakah ID Menu ada atau tidak, jika ID tidak ada maka tidak dapat mengisi tabel transaksi
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM menu WHERE id_menu = ?", (id_menu,))
        row = cursor.fetchone()
        
        if not row:
            QMessageBox.warning(self, "Error", "ID Menu tidak ditemukan.") 
            return

        try:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO transactions (id_transaction, id_menu, count) VALUES (?, ?, ?)", (id_transaksi, id_menu, jumlah))
            self.conn.commit()
            QMessageBox.information(self, "Success", "Transaksi berhasil ditambahkan.")
            self.clear_inputs()
            self.read_transaksi()  # Refresh the table view
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "Error", "ID Transaksi sudah ada, buat yang lain.")
        
    def read_transaksi(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id_transaction, transactions.id_menu, count, name, price FROM transactions INNER JOIN menu ON menu.id_menu = transactions.id_menu")
        rows = cursor.fetchall()
        
        # Membuat model tabel
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(['ID Transaksi', 'ID Menu', 'Jumlah', 'Nama Menu', 'Harga Menu', 'Total pembelian'])

        for row in rows:
            items = [
                QStandardItem(str(row[0])),
                QStandardItem(str(row[1])),
                QStandardItem(str(row[2])),
                QStandardItem(str(row[3])),
                QStandardItem(str(row[4])),
                QStandardItem(str(row[4] * row[2])) # Menghitung harga menu dengan total pembelian
            ]
            model.appendRow(items)

        # Menampilkan model dalam QTableView
        self.table_transaksi.setModel(model)
        self.table_transaksi.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
    def update_transaksi(self):
        id_transaksi = self.input_id_transaksi.text()
        id_menu = self.input_menu_transaksi.text()
        jumlah = self.input_jumlah_transaksi.text()
        if not id_transaksi or not id_menu or not jumlah:
            QMessageBox.warning(self, "Error", "Kolom ID Transaksi/ID Menu/Jumlah Pembelian tidak boleh kosong.")
            return
        
        # Melakukan pengecekan apakah ID Menu ada atau tidak, jika ID tidak ada maka tidak dapat mengisi tabel transaksi
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM menu WHERE id_menu = ?", (id_menu,))
        row = cursor.fetchone()
        
        if not row:
            QMessageBox.warning(self, "Error", "ID Menu tidak ditemukan.") 
            return

        cursor = self.conn.cursor()
        cursor.execute("UPDATE transactions SET id_menu=?, count=? WHERE id_transaction=?", (id_menu, jumlah, id_transaksi))
        self.conn.commit()
        if cursor.rowcount > 0:
            QMessageBox.information(self, "Success", "Transaksi berhasil diupdate.")
            self.clear_inputs()
            self.read_transaksi()  # Refresh the table view
        else:
            QMessageBox.warning(self, "Error", "ID Transaksi tidak ditemukan.")
        
    def delete_transaksi(self):
        id_transaksi = self.input_id_transaksi.text()
        if not id_transaksi:
            QMessageBox.warning(self, "Error", "Kolom ID Transaksi tidak boleh kosong")
            return

        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM transactions WHERE id_transaction=?", (id_transaksi,))
        self.conn.commit()
        if cursor.rowcount > 0:
            QMessageBox.information(self, "Success", "Transaksi berhasil dihapus.")
            self.clear_inputs()
            self.read_transaksi()  # Refresh the table view
        else:
            QMessageBox.warning(self, "Error", "ID Transaksi tidak ditemukan.")
    
    def clear_inputs(self):
        self.input_id_menu.clear()
        self.input_nama_menu.clear()
        self.input_harga_menu.clear()

        self.input_id_transaksi.clear()
        self.input_menu_transaksi.clear()
        self.input_jumlah_transaksi.clear()

if __name__ == "__main__":
    app = QApplication([])
    window = MainApplication()
    window.show()
    app.exec_()