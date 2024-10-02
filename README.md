# Video Sentiment Analysis

This project is an advanced video sentiment analysis tool that uses the Gemini AI API to analyze the emotional content of uploaded videos. It provides insights such as overall sentiment, key emotional moments, sentiment timeline, and transcription.

## Demo

(https://streamable.com/yi9hof)

## Features

- Upload and analyze video files
- Overall sentiment summary
- Identification of key emotional moments with timestamps
- Sentiment timeline graph
- Word cloud of key emotions
- Emotion distribution pie chart
- Transcription of important dialogue
- Interactive navigation through emotional moments

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/m-deepankar-singh/video-sentiment-analysis.git
   cd video-sentiment-analysis
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```bash
   pip install streamlit google-generativeai plotly wordcloud matplotlib pandas
   ```

## Configuration

1. Obtain a Gemini AI API key from the Google AI Studio.

2. Replace `"YOUR_GEMINI_API_KEY"` in the script with your actual API key:
   ```python
   genai.configure(api_key="YOUR_GEMINI_API_KEY")
   ```

## Usage

1. Run the Streamlit app:
   ```bash
   streamlit run senti.py
   ```

2. Open your web browser and go to the URL provided by Streamlit (usually `http://localhost:8501`).

3. Use the file uploader to select a video file for analysis.

4. Click the "Analyze Sentiment" button to process the video.

5. Explore the various visualizations and insights provided by the analysis.

## Note

This application requires an active internet connection to communicate with the Gemini AI API for video analysis.


## Acknowledgements

- This project uses the Gemini AI API for video analysis.
- Visualizations are created using Plotly, Matplotlib, and WordCloud.
