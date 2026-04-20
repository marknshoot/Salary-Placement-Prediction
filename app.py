import streamlit as st
import requests
import plotly.graph_objects as go
import joblib
import pandas as pd

st.set_page_config(page_title="Placement & Salary Prediction", layout="wide")

classifier = joblib.load('classifier.pkl')
regressor = joblib.load('regressor.pkl')


def make_prediction(features):
    df = pd.DataFrame([features])
    
    placement = classifier.predict(df)[0]
    
    if placement == 0:
        return {"placement_prediction": 0, "salary_prediction": None}
    
    salary = regressor.predict(df)[0]
    return {"placement_prediction": 1, "salary_prediction": float(salary)}


# ---------- SIDEBAR: INPUTS ----------
st.sidebar.title("Student Input")

with st.sidebar.expander("📊 Academic", expanded=True):
    ssc_percentage = st.number_input("SSC Percentage", 0, 100, 80)
    hsc_percentage = st.number_input("HSC Percentage", 0, 100, 80)
    degree_percentage = st.number_input("Degree Percentage", 0, 100, 80)
    cgpa = st.number_input("CGPA", 0.0, 10.0, 8.0)
    entrance_exam_score = st.number_input("Entrance Exam Score", 0, 100, 80)
    backlogs = st.number_input("Backlogs", 0, None, 0)

with st.sidebar.expander("💼 Skills & Experience", expanded=True):
    technical_skill_score = st.number_input("Technical Skill Score", 0, 100, 80)
    soft_skill_score = st.number_input("Soft Skill Score", 0, 100, 80)
    internship_count = st.number_input("Internship Count", 0, 10, 0)
    live_projects = st.number_input("Live Projects", 0, 20, 0)
    work_experience_months = st.number_input("Work Experience (Months)", 0, 120, 0)
    certifications = st.number_input("Certifications", 0, 20, 0)

with st.sidebar.expander("👤 Personal", expanded=True):
    gender = st.selectbox("Gender", ["Male", "Female"], index=0)
    attendance_percentage = st.number_input("Attendance Percentage", 0, 100, 80)
    extracurricular_activities = st.selectbox("Extracurricular Activities", ["Yes", "No"], index=0)

predict_clicked = st.sidebar.button("🔮 Predict Placement & Salary", use_container_width=True)


# ---------- MAIN: DASHBOARD ----------
st.title("Placement & Salary Prediction Dashboard")
st.divider()

# Row 1 — Unified profile row: CGPA, Attendance battery, Gender, Extracurricular, Backlogs
col1, col2, col3, col4, col5 = st.columns([1, 2, 1, 1.2, 1])

with col1:
    st.caption("CGPA")
    st.markdown(f"## {cgpa:.2f}")

with col2:
    st.caption("Attendance")
    # Odometer gauge — red (low) → green (high) gradient
    if attendance_percentage >= 80:
        bar_color = "#22C55E"   # green
    elif attendance_percentage >= 60:
        bar_color = "#84CC16"   # lime
    elif attendance_percentage >= 40:
        bar_color = "#EAB308"   # yellow
    elif attendance_percentage >= 20:
        bar_color = "#F97316"   # orange
    else:
        bar_color = "#EF4444"   # red

    gauge_fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=attendance_percentage,
        number={"suffix": "%", "font": {"size": 28}},
        gauge={
            "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "gray"},
            "bar": {"color": bar_color, "thickness": 0.8},
            "bgcolor": "rgba(0,0,0,0)",
            "borderwidth": 1,
            "bordercolor": "lightgray",
            "steps": [
                {"range": [0, 20], "color": "rgba(239, 68, 68, 0.15)"},
                {"range": [20, 40], "color": "rgba(249, 115, 22, 0.15)"},
                {"range": [40, 60], "color": "rgba(234, 179, 8, 0.15)"},
                {"range": [60, 80], "color": "rgba(132, 204, 22, 0.15)"},
                {"range": [80, 100], "color": "rgba(34, 197, 94, 0.15)"},
            ],
        }
    ))
    gauge_fig.update_layout(
        height=140,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(gauge_fig, use_container_width=True, config={"displayModeBar": False})

with col3:
    st.caption("Gender")
    icon = "♂️" if gender == "Male" else "♀️"
    st.markdown(f"## {icon} {gender}")

with col4:
    st.caption("Extracurricular")
    icon = "✅" if extracurricular_activities == "Yes" else "❌"
    st.markdown(f"## {icon} {extracurricular_activities}")

with col5:
    st.caption("Backlogs")
    if backlogs > 0:
        st.markdown(f"## :red[⚠️ {backlogs}]")
    else:
        st.markdown(f"## ✅ {backlogs}")


st.divider()

# Row 2 — Radar (left) + Skills/Experience bars (right)
left_col, right_col = st.columns([1, 1])

with left_col:
    st.markdown("**Academic Profile**")
    web = go.Figure()
    web.add_trace(go.Scatterpolar(
        r=[ssc_percentage, hsc_percentage, degree_percentage, cgpa * 10, entrance_exam_score],
        theta=["SSC %", "HSC %", "Degree %", "CGPA ×10", "Entrance"],
        fill="toself",
        name="Student",
        line=dict(color="#4C9AFF")
    ))
    web.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=False,
        height=320,
        margin=dict(l=40, r=40, t=20, b=20)
    )
    st.plotly_chart(web, use_container_width=True)

