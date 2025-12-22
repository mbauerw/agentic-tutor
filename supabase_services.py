import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()


supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")


supa_client: Client = create_client(supabase_url, supabase_key)


def get_user_progress(userId: int):
    """Fetch user progress from Supabase for a given userId
        Args:
            userId (int): The ID of the user whose progress is to be fetched
        Returns:
            dict: User progress data
    """
    try:
        response = supa_client.table("user_progress").select("*").eq("user_id", userId).execute()
        return response.data
    except Exception as e:
        print(f"Error fetching user progress: {e}")
        return None


vals = get_user_progress(8)

print(vals)

