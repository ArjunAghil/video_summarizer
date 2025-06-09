 2. YouTube Video Summarizer Bot
 Goal:
 Build a tool where users can paste a YouTube video link and get a short summary or key points.
 Tech Stack:- Frontend: React or basic HTML form for URL input- Backend: Python Flask- AI: Whisper (for audio transcription) + GPT-4 or T5 (for summarization)- Libraries: youtube_transcript_api, transformers
 Work Division:- Person 1 (GenAI Expert):
  - Use Whisper to extract transcript or 'youtube_transcript_api' if available
  - Pass transcript to GPT-4 or T5 for summarization- Person 2 (Frontend Dev):
  - Create input form and display area for summaries
  - Implement loading state, error messages, etc.
Easy GenAI + WebDev Projects (Team of 3)- Person 3 (Backend Dev):
  - Build Flask API to handle video URL, transcript fetching, and AI integration
  - Deploy Flask backend to Render/Railway or use local server for testin
