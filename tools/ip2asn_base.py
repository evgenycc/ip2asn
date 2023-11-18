import sqlite3
from pathlib import Path


def create_base() -> None:
    """
    Создаем базу данных sqlite.
    """
    conn = sqlite3.connect('ip2asn_v4.db')
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS ip2asn(
                   cidr TEXT,
                   asn TEXT,
                   country_code TEXT,
                   country TEXT,
                   owner TEXT);
                """)
    cur.execute(f'CREATE INDEX IF NOT EXISTS index_cidr ON ip2asn (cidr)')
    cur.execute(f'CREATE INDEX IF NOT EXISTS index_asn ON ip2asn (asn)')
    cur.execute(f'CREATE INDEX IF NOT EXISTS index_country_code ON ip2asn (country_code)')
    cur.execute(f'CREATE INDEX IF NOT EXISTS index_owner ON ip2asn (owner)')
    conn.commit()
    cur.close()
    conn.close()


def select_from_base(row: str, data: str) -> list:
    """
    Поиск домена в таблицах. Если не найдено, возвращается Fasle.
    Если найдено - возвращается список с доменами.
    """
    conn = sqlite3.connect('ip2asn_v4.db')
    cur = conn.cursor()
    cur.execute(f"""SELECT {row} FROM ip2asn WHERE {row} = ?""", (data, ))
    data = cur.fetchmany()
    cur.close()
    conn.close()
    return data if data else False


def save_base(data: list) -> None:
    """
    Сохранение списка доменов в таблицы. В зависимости от состояния переменной
    bad выполняется тот или иной код, который сохраняет данные в разные таблицы.
    """
    conn = sqlite3.connect('ip2asn_v4.db')
    cur = conn.cursor()
    cur.execute('BEGIN TRANSACTION')
    cur.executemany("INSERT INTO ip2asn VALUES(?, ?, ?, ?, ?);", data)
    conn.commit()
    cur.close()
    conn.close()
