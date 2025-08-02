import asyncpg
import logging

class Database:
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.pool = None
        
    async def connect(self):
        self.pool = await asyncpg.create_pool(
            self.database_url,
            min_size=10,
            max_size=50,
            command_timeout=60
        )
        logging.info("Database connection pool created")
        
    async def disconnect(self):
        if self.pool:
            await self.pool.close()
            
    async def execute(self, query: str, *args):
        async with self.pool.acquire() as connection:
            return await connection.execute(query, *args)
            
    async def fetch(self, query: str, *args):
        async with self.pool.acquire() as connection:
            return await connection.fetch(query, *args)
            
    async def fetchrow(self, query: str, *args):
        async with self.pool.acquire() as connection:
            return await connection.fetchrow(query, *args)