from PyQt6.QtWidgets import *
from PyQt6 import uic
import sys
import os

from data import load_essays, save_essays
from model import Essay
from PyQt6.QtCore import Qt
from ai import get_answer, ask_question
from datetime import datetime

MAIN_UI_FILE = os.path.join(os.path.dirname(__file__), "nhatminh.ui")
HISTORY_UI_FILE = os.path.join(os.path.dirname(__file__), "history.ui")




essays = load_essays()


class HistoryWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(HISTORY_UI_FILE, self)
        
        # Thiết lập toggle mode button
        self.btnToggleMode.setText("☀️")
        self.btnToggleMode.setStyleSheet(
            """
            QPushButton {
                font-size: 18px;
                background-color: transparent;
                border: none;
            }
            """
        )
        
        # Khởi tạo biến
        self.dark_mode = False
        self.essays = []
        self.filtered_essays = []
        
        # Kết nối các signal và slot
        self.setup_connections()
        
        # Áp dụng theme mặc định và tải dữ liệu
        self.toggle_dark_mode()
        self.load_data()

    def setup_connections(self):
        """Kết nối các signal và slot"""
        self.btnToggleMode.clicked.connect(self.toggle_dark_mode)
        self.btnRefresh.clicked.connect(self.load_data)
        self.btnDelete.clicked.connect(self.delete_selected_essay)
        self.btnSearch.clicked.connect(self.search_essays)
        self.btnCopyEssay.clicked.connect(self.copy_essay)
        self.btnCopyFeedback.clicked.connect(self.copy_feedback)
        self.btnExport.clicked.connect(self.export_essay)
        self.listEssays.itemClicked.connect(self.display_essay_details)
        self.lineSearch.returnPressed.connect(self.search_essays)

    def load_data(self):
        """Tải dữ liệu từ file và hiển thị trong danh sách"""
        try:
            self.essays = load_essays()
            self.filtered_essays = self.essays.copy()
            self.populate_essay_list()
            self.labelStatus.setText(f"Đã tải {len(self.essays)} bài viết")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể tải dữ liệu: {str(e)}")
            self.labelStatus.setText("Lỗi khi tải dữ liệu")

    def populate_essay_list(self):
        """Hiển thị danh sách bài viết trong list widget"""
        self.listEssays.clear()
        
        for i, essay in enumerate(self.filtered_essays):
            # Tạo preview ngắn của bài viết (50 ký tự đầu)
            preview = essay.user_essay[:50] + "..." if len(essay.user_essay) > 50 else essay.user_essay
            preview = preview.replace('\n', ' ')  # Loại bỏ xuống dòng
            
            # Tạo item cho list
            item_text = f"Bài {i+1}: {preview}"
            item = QListWidgetItem(item_text)
            item.setData(Qt.ItemDataRole.UserRole, i)  # Lưu index của essay
            self.listEssays.addItem(item)

    def search_essays(self):
        """Tìm kiếm bài viết theo từ khóa"""
        search_text = self.lineSearch.text().strip().lower()
        
        if not search_text:
            self.filtered_essays = self.essays.copy()
        else:
            self.filtered_essays = []
            for essay in self.essays:
                # Tìm kiếm trong cả bài viết và feedback
                if (search_text in essay.user_essay.lower() or 
                    search_text in essay.ai_feedback.lower()):
                    self.filtered_essays.append(essay)
        
        self.populate_essay_list()
        self.labelStatus.setText(f"Tìm thấy {len(self.filtered_essays)}/{len(self.essays)} bài viết")

    def display_essay_details(self, item):
        """Hiển thị chi tiết bài viết khi được chọn"""
        try:
            index = item.data(Qt.ItemDataRole.UserRole)
            essay = self.filtered_essays[index]
            
            self.textOriginalEssay.setPlainText(essay.user_essay)
            self.textAIFeedback.setPlainText(essay.ai_feedback)
            
            self.labelStatus.setText(f"Đang xem bài viết {index + 1}")
        except Exception as e:
            QMessageBox.warning(self, "Lỗi", f"Không thể hiển thị chi tiết: {str(e)}")

    def delete_selected_essay(self):
        """Xóa bài viết được chọn"""
        current_item = self.listEssays.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn một bài viết để xóa!")
            return
        
        # Xác nhận xóa
        reply = QMessageBox.question(
            self, "Xác nhận", 
            "Bạn có chắc chắn muốn xóa bài viết này không?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                index = current_item.data(Qt.ItemDataRole.UserRole)
                essay_to_delete = self.filtered_essays[index]
                
                # Tìm và xóa essay trong danh sách gốc
                self.essays = [e for e in self.essays if e.user_essay != essay_to_delete.user_essay 
                              or e.ai_feedback != essay_to_delete.ai_feedback]
                
                # Lưu lại dữ liệu
                save_essays(self.essays)
                
                # Cập nhật giao diện
                self.load_data()
                
                # Xóa nội dung hiển thị
                self.textOriginalEssay.clear()
                self.textAIFeedback.clear()
                
                self.labelStatus.setText("Đã xóa bài viết thành công")
                QMessageBox.information(self, "Thành công", "Đã xóa bài viết!")
                
            except Exception as e:
                QMessageBox.critical(self, "Lỗi", f"Không thể xóa bài viết: {str(e)}")

    def copy_essay(self):
        """Copy bài viết gốc vào clipboard"""
        text = self.textOriginalEssay.toPlainText()
        if text:
            clipboard = QApplication.clipboard()
            clipboard.setText(text)
            self.labelStatus.setText("Đã copy bài viết vào clipboard")
        else:
            QMessageBox.warning(self, "Cảnh báo", "Không có bài viết nào để copy!")

    def copy_feedback(self):
        """Copy đánh giá AI vào clipboard"""
        text = self.textAIFeedback.toPlainText()
        if text:
            clipboard = QApplication.clipboard()
            clipboard.setText(text)
            self.labelStatus.setText("Đã copy đánh giá vào clipboard")
        else:
            QMessageBox.warning(self, "Cảnh báo", "Không có đánh giá nào để copy!")

    def export_essay(self):
        """Xuất bài viết ra file text"""
        current_item = self.listEssays.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn một bài viết để xuất!")
            return
        
        try:
            index = current_item.data(Qt.ItemDataRole.UserRole)
            essay = self.filtered_essays[index]
            
            # Mở dialog chọn nơi lưu file
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Xuất bài viết", f"bai_viet_{index+1}.txt", 
                "Text Files (*.txt);;All Files (*)"
            )
            
            if file_path:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write("=" * 50 + "\n")
                    file.write("BÀI VIẾT GỐC\n")
                    file.write("=" * 50 + "\n\n")
                    file.write(essay.user_essay)
                    file.write("\n\n" + "=" * 50 + "\n")
                    file.write("ĐÁNH GIÁ CỦA AI\n")
                    file.write("=" * 50 + "\n\n")
                    file.write(essay.ai_feedback)
                    file.write(f"\n\n" + "=" * 50 + "\n")
                    file.write(f"Xuất ngày: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
                    file.write("=" * 50 + "\n")
                
                self.labelStatus.setText(f"Đã xuất bài viết ra: {file_path}")
                QMessageBox.information(self, "Thành công", f"Đã xuất bài viết ra:\n{file_path}")
                
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể xuất file: {str(e)}")

    def toggle_dark_mode(self):
        """Chuyển đổi giữa chế độ sáng và tối"""
        self.dark_mode = not self.dark_mode

        if self.dark_mode:
            self.btnToggleMode.setText("🌙")
            # Dark mode styles - tương tự nhatminh.py
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #1E1E1E;
                }
                QLabel {
                    color: #FFFFFF;
                }
                QLabel#labelTitle {
                    font-size: 24px;
                    font-weight: bold;
                    color: #64B5F6;
                }
                QPushButton {
                    background-color: #2979FF;
                    color: white;
                    border-radius: 5px;
                    padding: 8px;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background-color: #1565C0;
                }
                QTextEdit {
                    background-color: #2D2D2D;
                    color: #FFFFFF;
                    border: 1px solid #555555;
                    border-radius: 5px;
                    padding: 10px;
                    font-size: 12px;
                }
                QLineEdit {
                    background-color: #2D2D2D;
                    color: #FFFFFF;
                    border: 1px solid #555555;
                    border-radius: 5px;
                    padding: 5px;
                    font-size: 12px;
                }
                QListWidget {
                    background-color: #2D2D2D;
                    color: #FFFFFF;
                    border: 1px solid #555555;
                    border-radius: 5px;
                    font-size: 12px;
                }
                QListWidget::item {
                    padding: 8px;
                    border-bottom: 1px solid #555555;
                }
                QListWidget::item:selected {
                    background-color: #2979FF;
                }
                QListWidget::item:hover {
                    background-color: #404040;
                }
                QWidget#mainContent, QWidget#leftPanel, QWidget#rightPanel {
                    background-color: #2D2D2D;
                    border-radius: 10px;
                    padding: 10px;
                }
                QPushButton#btnToggleMode {
                    font-size: 18px;
                    background-color: transparent;
                    border: none;
                }
            """)
        else:
            self.btnToggleMode.setText("☀️")
            # Light mode styles - tương tự nhatminh.py
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #FFFFFF;
                }
                QLabel {
                    color: #333333;
                }
                QLabel#labelTitle {
                    font-size: 24px;
                    font-weight: bold;
                    color: #1976D2;
                }
                QPushButton {
                    background-color: #2196F3;
                    color: white;
                    border-radius: 5px;
                    padding: 8px;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background-color: #1976D2;
                }
                QTextEdit {
                    background-color: #F5F5F5;
                    color: #333333;
                    border: 1px solid #DDDDDD;
                    border-radius: 5px;
                    padding: 10px;
                    font-size: 12px;
                }
                QLineEdit {
                    background-color: #F5F5F5;
                    color: #333333;
                    border: 1px solid #DDDDDD;
                    border-radius: 5px;
                    padding: 5px;
                    font-size: 12px;
                }
                QListWidget {
                    background-color: #F5F5F5;
                    color: #333333;
                    border: 1px solid #DDDDDD;
                    border-radius: 5px;
                    font-size: 12px;
                }
                QListWidget::item {
                    padding: 8px;
                    border-bottom: 1px solid #DDDDDD;
                }
                QListWidget::item:selected {
                    background-color: #2196F3;
                    color: white;
                }
                QListWidget::item:hover {
                    background-color: #E3F2FD;
                }
                QWidget#mainContent, QWidget#leftPanel, QWidget#rightPanel {
                    background-color: #FFFFFF;
                    border-radius: 10px;
                    padding: 10px;
                }
                QPushButton#btnToggleMode {
                    font-size: 18px;
                    background-color: transparent;
                    border: none;
                }
            """)



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(MAIN_UI_FILE, self)

        self.btnToggleMode.setText("☀️")
        self.btnToggleMode.setStyleSheet(
            """
            QPushButton {
                font-size: 18px;
                background-color: transparent;
                border: none;
            }
        """
        )
        self.dark_mode = False


        self.btnEvaluate.clicked.connect(self.evaluate_text)
        self.btnToggleMode.clicked.connect(self.toggle_dark_mode)
        self.btnAsk.clicked.connect(self.ask_additional_question)
        self.btnHistory.clicked.connect(self.open_history_window)

        # chế độ tối và lưu trữ bài viết/phản hồi
        self.dark_mode = False
        self.current_essay = ""
        self.current_feedback = ""
        self.history_window = None

        self.labelQuestion.setVisible(False)
        self.lineQuestion.setVisible(False)
        self.btnAsk.setVisible(False)

        self.toggle_dark_mode()

    def evaluate_text(self):
        """Xử lý khi người dùng nhấn nút đánh giá"""
        # Lấy nội dung bài viết
        text = self.textInput.toPlainText().strip()

        if not text:
            QMessageBox.warning(
                self, "Cảnh báo", "Vui lòng nhập bài viết cần đánh giá!"
            )
            return

        # Lấy trình độ từ combobox
        level = self.comboLevel.currentText()

        # Hiển thị thông báo đang xử lý
        self.textOutput.setPlainText("Đang đánh giá bài viết, vui lòng đợi...")
        QApplication.processEvents()  # Cập nhật giao diện

        # đánh giá
        result = get_answer(text, level)

        # Lưu bài viết 
        self.current_essay = text
        self.current_feedback = result

        # Hiển thị kq
        self.textOutput.setPlainText(result)

        # Hiển thị reply
        self.labelQuestion.setVisible(True)
        self.lineQuestion.setVisible(True)
        self.btnAsk.setVisible(True)
        
        # Lưu bài viết
        essays.append(Essay(self.current_essay, self.current_feedback))
        save_essays(essays)
        
    def ask_additional_question(self):
        """Xử lý khi người dùng đặt câu hỏi thêm"""
        # Kiểm tra xem đã có bài viết và phản hồi chưa
        if not self.current_essay or not self.current_feedback:
            QMessageBox.warning(
                self, "Cảnh báo", "Vui lòng đánh giá bài viết trước khi đặt câu hỏi!"
            )
            return

        # Lấy câu hỏi
        question = self.lineQuestion.text().strip()
        if not question:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng nhập câu hỏi!")
            return

        # Lấy trình độ
        level = self.comboLevel.currentText()

        # Hiển thị thông báo đang xử lý
        current_text = self.textOutput.toPlainText()
        self.textOutput.setPlainText(
            current_text + "\n\nĐang xử lý câu hỏi, vui lòng đợi..."
        )
        QApplication.processEvents()  # Cập nhật giao diện

        # Gọi API để trả lời câu hỏi
        answer = ask_question(
            self.current_essay, self.current_feedback, question, level
        )

        # Hiển thị câu hỏi và câu trả lời
        self.textOutput.setPlainText(
            current_text + f"\n\nCâu hỏi: {question}\n\nTrả lời: {answer}"
        )

        # Xóa nội dung câu hỏi
        self.lineQuestion.clear()

    def open_history_window(self):
        """Mở cửa sổ lịch sử bài viết"""
        try:
            if self.history_window is None or not self.history_window.isVisible():
                self.history_window = HistoryWindow()
                # Đồng bộ dark mode
                if self.dark_mode != self.history_window.dark_mode:
                    self.history_window.toggle_dark_mode()
            # mở cửa sổ lịch sử
            self.history_window.show()
      
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể mở cửa sổ lịch sử: {str(e)}")

    def toggle_dark_mode(self):
        """Chuyển đổi giữa chế độ sáng và tối"""
        self.dark_mode = not self.dark_mode

        # Thay đổi emoji
        if self.dark_mode:
            self.btnToggleMode.setText("🌙")

            # Áp dụng dark mode
            self.setStyleSheet(
                """
                QMainWindow {
                    background-color: #1E1E1E;
                }
                QLabel {
                    color: #FFFFFF;
                }
                QLabel#labelTitle {
                    font-size: 28px;
                    font-weight: bold;
                    color: #64B5F6;
                }
                QPushButton {
                    background-color: #2979FF;
                    color: white;
                    border-radius: 5px;
                    padding: 10px;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #1565C0;
                }
                QTextEdit {
                    background-color: #2D2D2D;
                    color: #FFFFFF;
                    border: 1px solid #555555;
                    border-radius: 5px;
                    padding: 10px;
                    font-size: 14px;
                }
                QComboBox {
                    background-color: #2D2D2D;
                    color: #FFFFFF;
                    border: 1px solid #555555;
                    border-radius: 5px;
                    padding: 5px;
                    font-size: 14px;
                }
                QLineEdit {
                    background-color: #2D2D2D;
                    color: #FFFFFF;
                    border: 1px solid #555555;
                    border-radius: 5px;
                    padding: 8px;
                    font-size: 14px;
                }
                QWidget#mainContent {
                    background-color: #2D2D2D;
                    border-radius: 10px;
                    padding: 20px;
                }
                QPushButton#btnToggleMode {
                    font-size: 18px;
                    background-color: transparent;
                    border: none;
                }
            """
            )
        else:
            self.btnToggleMode.setText("☀️")

            # Áp dụng light mode
            self.setStyleSheet(
                """
                QMainWindow {
                    background-color: #FFFFFF;
                }
                QLabel {
                    color: #333333;
                }
                QLabel#labelTitle {
                    font-size: 28px;
                    font-weight: bold;
                    color: #1976D2;
                }
                QPushButton {
                    background-color: #2196F3;
                    color: white;
                    border-radius: 5px;
                    padding: 10px;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #1976D2;
                }
                QTextEdit {
                    background-color: #F5F5F5;
                    color: #333333;
                    border: 1px solid #DDDDDD;
                    border-radius: 5px;
                    padding: 10px;
                    font-size: 14px;
                }
                QComboBox {
                    background-color: #F5F5F5;
                    color: #333333;
                    border: 1px solid #DDDDDD;
                    border-radius: 5px;
                    padding: 5px;
                    font-size: 14px;
                }
                QLineEdit {
                    background-color: #F5F5F5;
                    color: #333333;
                    border: 1px solid #DDDDDD;
                    border-radius: 5px;
                    padding: 8px;
                    font-size: 14px;
                }
                QWidget#mainContent {
                    background-color: #FFFFFF;
                    border-radius: 10px;
                    padding: 20px;
                }
                QPushButton#btnToggleMode {
                    font-size: 18px;
                    background-color: transparent;
                    border: none;
                }
            """
            )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
