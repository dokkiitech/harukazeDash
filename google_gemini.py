import os
from dotenv import load_dotenv
from supabase_access import get_user_data
import google.generativeai as genai
import json

load_dotenv()
GOOGLE_AISTUDIO_API_KEY = os.getenv("GOOGLE_AISTUDIO_API_KEY")
if not GOOGLE_AISTUDIO_API_KEY:
    raise ValueError("APIキーが正しく読み込まれていません。")

genai.configure(api_key=GOOGLE_AISTUDIO_API_KEY)
gemini = genai.GenerativeModel("gemini-2.0-flash")

def generate_response(prompt):
    response = gemini.generate_content(prompt)
    return response

def dash_response(user_id):
    user_data = get_user_data(user_id)

    prompt = (
        f"とあるユーザーはあなたと鬼ごっこをして、彼は逃走しようとしています。\n"
        f"彼は今まで{user_data['dash_count']}回逃走を試みており、{user_data['dash_success']}回成功しています。\n"
        f"彼は今まで{user_data['dash_continue']}回連続で逃走に成功しています。連続で成功していると捕まりやすくなります。\n"
        "あなたの判断が欲しいです。彼が逃げ切ったならTrueを、捕まったならFalseを返してください。\n"
        "もし、捕まったならその理由をネタっぽく、〜があったから捕まった。のような形で30文字程度で考えてください。"
        "マークアップではなく、必ずJSON形式で返してください。\n"
        "Use this JSON schema:"
        "Response= {'result': bool, 'reason': str}"
        "Return: list[Response]"
    )
    response = generate_response(prompt)
    response_text = response.candidates[0].content.parts[0].text.strip()
    if response_text.startswith("```"):
        response_text = response_text.split('```')[1].strip()
    lines = response_text.splitlines()
    if lines and lines[0].strip().lower() == "json":
        response_text = "\n".join(lines[1:]).strip()

    if not response_text:
        raise ValueError("Gemini APIから空のレスポンスが返されました。")

    try:
        response_json = json.loads(response_text)
    except json.JSONDecodeError as e:
        raise ValueError(f"レスポンスのJSONデコードに失敗しました: {e}\nレスポンステキスト: {response_text}")

    return response_json