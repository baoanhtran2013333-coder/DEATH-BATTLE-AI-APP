import urllib.parse
import streamlit as st

# 1. Cấu hình giao diện Web Streamlit
st.set_page_config(
    page_title="Death Battle AI Master", page_icon="⚔️", layout="wide"
)

st.title("⚔️ Death Battle AI Master (EF Arena, VSBW & DBVN Standard)")
st.caption(
    "Hệ thống phân tích Feat, Hax & Meta Debate chuẩn Endless Fictional Arena,"
    " VSBattles Wiki và DBVN 2.5."
)

with st.sidebar:
  st.header("⚙️ Tùy chọn")
  if st.button("🔄 Tạo kèo đấu mới", use_container_width=True):
    st.session_state.chat_messages = []
    st.rerun()

# 2. Bộ tri thức Death Battle đóng gói sẵn
SYSTEM_PROMPT = """
Bạn là "Death Battle Master AI" - Chuyên gia phân tích Versus Debating đỉnh cao tích hợp dữ liệu chuẩn từ:
1. Endless Fictional Arena Wiki (EFA - https://endless-fictional-arena.fandom.com/vi/wiki/Endless_Fictional_Arena)
2. VS Battles Wiki (VSBW - https://vsbattles.fandom.com/wiki/VS_Battles_Wiki)
3. Quy chuẩn tranh luận tại cộng đồng Việt Nam: Group DBVN 2.5, Endless Fictional (EF) và TikTok Death Battle VN.

QUY CHUẨN ĐÁNH GIÁ & QUY TẮC PHÂN TÍCH:
- TIERING SYSTEM: Sử dụng chuẩn Tiering System của VSBW & EFA (Từ Tier 11 đến Tier 1-A, High 1-A, Tier 0: Boundless / True Infinity).
- HAX & POWER SYSTEM: Phân tích kỹ các loại Hax đặc trưng (Existence Erasure, Conceptual Manipulation, Causality Manipulation, Fate/Time Manipulation, Immortality Types 1-9, Non-Existent Physiology, Reality Warping, BFR...).
- SPEED TIER: Normal, Subsonic, SoL, FTL, MFTL+, Infinite Speed, Immeasurable Speed, Irrelevant Speed.
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

# Hiển thị lịch sử chat trên giao diện
for msg in st.session_state.chat_messages:
  with st.chat_message(msg["role"]):
    st.markdown(msg["content"])

# Xử lý khi người dùng nhập tin nhắn vào khung Chat
if prompt := st.chat_input(
    "Nhập kèo đấu hoặc gửi phản biện/scan (Ví dụ: cc goku vs saitama)..."
):
  # Lưu và hiển thị tin nhắn người dùng
  st.session_state.chat_messages.append({"role": "user", "content": prompt})
  with st.chat_message("user"):
    st.markdown(prompt)

  # Đóng gói Prompt chứa đầy đủ luật Death Battle
  full_prompt = f"{SYSTEM_PROMPT}\n\nYÊU CẦU PHÂN TÍCH KÈO ĐẤU:\n{prompt}"
  encoded_prompt = urllib.parse.quote(full_prompt)

  # Tạo link chuyển tiếp trực tiếp
  chatgpt_link = f"https://chatgpt.com/?q={encoded_prompt}"

  bot_reply = f"""
🎯 **Đã xử lý dữ liệu cho kèo:** `{prompt}`

Đoạn Prompt chuẩn cấu trúc EFA / VSBW / DBVN 2.5 đã được tạo xong:

```text
{full_prompt}
