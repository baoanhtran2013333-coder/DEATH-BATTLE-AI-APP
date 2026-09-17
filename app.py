import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(page_title="Death Battle AI Master", page_icon="⚔️", layout="wide")

st.title("⚔️ Death Battle AI Master (VSBw & DBVN Standard)")
st.caption("AI tự động tra cứu, phân tích Feat, Hax, Speed Blitz và đưa ra Verdict chuẩn VSBattles Wiki.")

# Lấy API Key từ Streamlit Secrets nếu có, nếu không thì lấy từ input của người dùng
default_api_key = st.secrets.get("GEMINI_API_KEY", "")

user_api_key = st.sidebar.text_input(
    "Nhập Google Gemini API Key:", 
    value=default_api_key, 
    type="password",
    help="Nếu đã cài API Key trong Secrets thì không cần nhập thêm."
)
st.sidebar.markdown("[Lấy API Key miễn phí tại đây](https://aistudio.google.com/)")

api_key = user_api_key or default_api_key

SYSTEM_PROMPT = """
Bạn là "Death Battle Master AI" - Chuyên gia phân tích Power Scaling, Versus Debating theo chuẩn VS Battles Wiki và cộng đồng Death Battle VN 2.5.

NHIỆM VỤ:
Khi người dùng đưa ra một kèo đấu, bạn TỰ ĐỘNG tra cứu kiến thức về nhân vật và phân tích theo cấu trúc bên dưới. KHÔNG yêu cầu người dùng nhập chỉ số hay tự điền điểm thủ công.

CẤU TRÚC PHÂN TÍCH CHUẨN:
1. STATS OVERVIEW (TỔNG QUAN CHỈ SỐ):
   - Nhân vật A & B: Tên, Verse gốc.
   - AP / Durability Tier: Xác định theo VSBw (Street, Building, City, Planet, Multiversal, Outerversal...).
   - Speed Tier: Subsonic, FTL, MFTL+, Infinite, Immeasurable, hay Irrelevant.

2. HAX & RESISTANCE ANALYSIS:
   - Liệt kê các Hax nổi bật (Time Stop, Existence Erasure, Reality Warping...).
   - Kiểm tra Resistance: Hax của A có bị Resistance của B vô hiệu hóa dựa trên Feat thực tế trong tác phẩm không?
   - Phân loại: Low-Tier Hax vs Conceptual/High-Tier Hax.

3. WIN-CONS & SPEED BLITZ:
   - Đánh giá khả năng Speed Blitz.
   - Dimensional Outscale (nếu có).

4. BATTLE SCENARIO:
   - Mô tả diễn biến giao tranh ngắn gọn (3-5 câu), giữ đúng tính cách nhân vật và cách các năng lực tương tác.

5. FINAL VERDICT:
   - Tỷ lệ thắng (% Victory).
   - Tuyên bố nhân vật chiến thắng kèm lý do cốt lõi nhất.
"""

matchup = st.text_input("Nhập kèo đấu (Ví dụ: UI Daniel vs Sukuna hoặc Gojo vs Rick):")

if st.button("Phân Tích Kèo Đấu 💥"):
    if not api_key:
        st.error("Vui lòng nhập Gemini API Key ở thanh bên trái!")
    elif not matchup:
        st.warning("Vui lòng nhập tên kèo đấu!")
    else:
        with st.spinner("AI đang tra cứu dữ liệu nhân vật và phân tích..."):
            try:
                client = genai.Client(api_key=api_key)
                response = client.models.generate_content(
                    model='gemini-3.6-flash',
                    contents=matchup,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_PROMPT,
                        temperature=0.7
                    )
                )
                if response and hasattr(response, 'text'):
                    st.markdown("---")
                    st.markdown(response.text)
                else:
                    st.error("Không nhận được phản hồi từ AI. Vui lòng thử lại!")
            except Exception as e:
                st.error(f"Lỗi kết nối Gemini API: {e}")
