import asyncio
import aioredis


async def create_redis_pool():
    # 创建 Redis 连接池
    redis = await aioredis.Redis.from_url(
        "redis://localhost",
        encoding="utf-8",
        socket_timeout=5,
        socket_connect_timeout=5,
        retry_on_timeout=True,
        decode_responses=True,
        max_connections=10  # 设置连接池的最大连接数
    )
    return redis


async def close_redis_pool(redis):
    # 关闭 Redis 连接池
    redis.close()
    await redis.wait_closed()


async def get(key):
    # 从 Redis 获取数据
    redis = await create_redis_pool()
    value = await redis.get(key)
    await close_redis_pool(redis)
    return value


async def set(key, value):
    # 向 Redis 存储数据
    redis = await create_redis_pool()
    await redis.set(key, value)
    await close_redis_pool(redis)


async def delete(key):
    # 从 Redis 删除数据
    redis = await create_redis_pool()
    await redis.delete(key)
    await close_redis_pool(redis)


async def incr(key):
    # Redis 自增操作
    redis = await create_redis_pool()
    value = await redis.incr(key)
    await close_redis_pool(redis)
    return value


# 主函数入口
async def main():
    # 测试 Redis 操作
    await set('test_key', 'test_value')
    print(await get('test_key'))
    await incr('counter')
    print(await get('counter'))
    await delete('test_key')
    await delete('counter')


# 运行主函数
if __name__ == '__main__':
    asyncio.run(main())
