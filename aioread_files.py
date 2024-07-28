import asyncio
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


async def match_content_in_file(filename: str, content: str, encoding: str = "gbk") -> bool:
    async with aiofiles.open(filename, mode="r", encoding=encoding) as f:
        # text = await f.read()
        # return content in text

        async for line in f:
            if content in line:
                return True


def match_content_in_file2(filename: str, content: str, encoding: str = "gbk") -> bool:
    with open(filename, mode="r", encoding=encoding) as f:
        # text = f.read()
        # return content in text

        for line in f:
            if content in line:
                return True


async def main3():
    start = time.time()
    tasks = [match_content_in_file(f, '808395') for f in files]
    l = await asyncio.gather(*tasks)
    print(l)
    end = time.time()
    print(end - start)


def main2():
    start = time.time()
    l = []
    for f in files:
        l.append(match_content_in_file2(f, '808395'))
    print(l)
    end = time.time()
    print(end - start)


# python 编写协程时，使用 aiofiles 比 open 还慢_aiofiles 有必要吗

# 这个问题主要是磁盘 io 与网络 io 不同，磁盘顺序读写单个文件最快，并发读写会涉及到多个文件的切换问题，反而花了更多的时间，所以异步编程使用 aiofiles 要谨慎。
# 也大致的想了一下如果解决这个问题的办法，可以考虑把文件读写任务抽离出来，放到队列里面，然后用专门的线程或进程去按顺序去处理，这样就可以实现异步处理并且速度也快

# 对比分析：
# 在实际运行中，main3（异步方式）的运行时间比 main2（同步方式）更长，这可能是因为异步操作的额外开销，如事件循环的调度、上下文切换等。
# 然而，在处理大量文件或大文件时，异步方式通常会表现出更好的性能，因为它可以避免长时间的 I/O 阻塞，充分利用 CPU 和 I/O 资源。
# 如果异步方式表现不佳，可能需要检查是否有其他因素影响了性能，例如文件系统的瓶颈、网络延迟（如果文件不在本地）、或者异步代码中的阻塞操作等。
if __name__ == '__main__':
    asyncio.run(main3())  # 很慢
    main2()  # 很快
