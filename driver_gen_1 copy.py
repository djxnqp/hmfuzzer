import requests

import requests
import json,time
import subprocess
cookie = "_ga=GA1.1.1356203443.1737082635; gptSessionId=810fc7fb-62f8-4d14-b40e-5483d599ef1b; _ga_C8Z1RNL7H7=GS1.1.1740110319.66.0.1740110319.0.0.0"

def getMessageID(prompt):
    #print(prompt)
    global cookie
    url = 'https://www.chatgp4.com/api/gpt/chat/sendMessage'
    headers = {
        'accept': 'application/json',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-type': 'application/json',
        'cookie': cookie,
        'origin': 'https://www.chatgp4.com',
        'referer': 'https://www.chatgp4.com/gpt/',
        'sec-ch-ua': '";Not A Brand";v="99", "Chromium";v="94"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 SE 2.X MetaSr 1.0'
    }
    data = {"chatId":113054,"type":"gpt4","prompt":prompt,"image":[]}
    response = requests.post(url,headers=headers,json=data,timeout=30)
    #print(response.text)
    dictionary = json.loads(response.text)
    return dictionary["messages"][1]["id"]


def  getMessage(ID):
    global cookie
    url = 'https://www.chatgp4.com/api/gpt/chat/prompt'
    headers = {
        'accept': 'application/json',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-type': 'application/json',
        'cookie': cookie,
        'origin': 'https://www.chatgp4.com',
        'referer': 'https://www.chatgp4.com/gpt/',
        'sec-ch-ua': '";Not A Brand";v="99", "Chromium";v="94"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 SE 2.X MetaSr 1.0'
    }
    data = {"chatId":113054,"messageId":ID}
    response = requests.post(url,headers=headers,json=data,timeout=30)
    response.encoding = 'utf-8'  # 明确指定编码方式

    #print(response.text)
    return response.text

def gpt4Test1(prompt):
    while True:
        try:
            ID = getMessageID(prompt)
            break
        except:
            print("获取ID异常")
            time.sleep(0.1)
            continue
    while True:
        try:
            msg = getMessage(ID)
            return msg
        except:
            print("获取msg异常")
            time.sleep(0.1)
            continue

import requests
def gpt4Test2(prompt):
    while True:
        try:
            url = 'http://159.138.133.44:6009/predict'
            data = {'text': prompt}
            headers = {'Content-Type': 'application/json'}
            response = requests.post(url, json=data, headers=headers,timeout=300)
            return response.text  
        except:
            print("获取msg异常")
            time.sleep(0.1)
            continue

    #print(response.status_code)  # 打印状态码
    # 打印响应内容

import os,re
from openai import OpenAI

def gpt4Test(prompt):
    num = 0
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
                #max_tokens = 92769
            )
            return completion.choices[0].message.content;
        except:
            num = num + 1
            if(num > 5):
                return None
            print("获取msg异常")
            time.sleep(0.1)
            continue



import os


import re
from typing import Tuple

def getTitleAndContent(content):
    """
    从给定文档中提取标题和描述。
    
    参数
    ----
    content : str
        完整的文档字符串（支持换行符）。
    
    返回
    ----
    Tuple[str, str]
        (title, description)
    """
    if not content:
        return "", ""
    
    # 去掉首尾空白，方便后续处理
    text = content.strip()
    
    # 1. 取一级标题
    #    ^#\s+(.+)$  仅匹配行首的 "# xxx"
    title_match = re.search(r'^#\s+(.+)$', text, flags=re.MULTILINE)
    title = title_match.group(1).strip() if title_match else ""
    
    # 2. 取紧跟标题后的第一段纯文本（非空行、非标题、非代码块、非列表）
    #    先去掉标题行本身
    body = text[title_match.end():] if title_match else text
    
    #    用空行分段，取第一段即可
    first_para = body.strip().split('\n\n')[0] if body.strip() else ""
    
    #    去掉首尾空白、去掉多余换行
    description = " ".join(first_para.split())
    
    return title, description

#封装
def get_md_files(directory):
    md_files = []
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            if file_path.endswith('.md'):
                md_files.append(file_path)
        else:
            md_files.extend(get_md_files(file_path))
    return md_files

import chromadb

