import asyncio
import concurrent.futures
import time

import aiofiles

files = [
    r'logfile/20210523.log',
    r'logfile/20210522.log',
    r'logfile/20210521.log',
    r'logfile/20210524.log',
    r'logfile/20210525.log',
    r'logfile/20210520.log',
    r'logfile/20210519.log',
]


def match_content_in_file_sync(filename: str, content: str, encoding: str = "gbk") -> bool:
    with open(filename, mode="r", encoding=encoding) as f:
        for line in f:
            if content in line:
                return True
    return False


async def match_content_in_file_async(executor, filename: str, content: str, encoding: str = "gbk") -> bool:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, match_content_in_file_sync, filename, content, encoding)


async def main4():
    start = time.time()
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=5)  # 创建线程池
    tasks = [match_content_in_file_async(executor, f, '808395') for f in files]
    results = await asyncio.gather(*tasks)
    print(results)
    end = time.time()
    print("Total time:", end - start)


if __name__ == '__main__':
    # 异步
    # 0.006074428558349609
    # 同步
    # 0.0009970664978027344
    # 线程池+异步+同步
    # 0.0049593448638916016
    asyncio.run(main4())
