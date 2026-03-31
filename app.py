import json
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="フィードバック資料", layout="wide")

DATA = Path(__file__).parent / "data"

metadata = json.loads((DATA / "metadata.json").read_text(encoding="utf-8"))
scores = pd.read_csv(DATA / "scores.csv")
category_summary = pd.read_csv(DATA / "category_summary.csv")

st.title("フィードバック資料（クラウド版）")

st.write(f"部門：{metadata['department_name']}")
st.write(f"回答者数：{metadata['org_response_sample']}")

st.subheader("カテゴリ別スコア")

fig = px.bar(category_summary, x="カテゴリ", y="今回")
st.plotly_chart(fig)
