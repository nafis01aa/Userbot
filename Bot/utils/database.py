from Bot import schedule_conn

class UMdb:
    @staticmethod
    async def insert_schedule_data(self, data):
        return await schedule_conn.insert_one(data)

    async def all(self):
        pass
