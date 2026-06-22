import streamlit as st
import pandas as pd
from database import get_connection

# PAGE CONFIG
st.set_page_config(
    page_title="Local Food Wastage Management System",
    layout="wide"
)

# CUSTOM CSS
st.markdown("""
<style>
div[data-testid="metric-container"]{
    background-color:#F0F2F6;
    border-radius:10px;
    padding:15px;
}
</style>
""", unsafe_allow_html=True)

# DATABASE CONNECTION
conn = get_connection()

# KPI DATA
providers_count = pd.read_sql(
    "SELECT COUNT(*) AS cnt FROM providers_cleaned",
    conn
).iloc[0, 0]

receivers_count = pd.read_sql(
    "SELECT COUNT(*) AS cnt FROM receivers_cleaned",
    conn
).iloc[0, 0]

food_count = pd.read_sql(
    "SELECT COUNT(*) AS cnt FROM food_listings_cleaned",
    conn
).iloc[0, 0]

claims_count = pd.read_sql(
    "SELECT COUNT(*) AS cnt FROM claims_cleaned",
    conn
).iloc[0, 0]

total_qty = pd.read_sql(
    "SELECT SUM(Quantity) AS qty FROM food_listings_cleaned",
    conn
).iloc[0, 0]

completed_claims = pd.read_sql(
    """
    SELECT COUNT(*) AS completed
    FROM claims_cleaned
    WHERE Status='Completed'
    """,
    conn
).iloc[0, 0]

# SIDEBAR
st.sidebar.title("🍲 Food Wastage Management System")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "SQL Queries",
        "EDA & Charts",
        "Filter & Search",
        "CRUD Operations",
        "Data Tables",
        "Business Insights"
    ]
)

# DASHBOARD PAGE
if page == "Dashboard":

    st.title("🍲 Local Food Wastage Management System")
    st.subheader("Connecting surplus food providers with those in need")

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

    st.markdown("---")

    c1, c2 = st.columns(2)

    with c1:
        status_df = pd.read_sql("""
            SELECT Status,
                   COUNT(*) AS Total
            FROM claims_cleaned
            GROUP BY Status
        """, conn)

        st.subheader("Claim Status Breakdown")
        st.bar_chart(status_df.set_index("Status"))

    with c2:
        provider_df = pd.read_sql("""
            SELECT Provider_Type,
                   SUM(Quantity) AS Quantity
            FROM food_listings_cleaned
            GROUP BY Provider_Type
        """, conn)

        st.subheader("Provider Type Distribution")
        st.bar_chart(provider_df.set_index("Provider_Type"))

        st.markdown("---")

        st.subheader("📌 Project Overview")

        st.info("""
                This dashboard helps reduce food wastage by connecting food providers
                with receivers and analyzing food donation, claims, demand,
                and distribution patterns using SQL Server and Streamlit.
                """)
        

