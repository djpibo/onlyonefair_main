from supabase import create_client, Client
from common import config
import redis

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def connect_supabase():
    supabase: Client = create_client(config.SUPABASE_URL, config.SUPABASE_KEY)
    return supabase

def connect_redis():
    return redis.Redis(host='localhost', port=6379, db=0)