import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(
    page_title="Visualizations",
)
st.title("Data Visualizations")
st.write("This page displays graphs based on the collected data.")

#Load Data
df = pd.DataFrame()
json_data = {}
if os.path.exists("data.csv") and os.path.getsize("data.csv") > 0:
    df = pd.read_csv("data.csv")
    day_map = {
        "0": "Monday", "1": "Tuesday", "2": "Wednesday", "3": "Thursday",
        "4": "Friday", "5": "Saturday", "6": "Sunday",
        0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday",
        4: "Friday", 5: "Saturday", 6: "Sunday"
    }
    df.rename(columns=lambda x: day_map.get(x, day_map.get(str(x), x)), inplace=True)
        
if os.path.exists("data.json") and os.path.getsize("data.json") > 0:
    with open("data.json", "r") as f:
        json_data = json.load(f)

st.divider()
st.header("Raw Data")
if not df.empty:
    st.dataframe(df)
else:
    st.info("No CSV data to display.")

#Graph 1
st.divider()
st.subheader("Graph 1: TikTok Hours Distribution (Static)")
if not df.empty:
    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    
    # Calculates average hours each day
    daily_avg = df.mean()  # Series with index = days
    
    daily_avg = daily_avg.reindex([d for d in day_order if d in daily_avg.index])
    
    daily_avg_df = pd.DataFrame({
        'Day': pd.Categorical(daily_avg.index, categories=day_order, ordered=True),
        'Average Hours': daily_avg.values
    })
    
    # Sorts by day to ensure correct order of days
    daily_avg_df = daily_avg_df.sort_values('Day')
    
    # Streamlit bar chart with x and y axes
    st.bar_chart(daily_avg_df, x='Day', y='Average Hours')
else:
    st.info("No data available for visualization.")
    
# Graph 2
st.divider()
st.subheader("Graph 2: TikTok Hours vs Productivity (Dynamic)")
if json_data.get("productivity_data") and not df.empty:
    hours_categories = list(json_data["productivity_data"].keys())
    productivity_scores = list(json_data["productivity_data"].values())
    
    #Creates properly labeled DataFrame for line chart
    productivity_df = pd.DataFrame({
        'Hours Range': hours_categories,
        'Productivity Score': productivity_scores
    })
    
    #Streamlit line chart with explicit x and y axes
    st.line_chart(productivity_df, x='Hours Range', y='Productivity Score')
    
    # Calculates user average 
    melted = df.melt(value_vars=df.columns)
    if not melted.empty:
        user_avg = melted["value"].mean()
        bins = [0, 1, 2, 3, 4, 5, 6, float('inf')]
        labels = ["0-1","1-2","2-3","3-4","4-5","5-6","6+"]
        category = pd.cut([user_avg], bins=bins, labels=labels)[0]
        user_score = json_data["productivity_data"].get(str(category), "N/A")
        st.info(f"Based on your average of {user_avg:.2f} hours/day, your estimated productivity score is {user_score}/100.")
    else:
        st.info("No usage data available to calculate your average productivity score.")
    st.write("**Description:** Compare average daily TikTok usage with productivity scores.")
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
    
    # Defines day order for consistent display
    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    
    if selected_week == "All Weeks":
        weekly_avg = df_reset.drop("Week", axis=1).mean()
        
        #Reindex to ensure correct day order
        weekly_avg = weekly_avg.reindex([d for d in day_order if d in weekly_avg.index])
        
        # Create properly labeled DataFrame with categorical day order
        weekly_avg_df = pd.DataFrame({
            'Day': pd.Categorical(weekly_avg.index, categories=day_order, ordered=True),
            'Average Hours': weekly_avg.values
        })
        
        #Sort by day
        weekly_avg_df = weekly_avg_df.sort_values('Day')
        
        st.bar_chart(weekly_avg_df, x='Day', y='Average Hours')
    else:
        week_data = df_reset[df_reset["Week"] == selected_week].drop("Week", axis=1)
        if not week_data.empty:
            #Transposes and create proper DataFrame
            week_data_transposed = week_data.T
            week_data_transposed.columns = ['Hours']
            
            #Reindex to ensure correct day order
            week_data_transposed = week_data_transposed.reindex([d for d in day_order if d in week_data_transposed.index])
            
            #Creates properly labeled DataFrame with categorical day order
            week_display_df = pd.DataFrame({
                'Day': pd.Categorical(week_data_transposed.index, categories=day_order, ordered=True),
                'Hours': week_data_transposed['Hours'].values
            })
            
            #Sorts by day 
            week_display_df = week_display_df.sort_values('Day')
            
            st.bar_chart(week_display_df, x='Day', y='Hours')
        else:
            st.info("No data available for this week.")
    st.write("**Description:** Explore daily TikTok usage by week. Select a specific week or view averages across all weeks.")
else:
    st.info("No data available for visualization.")
