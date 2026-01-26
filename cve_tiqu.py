#递归读取某个文件下所有的json内容
import os
import json
import sqlite3,json
conn = sqlite3.connect('auth.db')

# 创建一个Cursor:
cursor = conn.cursor()
#cursor.execute('''''') 


def read_json_files(folder_path):
    """
    递归读取指定文件夹及其子文件夹中的所有 JSON 文件内容

    参数:
        folder_path (str): 要读取的文件夹路径

    返回:
        list: 包含所有 JSON 文件内容的列表
    """
    json_contents = []

    # 遍历文件夹及其子文件夹
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            # 检查文件扩展名是否为 .json
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                try:
                    #print(file_path)
                    # 打开并读取 JSON 文件
                    with open(file_path, 'r', encoding='utf-8') as f:
                        json_content = json.load(f)
                        #json_contents.append(json_content)
                        #print(f"成功读取文件: {json_content}")
                        #开始解析json文件
                        product  = json_content["containers"]["cna"]["affected"][0]["product"]
                        vendor = json_content["containers"]["cna"]["affected"][0]["vendor"]
                        status = json_content["containers"]["cna"]["affected"][0]["versions"][0]["status"]
                        version = json_content["containers"]["cna"]["affected"][0]["versions"][0]["version"]
                        cveId = json_content["cveMetadata"]["cveId"]
                        dateReserved = json_content["cveMetadata"]["dateReserved"]
                        datePublished =  json_content["cveMetadata"]["datePublished"]
                        dateUpdated =  json_content["cveMetadata"]["dateUpdated"]
                        descriptions =  json_content["containers"]["cna"]["descriptions"][0]["value"]
                        #print(product,version)
                        if(product == "HarmonyOS" and version == "5.0.0"):
                            data = (cveId,product,vendor,status,version,dateReserved,datePublished,dateUpdated,descriptions,json.dumps(json_content))
                            #cursor.execute('''
                            #INSERT INTO hm_current_cve_bug_list (cwe_id,product,vendor,status,version,dateReserved,datePublished,dateUpdated,descriptions,remark) VALUES (?, ?,?, ?,?, ?, ?,?, ?,?)
                            #''', data)
                            #conn.commit()
                            json_contents.append(data)


                except Exception as e:
                    print(f"读取文件 {file_path} 时出错: {e}")
                    pass

    return json_contents

folder_path = r"D:\1\main2\cvelistV5-main\cves\2025"
all_json_contents = read_json_files(folder_path)
print(f"共读取到 {len(all_json_contents)} 个 JSON 文件的内容")



# 提交事务
conn.commit()
# 关闭连接
cursor.close()
conn.close()
