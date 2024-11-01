import psycopg2
import os
from datetime import datetime

class Database:
    def __init__(self):
        # Railway bergan URL dan foydalanamiz
        DATABASE_URL = os.environ.get("DATABASE_URL")
        self.conn = psycopg2.connect(DATABASE_URL)
        self.create_tables()
    
    def create_tables(self):
        with self.conn.cursor() as cur:
            # Foydalanuvchilar jadvali
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id BIGINT PRIMARY KEY,
                    username TEXT,
                    first_name TEXT,
                    joined_date TIMESTAMP
                )
            """)
            
            # Test statistikasi jadvali
            cur.execute("""
                CREATE TABLE IF NOT EXISTS test_stats (
                    id SERIAL PRIMARY KEY,
                    user_id BIGINT,
                    test_date TIMESTAMP,
                    lesson_number INTEGER,
                    correct_answers INTEGER,
                    total_questions INTEGER
                )
            """)
        self.conn.commit()
    
    def add_user(self, user_id, username, first_name):
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO users (user_id, username, first_name, joined_date)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (user_id) DO NOTHING
            """, (user_id, username, first_name, datetime.now()))
        self.conn.commit()
    
    def add_test_result(self, user_id, lesson_number, correct, total):
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO test_stats 
                (user_id, test_date, lesson_number, correct_answers, total_questions)
                VALUES (%s, %s, %s, %s, %s)
            """, (user_id, datetime.now(), lesson_number, correct, total))
        self.conn.commit()
    
    def get_daily_stats(self):
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT 
                    COUNT(DISTINCT user_id) as users_count,
                    COUNT(*) as tests_count,
                    AVG(CAST(correct_answers AS FLOAT) / total_questions * 100) as average_score
                FROM test_stats
                WHERE DATE(test_date) = CURRENT_DATE
            """)
            return cur.fetchone()
