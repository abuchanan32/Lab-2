import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(
    page_title="Visualizations",
)
st.title("Data Visualizations")
st.write("This page displays graphs based on the collected data.")

# Load Data
df = pd.DataFrame()
json_data = None

if os.path.exists("data.csv") and os.path.getsize("data.csv") > 0:
    df = pd.read_csv("data.csv")
    day_map = {
        "0": "Monday", "1": "Tuesday", "2": "Wednesday", "3": "Thursday",
        "4": "Friday", "5": "Saturday", "6": "Sunday",
        0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday",
        4: "Friday", 5: "Saturday", 6: "Sunday"
    }
    df.rename(columns=lambda x: day_map.get(x, day_map.get(str(x), x)), inplace=True)

# --- Simplified JSON loading ---
json_paths = ['Lab02/data.json', 'data.json', '../data.json']
for path in json_paths:
    try:
        with open(path, 'r') as file:
            json_data = json.load(file)
        st.success(f"JSON data loaded successfully from: {path}")
        st.write(f"JSON keys: {list(json_data.keys())}")
        st.write(f"Has 'data_points'? {'data_points' in json_data}")
        break
    except Exception as e:
        st.error(f"Error loading JSON from {path}: {str(e)}")

if json_data is None:
    st.error("Could not load any valid JSON file.")
# -----------------------------------------------------------

st.divider()
st.header("Raw Data")
if not df.empty:
    st.dataframe(df)
else:
    st.info("No CSV data to display.")

# Graph 1
st.divider()
st.subheader("Graph 1: TikTok Hours Distribution (Static)")
if not df.empty:
    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    daily_avg = df.mean()
    daily_avg = daily_avg.reindex([d for d in day_order if d in daily_avg.index])

    daily_avg_df = pd.DataFrame({
        'Day': pd.Categorical(daily_avg.index, categories=day_order, ordered=True),
        'Average Hours': daily_avg.values
    })

    daily_avg_df = daily_avg_df.sort_values('Day')
    st.bar_chart(daily_avg_df, x='Day', y='Average Hours')
else:
    st.info("No data available for visualization.")

# Graph 2
st.divider()
st.subheader("Graph 2: TikTok Hours vs Productivity (Dynamic)")

if json_data and "productivity_data" in json_data:
    prod = json_data["productivity_data"]

    # Create properly ordered DataFrame for the chart
    hours_order = ["0-1", "1-2", "2-3", "3-4", "4-5", "5-6", "6+"]
    
    df_prod = pd.DataFrame({
        "Hours Range": pd.Categorical([h for h in hours_order if h in prod], 
                                     categories=hours_order, 
                                     ordered=True),
        "Productivity Score": [prod[h] for h in hours_order if h in prod]
    })
    
    # Sort by the categorical order
    df_prod = df_prod.sort_values('Hours Range')
    
    # Display the chart with proper indexing
    st.line_chart(df_prod.set_index('Hours Range'))

    # Calculate user average hours/day (only if CSV data exists)
    if not df.empty:
        avg = df.select_dtypes(include="number").melt()["value"].mean()

        # Determine category and score
        bins = [0,1,2,3,4,5,6,float("inf")]
        labels = ["0-1","1-2","2-3","3-4","4-5","5-6","6+"]
        cat = pd.cut([avg], bins=bins, labels=labels, right=False)[0]
        score = prod.get(str(cat), "N/A")

        st.info(f"Based on your average of {avg:.2f} hours/day, your estimated productivity score is {score}/100.")
    else:
        st.info("Submit survey data to see your personalized productivity score!")
else:
    st.info("No productivity data available for visualization.")


# Graph 3
st.divider()
st.subheader("Graph 3: Daily TikTok Usage by Week (Dynamic)")
if not df.empty:
    df_reset = df.reset_index(drop=True)
    df_reset["Week"] = df_reset.index + 1
    weeks = ["All Weeks"] + df_reset["Week"].tolist()
    selected_week = st.selectbox("Select week to view:", options=weeks)

    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    if selected_week == "All Weeks":
        weekly_avg = df_reset.drop("Week", axis=1).mean()
        weekly_avg = weekly_avg.reindex([d for d in day_order if d in weekly_avg.index])
        weekly_avg_df = pd.DataFrame({
            'Day': pd.Categorical(weekly_avg.index, categories=day_order, ordered=True),
            'Average Hours': weekly_avg.values
        })
        weekly_avg_df = weekly_avg_df.sort_values('Day')
        st.bar_chart(weekly_avg_df, x='Day', y='Average Hours')
    else:
        week_data = df_reset[df_reset["Week"] == selected_week].drop("Week", axis=1)
        if not week_data.empty:
            week_data_transposed = week_data.T
            week_data_transposed.columns = ['Hours']
            week_data_transposed = week_data_transposed.reindex([d for d in day_order if d in week_data_transposed.index])
            week_display_df = pd.DataFrame({
                'Day': pd.Categorical(week_data_transposed.index, categories=day_order, ordered=True),
                'Hours': week_data_transposed['Hours'].values
            })
            week_display_df = week_display_df.sort_values('Day')
            st.bar_chart(week_display_df, x='Day', y='Hours')
        else:
            st.info("No data available for this week.")
    st.write("**Description:** Explore daily TikTok usage by week. Select a specific week or view averages across all weeks.")
else:
    st.info("No data available for visualization.")
