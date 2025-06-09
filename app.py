from flask import Flask, request, jsonify, render_template
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
import requests
import re
import uuid
import os
import yt_dlp
from together import Together

app = Flask(__name__, static_url_path='/static', static_folder='static', template_folder='templates')

# ✅ Your Together API key (use securely in production)
client = Together(api_key='e7a501a28a46881b3559d8599dd96cf6bb100fe303fc4cfa67f02c023b193d41')

def extract_video_id(url):
    # Handles: watch?v=, youtu.be/, live/
    patterns = [
        r"(?:v=)([a-zA-Z0-9_-]{11})",
        r"(?:youtu\.be/)([a-zA-Z0-9_-]{11})",
        r"(?:live/)([a-zA-Z0-9_-]{11})"
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            print("Extracted Video ID:", match.group(1))
            return match.group(1)
    return None


def transcribe_with_together_whisper(file_path):
    """Uses Together.ai Whisper to transcribe audio"""
    url = "https://api.together.xyz/v1/audio/transcriptions"
    headers = {"Authorization": f"Bearer {client.api_key}"}
    with open(file_path, 'rb') as f:
        response = requests.post(
            url,
            headers=headers,
            data={"model": "openai/whisper-large-v3", "language": "en"},
            files={"file": f}
        )
    if response.status_code == 200:
        return response.json()["text"]
    else:
        raise Exception("Whisper transcription failed.")

def summarize_with_together(text):
    """Summarizes text using Together's Meta-Llama"""
    prompt = f"Summarize the following YouTube transcript in 5-6 key points:\n{text}"
    messages = [{"role": "user", "content": prompt}]
    
    completion = client.chat.completions.create(
        model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
        messages=messages
    )
    
    return completion.choices[0].message.content.strip()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    try:
        data = request.get_json(force=True)
        url = data.get("url")
        if not url:
            return jsonify({"error": "URL is missing"}), 400

        video_id = extract_video_id(url)
        if not video_id:
            return jsonify({"error": "Invalid YouTube URL"}), 400

        try:
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
            full_text = " ".join([item['text'] for item in transcript_list])
        except (TranscriptsDisabled, NoTranscriptFound):
            return jsonify({"error": "Transcript not available for this video."}), 400

        if len(full_text) > 4000:
            full_text = full_text[:4000]  # Trim for model input limit

        summary = summarize_with_together(full_text)
        return jsonify({"summary": summary})

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": "Something went wrong."}), 500

if __name__ == '__main__':
    app.run(debug=True)