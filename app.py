import streamlit as st
import requests

# 1. Cấu hình trang Streamlit
st.set_page_config(page_title="Death Battle AI Master", page_icon="⚔️", layout="wide")

st.title("⚔️ Death Battle AI Master (EF Arena, VSBW & DBVN Standard)")
st.caption("AI tra cứu Feat, Hax, Tiering System & Meta Debate chuẩn Endless Fictional Arena, VSBattles Wiki và DBVN 2.5.")

# 2. Tự động lấy API Key từ Streamlit Secrets
api_key = st.secrets.get("GROQ_API_KEY", "")

with st.sidebar:
    st.header("⚙️ Tùy chọn")
    if st.button("🔄 Tạo kèo đấu mới", use_container_width=True):
        st.session_state.chat_messages = []
        st.rerun()

# 3. System Prompt tích hợp toàn bộ tri thức EFA, VSBW & VS Debating VN
SYSTEM_PROMPT = """
Bạn là "Death Battle Master AI" - Chuyên gia phân tích Versus Debating đỉnh cao tích hợp dữ liệu chuẩn từ:
1. Endless Fictional Arena Wiki (EFA - https://endless-fictional-arena.fandom.com/vi/wiki/Endless_Fictional_Arena)
2. VS Battles Wiki (VSBW - https://vsbattles.fandom.com/wiki/VS_Battles_Wiki)
3. Quy chuẩn tranh luận tại cộng đồng Việt Nam: Group DBVN 2.5, Endless Fictional (EF) và TikTok Death Battle VN.

QUY CHUẨN ĐÁNH GIÁ & QUY TẮC PHÂN TÍCH:
- TIERING SYSTEM: Sử dụng chuẩn Tiering System của VSBW & EFA (Từ Tier 11: Lower Dimensional đến Tier 1-A: Outerverse, High 1-A, Tier 0: Boundless / True Infinity).
- HAX & POWER SYSTEM: Phân tích kỹ các loại Hax đặc trưng (Existence Erasure, Conceptual Manipulation, Causality Manipulation, Fate/Time Manipulation, Immortality Types 1-9, Non-Existent Physiology, Reality Warping, BFR...).
- SPEED TIER: Normal, Subsonic, Speed of Light (SoL), FTL, Massively FTL+, Infinite Speed, Immeasurable Speed, Irrelevant Speed.
- QUY TẮC DEBATE CỘNG ĐỒNG VN:
  + Bắt lỗi NLF (No Limits Fallacy), Highball/Wank vô căn cứ, Downplay cố tình, và Feat ảo (Outlier / Out of Context).
  + Yêu cầu Scan/Proof hoặc Feat cụ thể trong Manga/Comic/LN/VN thay vì tin tưởng vào Statement suông.
  + Xét kỹ Speed Equalized vs Speed Unequalized, Bloodlust, Prep time, Standard Battle Assumptions (SBA).

CẤU TRÚC PHÂN TÍCH CHUẨN:
1. STATS OVERVIEW (Tier, AP/DC, Speed, Lifting/Striking Strength, Durability theo VSBW/EFA)
2. HAX & RESISTANCE ANALYSIS (Liệt kê Hax nổi bật, Kháng Hax và Hax kháng lại đối thủ)
3. FEATS & PROOF EVALUATION (Phân tích các chiến tích đỉnh cao, Anti-Feat, Outlier)
4. BATTLE SCENARIO & COUNTER (Kịch bản giao đấu, tương tác Hax, khả năng Outsmart/Outspeed)
5. FINAL VERDICT (% Tỷ lệ thắng + Winner cụ thể theo chuẩn DBVN 2.5/EFA)
"""

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

# Hiển thị lịch sử chat
for msg in st.session_state.chat_messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Danh sách các mô hình chạy ổn định trên Groq
GROQ_MODELS = [
    "llama-3.1-8b-instant",
    "llama3-70b-8192",
    "mixtral-8x7b-32768"
]

if prompt := st.chat_input("Nhập kèo đấu hoặc gửi phản biện/scan/bằng chứng cho AI..."):
    if not api_key:
        st.error("⚠️ Chưa cài đặt GROQ_API_KEY trong Streamlit Secrets!")
    else:
        st.session_state.chat_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("AI đang tra cứu Feat, Hax & Meta Debate từ EFA, VSBW và DBVN..."):
                headers = {
                    "Authorization": f"Bearer {api_key.strip()}",
                    "Content-Type": "application/json"
                }

                messages_payload = [{"role": "system", "content": SYSTEM_PROMPT}]
                for m in st.session_state.chat_messages[-6:]:
                    messages_payload.append({"role": m["role"], "content": m["content"]})

                success = False
                last_error_msg = ""

                # Thử lần lượt từng model
                for model in GROQ_MODELS:
                    payload = {
                        "model": model,
                        "messages": messages_payload,
                        "temperature": 0.6
                    }
                    try:
                        res = requests.post(
                            "https://api.groq.com/openai/v1/chat/completions",
                            headers=headers,
                            json=payload,
                            timeout=30
                        )
                        data = res.json()
                        if res.status_code == 200 and "choices" in data:
                            bot_reply = data["choices"][0]["message"]["content"]
                            st.markdown(bot_reply)
                            st.session_state.chat_messages.append({"role": "assistant", "content": bot_reply})
                            success = True
                            break
                        else:
                            last_error_msg = data.get("error", {}).get("message", res.text)
                    except Exception as e:
                        last_error_msg = str(e)

                if not success:
                    st.error(f"Lỗi API Groq: {last_error_msg}")
