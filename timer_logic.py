import time
import streamlit as st

def countdown(minutes, label):
    with st.empty():
        for sec in range(minutes * 60, 0, -1):
            mins, secs = divmod(sec, 60)
            st.markdown(f"**{label} 남은 시간: {mins:02d}:{secs:02d}**")
            time.sleep(1)

def run_pomodoro(focus_time, break_time, rounds):
    total_focus = 0

    for i in range(1, rounds + 1):
        st.write(f"## 🔵 라운드 {i}: 집중 {focus_time}분")
        countdown(focus_time, "⏳ 집중")
        total_focus += focus_time

        if i < rounds:
            st.write(f"### ⏸ 휴식 {break_time}분")
            countdown(break_time, "🌿 휴식")

    return total_focus