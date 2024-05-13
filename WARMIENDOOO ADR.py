#impor pustaka tipe dict phyton
from typing import Dict
#fungsi yang digunakan
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import QTimer, QDateTime, Qt

#tempat menyimpan username
class LoginWindow(QWidget):
    user_warmiendo: dict[str, str]

    #menetapkan username dan password
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.initUI()

        #daftar username dan password
        self.user_warmiendo = {
            'dian': '05231018',
            'adelano': '18231048',
            'rizal': '03231050'}

    #menampilkan window dan button
    def initUI(self):
        self.setWindowTitle('Login')
        self.setGeometry(300, 300, 400, 300)

        # Mengatur latar belakang window login menggunakan QPixmap
        pixmap = QPixmap("login.png")
        background_label = QLabel(self)
        background_label.setPixmap(pixmap)
        background_label.setGeometry(0,0, self.width(), self.height())

        layout = QVBoxLayout()

        self.username_label = QLabel('Username:', self)
        layout.addWidget(self.username_label)

        self.username_input = QLineEdit(self)
        layout.addWidget(self.username_input)

        self.password_label = QLabel('Password:', self)
        layout.addWidget(self.password_label)

        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        self.time_label = QLabel('', self)
        layout.addWidget(self.time_label)

        self.login_button = QPushButton('Login', self)
        self.login_button.clicked.connect(self.login)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    #membuat waktu sesuai perangkat
        self.update_time()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

    def update_time(self):
        now = QDateTime.currentDateTime()
        current_time = now.toString(Qt.DefaultLocaleLongDate)
        self.time_label.setText(f'Waktu pemesanan: {current_time}')

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        #memeriksa apakah input username dan password cocok dengan yang disimpan
        if username in self.user_warmiendo and self.user_warmiendo[username] == password:
            self.close()
            self.main_window.show()
        else:
            QMessageBox.warning(self, 'Error', 'Maap Ga Kenal')

