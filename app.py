import streamlit as st
import urllib.parse

st.set_page_config(page_title="Death Battle AI Master", page_icon="⚔️", layout="wide")

st.title("⚔️ Death Battle AI Master Prompt Generator")
st.caption("Tạo Prompt chuẩn Endless Fictional Arena, VSBW & DBVN 2.5 để chat trực tiếp trên ChatGPT / Gemini / DuckDuckGo AI.")

# Form nhập thông tin kèo đấu
with st.form("versus_form"):
    char1 = st.text_input("Nhân vật 1 (ví dụ: CC Goku):")
    char2 = st.text_input("Nhân vật 2 (ví dụ: Cosmic Armor Superman):")
    condition = st.text_input("Điều kiện trận đấu (ví dụ: Speed Equalized, Bloodlust, SBA):", value="Standard Battle Assumptions (SBA)")
    
    submitted = st.form_submit_button("🔥 Tạo Prompt & Phân Tích")

if submitted and char1 and char2:
    full_prompt = f"""
Bạn là "Death Battle Master AI" - Chuyên gia phân tích Versus Debating đỉnh cao tích hợp dữ liệu chuẩn từ:
1. Endless Fictional Arena Wiki (EFA)
2. VS Battles Wiki (VSBW)
3. Group DBVN 2.5, Endless Fictional (EF) và TikTok Death Battle VN.

Hãy phân tích kèo đấu: {char1} vs {char2}
Điều kiện: {condition}

CẤU TRÚC PHÂN TÍCH:
1. STATS OVERVIEW (Tier, AP/DC, Speed, Lifting/Striking Strength, Durability theo VSBW/EFA)
2. HAX & RESISTANCE ANALYSIS (Liệt kê Hax nổi bật, Kháng Hax)
3. FEATS & PROOF EVALUATION (Phân tích chiến tích, Anti-Feat, Outlier)
4. BATTLE SCENARIO & COUNTER (Kịch bản giao đấu, tương tác Hax)
5. FINAL VERDICT (% Tỷ lệ thắng + Winner)
"""
    st.success("✅ Đã tạo Prompt chuẩn!")
    st.text_area("Prompt của bạn (Có thể copy):", full_prompt, height=250)
    
    # Tạo đường dẫn mở nhanh các trang AI miễn phí
    encoded_prompt = urllib.parse.quote(full_prompt)
    
    col1, col2 = st.columns(2)
    with col1:
        st.link_button("🚀 Chat ngay trên ChatGPT (Miễn phí)", f"https://chatgpt.com/?q={encoded_prompt}", use_container_width=True)
    with col2:
        st.link_button("🚀 Chat ngay trên DuckDuckGo AI (Không cần tài khoản)", "https://duckduckgo.com/chat", use_container_width=True)
