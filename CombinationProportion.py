import sqlite3
conn = sqlite3.connect('auth.db')

# 创建一个Cursor:
cursor = conn.cursor()

#查询生成的驱动
#cursor.execute('''select driver_code FROM fuzz_record_pytorch;''') 
cursor.execute('''select driver_code FROM fuzz_record_tensorflow;''') 
rows = cursor.fetchall()



# 关闭连接
cursor.close()
conn.close()


#1.先提取这个驱动代码里面所有的api

#deal_document_path =  r"D:\桌面整理\20250108\鸿蒙\data\HMFuzzerdata\api_def_torch.txt"
deal_document_path =  r"D:\桌面整理\20250108\鸿蒙\data\HMFuzzerdata\api_def_tf.txt"


#读取pytorch 文档
apis = []
with open(deal_document_path, 'r',encoding='utf-8',errors='ignore') as file:
    # 读取文件内容
    line = file.readline()
    while line:
        # 处理每一行数据
        #print(line)
        line = file.readline()
        apis.append(line)

#判断驱动中的api是否在深度学习库中
def is_in_apis(api):
    global apis
    for apitemp in apis:
        if api in apitemp:
            return True;
    return False


#提取驱动中的api
import re

FUNC_CALL_RE = re.compile(r'\b([A-Za-z_][A-Za-z0-9_]*)\s*\(')
FALSE_POS = {
    'if', 'elif', 'while', 'for', 'def', 'class', 'with', 'except'
}

def extract_calls(source: str) -> list[str]:
    seen = set()
    result = []
    for name in FUNC_CALL_RE.findall(source):
        if name not in FALSE_POS and name not in seen:
            seen.add(name)
            result.append(name)
    return result


#统计组合API的数量
comNum = 0;
for row in rows:
    num = 0 #当前驱动包含api的数量
    fucs = extract_calls(row[0])  #提取所有的函数
    for fuc in fucs:
        if is_in_apis(fuc):
            num = num + 1;

    if num >= 2:
        comNum = comNum + 1;

print(f"总共:{len(rows)},组合驱动：{comNum}")
    


    


#2.判断这些API是否在api列表中，如果存在两个以上认为是组合驱动


