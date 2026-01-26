import os
import markdown
import re
import json

import sqlite3
conn = sqlite3.connect('auth.db')

# 创建一个Cursor:
cursor = conn.cursor()
 
# 执行SQL语句，创建user表:
cursor.execute('''CREATE TABLE IF NOT EXISTS auth_info 
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    auth_name VARCHAR(256),
    auth_des VARCHAR(2048),
    auth_level VARCHAR(128),
    auth_mode VARCHAR(128),
    auth_acl VARCHAR(128),
    auth_Valid VARCHAR(128)
)
''')

def list_files(directory):
    return [os.path.join(directory, file) for file in os.listdir(directory)]

# 使用正则表达式提取信息
def parse_markdown_to_json(markdown_text):
    # 按照标题分割文本
    sections = re.split(r'\n## ', markdown_text.strip())
    sections[0] = sections[0].replace("\n", "")  # 清除第一个标题前的换行

    result = []
    resultY = []
    for section in sections:
        # 提取权限名称
        auth_name_match = re.search(r'^ohos\.permission\.\w+', section)
        auth_name = auth_name_match.group(0) if auth_name_match else ""

        # 提取权限描述
        auth_des_match = re.search(r'^ohos\.permission\.\w+\n\n(.+?)\n\n', section, re.DOTALL)
        auth_des = auth_des_match.group(1).strip() if auth_des_match else ""

        # 提取其他字段
        auth_level = re.search(r'\*\*Permission level\*\*: (\w+)', section).group(1) if re.search(r'\*\*Permission level\*\*: (\w+)', section) else ""
        auth_mode = re.search(r'\*\*Authorization mode\*\*: (\w+)', section).group(1) if re.search(r'\*\*Authorization mode\*\*: (\w+)', section) else "system_grant"
        auth_acl = re.search(r'\*\*Enable via ACL\*\*: (\w+)', section).group(1) if re.search(r'\*\*Enable via ACL\*\*: (\w+)', section) else ""
        auth_valid = re.search(r'\*\*Valid since\*\*: (\d+)', section).group(1) if re.search(r'\*\*Valid since\*\*: (\d+)', section) else ""
        
        # 将提取的信息添加到结果列表
        if(auth_name != ""):
            result.append({
                "auth_name": auth_name,
                "auth_des": auth_des,
                "auth_level": auth_level,
                "auth_mode": auth_mode,
                "auth_acl": auth_acl,
                "auth_Valid": auth_valid
            })
            resultY.append((auth_name,auth_des,auth_level,auth_mode,auth_acl,auth_valid))
    return resultY


auth_files_dir = r"D:\桌面整理\20250108\鸿蒙\doc\docs\en\okmddir\auths"
file_list = list_files(auth_files_dir)
for file1 in file_list:
    with open(file1, 'r',encoding='utf-8',errors='ignore') as file:
        # 读取文件内容
        content = file.read()
        parsed_datas = parse_markdown_to_json(content)
        for data in parsed_datas:
            # 插入数据，id会自动增加
            cursor.execute('''
            INSERT INTO auth_info (auth_name, auth_des,auth_level,auth_mode,auth_acl,auth_Valid)
            VALUES (?, ?,?, ?,?, ?)
            ''', data)


# 提交事务
conn.commit()
# 关闭连接
cursor.close()
conn.close()


