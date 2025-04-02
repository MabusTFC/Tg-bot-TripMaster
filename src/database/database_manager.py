
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

async def save_route_db(tg_id: int, citys: list[str]):
    pool = await connect_db()
    async with pool.acquire() as conn:

        user_id = await conn.fetchval("SELECT tg_id FROM Users WHERE tg_id = $1;", tg_id)

        if user_id:
            await conn.execute("""
                INSERT INTO Paths (citys, user_id)
                VALUES ($1, $2)
            """, citys, user_id)
        else:
            print(f"Пользователь с tg_id={tg_id} не найден")

async def citys_list_db(tg_id: int):
    pool = await connect_db()
    async with pool.acquire() as conn:
        citys = await conn.fetchval(
                "SELECT citys FROM Paths WHERE user_id = (SELECT tg_id FROM Users WHERE tg_id = $1) LIMIT 1;", tg_id)

    return citys