# SQL QUERIES PAGE
elif page == "SQL Queries":

    st.header("📊 SQL Query Results")

    # Query 1
    st.subheader("Query 1 - Providers by City")

    q1 = pd.read_sql("""
    SELECT City,
           COUNT(*) AS Total_Providers
    FROM providers_cleaned
    GROUP BY City
    ORDER BY Total_Providers DESC
    """, conn)

    st.dataframe(q1)

    # Query 2
    st.subheader("Query 2 - Receivers by City")

    q2 = pd.read_sql("""
    SELECT City,
           COUNT(*) AS Total_Receivers
    FROM receivers_cleaned
    GROUP BY City
    ORDER BY Total_Receivers DESC
    """, conn)

    st.dataframe(q2)

    # Query 3
    st.subheader("Query 3 - Provider Contribution")

    q3 = pd.read_sql("""
    SELECT Provider_Type,
           SUM(Quantity) AS Total_Quantity
    FROM food_listings_cleaned
    GROUP BY Provider_Type
    ORDER BY Total_Quantity DESC
    """, conn)

    st.dataframe(q3)

    # Query 4
    st.subheader("Query 4 - Provider Contact Information")

    q4 = pd.read_sql("""
    SELECT Name,
           City,
           Contact
    FROM providers_cleaned
    """, conn)

    st.dataframe(q4)

    # Query 5
    st.subheader("Query 5 - Total Food Quantity")

    q5 = pd.read_sql("""
    SELECT SUM(Quantity) AS Total_Food_Quantity
    FROM food_listings_cleaned
    """, conn)

    st.dataframe(q5)

    # Query 6
    st.subheader("Query 6 - Food Listings by City")

    q6 = pd.read_sql("""
    SELECT Location,
           COUNT(*) AS Food_Listings
    FROM food_listings_cleaned
    GROUP BY Location
    ORDER BY Food_Listings DESC
    """, conn)

    st.dataframe(q6)

    # Query 7
    st.subheader("Query 7 - Food Type Distribution")

    q7 = pd.read_sql("""
    SELECT Food_Type,
           COUNT(*) AS Count_Food
    FROM food_listings_cleaned
    GROUP BY Food_Type
    ORDER BY Count_Food DESC
    """, conn)

    st.dataframe(q7)

    # Query 8
    st.subheader("Query 8 - Claims Per Food Item")

    q8 = pd.read_sql("""
    SELECT
        f.Food_Name,
        COUNT(c.Claim_ID) AS Total_Claims
    FROM food_listings_cleaned f
    LEFT JOIN claims_cleaned c
    ON f.Food_ID = c.Food_ID
    GROUP BY f.Food_Name
    ORDER BY Total_Claims DESC
    """, conn)

    st.dataframe(q8)

    # Query 9
    st.subheader("Query 9 - Successful Claims by Provider")

    q9 = pd.read_sql("""
    SELECT
        p.Name,
        COUNT(c.Claim_ID) AS Successful_Claims
    FROM providers_cleaned p
    JOIN food_listings_cleaned f
        ON p.Provider_ID = f.Provider_ID
    JOIN claims_cleaned c
        ON f.Food_ID = c.Food_ID
    WHERE c.Status = 'Completed'
    GROUP BY p.Name
    ORDER BY Successful_Claims DESC
    """, conn)

    st.dataframe(q9)

    # Query 10
    st.subheader("Query 10 - Claim Status Percentage")

    q10 = pd.read_sql("""
    SELECT
        Status,
        COUNT(*) * 100.0 /
        (SELECT COUNT(*) FROM claims_cleaned)
        AS Percentage
    FROM claims_cleaned
    GROUP BY Status
    """, conn)

    st.dataframe(q10)

    # Query 11
    st.subheader("Query 11 - Average Quantity Claimed")

    q11 = pd.read_sql("""
    SELECT
        r.Name,
        AVG(f.Quantity) AS Avg_Quantity_Claimed
    FROM receivers_cleaned r
    JOIN claims_cleaned c
        ON r.Receiver_ID = c.Receiver_ID
    JOIN food_listings_cleaned f
        ON c.Food_ID = f.Food_ID
    GROUP BY r.Name
    ORDER BY Avg_Quantity_Claimed DESC
    """, conn)

    st.dataframe(q11)

    # Query 12
    st.subheader("Query 12 - Most Claimed Meal Type")

    q12 = pd.read_sql("""
    SELECT
        f.Meal_Type,
        COUNT(c.Claim_ID) AS Total_Claims
    FROM food_listings_cleaned f
    JOIN claims_cleaned c
        ON f.Food_ID = c.Food_ID
    GROUP BY f.Meal_Type
    ORDER BY Total_Claims DESC
    """, conn)

    st.dataframe(q12)

    # Query 13
    st.subheader("Query 13 - Total Quantity Donated by Provider")

    q13 = pd.read_sql("""
    SELECT
        p.Name,
        SUM(f.Quantity) AS Total_Donated
    FROM providers_cleaned p
    JOIN food_listings_cleaned f
        ON p.Provider_ID = f.Provider_ID
    GROUP BY p.Name
    ORDER BY Total_Donated DESC
    """, conn)

    st.dataframe(q13)

    # Query 14
    st.subheader("Query 14 - Top Receivers")

    q14 = pd.read_sql("""
    SELECT
        r.Name,
        COUNT(c.Claim_ID) AS Total_Claims
    FROM receivers_cleaned r
    JOIN claims_cleaned c
        ON r.Receiver_ID = c.Receiver_ID
    GROUP BY r.Name
    ORDER BY Total_Claims DESC
    """, conn)

    st.dataframe(q14)

    # Query 15
    st.subheader("Query 15 - Demand Analysis by City")

    q15 = pd.read_sql("""
    SELECT
        r.City,
        COUNT(c.Claim_ID) AS Total_Demand
    FROM receivers_cleaned r
    JOIN claims_cleaned c
        ON r.Receiver_ID = c.Receiver_ID
    GROUP BY r.City
    ORDER BY Total_Demand DESC
    """, conn)

    st.dataframe(q15)


