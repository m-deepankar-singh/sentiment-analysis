import os
import time
import re
import streamlit as st
import google.generativeai as genai
from google.api_core import exceptions, retry
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd

genai.configure(api_key="GEMINI_API_KEY")

@st.cache_data
def upload_and_process_video(uploaded_file):
    with st.spinner("Uploading and processing video..."):
        with open("temp_video.mp4", "wb") as f:
            f.write(uploaded_file.getvalue())
        
        video_file = genai.upload_file(path="temp_video.mp4")
        
        while video_file.state.name == "PROCESSING":
            time.sleep(5)
            video_file = genai.get_file(video_file.name)
        
        if video_file.state.name == "FAILED":
            raise ValueError(f"Video processing failed: {video_file.state.name}")
        
        return video_file

@retry.Retry(predicate=retry.if_exception_type(ConnectionError))
def analyze_video_sentiment(video_file):
    model = genai.GenerativeModel('gemini-1.5-pro-002')
    prompt = """
    Analyze the sentiment of this video and provide the following information:
    1. Overall sentiment: Give a brief summary of the overall sentiment.
    2. Emotional moments: List at least 5 key emotional moments with their timestamps (in MM:SS format), detected emotion, and a brief description.
    3. Sentiment timeline: Provide a sentiment score for at least 10 timestamps throughout the video, with scores ranging from -1 (very negative) to 1 (very positive).
    4. Key emotions: List the top 10 key emotions detected in the video.
    5. Transcription: Provide a brief transcription of important dialogue or narration.

    Format your response as follows:

    Overall sentiment: [Your summary here]

    Emotional moments:
    - [MM:SS] - [Emotion]: [Description]
    [Repeat for at least 5 moments]

    Sentiment timeline:
    [MM:SS]: [Score]
    [Repeat for at least 10 timestamps]

    Key emotions:
    [List of 10 emotions]

    Transcription:
    [Your transcription here]
    """
    response = model.generate_content([prompt, video_file])
    return response.text

def parse_response(text):
    data = {
        'overall_sentiment': '',
        'emotional_moments': [],
        'sentiment_timeline': [],
        'key_emotions': [],
        'transcription': ''
    }
    
    match = re.search(r'Overall sentiment:(.*?)(?:\n\n|\Z)', text, re.DOTALL)
    if match:
        data['overall_sentiment'] = match.group(1).strip()
    
    moments = re.findall(r'- (\d{2}:\d{2}) - ([^:]+): (.+)', text)
    data['emotional_moments'] = [{'timestamp': m[0], 'emotion': m[1], 'description': m[2]} for m in moments]
    
    timeline = re.findall(r'(\d{2}:\d{2}): (-?\d+(?:\.\d+)?)', text)
    data['sentiment_timeline'] = [{'timestamp': t[0], 'score': float(t[1])} for t in timeline]
    
    match = re.search(r'Key emotions:(.*?)(?:\n\n|\Z)', text, re.DOTALL)
    if match:
        data['key_emotions'] = [e.strip() for e in match.group(1).strip().split('\n')]
    
    match = re.search(r'Transcription:(.*?)(?:\Z)', text, re.DOTALL)
    if match:
        data['transcription'] = match.group(1).strip()
    
    return data

def create_sentiment_timeline(sentiment_data):
    df = pd.DataFrame(sentiment_data['sentiment_timeline'])
    df['timestamp'] = pd.to_timedelta(df['timestamp'].apply(lambda x: f"00:{x}"))
    df['seconds'] = df['timestamp'].dt.total_seconds()
    fig = px.line(df, x='seconds', y='score', title='Sentiment Timeline',
                  labels={'seconds': 'Time (seconds)', 'score': 'Sentiment Score'},
                  hover_data=['timestamp'])
    fig.update_layout(hovermode="x unified")
    return fig

def create_word_cloud(emotions):
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(emotions))
    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    return fig

def create_emotion_pie_chart(emotions):
    emotion_counts = pd.Series(emotions).value_counts()
    fig = px.pie(values=emotion_counts.values, names=emotion_counts.index, title='Key Emotions Distribution')
    return fig

def main():
    st.set_page_config(layout="wide")
    st.title("Advanced Video Sentiment Analysis")
    st.write("Upload a video file to analyze its sentiment using Gemini AI.")

    uploaded_file = st.file_uploader("Choose a video file", type=["mp4", "avi", "mov", "mpeg"])

    if uploaded_file is not None:
        col1, col2 = st.columns([2, 1])
        with col1:
            st.video(uploaded_file)
        
        with col2:
            if st.button("Analyze Sentiment", key="analyze_button"):
                try:
                    video_file = upload_and_process_video(uploaded_file)
                    
                    with st.spinner("Analyzing video sentiment..."):
                        response_text = analyze_video_sentiment(video_file)
                        sentiment_data = parse_response(response_text)
                    
                    st.session_state.sentiment_data = sentiment_data
                    
                    # Clean up
                    video_file.delete()
                    os.remove("temp_video.mp4")
                    
                except exceptions.PermissionDenied as e:
                    st.error(f"Permission denied: {e}. Please check your API key and permissions.")
                except ValueError as e:
                    st.error(f"Error: {e}")
                except Exception as e:
                    st.error(f"An unexpected error occurred: {e}")

    if 'sentiment_data' in st.session_state:
        data = st.session_state.sentiment_data
        
        st.subheader("Overall Sentiment")
        st.write(data['overall_sentiment'])
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Sentiment Timeline")
            timeline_fig = create_sentiment_timeline(data)
            st.plotly_chart(timeline_fig, use_container_width=True)
            
            st.subheader("Key Emotions")
            wordcloud_fig = create_word_cloud(data['key_emotions'])
            st.pyplot(wordcloud_fig)
        
        with col2:
            st.subheader("Emotional Moments")
            for moment in data['emotional_moments']:
                st.markdown(f"**{moment['timestamp']}** - {moment['emotion']}")
                st.write(moment['description'])
                st.divider()
            
            st.subheader("Emotions Distribution")
            pie_chart = create_emotion_pie_chart(data['key_emotions'])
            st.plotly_chart(pie_chart, use_container_width=True)
        
        st.subheader("Transcription")
        st.write(data['transcription'])
        
        st.subheader("Navigate to Specific Moment")
        timestamps = [moment['timestamp'] for moment in data['emotional_moments']]
        selected_time = st.select_slider("Select a timestamp", options=timestamps)
        selected_moment = next(moment for moment in data['emotional_moments'] if moment['timestamp'] == selected_time)
        st.write(f"Emotion: {selected_moment['emotion']}")
        st.write(f"Description: {selected_moment['description']}")

if __name__ == "__main__":
    main()