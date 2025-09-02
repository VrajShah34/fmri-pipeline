import streamlit as st
import pandas as pd
import json
import matplotlib.pyplot as plt
import plotly.express as px
import os

# Paths
OUT_DIR = "hda7_outputs"
DATA_PATH = "secondary_dataset.csv"
REPORT_PATH = os.path.join(OUT_DIR, "report_summary.json")
FI_PATH = os.path.join(OUT_DIR, "permutation_importance.csv")
ABLATION_PATH = os.path.join(OUT_DIR, "ablation_results.csv")

st.set_page_config(page_title="HDA-7 fMRI Dashboard", layout="wide")

# --- Sidebar Filters ---
st.sidebar.title("Filters")
label_filter = st.sidebar.selectbox("Select Group", ["All", "SocialAnxiety", "Control"])
subject_filter = st.sidebar.text_input("Filter by Subject ID (optional)", "")

# --- Load Data ---
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH, sep="\t" if "\t" in open(DATA_PATH).read(1000) else ",")
    return df

@st.cache_data
def load_report():
    with open(REPORT_PATH) as f:
        return json.load(f)

df = load_data()
report = load_report()

# --- Apply Filters ---
if label_filter != "All" and "Label" in df.columns:
    df = df[df["Label"] == label_filter]
if subject_filter:
    df = df[df["Subject_ID"].str.contains(subject_filter, case=False)]

# --- KPIs ---
st.title("📊 HDA-7: fMRI Connectivity Dashboard")

st.subheader("Key Performance Indicators (Final Model)")
kpi_cols = st.columns(4)
metrics = report["metrics"]

kpi_cols[0].metric("ROC-AUC", f"{metrics['roc_auc']:.3f}")
kpi_cols[1].metric("PR-AUC", f"{metrics['pr_auc']:.3f}")
kpi_cols[2].metric("Accuracy", f"{metrics['accuracy']:.3f}")
kpi_cols[3].metric("F1 Score", f"{metrics['f1']:.3f}")

st.write(f"Best Model: **{report['best_model']}**  |  Run: {report['timestamp']}")

# --- Feature Importance ---
if os.path.exists(FI_PATH):
    st.subheader("🔎 Feature Importance (Permutation)")
    fi = pd.read_csv(FI_PATH)
    fig = px.bar(fi.head(15), x="importance_mean", y="feature", orientation="h")
    st.plotly_chart(fig, use_container_width=True)

# --- Ablation Study ---
if os.path.exists(ABLATION_PATH):
    st.subheader("🧪 Ablation Study Results")
    ablation = pd.read_csv(ABLATION_PATH)
    fig = px.bar(ablation, x="group", y="roc_auc_mean", error_y="roc_auc_std", title="Ablation ROC-AUC by Feature Group")
    st.plotly_chart(fig, use_container_width=True)

# --- ROC/PR/Calibration ---
st.subheader("📈 Diagnostic Plots")
plot_cols = st.columns(3)
for idx, name in enumerate(["roc", "pr", "calibration"]):
    path = os.path.join(OUT_DIR, f"final_{report['best_model']}_{name}.png") if name != "calibration" \
           else os.path.join(OUT_DIR, f"calibration_{report['best_model']}.png")
    if os.path.exists(path):
        plot_cols[idx].image(path, caption=name.upper())

# --- Subject-Level Data ---
st.subheader("🧑‍🤝‍🧑 Subject-Level Connectivity Metrics")
st.dataframe(df)

# Optional CSV Download
st.download_button(
    label="Download Filtered Data as CSV",
    data=df.to_csv(index=False).encode("utf-8"),
    file_name="filtered_connectivity_data.csv",
    mime="text/csv",
)
