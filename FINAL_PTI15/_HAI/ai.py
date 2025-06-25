# ai.py - Xử lý tóm tắt văn bản bằng AI
# File này chứa hàm tóm tắt văn bản sử dụng Google Gemini AI

# Khóa API Google Gemini - Lưu ý: Trong thực tế nên lưu trong file riêng hoặc biến môi trường
API_KEY = "---"

from google import genai

# Khởi tạo client với API key
client = genai.Client(api_key=API_KEY)

def summarize_text(text, length, format):
    """
    Tóm tắt văn bản sử dụng Google Gemini AI
    
    Args:
        text: văn bản cần tóm tắt
        length: độ dài mong muốn ("Ngắn", "Trung bình", "Dài")
        format: định dạng tóm tắt ("Đoạn Văn", "Gạch Đầu Dòng")
    
    Returns:
        Văn bản đã được tóm tắt
    """
    try:
        # Chuyển đổi độ dài thành số từ
        length_mapping = {
            "Ngắn": "50-100",
            "Trung bình": "150-250",
            "Dài": "300-500"
        }
        
        # Chuyển đổi định dạng
        format_mapping = {
            "Đoạn Văn": "dạng đoạn văn liên tục",
            "Gạch Đầu Dòng": "dạng danh sách gạch đầu dòng với các ý chính"
        }
        
        # Tạo prompt cho AI
        prompt = f"""
        Nhiệm vụ: Tóm tắt văn bản dưới đây.
        
        Yêu cầu:
        - Độ dài: {length_mapping.get(length, "150-250")} từ
        - Định dạng: {format_mapping.get(format, "dạng đoạn văn liên tục")}
        - Sử dụng tiếng Việt
        - Giữ lại các thông tin quan trọng nhất
        - Chỉ trả về nội dung tóm tắt, không giải thích gì thêm
        - Không thêm các kí tự định dạng đặc biệt, chỉ trả về plain text
        ---
        Văn bản cần tóm tắt:
        {text}
        """
        
        # Gọi API để tóm tắt
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",  # Sử dụng model mới nhất
            contents=prompt,
        )
        
        # Trả về kết quả tóm tắt
        return response.text
    
    except Exception as e:
        # Nếu có lỗi, trả về thông báo lỗi
        error_message = f"Lỗi khi tóm tắt văn bản: {str(e)}"
        print(error_message)
        return error_message

