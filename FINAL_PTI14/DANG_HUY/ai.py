
import pandas as pd
import io
import os

API_KEY ="---"

from google import genai

client = genai.Client(api_key=API_KEY)




def generate_content(topic, content):
    
    prompt = f"""Tạo file csv chứa nội dung 15 câu hỏi trắc nghiệm về chủ đề: {topic}.
Nội dung cụ thể:
{content}


---

Chú ý chỉ trả về nội dung csv để tôi dùng code python gen ra file excel luôn để import vào quizizz, không giải thích gì thêm
Ngôn ngữ của câu hỏi giống ngôn ngữ của chủ đề và nội dung cụ thể
---
Tuân thủ nghiêm ngặt theo mẫu dưới đây:
Question Text,Question Type,Option 1,Option 2,Option 3,Option 4,Option 5,Correct Answer,Time in seconds,Image Link,Answer explanation
"Text of the question

(required)


","Question Type

(default is Multiple Choice)

","Text for option 1

(required in all cases except open-ended & draw questions)","Text for option 2

(required in all cases except open-ended & draw questions)","Text for option 3

(optional)


","Text for option 4

(optional)


","Text for option 5

(optional)


","The correct option choice (between 1-5).

Leave blank for ""Open-Ended"", ""Poll"", ""Draw"" and ""Fill-in-the-Blank"".","Time in seconds

(optional, default value is 30 seconds)
","Link of the image

(optional)


","Explanation for the answer
(optional)


"
Which of these is the largest planet in the Solar System?,Multiple Choice,Earth,Mars,Mercury,Jupiter,Pluto,4,20,https://cdn.pixabay.com/photo/2014/09/08/09/24/solar-system-439046_1280.jpg,"Jupiter is a gas giant made primarily of hydrogen and helium. Unlike terrestrial planets that have solid surfaces, gas giants like Jupiter don't have a well-defined solid surface, allowing them to accumulate more mass in a gaseous form. This composition has allowed Jupiter to grow significantly larger than planets with solid surfaces."
Which of these celestial bodies are planets?,Checkbox,Venus,Neptune,Uranus,Pluto,,"1,2,3",45,https://upload.wikimedia.org/wikipedia/commons/7/71/Protoplanetary-disk.jpg,
Name any one of the two moons of Mars,Fill-in-the-Blank,Phobos,Deimos,,,,,60,https://upload.wikimedia.org/wikipedia/commons/2/2f/PIA17352-MarsMoons-PhobosPassesDeimos-RealTime.gif,
What would you do in outer space?,Open-Ended,,,,,,,180,,
Which of these is your favorite?,Poll,Stars,Planets,Comets,,,,20,,
How are you feeling today (Draw an emoji),Draw,,,,,,,20,,
"""
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )
    return response.text

def csv_to_excel(csv_text, output_filename):
    """
    Nhận vào một chuỗi văn bản có định dạng CSV và xuất ra một file Excel.
    
    Args:
        csv_text (str): Chuỗi văn bản chứa dữ liệu CSV.
        output_filename (str): Tên của file Excel đầu ra (ví dụ: 'quiz_data.xlsx').
    """
    if not output_filename.endswith('.xlsx'):
        output_filename += '.xlsx'
        
    try:
        # Sử dụng io.StringIO để đọc chuỗi văn bản như một file
        # Điều này tránh việc phải tạo một file .csv tạm thời
        csv_file_like_object = io.StringIO(csv_text)
        
        # Đọc dữ liệu CSV bằng pandas
        df = pd.read_csv(csv_file_like_object, engine='python')
        
        # Xuất DataFrame ra file Excel
        # index=False để không ghi cột chỉ số (0, 1, 2...) của pandas vào file Excel
        df.to_excel(output_filename, index=False)
        
        print(f"Thành công! File Excel đã được tạo tại: {os.path.abspath(output_filename)}")
        
    except ImportError:
        print("Thư viện 'pandas' hoặc 'openpyxl' chưa được cài đặt.")
        print("Vui lòng chạy lệnh: pip install pandas openpyxl")
    except Exception as e:
        print(f"Đã xảy ra lỗi khi tạo file Excel: {e}")
        
        
