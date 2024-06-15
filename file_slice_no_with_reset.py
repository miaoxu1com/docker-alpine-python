import os
import hashlib
import asyncio
from multiprocessing import Pool, cpu_count, Manager
from concurrent.futures import ThreadPoolExecutor
import timeit


# 读取文件切片并计算MD5的函数
def process_file_chunk(args):
    file_path, index, start, end = args
    try:
        # 读取文件切片
        with open(file_path, 'rb') as f:
            f.seek(start)
            data = f.read(end - start)
        # 计算MD5
        md5_digest = hashlib.md5(data).hexdigest()
        return (index, {
            'start_byte': start,
            'end_byte': end,
            'md5': md5_digest,
            'data': data  # 根据需要，可以选择存储或不存储数据
        })
    except Exception as e:
        # 如果出现异常，返回错误信息
        return index, {'error': str(e)}


# 主函数，分配任务到多个进程
def main(file_path, chunk_size):
    file_size = os.path.getsize(file_path)
    num_chunks = (file_size + chunk_size - 1) // chunk_size
    chunk_params = [(file_path, i, i * chunk_size, min((i + 1) * chunk_size, file_size)) for i in range(num_chunks)]

    with Pool(processes=cpu_count()) as pool:
        # 使用starmap分发任务和参数
        result_items = pool.map(process_file_chunk, chunk_params)

        # 将结果按索引排序
    result_items.sort(key=lambda x: x[0])
    for index, result in result_items:
        if 'error' in result:
            print(f"Error processing chunk {index}: {result['error']}")
        else:
            print(f"Chunk {index} from {result['start_byte']} to {result['end_byte']} - MD5: {result['md5']}")


def test_main():
    file_path = 'test.txt'  # 替换为你的大文件路径
    chunk_size = 5 * 1024 * 1024  # 5MB
    main(file_path, chunk_size)


if __name__ == '__main__':
    test_main()
    # t = timeit.timeit(test_main, number=10)
    # print("耗时", t)
