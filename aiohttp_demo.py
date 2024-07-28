import asyncio
import aiohttp
import time


async def send_post_request():
    url = "https://httpbin.org/post"  # 目标 URL

    # 测量开始时间
    start_time = time.time()

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json={"key": "value"}) as response:
            # 等待响应
            resp_json = await response.json()
            # 测量结束时间
            end_time = time.time()

            # 输出响应内容和耗时
            print(f"Response: {resp_json}")
            print(f"Request took {end_time - start_time:.4f} seconds.")


# 主函数入口
async def main():
    await send_post_request()


# 运行主函数
if __name__ == '__main__':
    asyncio.run(main())
