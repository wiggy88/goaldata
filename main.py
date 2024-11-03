import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv('https://raw.githubusercontent.com/wiggy88/goaldata/main/allleagues_goals.csv')


# Function to convert "Minute" to numeric and classify by half
def convert_to_minutes_and_segment(time):
    if isinstance(time, str) and '+' in time:
        base, extra = map(int, time.split('+'))
        if base == 45:
            return '45+'  # First-half stoppage time
        elif base == 90:
            return '91+'  # Second-half stoppage time
    else:
        minute = int(time)
        if minute <= 15:
            return '0-15'
        elif minute <= 30:
            return '16-30'
        elif minute <= 45:
            return '31-45'
        elif minute <= 60:
            return '46-60'
        elif minute <= 75:
            return '61-75'
        elif minute <= 90:
            return '76-90'
        else:
            return '91+'  # Additional extra time beyond regular stoppage


# Apply the function to the "Minute" column to classify minutes
df['15_min_segment'] = df['Minute'].apply(convert_to_minutes_and_segment)

# Create MatchID column if not present
if 'MatchID' not in df.columns:
    df['MatchID'] = df['Date'].astype(str) + '_' + df['Team'] + '_' + df['Opponent']

# Streamlit app starts here
st.title("Football Data Exploration App")

# Sidebar filters
st.sidebar.header("Filters")
st.sidebar.markdown("<h3 style='font-size: 20px;'>Select League:</h3>", unsafe_allow_html=True)
selected_league = st.sidebar.selectbox("Choose a league:", df['League'].unique())

# Filter data based on selected league
filtered_data = df[df['League'] == selected_league]

# Display overall league stats
st.subheader(f"Overall Stats for {selected_league}")

# Calculate and display top scorers for the selected league
top_scorers = filtered_data['Scorer'].value_counts().head(10)
st.subheader("Top Scorers in " + selected_league)
st.bar_chart(top_scorers)

# Calculate and display top assist providers for the selected league
top_assists = filtered_data['Assist'].value_counts().head(10)
st.subheader("Top Assisters in " + selected_league)
st.bar_chart(top_assists)

# Calculate average goal times for the selected league
average_goal_times = filtered_data['15_min_segment'].value_counts().sort_index()
st.subheader("Average Goal Times in " + selected_league)
st.bar_chart(average_goal_times)

# Count goals by team in the selected league
goals_by_team = filtered_data['Team'].value_counts()
st.subheader("Goals by Team in " + selected_league)
st.bar_chart(goals_by_team)

# Count goals by the 15-minute segments for the selected league
goals_by_segment = filtered_data['15_min_segment'].value_counts().sort_index()
st.subheader("Goals by 15-Minute Segment in " + selected_league)
st.bar_chart(goals_by_segment)

# Team selection for individual stats
st.sidebar.markdown("<h3 style='font-size: 20px;'>Select Team:</h3>", unsafe_allow_html=True)
selected_team = st.sidebar.selectbox("Choose a team:", filtered_data['Team'].unique())

# Display team stats
if selected_team:
    team_data = filtered_data[filtered_data['Team'] == selected_team]
    st.subheader(f"Stats for {selected_team}")

    # Display team goals and assists
    team_top_scorers = team_data['Scorer'].value_counts().head(10)
    st.subheader("Top Scorers for " + selected_team)
    st.bar_chart(team_top_scorers)

    team_top_assists = team_data['Assist'].value_counts().head(10)
    st.subheader("Top Assisters for " + selected_team)
    st.bar_chart(team_top_assists)

    # Count goals by the 15-minute segments for the selected team
    team_goals_by_segment = team_data['15_min_segment'].value_counts().sort_index()
    st.subheader("Goals by 15-Minute Segment for " + selected_team)
    st.bar_chart(team_goals_by_segment)

# Player selection for individual stats
st.sidebar.markdown("<h3 style='font-size: 20px;'>Select Player:</h3>", unsafe_allow_html=True)
selected_player = st.sidebar.selectbox("Choose a player:", df[df['League'] == selected_league]['Scorer'].unique())

# Display player stats
if selected_player:
    player_data = filtered_data[filtered_data['Scorer'] == selected_player]
    st.subheader(f"Stats for {selected_player}")

    # Display goals scored by the player
    player_goals = player_data['Scorer'].value_counts()
    st.bar_chart(player_goals)

    # Display assists provided by the player
    player_assists = player_data['Assist'].value_counts()
    st.subheader("Assists by " + selected_player)
    st.bar_chart(player_assists)

