import sys
import requests
import csv
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLineEdit,
    QPushButton, QLabel, QListWidget, QStatusBar, QMenuBar, QAction,
    QFileDialog, QMessageBox, QToolBar
)
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtCore import QDateTime, Qt

API_KEY = '7dfbca8e43cd4dff000f992ffab7869b'

class WeatherApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aplikasi Cuaca Harian")
        self.setGeometry(100, 100, 500, 550)
        self.dark_mode = False  

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        self.city_input = QLineEdit()
        self.city_input.setPlaceholderText("Masukkan nama kota")
        self.city_input.setStyleSheet("padding: 5px; font-size: 14px; border: 1px solid gray;")
        self.layout.addWidget(self.city_input)

        self.check_button = QPushButton("Cek Cuaca")
        self.check_button.clicked.connect(self.get_weather)
        self.check_button.setStyleSheet("background-color: #3498db; color: white; padding: 5px;")
        self.layout.addWidget(self.check_button)

        self.result_label = QLabel("Informasi cuaca akan muncul di sini.")
        self.result_label.setWordWrap(True)
        self.result_label.setMaximumHeight(150)
        self.result_label.setStyleSheet("""
            border: 2px solid #3498db;
            border-radius: 8px;
            background-color: #f0faff;
            padding: 10px;
            font-size: 13px;
        """)
        self.layout.addWidget(self.result_label)

        self.history_list = QListWidget()
        self.layout.addWidget(self.history_list)

        self.export_button = QPushButton("Export Riwayat ke CSV")
        self.export_button.clicked.connect(self.export_to_csv)
        self.export_button.setStyleSheet("background-color: #2ecc71; color: white; padding: 5px;")
        self.layout.addWidget(self.export_button)

        self.central_widget.setLayout(self.layout)

        status_bar = QStatusBar()
        label_identitas = QLabel("Andi Sibwayiq Abi Mahmud | F1D022002")
        status_bar.addWidget(label_identitas)  
        self.setStatusBar(status_bar)

        self.create_menu_bar()
        self.create_top_toolbar()  
        self.tampilkan_5_kota_terpanas()

    def create_menu_bar(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")
        delete_menu = menubar.addMenu("Delete")
        help_menu = menubar.addMenu("Help")

        export_action = QAction("Export CSV", self)
        export_action.triggered.connect(self.export_to_csv)
        file_menu.addAction(export_action)

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        delete_all_action = QAction("Hapus Semua Riwayat", self)
        delete_all_action.triggered.connect(self.hapus_riwayat)
        delete_menu.addAction(delete_all_action)

        delete_selected_action = QAction("Hapus Riwayat Terpilih", self)
        delete_selected_action.triggered.connect(self.hapus_riwayat_terpilih)
        delete_menu.addAction(delete_selected_action)

        about_action = QAction("Tentang Aplikasi", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def create_top_toolbar(self):
        toolbar = QToolBar("Toolbar Atas")
        self.addToolBar(Qt.TopToolBarArea, toolbar)

        theme_button = QPushButton("Ubah Tema")
        theme_button.clicked.connect(self.toggle_theme)
        theme_button.setStyleSheet("padding: 4px; background-color: #95a5a6; color: white; font-weight: bold;")
        toolbar.addWidget(theme_button)

        toolbar.setMovable(False)

    def show_about(self):
        QMessageBox.information(self, "Tentang", "Aplikasi Cuaca Harian  yang di peruntungkan kaum2 gabut\nDibuat oleh Andi Sibwayiq Abi Mahmud\nNIM: F1D022002")

    def tampilkan_5_kota_terpanas(self):
        kota_list = ["Jakarta", "Surabaya", "Medan", "Makassar", "Bandung", "Kota Bima"]
        hasil = []

        for kota in kota_list:
            try:
                url = f"https://api.openweathermap.org/data/2.5/weather?q={kota}&appid={API_KEY}&units=metric&lang=id"
                response = requests.get(url)
                data = response.json()
                if response.status_code == 200:
                    suhu = data["main"]["temp"]
                    deskripsi = data["weather"][0]["description"]
                    hasil.append((kota, suhu, deskripsi))
            except Exception as e:
                print(f"Gagal ambil data kota {kota}: {e}")

        hasil.sort(key=lambda x: x[1], reverse=True)

        text = "\U0001F321\ufe0f 5 Kota Terbesar di Indonesia (Real-Time):\n\n"
        for kota, suhu, deskripsi in hasil[:5]:
            text += f"{kota}: {suhu}°C, {deskripsi}\n"

        self.result_label.setText(text)

    def get_weather(self):
        city = self.city_input.text().strip()
        if not city:
            self.result_label.setText("Kota tidak boleh kosong.")
            return

        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=id"

        try:
            response = requests.get(url)
            data = response.json()

            if response.status_code == 200:
                suhu = data["main"]["temp"]
                kelembaban = data["main"]["humidity"]
                deskripsi = data["weather"][0]["description"]
                waktu = QDateTime.currentDateTime().toString("dd-MM-yyyy HH:mm:ss")

                result_text = f"""
                <div style='border:2px solid #2980b9; border-radius:8px; background-color:#fefefe; padding:10px;'>
                    <b>Kota:</b> {city}<br>
                    <b>Suhu:</b> {suhu}°C<br>
                    <b>Kelembaban:</b> {kelembaban}%<br>
                    <b>Cuaca:</b> {deskripsi}<br>
                    <b>Waktu:</b> {waktu}
                </div>
                """
                self.result_label.setText(result_text)
                self.result_label.setTextFormat(1)
                self.history_list.addItem(f"{city} | ({waktu}) | {suhu}°C | {kelembaban}% | {deskripsi}")

                self.set_weather_color(deskripsi)
            else:
                self.result_label.setText(f"Error: {data.get('message', 'Gagal mengambil data')}")
        except Exception as e:
            self.result_label.setText(f"Gagal: {str(e)}")

    def set_weather_color(self, description):
        palette = QPalette()
        desc = description.lower()

        if "hujan" in desc:
            palette.setColor(QPalette.Window, QColor(120, 170, 255))
        elif "awan" in desc:
            palette.setColor(QPalette.Window, QColor(190, 190, 190))
        elif "cerah" in desc or "clear" in desc:
            palette.setColor(QPalette.Window, QColor(255, 230, 100))
        else:
            palette.setColor(QPalette.Window, QColor(255, 255, 255))

        self.setPalette(palette)

    def export_to_csv(self):
        if self.history_list.count() == 0:
            QMessageBox.warning(self, "Kosong", "Belum ada data untuk diekspor.")
            return

        path, _ = QFileDialog.getSaveFileName(self, "Simpan CSV", "", "CSV Files (*.csv)")
        if path:
            try:
                with open(path, 'w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(["Riwayat Pencarian"])
                    for i in range(self.history_list.count()):
                        writer.writerow([self.history_list.item(i).text()])
                QMessageBox.information(self, "Sukses", "Data berhasil diekspor!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Gagal menyimpan file: {str(e)}")

    def hapus_riwayat(self):
        self.history_list.clear()
        QMessageBox.information(self, "Hapus", "Riwayat pencarian berhasil dihapus.")

    def hapus_riwayat_terpilih(self):
        current_item = self.history_list.currentItem()
        if current_item:
            reply = QMessageBox.question(
                self,
                "Konfirmasi Hapus",
                "Yakin ingin menghapus item terpilih?",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                row = self.history_list.currentRow()
                self.history_list.takeItem(row)
        else:
            QMessageBox.warning(self, "Peringatan", "Silakan pilih item yang ingin dihapus.")

    # ==== TEMA ====
    def toggle_theme(self):
        if self.dark_mode:
            self.set_light_theme()
        else:
            self.set_dark_theme()
        self.dark_mode = not self.dark_mode

    def set_dark_theme(self):
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
        dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.Text, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
        dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))

        self.setPalette(dark_palette)

    def set_light_theme(self):
        self.setPalette(QApplication.palette())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WeatherApp()
    window.show()
    sys.exit(app.exec_())
