from datetime import datetime, timedelta
from collections import Counter

from asyncpg import Connection
from database.database import connect_db


async def add_user(tg_id: int, tg_tag: str):
    pool = await connect_db()
    async with pool.acquire() as conn:
        await conn.execute("""
            INSERT INTO Users (tg_id, balance, yandex_calendar, name) 
            VALUES ($1, 0, '', $2)
            ON CONFLICT (tg_id) DO NOTHING;
        """, tg_id, tg_tag)



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
        result = await conn.fetch("""
                SELECT citys FROM Paths
                WHERE user_id = $1
            """, tg_id)
        return [record["citys"] for record in result]

async def get_user_role_from_manager(name: str) -> str | None:
    pool = await connect_db()
    async with pool.acquire() as conn:
        role = await conn.fetchval(
            "SELECT role FROM manager WHERE name = $1;",
            name
        )
    return role


async def add_manager_user_by_name(name: str, role: str = "manager"):
    pool = await connect_db()
    async with pool.acquire() as conn:
        existing_manager = await conn.fetchval("""
            SELECT name FROM manager WHERE name = $1;
        """, name)

        if existing_manager:
            raise ValueError(f"Менеджер с именем '{name}' уже существует.")

        await conn.execute("""
            INSERT INTO manager (name, role)
            VALUES ($1, $2);
        """, name, role)

async def delete_manager_from_db(name: str):
    pool = await connect_db()
    async with pool.acquire() as conn:
        result = await conn.execute("""
            DELETE FROM manager WHERE name = $1;
        """, name)

        if result == "DELETE 0":
            raise ValueError(f"Менеджер с именем '{name}' не найден.")


async def get_all_managers_list():
    pool = await connect_db()
    async with pool.acquire() as conn:
        managers = await conn.fetch("""
            SELECT name FROM manager WHERE role = 'manager';
        """)
        return [manager['name'] for manager in managers]


async def get_stistic_city_db(conn: Connection) -> dict:
    result = await conn.fetch("""SELECT unnest(citys) AS city FROM Paths""")

    cities = [record['city'] for record in result]

    city_counts = dict(Counter(cities))

    return city_counts

async def get_new_users_by_day(conn: Connection) -> dict:
    ten_days_ago = datetime.now() - timedelta(days=10)

    result = await conn.fetch("""
        SELECT DATE(registration_date) AS reg_date, COUNT(*) AS count
        FROM Users
        WHERE registration_date >= $1
        GROUP BY reg_date
        ORDER BY reg_date
    """, ten_days_ago)

    stats = {record["reg_date"].strftime('%Y-%m-%d'): record["count"] for record in result}

    return stats
