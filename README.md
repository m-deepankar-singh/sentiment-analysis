# Advanced Video Sentiment Analysis

This project is an advanced video sentiment analysis tool that uses the Gemini AI API to analyze the emotional content of uploaded videos. It provides insights such as overall sentiment, key emotional moments, sentiment timeline, and transcription.

## Demo

Click the image below to watch the demo video:

[![Video Demo](https://cdn-cf-east.streamable.com/image/yi9hof.jpg?Expires=1700687100&Signature=fpxWZJWXjUYSM7Kj3y9VWF4i5C0wQEjX2B9oYzYnbz~OZSdcAo9cqhg8SZKPsHRjqLsTl1GN56sFCKqcWWUXpsDkRLPVulj~nTVX5rkDuZi9uajVjufLRdgVdZWPvOg6m6EFJ4JO1wmdtwdCqcGLRj1B4OAmkNX3EIXZ79HWi8NRGS1BHqh5iZCWYe~77Ff6K3Yim~C5rvJCMq7rAiHKjWFh92jLjfR6L8X5i7zUAr4I-8kufC8HEwkOWSbM3NPVZ~5Cm~lYR9SzNsVmfN3wPHPpHxLDz1VlVT-kUJr7sW5EQvdBLhfSFBOsUQOIMGQZGXA1tBqAUJ7CIjw6zeMVcw__&Key-Pair-Id=APKAIEYUVEN4EVB2OKEQ)](https://streamable.com/yi9hof)

In this demo, you can see how the app analyzes a video, providing sentiment analysis, emotional moments, and various visualizations of the results.

## Features

- Upload and analyze video files
- Overall sentiment summary
- Identification of key emotional moments with timestamps
- Sentiment timeline graph
- Word cloud of key emotions
- Emotion distribution pie chart
- Transcription of important dialogue
- Interactive navigation through emotional moments

[Rest of the README content remains the same]

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
