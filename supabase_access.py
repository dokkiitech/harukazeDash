from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_user_data(user_id):
    """
    ユーザーデータを取得または初期化する関数
    """
    user_data = supabase.table("users").select("*").eq("discord_id", user_id).execute()
    
    if len(user_data.data) == 0:
        # ユーザーデータが存在しない場合、新規作成
        user_data = {
            "discord_id": user_id,
            "coins": 0,
            "dash_count": 0,
            "dash_success": 0
        }
        supabase.table("users").insert(user_data).execute()
    else:
        user_data = user_data.data[0]
    
    return user_data

def save_user_data(user_data):
    """
    ユーザーデータをSupabaseに保存する関数
    """
    supabase.table("users").update(user_data).eq("discord_id", user_data["discord_id"]).execute()