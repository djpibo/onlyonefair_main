from config.connect import connect_supabase

class CommonRepository:
    def __init__(self):
        self.supabase = connect_supabase()

    def insert_tag_count(self, param):
        self.supabase.table("Count_Info").insert({"id": param}).execute()