import contextlib
from typing import Optional, AsyncIterator

import asyncpg

from data import config


class Database:
    def __init__(self):
        self._pool: Optional[asyncpg.Pool] = None

    async def create_users_table(self):
        sql = '''create table if not exists users(
        user_id BIGINT PRIMARY KEY
        );
        '''
        await self.execute(sql, execute=True)

    async def create_viewed_profiles_table(self):
        sql = '''create table if not exists viewed_profiles(
        user_and_viewed_profile_id BIGINT PRIMARY KEY,
        user_id BIGINT,
        FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE
        );
        '''
        await self.execute(sql, execute=True)

    async def add_user(self, user_id):
        sql = "INSERT INTO users (user_id) VALUES($1) returning *"
        return await self.execute(sql, user_id, execute=True)

    async def get_user(self, user_id):
        sql = "SELECT * FROM users WHERE user_id = $1"
        return await self.execute(sql, user_id, fetchrow=True)

    async def delete_user(self, user_id):
        sql = "DELETE FROM users WHERE user_id = $1"
        return await self.execute(sql, user_id, execute=True)

    async def add_viewed_profile(self, user_id, viewed_profile_id):
        sql = "INSERT INTO viewed_profiles (user_and_viewed_profile_id, user_id) VALUES($1, $2) returning *"
        user_and_viewed_profile_id = int(str(user_id) + str(viewed_profile_id))
        return await self.execute(sql, user_and_viewed_profile_id, user_id, execute=True)

    async def get_viewed_profile(self, user_and_viewed_profile_id):
        sql = "SELECT user_and_viewed_profile_id FROM viewed_profiles WHERE user_and_viewed_profile_id = $1"
        return await self.execute(sql, user_and_viewed_profile_id, fetchval=True)

    async def drop_tables(self):
        sql = 'DROP TABLE users CASCADE'
        await self.execute(sql, execute=True)
        sql = 'DROP TABLE viewed_profiles CASCADE'
        await self.execute(sql, execute=True)

    async def execute(self, command, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False
                      ):
        async with self._transaction() as connection:
            if fetch:
                result = await connection.fetch(command, *args)
            elif fetchval:
                result = await connection.fetchval(command, *args)
            elif fetchrow:
                result = await connection.fetchrow(command, *args)
            elif execute:
                result = await connection.execute(command, *args)
        return result

    @contextlib.asynccontextmanager
    async def _transaction(self) -> AsyncIterator[asyncpg.Connection]:
        if self._pool is None:
            self._pool = await asyncpg.create_pool(
                user=config.DB_USER,
                password=config.DB_PASS,
                host=config.DB_HOST,
                database=config.DB_NAME,
            )
        async with self._pool.acquire() as conn:
            async with conn.transaction():
                yield conn

    async def close(self) -> None:
        if self._pool is None:
            return None

        await self._pool.close()
