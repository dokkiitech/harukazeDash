from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def initialize_user_data(user_id): # Supabase初期化
    user_data = {
        "discord_id": user_id,
        "coins": 0,
        "dash_count": 0,
        "dash_success": 0,
        "chase_count": 0,
        "chase_success": 0
    }
    supabase.table("users").upsert(user_data).execute()
    print("[Initialize]:", user_data) #debug

def get_user_data(user_id): # Supabase取得・初期化
    user_data = supabase.table("users").select("*").eq("discord_id", user_id).execute()

    if len(user_data.data) == 0:
        initialize_user_data(user_id)

    # 再度取得
    user_data = supabase.table("users").select("*").eq("discord_id", user_id).execute()

    print("[Get]:", user_data) #debug

    return user_data.data[0]

def save_user_data(user_id, user_data):# Supabase保存
    supabase.table("users").update(
        {
            "coins": user_data["coins"],
            "dash_count": user_data["dash_count"],
            "dash_success": user_data["dash_success"],
            "chase_count": user_data["chase_count"],
            "chase_success": user_data["chase_success"]
        }
    ).eq("discord_id", user_id).execute()

    print("[Save]:", user_data) #debug