def  getAndroidExample(title,content1):
    res = []
    # 1. 连接/创建本地数据库
    client = chromadb.PersistentClient(path="./chroma_db2")

    # 2. 获取或新建 Collection
    collection = client.get_or_create_collection(name="faq")

    # 3. 写入几条示例文档（已存在可跳过）
    if collection.count() == 0:
        docs = [
            title,
            content1,
        ]
        collection.add(documents=docs, ids=[f"id{i}" for i in range(len(docs))])

    # 4. 按相似性检索：返回前 5 个
    query = "数据库连接失败怎么办？"
    results = collection.query(
        query_texts=[query],  # 可一次传多条
        n_results=2           # 返回前 5 条
    )

    # 5. 打印结果
    for doc, dist in zip(results["documents"][0], results["distances"][0]):
        print(f"{dist:.3f}  {doc}")
        res.append(results["documents"][0])
    return res


#封装驱动生成提示词
driver_prompt_list = []
document_paths = []
driver_prompt_template = '''
Execute [instruction] based on [document]
[document]
{documentPlaceholder}
[example]
{example}
[Instruction]
1.**import requirements**：  Import the corresponding package based on [document]
2.**Drive requirements**:Generate a fuzzy test driver that covers all APIs of [document] as much as possible
3.**Driver calling**: We need to provide an example of driver invocation that meets the following requirements: 
##1.Import the corresponding package at the//package position in the following ts code，Check not to import packages repeatedly
##2.Insert the fuzz test driver call code at thev//code position in the following ts code
```ts
    import common from '@ohos.app.ability.common';
    import window from '@ohos.window';
    //package

    @Entry
    @Component
    struct KeepScreenOn {
    @State message: string = '常亮状态 : '
    @State isScreenOn: boolean = false
    private context: common.BaseContext = getContext(this) as common.BaseContext

    async keepScreenOn(status:boolean) {
        let windowClass = await window.getLastWindow(this.context) //获取窗口实例
        await windowClass.setWindowKeepScreenOn(status) //设置窗口常亮或取消
        this.isScreenOn = await windowClass.getWindowProperties().isKeepScreenOn//查看屏幕常亮状态
    }

    onPageShow(): void {
        this.keepScreenOn(true)
        //code
    }

    build() {
        Row() {
        Column() {
            Text(this.message + this.isScreenOn)
            .fontSize(50)
            .fontWeight(FontWeight.Bold)
        }
        .width('100%')
        }
        .height('100%')
        }
    }
```
4.**code requirements**: The generated content only includes the code itself and does not contain any other content,The output code is included in ```ts ```
5.**Debugging information requirements**: If the generated driver code contains debugging output information such as
Both console.info () and console.error() use hilog.error() and hilog.info(), and their function declarations are as follows
```ts
/**
* Outputs error-level logs.
*
* @param { number } domain Indicates the service domain, which is a hexadecimal integer ranging from 0x0 to 0xFFFF
* @param { string } tag Identifies the log tag, length cannot exceed 32 bytes.
* @param { string } format Indicates the log format string.
* @param { any[] }args Indicates the log parameters.
* @syscap SystemCapability. HiviewDFX.HiLog
* @crossplatform
* @atomicservice
* @since 11
*/
function error(domain: number, tag: string, format: string, ...args: any[]): void;

/**
* Outputs info-level logs.
*
* @param { number } domain Indicates the service domain, which is a hexadecimal integer ranging from 0x0 to 0xFFFF
* @param { string } tag Identifies the log tag, length cannot exceed 32 bytes.
* @param { string } format Indicates the log format string.
* @param { any[] }args Indicates the log parameters.
* @syscap SystemCapability. HiviewDFX.HiLog
* @crossplatform
* @atomicservice
* @since 11
*/
function info(domain: number, tag: string, format: string, ...args: any[]): void;

For example:
hilog.error(0x0000, 'testTag', 'Failed to load the content. Cause: % {public}s ',  JSON.stringify(err) ?? '');
hilog.info(0x0000, 'testTag', 'Succeeded in loading the content.');
```
'''
#print(data_template)

def dynamic_format(template, data):
    import re
    # 正则表达式用于匹配 {...}
    pattern = re.compile(r"\{(\w+)\}")
    
    def replacer(match):
        key = match.group(1)
        return str(data.get(key, match.group(0)))  # 如果 key 不在 data 中则返回原样输出
    
    return pattern.sub(replacer, template)

deal_document_path =  r"D:\桌面整理\20250108\鸿蒙\doc\docs\en\okmddir"
files = get_md_files(deal_document_path)
for file in files:
  with open(file, 'r',encoding='utf-8',errors='ignore') as file1:
    # 读取文件内容
    content = file1.read()
    #print(driver_prompt_template.format({'documentPlaceholder' : content}))
    title,content1 =  getTitleAndContent(content)
    example  = getAndroidExample(title,content1)
    p = {'documentPlaceholder' : content,"example" : example}
    res = dynamic_format(driver_prompt_template,p)
    #print(res)
    #exit()
    driver_prompt_list.append(res)
    document_paths.append(file)
