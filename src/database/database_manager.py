
from database.database import connect_db


async def add_user(tg_id: int):
    pool = await connect_db()
    async with pool.acquire() as conn:
        await conn.execute("""
            INSERT INTO Users (tg_id, balance, yandex_calendar) 
            VALUES ($1, 0, '')
            ON CONFLICT (tg_id) DO NOTHING;
        """, tg_id)



async def update_balance(tg_id: int, amount: float):
    pool = await connect_db()
    async with pool.acquire() as conn:
        await conn.execute("""
            UPDATE Users 
            SET balance = balance + $1 
            WHERE tg_id = $2;
        """, amount, tg_id)



