import streamlit as st
import psycopg2
import pandas as pd
import plotly.graph_objects as go
import psycopg2
import subprocess
# creating engine

st.title("Hand Gesture Based Rock-Paper-Scissor Game")

tab1, tab2 = st.tabs(["Game", "Scoresheet"])

with tab1:
    st.header("Welcome to Rock-Paper-Scissor Game")
    st.subheader("Intructions")
    st.write("""
    1. Press "Start the game" button.
    2. A game window will open, press "s" key to initiate the game and hold your hand sign (Make sure it is visible in the right window).
    3. A player can press as many as possible times to play the game, by pressing "s" at each round's end
    3. The scores will be stored in a local database, the user can view the scoresheet in the scoresheet tab.
    """)
    st.warning("!Disclaimer: This game requires camera access, and we ensure that the data from camera is not stored or utilized outside the project.!")
    if st.button('Start the game'):
        #establishing the connection
        subprocess.run(["python", "main.py"])

with tab2:
    st.header("Scoresheet")
    @st.experimental_singleton
    def init_connection():
        return psycopg2.connect(**st.secrets["postgres"])
    conn = init_connection()
    # creating cursor object
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM rps_data")
    a = cursor.fetchall()
    df=pd.DataFrame(a,columns=['Start Date', 'Start Time', 'End Date', 'End Time', 'Elapsed', 'AI Score', 'Player Score'])
    st.dataframe(df)
    st_new_date = []
    end_new_date = []
    for i in range(len(df)):
        st_new_date.append(str(df['Start Date'][i])+' '+df['Start Time'][i])
        end_new_date.append(str(df['End Date'][i])+' '+df['End Time'][i])
    df['st_new_date'] = st_new_date
    df['end_new_date'] = end_new_date
    df['st_new_date']= pd.to_datetime(df['st_new_date'])
    df['st_new_date']=df['st_new_date'].dt.strftime('%m/%d/%Y %I:%M:%S')
    df['end_new_date']= pd.to_datetime(df['end_new_date'])
    df['end_new_date']=df['end_new_date'].dt.strftime('%m/%d/%Y %I:%M:%S')
    df['AI Score'] = df['AI Score'].astype(int)
    df['Player Score'] = df['Player Score'].astype(int)
    fig1 = go.Figure()
    fig1.add_bar(x=df["end_new_date"], y=df['AI Score'], name='AI Score')
    fig1.add_bar(x=df["end_new_date"], y=df['Player Score'], name='Player Score')
    fig1.update_layout(
    title="AI Score vs Player Score"
    )
    st.plotly_chart(fig1, use_container_width=True)
    fig2 = go.Figure()
    fig2.add_scatter(x=df["end_new_date"], y = df["Elapsed"], mode='lines')
    fig2.update_layout(
    title="Time spent in game (in minutes)"
    )
    st.plotly_chart(fig2)
    conn.close()