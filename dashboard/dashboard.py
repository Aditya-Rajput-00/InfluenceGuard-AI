import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="InfluenceGuard AI", layout="wide")

df = pd.read_csv("D:\\Project\\InfluenceGuard-AI\\data\\processed_influencers.csv")

st.markdown(
    """
    <h1 style='font-size:45px;'>
    AI-Powered Fake Influencer Detection
    </h1>

    <h3 style='color:gray;'>
    Brand Trust Analytics Dashboard
    </h3>
    """,
    unsafe_allow_html=True,
)

st.sidebar.header("Filter Influencers")

st.sidebar.markdown("---")

st.sidebar.markdown("### InfluenceGuard AI")

st.sidebar.caption("AI-Powered Influencer Risk Analytics Platform")

country = st.sidebar.selectbox("Select Country", df["Audience Country"].unique())

filtered_df = df[df["Audience Country"] == country]

total_influencers = len(filtered_df)

avg_engagement = round(filtered_df["Engagement Rate"].mean(), 2)

high_risk = len(filtered_df[filtered_df["Fake Score"] > 40])

avg_trust = round(filtered_df["Trust Score"].mean(), 2)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Influencers", total_influencers)

col2.metric("Avg Engagement", avg_engagement)

col3.metric("High Risk Accounts", high_risk)

col4.metric("Avg Trust Score", avg_trust)

st.dataframe(filtered_df.head())

tab1, tab2, tab3 = st.tabs(["Overview", "AI Insights", "Risk Analysis"])

with tab1:

    top_10 = filtered_df.nlargest(10, "Followers")

    fig = px.bar(
        top_10,
        x="Name",
        y="Followers",
        color="Trust Score",
        title="Top 10 Influencers by Followers",
    )

    st.plotly_chart(fig)

with tab2:

    fig2 = px.histogram(
        filtered_df, x="Engagement Rate", nbins=30, title="Engagement Rate Distribution"
    )

    fig3 = px.scatter(
        filtered_df,
        x="Followers",
        y="Engagement Rate",
        color="Anomaly",
        hover_data=["Name"],
        title="AI Anomaly Detection",
    )

    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(fig2, use_container_width=True)

    with col2:
        st.plotly_chart(fig3, use_container_width=True)

with tab3:

    st.subheader("High Risk Influencers")

    high_risk_df = filtered_df[filtered_df["Fake Score"] > 40]

    st.dataframe(
        high_risk_df[
            ["Name", "Followers", "Engagement Rate", "Fake Score", "Trust Score"]
        ]
    )

    csv = filtered_df.to_csv(index=False)

    st.download_button(
        label="Download Processed Data",
        data=csv,
        file_name="processed_influencers.csv",
        mime="text/csv",
    )

category_data = filtered_df["Category"].value_counts().head(5).reset_index()

category_data.columns = ["Category", "Count"]

fig_pie = px.pie(
    category_data, names="Category", values="Count", title="Top Influencer Categories"
)

st.plotly_chart(fig_pie, use_container_width=True)