#menu utama pesanan
class MainWindow(QMainWindow):
    #mengatur button dan window
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pemesanan Warmiendooo")
        self.setGeometry(300, 300, 1000, 400)

        # Mengatur latar belakang window menu utama menggunakan QPixmap
        pixmap = QPixmap("menu.png")
        background_label = QLabel(self)
        background_label.setPixmap(pixmap)
        background_label.setGeometry(0, 0, self.width(), self.height())

        layout = QVBoxLayout()

        menu_groupbox = QGroupBox("Menu")
        menu_layout = QVBoxLayout()
        menu_groupbox.setLayout(menu_layout)

        #memberi nama dan harga pada menu
        lbl_Judul_Menu = QLabel("List Menu:", self)
        menu_layout.addWidget(lbl_Judul_Menu)

        self.cbx_menu = QComboBox(self)
        self.cbx_menu.addItems(['Paket Gorengz Indomie {All Varian,Nasi,Sawi,Telor,Es Teh} (Rp. 12.000)',
                                'Paket Kwuahh {Indomie All Varian,Pentol,Sawi,Telor,Es Teh} (Rp. 12.000)',
                                'Mie Goreng All Varian (Rp. 4.000)',
                                'Mie Kuah All Varian (Rp. 4.000)', 'Only Xtra Menu'])
        self.harga_menu_indeks = [12000, 12000, 4000, 4000, 0]
        menu_layout.addWidget(self.cbx_menu)

        lbl_extra = QLabel("Xtra Menu:", self)
        menu_layout.addWidget(lbl_extra)

        self.chx_telor = QCheckBox('Telor {dadar/ceplok/rebus} (Rp. 4.000)', self)
        self.chx_pentol = QCheckBox('Pentol (Rp. 8.000)', self)
        self.chx_nugget = QCheckBox('Nugget (Rp. 8.000)', self)
        self.chx_nasi = QCheckBox('Nasi (Rp. 4.000)', self)
        self.chx_air_mineral = QCheckBox('Air Mineral (Rp. 3.000)', self)
        self.chx_es_teh = QCheckBox('Es Teh (Rp. 4.000)', self)
        self.chx_es_jeruk = QCheckBox('Es Jeruk (Rp. 5.000)', self)

        menu_layout.addWidget(self.chx_telor)
        menu_layout.addWidget(self.chx_pentol)
        menu_layout.addWidget(self.chx_nugget)
        menu_layout.addWidget(self.chx_nasi)
        menu_layout.addWidget(self.chx_air_mineral)
        menu_layout.addWidget(self.chx_es_teh)
        menu_layout.addWidget(self.chx_es_jeruk)

        layout.addWidget(menu_groupbox)

        #menghitung harga dan mengatur bentuk dan ukuran font harga yang keluar
        self.btn_hitung = QPushButton("Input Data Pembeli", self)
        self.btn_hitung.clicked.connect(self.hitung)
        layout.addWidget(self.btn_hitung)

        self.lbl_harga = QLabel("Harga:", self)
        layout.addWidget(self.lbl_harga)

        self.font_total = QFont()
        self.font_total.setBold(True)
        self.font_total.setPointSize(14)

        self.lbl_total = QLabel(self)
        self.lbl_total.setFont(self.font_total)
        layout.addWidget(self.lbl_total)

        self.pesanan_textedit = QTextEdit(self)
        layout.addWidget(self.pesanan_textedit)

        self.waktu_pemesanan_label = QLabel('', self)
        layout.addWidget(self.waktu_pemesanan_label)

        #agar window pemesanan tidak hilang saat fungsi sudah dijalankan
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # Hubungkan fungsi update_total ke button check box dan combo box
        self.cbx_menu.activated.connect(self.update_total)
        self.chx_telor.clicked.connect(self.update_total)
        self.chx_pentol.clicked.connect(self.update_total)
        self.chx_nugget.clicked.connect(self.update_total)
        self.chx_nasi.clicked.connect(self.update_total)
        self.chx_air_mineral.clicked.connect(self.update_total)
        self.chx_es_teh.clicked.connect(self.update_total)
        self.chx_es_jeruk.clicked.connect(self.update_total)

    def update_total(self):
        harga_menu = self.harga_menu_indeks[self.cbx_menu.currentIndex()]
        harga_extra = self.get_total_extra()
        total_harga = harga_menu + harga_extra
        self.lbl_total.setText(f"Rp. {total_harga}")
        self.lbl_total.adjustSize()

    def get_total_extra(self):
        total = 0
        if self.chx_telor.isChecked():
            total += 4000
        if self.chx_pentol.isChecked():
            total += 8000
        if self.chx_nugget.isChecked():
            total += 8000
        if self.chx_nasi.isChecked():
            total += 4000
        if self.chx_air_mineral.isChecked():
            total += 3000
        if self.chx_es_teh.isChecked():
            total += 4000
        if self.chx_es_jeruk.isChecked():
            total += 5000
        return total

    #menampilkan harga total
    def hitung(self):
        harga_menu = self.harga_menu_indeks[self.cbx_menu.currentIndex()]
        harga_extra = self.get_total_extra()
        total_harga = harga_menu + harga_extra
        self.lbl_total.setText(f"Rp. {total_harga}")
        self.lbl_total.adjustSize()

        #memasukan total pesanan ke data yang akan ditampilkan
        dialog = NamaPembeliDialog(self)
        dialog.setGeometry(500, 500, 300, 150)
        if dialog.exec_():
            nama_pembeli = dialog.nama_pembeli_input.text()
            if nama_pembeli:
                pesanan = self.cbx_menu.currentText() + '\n'
                pesanan += 'Extra: ' + ', '.join(
                    [checkbox.text() for checkbox in self.findChildren(QCheckBox) if checkbox.isChecked()]) + '\n\n'
                self.tambah_pesanan(f'Nama Pembeli: {nama_pembeli}\n{pesanan}')

    # memasukan waktu ke data yang akan ditampilkan
    def tambah_pesanan(self, pesanan):
        self.pesanan_textedit.append(pesanan)
        now = QDateTime.currentDateTime()
        current_time = now.toString(Qt.DefaultLocaleLongDate)
        self.waktu_pemesanan_label.setText(f'Waktu pemesanan: {current_time}')

#menampilkan window input data pembeli
class NamaPembeliDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Data Pelanggan")

        layout = QVBoxLayout()

        self.nama_pembeli_label = QLabel("Masukkan nama pembeli:", self)
        layout.addWidget(self.nama_pembeli_label)

        self.nama_pembeli_input = QLineEdit(self)
        layout.addWidget(self.nama_pembeli_input)

        self.ok_button = QPushButton("PRINT", self)
        self.ok_button.clicked.connect(self.accept)
        layout.addWidget(self.ok_button)
        self.setLayout(layout)
        # Menghilangkan tombol "?" akibat fungsi Qdialog
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

#eksekusi codingan oleh phyton dari awal hingga akhir
if __name__ == '__main__':
    app = QApplication([])
    main_window = MainWindow()
    login_window = LoginWindow(main_window)
    login_window.show()
    app.exec_()