from supabase import create_client, Client
import redis

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# SUPABASE
SUPABASE_URL = "https://mvqxuteltnxhbwvgxzlb.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im12cXh1dGVsdG54aGJ3dmd4emxiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjM0NTkxNDMsImV4cCI6MjAzOTAzNTE0M30.NIYa3m8HA_31Fjgzr52IScmUjA1o-uEW1V7uU_DW2Pw"
def connect_supabase():
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    return supabase

def connect_redis():
    return redis.Redis(host='localhost', port=6379, db=0)