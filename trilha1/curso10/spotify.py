import streamlit as st
import pandas as pd
import altair as alt
import time

st.set_page_config(page_title="Spotify Streams", layout="wide")


@st.cache_data
def load_data():
    df = pd.read_csv("data/spotify.csv")
    # Imagine que aqui tem alguma operação muito pesada
    time.sleep(5)
    return df


df = load_data()
st.session_state['df_spotify'] = df

top_streams = df[['Track', 'Stream']].head(30).sort_values(by='Stream', ascending=False)
chart_top_streams = alt.Chart(top_streams).mark_bar().encode(x=alt.X("Track", sort=None), y="Stream")
st.title("Top Spotify Streams of all time")
st.altair_chart(chart_top_streams, use_container_width=True)

# df.set_index("Track", inplace=True)
artists = df['Artist'].value_counts().index
artist = st.sidebar.selectbox("Artist", artists)
df_filtered = df[df['Artist'] == artist]

albuns = df_filtered['Album'].value_counts().index
album = st.sidebar.selectbox("Album", albuns)
df_filtered = df[df['Album'] == album]

col1, col2 = st.columns(2)

col1.bar_chart(df_filtered[['Track', 'Stream']], y="Stream", x="Track")
col2.line_chart(df_filtered[['Track', 'Danceability']], y="Danceability", x="Track")

display = st.sidebar.checkbox('Display', value=True)
if display:
    df_filtered.sort_values(by='Stream', ascending=False, inplace=True)
    st.subheader(f"Top Tracks for {artist} - {album}")
    st.dataframe(df_filtered[['Stream']].head(10), width=350)
