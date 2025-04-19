from db_utils import get_or_create_user  # またはファイル内に直接定義されてるならそのままでOK
import random

def handle_dash(user_id, username):
    user = get_or_create_user(user_id, username)
    
    # 成功か失敗をランダムに決定
    success = random.random() < 0.5  # 50% 成功

    if success:
        user['coins'] += 10
        user['dash_success'] += 1
    else:
        user['coins'] -= 5
    
    user['dash_count'] += 1

    # Supabaseに更新
    from main import supabase  # もしくは supabase が使えるように import しておく
    supabase.table("users").update({
        "coins": user['coins'],
        "dash_success": user['dash_success'],
        "dash_count": user['dash_count']
    }).eq("discord_id", user_id).execute()

    return success, user['coins']