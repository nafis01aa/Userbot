from Bot import schedule_conn

class UMdb:
    @staticmethod
    async def insert_schedule_data(self, data):
        return await schedule_conn.insert_one(data)

    @staticmethod
    async def remove_schedule_data(self, id):
        return await schedule_conn.remove_one({'_id': id})
