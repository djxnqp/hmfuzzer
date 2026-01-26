import os,re,time
from openai import OpenAI
import requests
import json,time
import tempfile
import subprocess
import os

deal_document_path =  r"D:\桌面整理\20250108\鸿蒙\data\HMFuzzerdata\api_def_torch.txt"


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

#开始生成驱动
PROMPT = '''
Generate a Python driver based on the API provided by the user as follows:
1) Import the corresponding Python library
2) Generate input data
3) Call the API provided by the user
Your output should only contain directly executable Python code and no other content,Please filter out the thought process（不要输出<think></think>内容和标签）

[API]

'''


def gpt4Test(prompt):
    num1 = 0;
    while True:
        try:
           
            client = OpenAI(
                api_key = "sk-mh8uQAAl6ipWUkrN9DZ1ull4iI4ppt8GstgkNUFRwg34dmYq",
                base_url = "https://api.suanli.cn/v1",
               
            )

            # Non-streaming:
            print("----- standard request -----")
            completion = client.chat.completions.create(
                model = "Qwen3-32B",  # your model endpoint ID
                messages = [
                    {"role": "system", "content": "You are an expert in fuzzy test drive generation for Python deep learning frameworks, capable of generating corresponding fuzzy test drives based on user-provided information"},
                    {"role": "user", "content": prompt
                    },
                ],
            )
            return completion.choices[0].message.content;
        except:
            num1 = num1 + 1
            if(num1 > 10):
                return None;
            print("获取msg异常")
            time.sleep(0.1)
            continue


#提取 python 代码
def extract_python_code(text):
    # 使用正则表达式匹配 ``` 包裹的内容，忽略代码语言标识
    pattern = r"```(?:\w+\n)?(.*?)```"
    code_blocks = re.findall(pattern, text, re.DOTALL)
    return code_blocks


def dynamic_format(template, data):
    import re
    # 正则表达式用于匹配 {...}
    pattern = re.compile(r"\{(\w+)\}")
    
    def replacer(match):
        key = match.group(1)
        return str(data.get(key, match.group(0)))  # 如果 key 不在 data 中则返回原样输出
    
    return pattern.sub(replacer, template)


#运行python 拿到结果
def run_python_code(code):
   
    try:
        # 创建一个临时文件
        with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as temp_file:
            temp_file.write(code.encode())  # 将代码写入临时文件
            temp_file_path = temp_file.name  # 获取临时文件的路径

        # 运行临时文件并捕获输出
        result = subprocess.run(
            ["python", temp_file_path],  # 指定Python解释器运行临时文件
            capture_output=True,        # 捕获标准输出和标准错误
            text=True                   # 以文本形式处理输出
        )

        # 删除临时文件
        os.remove(temp_file_path)

        # 检查运行是否成功
        if result.returncode == 0:
            return (1,result.stdout)  # 返回标准输出
        else:
            return (0,f"Error: {result.stderr}")  # 返回错误信息

    except Exception as e:
        return (0,f"An unexpected error occurred: {e}")  # 返回错误信息



PROMPT_REPAIR = '''
You are an expert in fixing Python code. Please modify the Python code according to the error message
[python_code]
{python_code}
[errorInfo]
{errorInfo}
'''

import sqlite3
conn = sqlite3.connect('auth.db')

# 创建一个Cursor:
cursor = conn.cursor()
num = 0
overnum = 65
for api in apis:
    try:
        if(num < overnum):
            num = num + 1
            continue
        if(api.strip() != ""):
            code_raw = extract_python_code(gpt4Test(PROMPT + api))
            print(code_raw[0])
            res = run_python_code(code_raw[0])
            print(res)
            errflag = 0;
            if(res[0] == 0):
                errflag = 1;
            run_res =  res[1];
            run_code =  code_raw[0];
            data = (api,run_code,run_res,str(errflag))
            
            cursor.execute('''
                    INSERT INTO fuzz_record_pytorch (path,driver_code,fuzz_log,is_error)
                    VALUES (?, ?,?, ?)
                    ''', data)
            conn.commit()
    except:
        continue

# 关闭连接
cursor.close()
conn.close()

      












