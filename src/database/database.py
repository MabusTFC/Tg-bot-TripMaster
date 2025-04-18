import os
from dotenv import load_dotenv
import asyncpg


load_dotenv()

async def connect_db():
    return await asyncpg.create_pool(
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )

async def init_db():
    pool = await connect_db()
    async with pool.acquire() as conn:
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS Users (
                tg_id BIGINT PRIMARY KEY,
                balance NUMERIC DEFAULT 0,
                yandex_calendar TEXT,
                code_autorization_google TEXT DEFAULT '',
                name TEXT UNIQUE,
                registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS Paths (
                id SERIAL PRIMARY KEY,
                citys TEXT[],
                selected_route JSONB,  -- Новый столбец для хранения полного маршрута в JSON
                user_id BIGINT REFERENCES Users(tg_id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS UnSavedPaths (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                citys TEXT[],  
                user_id BIGINT REFERENCES Users(tg_id) ON DELETE CASCADE
            );
            
            CREATE TABLE IF NOT EXISTS manager (
                id SERIAL PRIMARY KEY,
                name TEXT UNIQUE NOT NULL,
                role TEXT NOT NULL
            );
        """)

