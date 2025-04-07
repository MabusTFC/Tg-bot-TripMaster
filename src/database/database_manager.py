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

async def update_auth_code(tg_id: int, auth_code: str):
    pool = await connect_db()
    async with pool.acquire() as conn:
        await conn.execute("""
            UPDATE Users 
            SET code_autorization_google = $1 
            WHERE tg_id = $2;
        """, auth_code, tg_id)

async def get_auth_code(tg_id: int) -> str | None:
    pool = await connect_db()
    async with pool.acquire() as conn:
        return await conn.fetchval("""
            SELECT code_autorization_google 
            FROM Users 
            WHERE tg_id = $1;
        """, tg_id)

async def has_auth_code(tg_id: int) -> bool:
    pool = await connect_db()
    async with pool.acquire() as conn:
        code = await conn.fetchval("""
            SELECT code_autorization_google 
            FROM Users 
            WHERE tg_id = $1 AND code_autorization_google != '';
        """, tg_id)
        return code is not None


async def save_route_with_details(tg_id: int, cities: list[str], route_details: dict):
    """
    Сохраняет маршрут с деталями в JSON формате
    :param tg_id: ID пользователя
    :param cities: Список городов (для обратной совместимости)
    :param route_details: Полная информация о маршруте в формате JSON
    """
    pool = await connect_db()
    async with pool.acquire() as conn:
        await conn.execute("""
            INSERT INTO Paths (citys, selected_route, user_id)
            VALUES ($1, $2, $3)
        """, cities, route_details, tg_id)

async def get_routes_with_details(tg_id: int) -> list[dict]:
    """
    Получает все маршруты пользователя с деталями
    :param tg_id: ID пользователя
    :return: Список словарей с полной информацией о маршрутах
    """
    pool = await connect_db()
    async with pool.acquire() as conn:
        records = await conn.fetch("""
            SELECT id, citys, selected_route 
            FROM Paths
            WHERE user_id = $1
        """, tg_id)
        return [dict(record) for record in records]

async def update_route_details(route_id: int, new_details: dict):
    """
    Обновляет детали конкретного маршрута
    :param route_id: ID маршрута в таблице Paths
    :param new_details: Новые детали маршрута в формате JSON
    """
    pool = await connect_db()
    async with pool.acquire() as conn:
        await conn.execute("""
            UPDATE Paths
            SET selected_route = $1
            WHERE id = $2
        """, new_details, route_id)