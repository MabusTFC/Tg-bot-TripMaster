import datetime

from src.database.database import connect_db
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import os
import uuid

from matplotlib.ticker import MaxNLocator
from database.database import connect_db
from database.database_manager import (
    get_stistic_city_db,
    get_new_users_by_day
)

async def statistic_citys_graph():
    #переиспользование подключения к бд
    pool = await connect_db()
    async with pool.acquire() as conn:

        city_counts = await get_stistic_city_db(conn)

    sorted_items = sorted(city_counts.items(), key=lambda x: x[1], reverse=True)
    cities = [item[0] for item in sorted_items]
    counts = [item[1] for item in sorted_items]

    plt.figure(figsize=(10, 6))
    bars = plt.bar(cities, counts, color='skyblue')

    if len(bars) > 0:
        bars[0].set_color('orange')  # 1 место
    if len(bars) > 1:
        bars[1].set_color('gray')  # 2 место
    if len(bars) > 2:
        bars[2].set_color('#cd7f32')  #3 место

    plt.xlabel('Города')
    plt.ylabel('Количество выборов')
    plt.title('Статистика популярности городов')
    plt.xticks(rotation=45)
    plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.tight_layout()

    filename = f"city_stat_{uuid.uuid4().hex}.png"
    filepath = os.path.join("temp", filename)
    os.makedirs("temp", exist_ok=True)
    plt.savefig(filepath)
    plt.close()

    return filepath

async def new_users_graph():
    # переиспользование подключения к бд
    pool = await connect_db()
    async with pool.acquire() as conn:
        stats = await get_new_users_by_day(conn)

    today = datetime.now().date()
    dates = [(today - timedelta(days=i)).strftime('%Y-%m-%d') for i in reversed(range(10))]
    counts = [stats.get(date, 0) for date in dates]

    plt.figure(figsize=(10, 6))
    plt.plot(dates, counts, marker='o', linestyle='-', color='teal')

    plt.xlabel('Дата')
    plt.ylabel('Новые пользователи')
    plt.title('Новые пользователи за последние 10 дней')
    plt.xticks(rotation=45)
    plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.tight_layout()

    filename = f"new_users_{uuid.uuid4().hex}.png"
    filepath = os.path.join("temp", filename)
    os.makedirs("temp", exist_ok=True)
    plt.savefig(filepath)
    plt.close()

    return filepath