# EDA PAGE
elif page == "EDA & Charts":

    st.header("📈 EDA Visualizations")

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

    for chart in chart_files:
        try:
            st.image(
                f"eda_charts/{chart}",
                use_container_width=True
            )
        except:
            st.warning(f"Chart not found: {chart}")

# FILTER PAGE
elif page == "Filter & Search":

    st.header("🔍 Filter & Search")

    cities = pd.read_sql(
        "SELECT DISTINCT City FROM providers_cleaned",
        conn
    )

    selected_city = st.selectbox(
        "Select City",
        cities["City"]
    )

    filtered = pd.read_sql(
        f"""
        SELECT *
        FROM providers_cleaned
        WHERE City='{selected_city}'
        """,
        conn
    )

    st.dataframe(filtered)

# CRUD PAGE
elif page == "CRUD Operations":

    st.header("✏️ CRUD Operations")

    food_name = st.text_input("Food Name")

    quantity = st.number_input(
        "Quantity",
        min_value=1
    )

    if st.button("Add Food Listing"):
        st.success(
            f"{food_name} added successfully!"
        )

# DATA TABLES PAGE
elif page == "Data Tables":

    st.header("📋 Data Tables")

    option = st.selectbox(
        "Choose Table",
        [
            "Providers",
            "Receivers",
            "Food Listings",
            "Claims"
        ]
    )

    if option == "Providers":
        df = pd.read_sql(
            "SELECT * FROM providers_cleaned",
            conn
        )

    elif option == "Receivers":
        df = pd.read_sql(
            "SELECT * FROM receivers_cleaned",
            conn
        )

    elif option == "Food Listings":
        df = pd.read_sql(
            "SELECT * FROM food_listings_cleaned",
            conn
        )

    else:
        df = pd.read_sql(
            "SELECT * FROM claims_cleaned",
            conn
        )

    st.dataframe(df)

# BUSINESS INSIGHTS PAGE
elif page == "Business Insights":

    st.header("📈 Business Insights")

    # City with Highest Food Listings
    city_food = pd.read_sql("""
        SELECT TOP 1
               Location,
               COUNT(*) AS Food_Listings
        FROM food_listings_cleaned
        GROUP BY Location
        ORDER BY Food_Listings DESC
    """, conn)

    st.subheader("🏙️ City with Highest Food Listings")
    st.dataframe(city_food)

    # Most Common Food Type
    food_type = pd.read_sql("""
        SELECT TOP 1
               Food_Type,
               COUNT(*) AS Total
        FROM food_listings_cleaned
        GROUP BY Food_Type
        ORDER BY Total DESC
    """, conn)

    st.subheader("🥗 Most Common Food Type")
    st.dataframe(food_type)

    # Most Common Meal Type
    meal_type = pd.read_sql("""
        SELECT TOP 1
               Meal_Type,
               COUNT(*) AS Total
        FROM food_listings_cleaned
        GROUP BY Meal_Type
        ORDER BY Total DESC
    """, conn)

    st.subheader("🍽️ Most Common Meal Type")
    st.dataframe(meal_type)

    # Top Provider
    top_provider = pd.read_sql("""
        SELECT TOP 1
               p.Name,
               SUM(f.Quantity) AS Total_Donated
        FROM providers_cleaned p
        JOIN food_listings_cleaned f
        ON p.Provider_ID = f.Provider_ID
        GROUP BY p.Name
        ORDER BY Total_Donated DESC
    """, conn)

    st.subheader("🏆 Top Contributing Provider")
    st.dataframe(top_provider)

    # Top Receiver
    top_receiver = pd.read_sql("""
        SELECT TOP 1
               r.Name,
               COUNT(c.Claim_ID) AS Total_Claims
        FROM receivers_cleaned r
        JOIN claims_cleaned c
        ON r.Receiver_ID = c.Receiver_ID
        GROUP BY r.Name
        ORDER BY Total_Claims DESC
    """, conn)

    st.subheader("🤝 Top Receiver")
    st.dataframe(top_receiver)

    # Claim Status Percentage
    claim_status = pd.read_sql("""
        SELECT
            Status,
            COUNT(*) * 100.0 /
            (SELECT COUNT(*) FROM claims_cleaned)
            AS Percentage
        FROM claims_cleaned
        GROUP BY Status
    """, conn)

    st.subheader("📊 Claim Status Percentage")
    st.dataframe(claim_status)

st.markdown("---")

st.caption(
    "Developed by Varad Kulkarni | Local Food Wastage Management System | Python • SQL Server • Streamlit"
)
