import requests
import json,time
import os,re
from openai import OpenAI

def dynamic_format(template, data):
    import re
    # 正则表达式用于匹配 {...}
    pattern = re.compile(r"\{(\w+)\}")
    
    def replacer(match):
        key = match.group(1)
        return str(data.get(key, match.group(0)))  # 如果 key 不在 data 中则返回原样输出
    
    return pattern.sub(replacer, template)


def gpt4Test(prompt):
    while True:
        try:
           
            client = OpenAI(
                api_key = "b501ca1f-083c-4311-8cbd-0586449bcd57",
                base_url = "https://ark.cn-beijing.volces.com/api/v3",
            )

            # Non-streaming:
            print("----- standard request -----")
            completion = client.chat.completions.create(
                model = "deepseek-r1-250120",  # your model endpoint ID
                messages = [
                    {"role": "system", "content": "You are a skilled writer of the HarmonyOS Fuzzy Test Driver (arkts language, which is similar to typescript) and can generate fuzzy test driver code based on user input"},
                    {"role": "user", "content": prompt
                    },
                ],
            )
            return completion.choices[0].message.content;
        except:
            print("获取msg异常")
            time.sleep(0.1)
            continue

data_template = r'''
    **task requirements**: You are a fuzzy test seed generator,Generate a batch of initial seeds for fuzz testing for each API based on the following documentation and code,The output only contains JSON itself and does not contain any other content.
    [document]
    {document}

    [code]
    ```code
    {code}
    ```
    [Instruction]
    Generate an initial seed list for each API in the code based on the documentation, with the output format in JSON format and the api name as the key. and the seed list as the value. 
    
   
    ```

    [output]
     ```json
    {
        "hceService.startHCE" : [[
            "123", "456"
        ],[
            "789", "111213"
        ]],

        "hceService.sendResponse" : [
            [0x00, 0xA4, 0x04, 0x00, 0x0E, 0x32, 0x50, 0x41, 0x59, 0x2E, 0x53, 0x59, 0x53, 0x2E, 0x44, 0x44, 0x46, 0x30, 0x31, 0x00],
            [0x90, 0x00]
        ]
    }
    ```

    [output]
'''


import re

def extract_between(text, start_marker, end_marker, use_regex=True):
    """
    提取两个字符串之间的内容。

    参数:
        text (str): 要处理的文本。
        start_marker (str): 起始标记。
        end_marker (str): 结束标记。
        use_regex (bool): 是否使用正则表达式。默认为False。

    返回:
        str: 提取的内容，如果没有找到则返回None。
    """
    if use_regex:
        # 使用正则表达式提取内容
        pattern = re.escape(start_marker) + r'(.*?)' + re.escape(end_marker)
        match = re.search(pattern, text, re.DOTALL)
        if match:
            return match.group(1).strip()
        else:
            return None
    else:
        # 使用普通字符串操作提取内容
        start_index = text.find(start_marker)
        if start_index == -1:
            return None
        start_index += len(start_marker)

        end_index = text.find(end_marker, start_index)
        if end_index == -1:
            return None

        return text[start_index:end_index].strip()



import sqlite3
conn = sqlite3.connect('auth.db')

# 创建一个Cursor:
cursor = conn.cursor()
cursor.execute('''select * FROM driver_info_ds  where driver_is_success = 'success';''') 

rows = cursor.fetchall()

seed_gen_prompts = []
for row in rows:
    document_data = row[5]
    code = row[6]
    document_data = extract_between(document_data,"[document]","[Instruction]").strip("[document]")

    p = {'document' : document_data,"code" : code}
    res = dynamic_format(data_template,p)
    seed_gen_prompts.append((res,row[1]))
    



num = 0;
current_row = 888;  #从第几条开始继续（断点）
over_row = current_row + 10000      #第几条开始结束
print("总共多少条: " + str(len(seed_gen_prompts)))
for driver_prompt  in seed_gen_prompts:
    print("当前第" + str(num) + "条数据")
    if num < current_row:
        num = num + 1;
        continue

    if num > over_row:
        print("结束")
        break

    driver_prompt = seed_gen_prompts[num][0]
    path = seed_gen_prompts[num][1]

    seeds = gpt4Test(driver_prompt)
    
    print(driver_prompt)
    print("---------------------------------")
    print(seeds)
    print("################################")
    #exit()
    

    data = (path,seeds)
    cursor.execute('''
            INSERT INTO seed_info_ds (path,seeds) VALUES (?, ?)
            ''', data)

    
    # 提交事务
    conn.commit()
    num = num + 1;
    #exit();
    

# 关闭连接
cursor.close()
conn.close()

