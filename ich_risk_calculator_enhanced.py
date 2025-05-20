import streamlit as st
import matplotlib.pyplot as plt

# Configure the app layout
st.set_page_config(page_title="ICH Risk Calculator", layout="wide")

# App title and intro
st.title("ICHcal Prediction Score for Intracanial Hemorrhage Risk in AMI-CS")
st.markdown("Use the ICHcal prediction score to estimate intracranial hemorrhage (ICH) risk in patients with acute myocardial infarction complicated by cardiogenic shock (AMI-CS).")

# Display an expandable information section
with st.expander("ℹ️ About this Score"):
    st.write("""
    This scoring system estimates the risk of intracranial hemorrhage (ICH) in patients with AMI-CS using the following variables:

    - **VA-ECMO** = 9 points  
    - **Acute ischemic stroke** = 5 points  
    - **Thrombophilia** = 2 points  
    - **Microaxial MCS (e.g., Impella)** = 2 points  
    - **Sepsis** = 2 points  
    - **Thrombolysis** = 2 points  
    - **Acute kidney injury (AKI)** = 2 point  
    - **Age < 65 years** = 1 point  

    The total score maps to predicted ICH risk.
    """)

# Define risk factors and associated points
risk_factors = {
    "VA-ECMO": 9,
    "Acute ischemic stroke": 5,
    "Thrombophilia": 2,
    "Microaxial MCS (e.g., Impella)": 2,
    "Sepsis": 2,
    "Thrombolysis": 2,
    "Acute kidney injury (AKI)": 2,
    "Age < 65 years": 1
}

# Create checkboxes for input
st.markdown("### ✅ Select Risk Factors Present:")
score = 0
for factor, pts in risk_factors.items():
    if st.checkbox(factor):
        score += pts

# Define function for risk mapping
def get_risk(score):
    if score <= 5:
        return "0.53%", "Low"
    elif score <= 10:
        return "1.96%", "Moderate"
    elif score <= 15:
        return "7.97%", "High"
    else:
        return "22.91%", "Very High"

# Get risk result
risk_percent, category = get_risk(score)

# Display results with color coding
st.markdown("### 📊 Results")
st.markdown(f"**Total Score:** `{score}`")

if category == "Low":
    st.success(f"Low Risk of ICH: {risk_percent}")
elif category == "Moderate":
    st.info(f"Moderate Risk of ICH: {risk_percent}")
elif category == "High":
    st.warning(f"High Risk of ICH: {risk_percent}")
else:
    st.error(f"Very High Risk of ICH: {risk_percent}")

# Improved bar chart with more space and clean annotations
st.markdown("### 🔍 Risk Probability by Score Range")

fig, ax = plt.subplots(figsize=(6, 6))  # Taller figure = more space
score_ranges = ["0–5", "6–10", "11–15", ">15"]
risks = [0.53, 1.96, 7.97, 22.91]  # <- Updated first value here

bars = ax.bar(score_ranges, risks, color="#1f77b4")
ax.set_ylabel("ICH Risk (%)")
ax.set_xlabel("Total Score Range")
ax.set_title("Estimated ICH Risk by Score Category")

# Annotate percentages above bars with extra spacing
for bar, risk in zip(bars, risks):
    height = bar.get_height()
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        height + 1.5,
        f"{risk}%",
        ha='center',
        va='bottom',
        fontsize=10
    )

plt.ylim(0, 28)  # Extend y-axis for headroom
st.pyplot(fig)

git checkout -b update-aki-score
