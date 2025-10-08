import glob
import os
import json
import shutil

# 配置路径
assets_path = "F:/软件/.minecraft/assets"
indexes_file = os.path.join(assets_path, "indexes/1.19.json")
output_dir = "MCmusic"
keywords = ['music', 'sounds']


try:
    os.mkdir(output_dir)
except FileExistsError:
    pass


with open(indexes_file, 'r', encoding='utf-8') as f:
    json_db = json.load(f)

# 获取所有资源文件路径
music_all_path_db = os.path.join(assets_path, "objects", "*", "*")
filepath_all = glob.glob(music_all_path_db)

# 创建哈希到路径的映射
filepath_all_zd = {os.path.basename(path): path for path in filepath_all}


def extract_music(data, result=None):
    """递归提取音乐文件信息"""
    if result is None:
        result = {'objects': {}}

    if isinstance(data, dict):
        for key, value in data.items():
            if key == 'objects':
                if isinstance(value, dict):
                    for file_path, file_data in value.items():
                        if any(keyword in file_path.lower() for keyword in keywords) and isinstance(file_data, dict):
                            if 'hash' in file_data and 'size' in file_data:
                                result['objects'][file_path] = {
                                    'hash': file_data['hash'],
                                    'size': file_data['size']
                                }
            else:
                extract_music(value, result)
    elif isinstance(data, list):
        for item in data:
            extract_music(item, result)
    return result


json_get_music = extract_music(json_db)['objects']
hashes = [file_info['hash'] for file_info in json_get_music.values()]

missing_hashes = []
for i, file_hash in enumerate(hashes):
    if file_hash not in filepath_all_zd:
        missing_hashes.append(file_hash)
        continue

    src_path = filepath_all_zd[file_hash]
    dst_path = os.path.join(output_dir, f"{i}.ogg")

    try:
        shutil.copyfile(src_path, dst_path)
    except Exception as e:
        print(f"Failed to copy {src_path}: {e}")

if missing_hashes:
    print("Missing files (hashes not found):")
    for h in missing_hashes:
        print(h)