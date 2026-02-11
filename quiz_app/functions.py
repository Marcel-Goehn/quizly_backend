import yt_dlp
import whisper
import json
from google import genai


def download_audio(id):
    url = f"https://www.youtube.com/watch?v={id}"
    tmp_filename = "quiz_app/audio/audio.aac"
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": tmp_filename,
        "quiet": True,
        "noplaylist": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        error_code = ydl.download(url)


def transcribe_audio():
    model = whisper.load_model("turbo")
    result = model.transcribe("quiz_app/audio/audio.aac")
    return result


def create_quiz(transcript):
    client = genai.Client()
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=f"""
                Based on the following transcript, generate a quiz in valid JSON format.
                The quiz must follow this exact structure:
                {{"title": "Create a concise quiz title based on the topic of the transcript.",
                "description": "Summarize the transcript in no more than 150 characters. 
                Do not include any quiz questions or answers.",
                "questions": [
                {{"question_title": "The question goes here.",
                "question_options": ["Option A", "Option B", "Option C", "Option D"],
                "answer": "The correct answer from the above options"}},
                ...
                (exactly 10 questions)]}}
                Requirements:
                - Each question must have exactly 4 distinct answer options.
                - Only one correct answer is allowed per question, 
                and it must be present in 'question_options'.
                - The output must be valid JSON and parsable as-is 
                (e.g., using Python's json.loads).
                - Do not include explanations, comments, or any text outside the JSON.
                This is the following Transcript: {transcript}
            """
    )
    cleaned_response = json.loads(response.text)
    return cleaned_response
