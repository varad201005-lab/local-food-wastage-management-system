import pandas as pd
import streamlit as st
import plotly.express as px

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Local Food Wastage Management System",
    layout="wide"
)

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>

div[data-testid="metric-container"] {
    background-color: #F0F2F6;
    border: 2px solid #00C853;
    border-radius: 15px;
    padding: 20px;
    text-align: center;
    box-shadow: 0px 2px 10px rgba(0,0,0,0.15);
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

providers = pd.read_csv("providers_cleaned.csv")
receivers = pd.read_csv("receivers_cleaned.csv")
food = pd.read_csv("food_listings_cleaned.csv")
claims = pd.read_csv("claims_cleaned.csv")

# --------------------------------------------------
# KPI CALCULATIONS
# --------------------------------------------------

providers_count = len(providers)
receivers_count = len(receivers)
food_count = len(food)
claims_count = len(claims)

total_qty = food["Quantity"].sum()

completed_claims = len(
    claims[
        claims["Status"] == "Completed"
    ]
)

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("🍲 Food Wastage")
st.sidebar.markdown("### Management System")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "EDA",
        "Data Tables",
        "Business Insights"
    ]
)

# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

if page == "Dashboard":

    st.title("🍲 Local Food Wastage Management System")

    st.subheader(
        "Connecting surplus food providers with receivers to reduce food wastage"
    )

    st.markdown("### Key Performance Indicators")

    row1_col1, row1_col2, row1_col3 = st.columns(3)
    row2_col1, row2_col2, row2_col3 = st.columns(3)

    with row1_col1:
        st.metric("👨‍🍳 Providers", providers_count)

    with row1_col2:
        st.metric("🤝 Receivers", receivers_count)

    with row1_col3:
        st.metric("🍱 Food Listings", food_count)

    with row2_col1:
        st.metric("📦 Claims", claims_count)

    with row2_col2:
        st.metric("🥗 Total Quantity", total_qty)

    with row2_col3:
        st.metric("✅ Completed Claims", completed_claims)

    st.markdown("---")

    st.info("""
    ### Project Overview

    This dashboard helps reduce food wastage by connecting food providers
    with receivers. The system uses Python, SQL Server, EDA, and Streamlit
    to analyze food donation patterns, claims, distribution efficiency,
    and demand trends.
    """)

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:

        claim_df = claims["Status"].value_counts().reset_index()
        claim_df.columns = ["Status", "Count"]

        fig1 = px.pie(
            claim_df,
            names="Status",
            values="Count",
            title="Claim Status Distribution",
            hole=0.5
        )

        st.plotly_chart(
            fig1,
            use_container_width=True
        )

    with chart_col2:

        provider_quantity = (
            food.groupby("Provider_Type")["Quantity"]
            .sum()
            .reset_index()
        )

        fig2 = px.bar(
            provider_quantity,
            x="Provider_Type",
            y="Quantity",
            title="Provider Type Contribution"
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

# --------------------------------------------------
# EDA PAGE
# --------------------------------------------------

elif page == "EDA":

    st.title("📈 Exploratory Data Analysis")

    chart_files = [
        "provider_type_distribution.png",
        "receiver_type_distribution.png",
        "food_type_distribution.png",
        "meal_type_distribution.png",
        "city_vs_food_listings.png",
        "provider_type_vs_quantity.png",
        "food_type_vs_quantity.png",
        "meal_type_vs_quantity.png",
        "city_provider_quantity.png",
        "food_meal_quantity.png",
        "provider_claim_quantity.png",
        "receiver_claim_quantity.png",
        "claim_status_distribution.png",
        "top_receivers.png",
        "top_providers.png"
    ]

    for i in range(0, len(chart_files), 2):

        col1, col2 = st.columns(2)

        with col1:
            if i < len(chart_files):
                st.subheader(
                    chart_files[i]
                    .replace(".png", "")
                    .replace("_", " ")
                    .title()
                )

                st.image(
                    chart_files[i],
                    use_container_width=True
                )

        with col2:
            if i + 1 < len(chart_files):
                st.subheader(
                    chart_files[i + 1]
                    .replace(".png", "")
                    .replace("_", " ")
                    .title()
                )

                st.image(
                    chart_files[i + 1],
                    use_container_width=True
                )

# --------------------------------------------------
# DATA TABLES
# --------------------------------------------------

elif page == "Data Tables":

    st.title("📋 Data Tables")

    option = st.selectbox(
        "Select Table",
        [
            "Providers",
            "Receivers",
            "Food Listings",
            "Claims"
        ]
    )

    if option == "Providers":
        st.dataframe(providers, use_container_width=True)

    elif option == "Receivers":
        st.dataframe(receivers, use_container_width=True)

    elif option == "Food Listings":
        st.dataframe(food, use_container_width=True)

    else:
        st.dataframe(claims, use_container_width=True)

# --------------------------------------------------
# BUSINESS INSIGHTS
# --------------------------------------------------

elif page == "Business Insights":

    st.title("📊 Business Insights")

    insight_col1, insight_col2 = st.columns(2)

    with insight_col1:

        st.subheader("🏙️ City with Highest Food Listings")

        highest_city = (
            food["Location"]
            .value_counts()
            .head(1)
        )

        st.dataframe(highest_city)

        st.subheader("🥗 Most Common Food Type")

        top_food = (
            food["Food_Type"]
            .value_counts()
            .head(1)
        )

        st.dataframe(top_food)

    with insight_col2:

        st.subheader("🍽️ Most Common Meal Type")

        top_meal = (
            food["Meal_Type"]
            .value_counts()
            .head(1)
        )

        st.dataframe(top_meal)

        st.subheader("📈 Claim Status Summary")

        status_summary = (
            claims["Status"]
            .value_counts()
            .reset_index()
        )

        status_summary.columns = [
            "Status",
            "Count"
        ]

        st.dataframe(status_summary)

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("---")

st.caption(
    "Developed by Varad Kulkarni | CSE (Data Science) | St. John College of Engineering and Management"
)
