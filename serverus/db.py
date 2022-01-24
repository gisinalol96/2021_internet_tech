import aiosqlite
import sqlite3
from flask import jsonify


async def select_all():
    conn = await aiosqlite.connect('billboards.db')
    conn.row_factory = aiosqlite.Row
    query = "with a as (" \
            "select id || ';' || info || ';' || address as billboard" \
            "     , customer_id " \
            "from billboards" \
            ")" \
            "select id" \
            "     , name" \
            "     , group_concat(billboard) as billboards " \
            "from customers " \
            "left join a " \
            "on a.customer_id = id " \
            "group by id, name"
    cur = await conn.execute(query)
    customers = await cur.fetchall()
    await cur.close()
    await conn.close()
    return jsonify([{
        'customerID': customer['id'],
        'customerName': customer['name'],
        'billboards': [{
            'billboardID': billboard.split(';')[0],
            'info': billboard.split(';')[1],
            'address': billboard.split(';')[2]
        } for billboard in (customer['billboards'].split(',') if customer['billboards'] is not None else [])]
    } for customer in customers])


async def insert_customer(customer_dict):
    conn = await aiosqlite.connect('billboards.db')
    await conn.execute('insert into customers values (:id, :name)', customer_dict)
    await conn.commit()
    await conn.close()


async def insert_billboard(billboard_dict):
    conn = await aiosqlite.connect('billboards.db')
    await conn.execute('insert into billboards values (:id, :info, :address, :customer_id)', billboard_dict)
    await conn.commit()
    await conn.close()


async def delete_billboard(params):
    conn = await aiosqlite.connect('billboards.db')
    await conn.execute('delete from billboards '
                       'where customer_id = :customerID '
                       'and id = :billboardID', params)
    await conn.commit()
    await conn.close()


async def update_billboard(params, customer_id, billboard_id):
    conn = await aiosqlite.connect('billboards.db')

    query = "update billboards set {0} where id = :billboard_id and customer_id = :r_customer_id".format(
        ', '.join([f"{key} = :{key}" for key in params]))
    params['billboard_id'] = billboard_id
    params['r_customer_id'] = customer_id

    await conn.execute(query, params)
    await conn.commit()
    await conn.close()

# Первоначальное заполнение
if __name__ == '__main__':
    init = [
            {
                "customerID": 0,
                "customerName": "ООО 'Моя оборона'",
                "billboards": [
                    {
                        "billboardID": 0,
                        "info": "Помидоры лучшие",
                        "address": "Гамбург"
                    },
                    {
                        "billboardID": 1,
                        "info": "Яблоки",
                        "address": "Портсмут"
                    }
                ]
            },
            {
                "customerID": 1,
                "customerName": "ООО 'Рога и Копыта'",
                "billboards": [
                    {
                        "billboardID": 2,
                        "info": "Рога",
                        "address": "Верхняя Пыжма"
                    },
                    {
                        "billboardID": 3,
                        "info": "Копыта",
                        "address": "Нижняя Пыжма"
                    }
                ]
            },
            {
                "customerID": 2,
                "customerName": "ОАО 'АОА'",
                "billboards": [
                ]
            }
        ]
    sconn = sqlite3.connect('billboards.db')
    sconn.execute('drop table customers')
    sconn.execute('drop table billboards')
    sconn.execute('vacuum')
    sconn.execute('create table customers(id integer, name text)')
    sconn.execute('create table billboards(id integer, info text, address text, customer_id integer)')
    sconn.commit()
    query_customers = 'insert into customers values (?, ?)'
    query_billboards = 'insert into billboards values (?, ?, ?, ?)'
    scustomers = []
    sbillboards = []
    for scustomer in init:
        scustomers.append((scustomer['customerID'], scustomer['customerName']))
        for sbillboard in scustomer['billboards']:
            sbillboards.append((sbillboard['billboardID'], sbillboard['info'], sbillboard['address'], scustomer['customerID']))
    sconn.executemany(query_customers, scustomers)
    sconn.executemany(query_billboards, sbillboards)
    sconn.commit()
    sconn.close()
