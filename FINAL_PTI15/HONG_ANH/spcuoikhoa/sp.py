from PyQt6 import uic
from PyQt6.QtWidgets import *

danh_sach_mon = [
    {"name": "Phở", "price": 35000},
    {"name": "Bánh Mì", "price": 15000},
    {"name": "Pizza", "price": 100000},
    {"name": "Hamburger", "price": 50000},
    {"name": "Trà Sữa", "price": 25000},
    {"name": "Gà Rán", "price": 45000},
    {"name": "Khoai Tây Chiên", "price": 25000},
    {"name": "Spaghetti", "price": 80000},
    {"name": "Chè Thái", "price": 30000},
]

class ThemMon(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("spthemmon.ui", self)
        self.pushButton_2.clicked.connect(self.cancle)
        self.pushButton.clicked.connect(self.them_mon)

    def them_mon(self):
        name = self.inputDish.text().strip()
        price_text = self.inputPrice.text().strip()

        if not name or not price_text.isdigit():  
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập tên món và giá hợp lệ!")
            return

        danh_sach_mon.append({"name": name, "price": float(price_text)})  
        self.inputDish.clear()
        self.inputPrice.clear()
        self.close()
        window.show_menu_table() 

    def cancle(self):
        self.close()


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("sp.ui", self)
        self.show_menu_table()
        
        self.btnThemMon.clicked.connect(self.open_themmon)
        self.btnTinhTien.clicked.connect(self.tinh_tien)
        self.btnXoa.clicked.connect(self.xoa_mon)
        self.btnClearAll.clicked.connect(self.xoa_het)  

    def open_themmon(self):
        self.themmon = ThemMon()  
        self.themmon.show()

    def tinh_tien(self):
        tong_tien = 0
        selected_rows = set(index.row() for index in self.tableWidget.selectedIndexes())  
        for row in selected_rows:
            tong_tien += danh_sach_mon[row]["price"]
        self.lbTotal.setText(f"Tổng tiền: {tong_tien} VNĐ")
    def xoa_mon(self):
        selected_indexes = self.tableWidget.selectedIndexes()
        if not selected_indexes:  

            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn món để xóa!")
            return

        row = selected_indexes[0].row()
        ten_mon = danh_sach_mon[row]["name"]

        reply = QMessageBox.question(
            self, "Xác nhận", f"Xóa {ten_mon}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            danh_sach_mon.pop(row)
            self.show_menu_table()

    def xoa_het(self):
        if not danh_sach_mon:  
            QMessageBox.warning(self, "Lỗi", "Danh sách món đã trống!")
            return

        reply = QMessageBox.question(
            self, "Xác nhận", "Xóa hết tất cả món?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            danh_sach_mon.clear()  
            self.show_menu_table() 
    def show_menu_table(self):
        self.tableWidget.setRowCount(len(danh_sach_mon))
        for i, mon in enumerate(danh_sach_mon):
            self.tableWidget.setItem(i, 0, QTableWidgetItem(mon["name"]))
            self.tableWidget.setItem(i, 1, QTableWidgetItem(str(mon["price"])))

app = QApplication([])
window = App()
window.show()
app.exec()