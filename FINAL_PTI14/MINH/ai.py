# API key cho Gemini
# Lưu ý: Bạn nên quản lý API key của mình một cách an toàn, ví dụ như sử dụng biến môi trường.
API_KEY = "---"

from google import genai
import google.generativeai as genai

def get_answer(text, level):
    """
    Gửi bài viết đến Gemini API để đánh giá

    Args:
        text (str): Bài viết cần đánh giá
        level (str): Trình độ học sinh (Beginner/Intermediate/Advanced)

    Returns:
        str: Phản hồi từ AI
    """
    try:
        genai.configure(api_key=API_KEY)

        model = genai.GenerativeModel('gemini-2.5-flash')

        role_info = f"""
        Bạn là giáo viên chấm bài viết tiếng Anh.
        Bạn sẽ nhận được một bài viết tiếng Anh của học sinh trình độ {level}.
        Mong bạn hãy chấm điểm rất chặt chẽ nếu người dùng là Advanced, chấm điểm ít chặt chẽ hơn đối với Intermediate, 
        chấm điểm rất nhẹ tay đối với Beginner.
        Hãy đánh giá dựa trên level của học sinh và nhận xét theo các tiêu chí:
        - Ngữ pháp (Grammar)
        - Từ vựng (Vocabulary)
        - Cấu trúc (Structure) 
        - Ý tưởng (Ideas)
        - Gợi ý cải thiện (Suggestions for improvement)
        - Phân tích từ vựng (cái này có thể cho ngắn)
        - Trả về bài viết được viết lại tốt hơn cho người dùng tham khảo
        - Cho các Video Youtube cho người dùng để giúp người dùng cải thiện.

        Cuối cùng, hãy cho điểm bài viết trên thang điểm 10.

        Trả về định dạng text cơ bản, chia các ý theo gạch đầu dòng, không dùng markdown.
        """

        question = (
            f"Đánh giá bài viết tiếng Anh này của học sinh trình độ {level}:\n\n{text}"
        )

        # Gemini sử dụng một định dạng hơi khác cho các cuộc hội thoại nhiều lượt
        # Ở đây chúng ta sẽ bắt đầu một cuộc trò chuyện mới mỗi lần để đơn giản.
        chat = model.start_chat(history=[
            {
                "role": "user",
                "parts": [role_info]
            },
            {
                "role": "model",
                "parts": ["Tôi đã sẵn sàng để chấm bài."]
            }
        ])

        response = chat.send_message(question)

        return response.text

    except Exception as e:
        return f"Lỗi khi kết nối với AI: {str(e)}"


def ask_question(essay, feedback, question, level):
    """
    Gửi câu hỏi thêm về bài viết đến Gemini API

    Args:
        essay (str): Bài viết gốc
        feedback (str): Phản hồi đã có
        question (str): Câu hỏi của học sinh
        level (str): Trình độ học sinh

    Returns:
        str: Phản hồi từ AI
    """
    try:
        genai.configure(api_key=API_KEY)

        model = genai.GenerativeModel('gemini-2.5-flash')

        # Xây dựng lại lịch sử trò chuyện để cung cấp ngữ cảnh
        history = [
            {
                "role": "user",
                "parts": [f"Bạn là giáo viên tiếng Anh đang hỗ trợ học sinh trình độ {level}."]
            },
            {
                "role": "model",
                "parts": ["Được thôi, tôi sẽ giúp."]
            },
            {
                "role": "user",
                "parts": [f"Bài viết của học sinh:\n{essay}\n\nĐánh giá của bạn:\n{feedback}"]
            },
            {
                "role": "model",
                "parts": ["Tôi đã xem lại bài viết và phản hồi của mình."]
            }
        ]
        
        chat = model.start_chat(history=history)
        response = chat.send_message(question)

        return response.text

    except Exception as e:
        return f"Lỗi khi kết nối với AI: {str(e)}"


