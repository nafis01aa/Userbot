from Bot import schedule_conn

class Mongodb:
    async def insert_data(self, data):
        return await schedule_conn.insert_one(data)

    async def all(self):
        pass
