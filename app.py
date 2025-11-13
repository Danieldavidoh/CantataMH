import json
import calendar
import streamlit as st
from datetime import datetime, date
import folium
from streamlit_folium import st_folium

# -----------------------------------------
# 1. 페이지 기본 설정
# -----------------------------------------
st.set_page_config(
    page_title="칸타타 투어 2025 캘린더",
    layout="wide"
)

st.title("🎵 칸타타 투어 2025 - 12월 공연 캘린더")
st.markdown("색상으로 공연 확률을 확인하고, 도시명을 클릭해 세부 정보를 보세요.")

# -----------------------------------------
# 2. JSON 불러오기
# -----------------------------------------
try:
    with open("tour_schedule.json", "r", encoding="utf-8") as f:
        tour_data = json.load(f)
except FileNotFoundError:
    st.error("⚠️ 'tour_schedule.json' 파일이 없습니다. 같은 폴더에 넣어주세요.")
    st.stop()

# -----------------------------------------
# 3. 데이터 정리
# -----------------------------------------
schedule = {}
for item in tour_data:
    d = datetime.strptime(item["date"], "%Y-%m-%d").day
    schedule[d] = {
        "city": item["city"],
        "possibility": item["possibility"]
    }

# -----------------------------------------
# 4. 색상 결정 함수
# -----------------------------------------
def get_color(possibility):
    if "100" in possibility:
        return "#9be39b"  # 초록
    elif "50" in possibility or "80" in possibility:
        return "#f5c36b"  # 노랑
    elif "20" in possibility or "10" in possibility or "0" in possibility:
        return "#f4a261"  # 주황
    else:
        return "#dddddd"  # 회색 (미정)

# -----------------------------------------
# 5. 12월 캘린더 생성
# -----------------------------------------
cal = calendar.Calendar(firstweekday=6)
month_days = cal.monthdayscalendar(2025, 12)
weekdays = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]

st.markdown("### 📅 December 2025")

# 요일 헤더
cols = st.columns(7)
for i, day in enumerate(weekdays):
    cols[i].markdown(f"**{day}**", unsafe_allow_html=True)

# 주 단위로 행 생성
for week in month_days:
    cols = st.columns(7)
    for i, day in enumerate(week):
        if day == 0:
            cols[i].markdown(" ")
        elif day in schedule:
            info = schedule[day]
            bg_color = get_color(info["possibility"])
            cols[i].markdown(
                f"""
                <div style='background:{bg_color}; border-radius:8px; padding:6px; text-align:center'>
                    <b>{day}</b><br>
                    <span style='font-size:13px'>{info["city"]}</span><br>
                    <span style='font-size:12px; color:#333'>{info["possibility"]}</span>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            cols[i].markdown(f"<div style='text-align:center'>{day}</div>", unsafe_allow_html=True)

# -----------------------------------------
# 6. 도시별 지도 표시
# -----------------------------------------
st.markdown("---")
st.subheader("🗺️ 공연 도시 지도")

city_coords = {
    "Nagpur": (21.1458, 79.0882),
    "Paratwada": (21.2673, 77.5263),
    "Buldhana": (20.5293, 76.1841),
    "Aurangabad": (19.8762, 75.3433),
    "Bandra": (19.0596, 72.8295),
    "Mumbai": (19.0760, 72.8777),
    "Ahmednagar": (19.0948, 74.7480),
    "Sangli": (16.8524, 74.5815),
    "Kolhapur": (16.7050, 74.2433),
    "Miraj": (16.8167, 74.6500),
    "Ichalkaranji": (16.6927, 74.4605),
    "Karad": (17.2898, 74.1816),
    "Kodoli": (16.8100, 74.3500),
    "Satara": (17.6805, 74.0183),
    "Adul": (20.3000, 75.5833),
    "Jawla Bazar": (19.3687, 76.6925),
    "Parbhani": (19.2700, 76.7700),
    "Shirur": (18.8253, 74.3753),
    "Palghar": (19.6969, 72.7699),
    "Ambernath": (19.1860, 73.1883),
    "Mira Road": (19.2842, 72.8681),
    "Wadala": (19.0169, 72.8581),
    "Solapur": (17.6599, 75.9064),
    "Nashik": (19.9975, 73.7898),
    "Pune": (18.5204, 73.8567)
}

# 지도 초기화
m = folium.Map(location=[19.5, 75.3], zoom_start=7, tiles="OpenStreetMap")

for item in tour_data:
    city_name = item["city"].split(",")[0].split("/")[0].strip()
    date_text = item["date"]
    possibility = item["possibility"]

    if city_name in city_coords:
        lat, lon = city_coords[city_name]
        folium.Marker(
            location=[lat, lon],
            popup=f"<b>{city_name}</b><br>날짜: {date_text}<br>가능성: {possibility}",
            tooltip=f"{city_name}",
            icon=folium.Icon(
                color="green" if "100" in possibility else "orange" if "50" in possibility else "red",
                icon="music",
                prefix="fa"
            )
        ).add_to(m)

st_folium(m, width=1000, height=600)
