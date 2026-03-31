import json
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="フィードバック資料", layout="wide")

DATA = Path(__file__).parent / "data"

# データ読み込み
metadata = json.loads((DATA / "metadata.json").read_text(encoding="utf-8"))
scores = pd.read_csv(DATA / "scores.csv")
category_summary = pd.read_csv(DATA / "category_summary.csv")
top_rank = pd.read_csv(DATA / "top_rank.csv")
bottom_rank = pd.read_csv(DATA / "bottom_rank.csv")
engagement_layers = pd.read_csv(DATA / "engagement_layers.csv")
q18 = pd.read_csv(DATA / "q18.csv")
q32 = pd.read_csv(DATA / "q32.csv")

# タイトル
st.title("フィードバック資料（クラウド版）")

st.write(f"部門：{metadata['department_name']}")
st.write(f"回答者数：{metadata['org_response_sample']}")

# タブ
tab1, tab2, tab3, tab4 = st.tabs(["概要", "スコア", "5択以外", "ランキング"])

# ----------------------
# ■ 概要
# ----------------------
with tab1:
    st.subheader("カテゴリ別サマリー")

    summary = category_summary.copy()
    summary["前回差"] = summary["今回"] - summary["前回"]
    summary["全体差"] = summary["今回"] - summary["職員全体"]

    st.dataframe(summary, use_container_width=True)

    st.subheader("レーダーチャート")

    categories = summary["カテゴリ"].tolist()

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=summary["今回"].tolist(),
        theta=categories,
        fill='toself',
        name='今回'
    ))

    fig.add_trace(go.Scatterpolar(
        r=summary["前回"].tolist(),
        theta=categories,
        name='前回'
    ))

    fig.add_trace(go.Scatterpolar(
        r=summary["職員全体"].tolist(),
        theta=categories,
        name='全体'
    ))

    st.plotly_chart(fig, use_container_width=True)

# ----------------------
# ■ スコア
# ----------------------
with tab2:
    st.subheader("カテゴリ別スコア")

    fig = px.bar(category_summary, x="カテゴリ", y="今回")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("設問別スコア")

    st.dataframe(scores, use_container_width=True)

# ----------------------
# ■ 5択以外
# ----------------------
with tab3:
    st.subheader("エンゲージメント構成")

    layers = engagement_layers.melt(
        id_vars=["区分"],
        var_name="層",
        value_name="割合"
    )

    fig = px.bar(layers, x="区分", y="割合", color="層", barmode="stack")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Q18")

    q18_melt = q18.melt(id_vars=["選択肢"], var_name="時点", value_name="割合")
    fig = px.bar(q18_melt, x="割合", y="選択肢", color="時点", barmode="group")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Q32")

    q32_melt = q32.melt(id_vars=["選択肢"], var_name="時点", value_name="割合")
    fig = px.bar(q32_melt, x="割合", y="選択肢", color="時点", barmode="group")
    st.plotly_chart(fig, use_container_width=True)

# ----------------------
# ■ ランキング
# ----------------------
with tab4:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("上位")
        st.dataframe(top_rank, use_container_width=True)

    with col2:
        st.subheader("下位")
        st.dataframe(bottom_rank, use_container_width=True)
