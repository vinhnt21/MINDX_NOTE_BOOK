# ai.py - Xử lý tạo câu hỏi trắc nghiệm và chấm điểm bằng AI
# File này chứa hàm tạo câu hỏi trắc nghiệm và chấm điểm sử dụng Google Gemini AI

# Khóa API Google Gemini - Lưu ý: Trong thực tế nên lưu trong file riêng hoặc biến môi trường
API_KEY = "---"

from google import genai

# Khởi tạo client với API key
client = genai.Client(api_key=API_KEY)

def generate_questions(text, num_questions=5):
    """
    Tạo câu hỏi trắc nghiệm từ nội dung văn bản bằng AI.
    Args:
        text: nội dung văn bản cần tạo câu hỏi
        num_questions: số lượng câu hỏi cần tạo
    Returns:
        Chuỗi các câu hỏi trắc nghiệm được tạo ra từ AI
    """
    try:
        # Tạo prompt cho AI
        prompt = f"""
        Nhiệm vụ: Tạo {num_questions} câu hỏi trắc nghiệm từ nội dung sau.
        
        Yêu cầu:
        - Sử dụng tiếng Việt
        - Mỗi câu hỏi có 4 đáp án A, B, C, D
        - Đánh số thứ tự câu hỏi
        - Không thêm đáp án đúng vào kết quả
        - Định dạng: 
          Câu 1: [Nội dung câu hỏi]
          A) [Đáp án A]
          B) [Đáp án B]
          C) [Đáp án C]
          D) [Đáp án D]
        
        Nội dung:
        {text}
        """
        
        # Gọi API để tạo câu hỏi
        response = client.models.generate_content(
            model="gemini-2.5-flash",  # Sử dụng model mới nhất
            contents=prompt,
        )
        
        # Trả về kết quả câu hỏi
        return response.text
    
    except Exception as e:
        # Nếu có lỗi, trả về thông báo lỗi
        error_message = f"Lỗi khi tạo câu hỏi: {str(e)}"
        print(error_message)
        return error_message

def grade_answers(questions, user_answers):
    """
    Chấm điểm đáp án của người dùng bằng AI.
    Args:
        questions: chuỗi câu hỏi trắc nghiệm
        user_answers: chuỗi đáp án của người dùng (ví dụ: "A, B, C, D, A")
    Returns:
        Kết quả chấm điểm bao gồm điểm số và giải thích
    """
    try:
        # Tạo prompt cho AI chấm điểm
        prompt = f"""
        Nhiệm vụ: Chấm điểm bài trắc nghiệm.
        
        Câu hỏi:
        {questions}
        
        Đáp án của học sinh: {user_answers}
        
        Yêu cầu:
        - Đưa ra đáp án đúng cho từng câu
        - Tính điểm (mỗi câu đúng 1 điểm)
        - Giải thích ngắn gọn cho các đáp án
        - Định dạng kết quả:
          ĐIỂM: [số điểm]/[tổng số câu]
          
          Đáp án đúng:
          Câu 1: [đáp án] - [giải thích ngắn]
          Câu 2: [đáp án] - [giải thích ngắn]
          ...
          
          Nhận xét: [nhận xét chung về kết quả]
        """
        
        # Gọi API để chấm điểm
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        
        # Trả về kết quả chấm điểm
        return response.text
    
    except Exception as e:
        # Nếu có lỗi, trả về thông báo lỗi
        error_message = f"Lỗi khi chấm điểm: {str(e)}"
        print(error_message)
        return error_message