with right_col:
    st.markdown("**Skill Scores**")
    skills = go.Figure(go.Bar(
        x=[technical_skill_score, soft_skill_score],
        y=["Technical", "Soft"],
        orientation="h",
        marker=dict(color=["#4C9AFF",  "#FA69B4" ]),
        text=[technical_skill_score, soft_skill_score],
        textposition="outside"
    ))
    skills.update_layout(
        xaxis=dict(range=[0, 110], title="Score"),
        height=140,
        margin=dict(l=20, r=20, t=10, b=20)
    )
    st.plotly_chart(skills, use_container_width=True)

    st.markdown("**Experience Counts**")
    experience = go.Figure()
    experience.add_trace(go.Bar(
        x=["Internships", "Projects", "Certs"],
        y=[internship_count, live_projects, certifications],
        name="Count",
        marker=dict(color="#38B2AC"),
        yaxis="y"
    ))
    experience.add_trace(go.Bar(
        x=["Work Months"],
        y=[work_experience_months],
        name="Months",
        marker=dict(color="#F6AD55"),
        yaxis="y2"
    ))
    experience.update_layout(
        yaxis=dict(title="Count", side="left"),
        yaxis2=dict(title="Months", side="right", overlaying="y"),
        height=150,
        margin=dict(l=20, r=20, t=10, b=30),
        legend=dict(orientation="h", y=-0.3)
    )
    st.plotly_chart(experience, use_container_width=True)

st.divider()

# ---------- PREDICTION SECTION ----------
st.subheader("Prediction Result")

if predict_clicked:
    features = {
        "backlogs": int(backlogs),
        "cgpa": float(cgpa),
        "technical_skill_score": int(technical_skill_score),
        "soft_skill_score": int(soft_skill_score),
        "ssc_percentage": int(ssc_percentage),
        "hsc_percentage": int(hsc_percentage),
        "degree_percentage": int(degree_percentage),
        "entrance_exam_score": int(entrance_exam_score),
        "internship_count": int(internship_count),
        "live_projects": int(live_projects),
        "work_experience_months": int(work_experience_months),
        "certifications": int(certifications),
        "attendance_percentage": int(attendance_percentage),
        "gender": gender,
        "extracurricular_activities": extracurricular_activities
    }

    result = make_prediction(features)

    if result is not None:
        placement = result.get("placement_prediction")
        salary = result.get("salary_prediction")

        p1_col, p2_col = st.columns(2)
        with p1_col:
            if placement == 1:
                st.success("### ✅ Placed")
            else:
                st.error("### ❌ Not Placed")
        with p2_col:
            if placement == 1:
                st.success(f"### 💰 Estimated Salary\n## {salary:,.2f}")
            else:
                st.info("### No salary estimate\n*Student predicted as not placed.*")
else:
    st.info("Fill in the student data in the sidebar and click **Predict** to see the result.")