import streamlit as st
import pandas as pd
import os


st.set_page_config(
    page_title="Survey",
)

st.title("Data Collection Survey")
st.write("Please fill out the form below to add your weekly TikTok usage data to the dataset.")

#Data Input
with st.form("survey_form"):
    st.subheader("Enter your TikTok usage hours for each day of the week:")
    
    # Creates input fields for each day
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    day_values = {}
    
    for day in days:
        day_values[day] = st.number_input(
            f"{day}:", 
            min_value=0.0, 
            max_value=24.0, 
            step=0.1,
            format="%.1f"
        )
    
    submitted = st.form_submit_button("Submit Data")
    
    if submitted:
        #Calculates total usage hours 
        total_hours = sum(day_values.values())
        
        if total_hours == 0:
            st.warning("Please enter at least some usage data before submitting.")
        else:
            #Creates DataFrame with the data
            week_data = pd.DataFrame([day_values])
            
            try:
                #Saves to CSV file
                csv_file = "data.csv"
                
                if os.path.exists(csv_file) and os.path.getsize(csv_file) > 0:
                    #Appends to existing file
                    week_data.to_csv(csv_file, mode='a', header=False, index=False)
                else:
                    # Creates new file with headers
                    week_data.to_csv(csv_file, mode='w', header=True, index=False)
                
                # Success message with total hour usage 
                st.success(f" Your TikTok hours have been saved successfully! Total hours this week: {total_hours:.1f} hours")
                
                # Displays what was submitted
                st.write("**Your submitted data:**")
                st.dataframe(week_data)
                
            except Exception as e:
                st.error(f"An error occurred while saving data: {str(e)}")
