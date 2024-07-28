import asyncio
import aiomysql


async def create_mysql_pool():
    # 创建连接池
    pool = await aiomysql.create_pool(
        host='127.0.0.1',
        port=3306,
        user='root',
        password='your_password',
        db='your_database',
        charset='utf8mb4',
        cursorclass=aiomysql.cursors.DictCursor,
        autocommit=True,
        minsize=5,  # 最小连接数
        maxsize=10,  # 最大连接数
        connect_timeout=10  # 设置连接超时时间
    )
    return pool


async def close_mysql_pool(pool):
    pool.close()
    await pool.wait_closed()


async def query(sql, args=None):
    pool = await create_mysql_pool()
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(sql, args)
            result = await cur.fetchall()
    await close_mysql_pool(pool)
    return result


async def execute(sql, args=None):
    pool = await create_mysql_pool()
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(sql, args)
    await close_mysql_pool(pool)


# 示例：查询操作
async def select_data():
    sql = "SELECT * FROM your_table WHERE id = %s"
    data = await query(sql, (1,))
    print(data)


# 示例：插入操作
async def insert_data():
    sql = "INSERT INTO your_table (column1, column2) VALUES (%s, %s)"
    await execute(sql, ('value1', 'value2'))


# 示例：更新操作
async def update_data():
    sql = "UPDATE your_table SET column1 = %s WHERE id = %s"
    await execute(sql, ('new_value', 1))


# 示例：删除操作
async def delete_data():
    sql = "DELETE FROM your_table WHERE id = %s"
    await execute(sql, (1,))


# 主函数入口
async def main():
    await select_data()
    await insert_data()
    await update_data()
    await delete_data()


# 选择多线程还是异步操作数据库，主要取决于你的应用需求、数据库类型、预期的负载以及你使用的编程语言和框架。下面是多线程和异步操作
# 数据库的一些关键差异和适用场景：
# 多线程
# 特点
# 并发执行：多线程可以让你的程序在多个线程中并发执行不同的任务，从而提高资源利用率和响应速度。
# 复杂性：多线程编程可能引入线程安全问题，需要考虑锁、死锁、竞态条件等问题。
# 资源消耗：每个线程都有自己的堆栈和上下文，可能会消耗更多的系统资源。
# 适用场景
# 当数据库操作是计算密集型而非 I/O 密集型时，多线程可以有效地利用多核处理器的能力。
# 对于需要执行复杂计算或长时间运行的任务，多线程可以避免阻塞主线程，保持 UI 或服务的响应性。
# 异步
# 特点
# 非阻塞：异步操作可以避免在等待 I/O 操作完成时阻塞线程，从而提高 I/O 密集型应用的效率。
# 资源效率：异步编程通常使用单线程或多线程事件循环，因此可以更高效地管理资源。
# 编程复杂性：异步编程可能需要更复杂的控制流和错误处理机制。
# 适用场景
# 当你的应用主要是 I/O 密集型的，如频繁的数据库读写、网络通信等，异步可以显著提高性能。
# 对于高并发的 Web 服务，异步可以更有效地处理大量并发请求，避免线程上下文切换带来的开销。
# 总结
# 如果你的应用需要处理大量的并发请求，并且大部分工作是 I/O 密集型的，那么异步可能是更好的选择。
# 如果你的应用涉及复杂的计算任务，或者你更熟悉多线程编程模型，多线程可能更适合。
# 在 Python 中，由于全局解释器锁（GIL）的存在，多线程在 CPU 密集型任务上的优势可能不如其他语言明显，而异步编程（如使用 asyncio）则可以更好地绕
# 过 GIL 的限制。
# 最终的选择应基于你的具体需求、预期的负载模式以及你对不同编程模型的熟悉程度。在某些情况下，结合使用多线程和异步编程
# （例如，在一个异步应用中使用多线程池处理 CPU 密集型任务）也可以是一个有效的策略。

# 运行主函数
if __name__ == '__main__':
    asyncio.run(main())
