import os
import hashlib
from multiprocessing import Pool, cpu_count


def file_slice_md5(file_path, start, size):
    """读取文件切片并计算MD5值"""
    with open(file_path, 'rb') as f:
        f.seek(start)
        data = f.read(size)
    return {
        'start_byte': start,
        'end_byte': start + size,
        'md5': hashlib.md5(data).hexdigest(),
        'data': data  # 存储数据可能占用大量内存，根据需要决定是否存储
    }


def process_file(file_path):
    """处理整个文件，将文件按指定大小切片，并计算每个切片的MD5值"""
    file_size = os.path.getsize(file_path)
    slice_size = 5 * 1024 * 1024  # 5MB
    num_slices = (file_size + slice_size - 1) // slice_size

    with Pool(processes=cpu_count()) as pool:
        slice_ranges = [(start, start + slice_size) for start in range(0, file_size, slice_size)]
        results = pool.starmap(file_slice_md5, [(file_path, start, slice_size) for start, _ in slice_ranges])

    # 按照切片的起始字节排序结果不是必要的，因为我们是连续读取的
    return results


def reconstruct_file(slices, output_file_path):
    """将切片数据写入新文件，以还原原始文件"""
    with open(output_file_path, 'wb') as f_output:
        for slice_info in slices:
            f_output.write(slice_info['data'])


if __name__ == '__main__':
    file_path = 'test.txt'  # 替换为你的大文件路径
    output_file_path = 'otest.txt'  # 还原后的文件路径

    # 处理文件并获取切片
    slices = process_file(file_path)

    # 还原文件
    reconstruct_file(slices, output_file_path)

    # 验证原始文件和还原后的文件是否相同
    original_md5 = hashlib.md5()
    reconstructed_md5 = hashlib.md5()

    # 计算两个文件的MD5值
    with open(file_path, 'rb') as f_original:
        while True:
            chunk = f_original.read(5 * 1024 * 1024)  # 读取5MB大小的块
            if not chunk:
                break
            original_md5.update(chunk)

    with open(output_file_path, 'rb') as f_reconstructed:
        while True:
            chunk = f_reconstructed.read(5 * 1024 * 1024)  # 读取5MB大小的块
            if not chunk:
                break
            reconstructed_md5.update(chunk)

    print(f"Original MD5: {original_md5.hexdigest()}")
    print(f"Reconstructed MD5: {reconstructed_md5.hexdigest()}")

    # 检查MD5值是否相同
    print("Verification result:", original_md5.hexdigest() == reconstructed_md5.hexdigest())