#print(driver_prompt_list)
#complie()


#修改驱动
compile_prompt = '''
Based on the compilation output[compilationoutput], determine whether the code has been compiled successfully. If it has been approved(The content of [compilationoutput] includes the BUILD SUCCESSFUL statement), reply with 'accepted'. Otherwise, modify the code[code].
[compilationoutput]
{}
[code]
{}
[Instruction]
**code requirements**: The generated content only includes the code itself and does not contain any other content,The output code is included in ```ts ```
**reply requirements**: Based on the compilation output[compilationoutput], determine whether the code has been compiled successfully. If it has been approved(The content of [compilationoutput] includes the BUILD SUCCESSFUL statement), reply with 'accepted'. Otherwise, modify the code[code].
'''
compile_num = 10


import re
#调用编译工具
def cmdExec(command):
    # 使用subprocess.run来执行命令
    result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8')
    # 输出命令的执行结果
    #print("-------------------",result.stdout,result.stderr,"-------------------",)
    stdout, stderr = result.communicate()
    return stdout, stderr


def writeCodeFile(res):
    file = open(r"C:\Users\36132\DevEcoStudioProjects\MyApplication16\entry\src\main\ets\pages\Index.ets", "w",encoding = 'utf-8')
    file.write(res)
    file.close()


def complie():
  os.chdir(r"C:\\Users\\36132\\DevEcoStudioProjects\\MyApplication16")
  a,b = cmdExec(r'"D:\hm\DevEco Studio\tools\node\node.exe" "D:\hm\DevEco Studio\tools\hvigor\bin\hvigorw.js" --mode module -p module=entry@default -p product=default -p requiredDeviceType=phone assembleHap --analyze=normal --parallel --incremental --daemon')
  return  a + b


import sqlite3
conn = sqlite3.connect('auth.db')

# 创建一个Cursor:
cursor = conn.cursor()


#提取 TypeScript 代码
def extract_typescript_code(text):
    # 使用正则表达式匹配 ``` 包裹的内容，忽略代码语言标识
    pattern = r"```(?:\w+\n)?(.*?)```"
    code_blocks = re.findall(pattern, text, re.DOTALL)
    return code_blocks

num = 0;
current_row = 1340;  #从第几条开始继续（断点）
over_row = current_row + 10000      #第几条开始结束
print("总共多少条: " + str(len(driver_prompt_list)))
for driver_prompt  in driver_prompt_list:
    print("当前第" + str(num) + "条数据")
    if num < current_row:
        num = num + 1;
        continue

    if num > over_row:
        print("结束")
        break

    path = document_paths[num]
    driver_prompt = driver_prompt_list[num]
    print(driver_prompt)
    #exit(0)


    res = gpt4Test(driver_prompt)
    if res == None:
        num = num + 1;
        continue
    print("---------------生成的驱动代码")
    print(res)
    

    #print(res)
    try:
        res = extract_typescript_code(res)[0]
    except:
        num = num + 1;
        continue
    writeCodeFile(res)                      #大模型生成驱动代码
   
    c_num = 0;
    s_flag = "fail"
    code_new = res
    flagP = True
    flagP1 = True
    for i in range(compile_num):            #每一次生成编译10次
        c_num = c_num + 1;
        res1 =  complie()   
        res = compile_prompt.format(res1,res) #构建编译输出提示词
        res = gpt4Test(res)
        if res == None:
            flagP1 = False
            break;
            #num = num + 1;
            #continue
        print("---------------修改的驱动代码")
        print(res1)
        if("BUILD SUCCESSFUL" in res1): #成功
            print("-------------------------------------------------------------------------成功一次")
            print(code_new)
            s_flag = "success"
            break
        try:
            res = extract_typescript_code(res)[0]
        except:
            print("驱动解析异常2")
            print(res)
            flagP = False
        
        code_new = res
        writeCodeFile(res)
    if(flagP == False):
        continue
    
    if(flagP1 == False):
        num = num + 1;
        continue
    data = (path,str(c_num),s_flag,res1,driver_prompt,code_new)
    cursor.execute('''
            INSERT INTO driver_info_ds (driver_name, driver_compile_num,driver_is_success,driver_compile_output,driver_document_info,driver_code)
            VALUES (?, ?,?, ?,?, ?)
            ''', data)
    
    # 提交事务
    conn.commit()
    num = num + 1;
    #exit();

# 关闭连接
cursor.close()
conn.close()





