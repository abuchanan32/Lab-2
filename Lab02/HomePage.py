import streamlit as st

#Pretty background pic
#finds main box that holds everything in streamlit app and applies my custom styles to it
#sets pic, ensures it fills screen, keeps centered, stops from repeating, makes it stay still when scrolling
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] {
        background-image: url("https://www.adobe.com/uk/express/learn/blog/media_1dc3f69a53d3b214edbdc1cf5423e0796acc1114b.jpg?width=1200&format=pjpg&optimize=medium");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    </style>
    """, unsafe_allow_html=True)

# Title of App
st.title("Web Development Lab02")

st.header("CS 1301 - Abigail Buchanan")

#App info
st.write("""
Welcome to my Streamlit Web Development Lab02 app! You can navigate between the pages using the sidebar to the left. The following pages are:

1. **Survey Page**: Log your daily TikTok screen time and how it made you feel. The data is saved automatically to a CSV file. 
2. **Visuals Page**: Explore interactive graphs that show your daily TikTok usage trends and average hours.  
3. **Data Insights (JSON)**: Access screen time tips and healthy goal comparisons from a stored JSON file.  

This webpage displays your screen time as data to help you reflect on your habits and cut back on doomscrolling. 

""") 

