import os

def is_directory_empty(path):
    """检查目录是否为空"""
    # 使用 os.listdir() 获取目录内容
    if os.path.exists(path) and os.path.isdir(path):
        return len(os.listdir(path)) == 0
    return False
