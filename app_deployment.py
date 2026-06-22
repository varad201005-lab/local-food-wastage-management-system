import os
import pandas as pd
import streamlit as st

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

providers = pd.read_csv("providers_cleaned.csv")

receivers = pd.read_csv("receivers_cleaned.csv")

food = pd.read_csv("food_listings_cleaned.csv")
st.write("FOOD COLUMNS:")
st.write(list(food.columns))
st.write(food.columns.tolist())

claims = pd.read_csv("claims_cleaned.csv")

providers_count = len(providers)

receivers_count = len(receivers)

food_count = len(food)

claims_count = len(claims)

total_qty = 0
# total_qty = food["Quantity_Available"].sum()

completed_claims = len(
    claims[
        claims["Status"] == "Completed"
    ]
)

st.title("🍲 Local Food Wastage Management System")

st.subheader(
    "Connecting surplus food providers with those in need"
)

col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    st.metric("Providers", providers_count)

with col2:
    st.metric("Receivers", receivers_count)

with col3:
    st.metric("Listings", food_count)

with col4:
    st.metric("Claims", claims_count)

with col5:
    st.metric("Total Qty", total_qty)

with col6:
    st.metric("Completed", completed_claims)

st.sidebar.title("🍲 Food Wastage")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "EDA",
        "Data Tables",
        "Business Insights"
    ]
)
if page == "Dashboard":

    st.header("Dashboard Overview")

    claim_status = claims["Status"].value_counts()

    st.subheader("Claim Status Distribution")

    st.bar_chart(claim_status)

    provider_quantity = food.groupby(
        "Provider_Type"
    )["Quantity_Available"].sum()

    st.subheader("Provider Type Contribution")

    st.bar_chart(provider_quantity)

elif page == "EDA":

    st.header("EDA Charts")

    chart_files = [

        "provider_type_distribution.png",
        "receiver_type_distribution.png",
        "food_type_distribution.png",
        "meal_type_distribution.png",
        "city_vs_food_listings.png",
        "provider_type_vs_quantity.png",
        "food_type_vs_quantity.png",
        "meal_type_vs_quantity.png",
        "claim_status_distribution.png",
        "top_receivers.png",
        "top_providers.png"

    ]

    for chart in chart_files:

        try:

            st.image("provider_type_distribution.png")
            
        except:

            st.warning(
                f"Missing file: {chart}"
            )

elif page == "Data Tables":

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
        st.dataframe(providers)

    elif option == "Receivers":
        st.dataframe(receivers)

    elif option == "Food Listings":
        st.dataframe(food)

    else:
        st.dataframe(claims)

elif page == "Business Insights":

    st.header("Business Insights")

    highest_city = food["Location"].value_counts().head(1)

    st.subheader(
        "City with Highest Food Listings"
    )

    st.dataframe(highest_city)

    top_food = food["Food_Type"].value_counts().head(1)

    st.subheader(
        "Most Common Food Type"
    )

    st.dataframe(top_food)

    top_meal = food["Meal_Type"].value_counts().head(1)

    st.subheader(
        "Most Common Meal Type"
    )

    st.dataframe(top_meal)

st.markdown("---")

st.caption(
    "Developed by Varad Kulkarni | Local Food Wastage Management System"
)
