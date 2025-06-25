# ai.py - Xử lý tóm tắt văn bản bằng AI
# File này chứa hàm tóm tắt văn bản sử dụng Google Gemini AI

# Khóa API Google Gemini - Lưu ý: Trong thực tế nên lưu trong file riêng hoặc biến môi trường
API_KEY = "---"

from google import genai

# Khởi tạo client với API key
client = genai.Client(api_key=API_KEY)

def create_outline(text):
    """
    Tạo kịch bản video TikTok từ ý tưởng của người dùng bằng AI.
    Args:
        text: văn bản cần tạo kịch bản
    Returns:
        Kịch bản video tiktok được tạo ra từ AI
    """
    try:
        # Chuyển đổi định dạng
        # Tạo prompt cho AI
        prompt = f"""
        Nhiệm vụ: Gợi ý kịch bản video tiktok dựa trên ý tưởng của người dùng.
        
        Yêu cầu:
        - Sử dụng tiếng Việt
        - Không thêm các kí tự định dạng đặc biệt, chỉ trả về plain text
        ---
        Ý tưởng của người dùng
        {text}
        """
        
        # Gọi API để tạo dàn ý
        response = client.models.generate_content(
            model="gemini-2.5-flash",  # Sử dụng model mới nhất
            contents=prompt,
        )
        
        # Trả về kết quả dàn ý
        return response.text
    
    except Exception as e:
        # Nếu có lỗi, trả về thông báo lỗi
        error_message = f"Lỗi khi tạo kịch bản: {str(e)}"
        print(error_message)
        return error_message

