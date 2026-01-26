import requests
import json,time
import os,re
from openai import OpenAI
import selectors
import os
import subprocess
from openai import OpenAI

import os,time
import json
import requests,threading
import paho.mqtt.publish as publish
import selectors
import random
import string

import os
import time
import datetime
import psutil

# 全局变量：维护自进程启动以来的峰值内存（单位：MB）
peek_memory_mb = 0.0

# 标记今天是否已经落盘过
_today_written = False


def get_current_memory_mb() :
    """
    获取当前进程已使用的物理内存（RSS，单位 MB）
    """
    process = psutil.Process(os.getpid())
    # rss 单位是字节，转成 MB
    return process.memory_info().rss / 1024 / 1024


def recordPeekMemory():
    """
    记录峰值内存，并在每天凌晨 00:00:00 把峰值写入 memory.txt
    """
    global peek_memory_mb, _today_written

    # 1. 更新峰值
    current = get_current_memory_mb()
    if current > peek_memory_mb:
        peek_memory_mb = current

    # 2. 判断是否到达 00:00:00
    now = datetime.datetime.now()
    if now.hour == 0 and now.minute == 0 and now.second == 0:
        # 防止同一秒内多次写入
        if not _today_written:
            _write_memory_log()
            _today_written = True
    else:
        # 过了 00:00:00 就把标记复位，等待下一个 00:00:00
        _today_written = False


def _write_memory_log():
    """
    把当天的峰值写入 memory.txt
    """
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    line = f'{timestamp},{int(peek_memory_mb)}M\n'
    with open('memory.txt', 'a', encoding='utf-8') as f:
        f.write(line)

def generate_random_string(length):
    random_string = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))
    return random_string

def get_response(userPrompt):
    print("----------------------提示词-------------------------")
    print(userPrompt)
    data = {'data': userPrompt}
    #print(data)
    code = requests.post("http://123.60.15.219:6003/getRes", data=data)
    return   code.text





#执行CMD命令
def cmdExec(command):
    try:
        # 使用subprocess.run来执行命令
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,universal_newlines=True)
        # 输出命令的执行结果
        print(result.stdout,result.stderr)
        return result.stdout, result.stderr
    except:
        pass
    return "",""
    


#设置环境变量
cmdExec('set "DEVECO_SDK_HOME"="D:/hm/DevEco Studio/sdk"')

#0.用codeql对鸿蒙源码进行静态分析


testNum = 0;


globallog = ""
def read_output(process, timeout=10):
    global globallog
    """
    读取子进程的输出，并在超时后停止
    """
    globallog = "";
    last_data_time = time.time()
    startTime = last_data_time
    output_activity = threading.Event()  # 用于标记是否有新数据

    def reader():
        global globallog
        nonlocal last_data_time
        while True:
            line = process.stdout.readline()
            if not line:
                break  # 子进程输出结束IPCObjectProxy
            #print(line, end='')
            if(("C02B70" not in line)  and ("C01560" not in line) and ("C05A02" not in line) and ("C01DA1" not in line)  and ("C01E00" not in line) and ("SendRequest" not in line) and ("C01F0B" not in line) and ("C01F0B" not in line)  and ("C02503" not in line)  and ("C01E00" not in line) and ("C02518" not in line) and ("C02C02" not in line) and ("C02510" not in line) and ("PafLog_CPP" not in line) and ("AiDataService" not in line) and ("DistEngine" not in line) and ("AppGallery" not in line) and ("IPCObjectProxy" not in line) and ("com.ohos.sceneboard" not in line) and ("HWBR-" not in line) and ("JsonUtil" not in line))  :
                #print(line)
                globallog = globallog + line;
            last_data_time = time.time()  # 更新最后接收到数据的时间
            output_activity.set()  # 标记有新数据

    # 启动读取线程
    thread = threading.Thread(target=reader)
    thread.daemon = True  # 设置为守护线程，主程序退出时自动终止
    thread.start()

    try:
        while True:
            # 等待是否有新数据
            output_activity.wait(timeout=1)  # 最多等待 1 秒

            
            # 检查是否超时
            #if time.time() - last_data_time > timeout:
            #    print("5秒内没有新数据，退出监听")
                #cmdExec(r'hdc shell aa force-stop com.example.myapplication')
            #    break
            #if time.time() - startTime > 60:
            #    print("接受日志的时间超过60s，退出")
            #    break
            
            #output_activity.clear()  # 重置事件，等待下一次数据

    except KeyboardInterrupt:
        print("\n监听被手动终止")
    #finally:
        # 确保子进程被正确关闭
        #process.stdout.close()
    #    process.terminate()
    #    process.wait()
    print("结束")

def gpt4Test(prompt):
    while True:
        try:
           
            client = OpenAI(
                api_key = "ce6ab1d0-6e20-4405-9f2c-456d7a781cb7",
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
#1.根据静态分析结果、适应度、执行日志 -> 生成驱动代码

#提取 TypeScript 代码
def extract_typescript_code(text):
    # 使用正则表达式匹配 ``` 包裹的内容，忽略代码语言标识
    pattern = r"```(?:\w+\n)?(.*?)```"
    code_blocks = re.findall(pattern, text, re.DOTALL)
    return code_blocks

def writeCodeFile(res):
    file = open(r"C:\Users\36132\DevEcoStudioProjects\MyApplication22\entry\src\main\ets\pages\Index.ets", "w",encoding = 'utf-8')
    file.write(res)
    file.close()

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
def complie():
  os.chdir(r"C:\\Users\\36132\\DevEcoStudioProjects\\MyApplication22")
  a,b = cmdExec(r'"D:\hm\DevEco Studio\tools\node\node.exe" "D:\hm\DevEco Studio\tools\hvigor\bin\hvigorw.js" --mode module -p module=entry@default -p product=default -p requiredDeviceType=phone assembleHap --analyze=normal --parallel --incremental --daemon')
  return  a + b

compile_num = 10

def driver_gen(pathid,data_template,cursor):
    global compile_num
    res = gpt4Test(data_template)
    try:
        res = extract_typescript_code(res)[0]
    except:
        print("新生成的驱动提取异常")
        return None
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
   
   
    globallog = ""
    if s_flag == "success":
        return code_new;
    else:
        return None;



    #data = (path,str(c_num),s_flag,res1,driver_prompt,code_new)
    #cursor.execute('''
    #        INSERT INTO driver_info_ds (driver_name, driver_compile_num,driver_is_success,driver_compile_output,driver_document_info,driver_code)
    #        VALUES (?, ?,?, ?,?, ?)
    #        ''', data)
    
    # 提交事务
    #conn.commit()




def  driverGen1(pathid,data_template,cursor):
    global testNum,globallog
    #log = "fail, The replaced value cannot exceed 100"
    testNum = testNum + 1
    print("----------------------运行辅助APP-------------------------")
    cmdExec(r'hdc shell aa force-stop com.example.myapplication11111111')  #停止运行当前的APP
    cmdExec(r'hdc shell aa start -a EntryAbility -b com.example.myapplication11111111') #运行APP

    code = driver_gen(pathid,data_template,cursor)

    print("----------------------停止运行辅助app-------------------------")
    cmdExec(r'hdc shell aa force-stop com.example.myapplication11111111')  #停止运行当前的APP


    

    if code == None:
        print("--------------------驱动生成异常------------------------------")
        return None;

    #code = get_response(data_template)
    #code =  data_template
    print("----------------------大模型生成的代码-------------------------")
    print(code)
    #将驱动代码写入鸿蒙项目的指定文件
    file = open(r"C:\Users\36132\DevEcoStudioProjects\MyApplication22\entry\src\main\ets\pages\Index.ets", "w",encoding = 'utf-8')
    file.write(code)
    file.close()

    #2.驱动代码语法校验（编译） 可以加一个修复智能体
    print("----------------------编译APP-------------------------")
    os.chdir(r"C:\\Users\\36132\\DevEcoStudioProjects\\MyApplication22")
    cmdExec(r'"D:\hm\DevEco Studio\tools\node\node.exe" "D:\hm\DevEco Studio\tools\hvigor\bin\hvigorw.js" clean --mode module -p product=default assembleHap --analyze=normal --parallel --incremental --daemon')

    #3.将编译生成的APP包上传虚拟机/真机
    print("----------------------停止运行当前的APP-------------------------")
    cmdExec(r'hdc shell aa force-stop com.example.myapplication')  #停止运行当前的APP
    print("----------------------删除虚拟机上原先的安装包-------------------------")
    cmdExec(r'hdc shell rm -rf data/local/tmp/0844c61b800a480d875feef6da6484f8')
    print("----------------------在虚拟机上新建一个文件夹，用于上传安装包-------------------------")
    cmdExec(r'hdc shell mkdir data/local/tmp/0844c61b800a480d875feef6da6484f8')  #新建一个目录用于放置编译好的APP
    print("----------------------将本地编译好的安装包上传虚拟机-------------------------")
    cmdExec(r'hdc file send C:\Users\36132\DevEcoStudioProjects\MyApplication22\entry\build\default\outputs\default\entry-default-signed.hap "data/local/tmp/0844c61b800a480d875feef6da6484f8"') #将编译好的包上传
    print("----------------------安装安装包-------------------------")
    cmdExec(r'hdc shell bm install -p data/local/tmp/0844c61b800a480d875feef6da6484f8') #安装APP
    cmdExec(r'hdc shell rm -rf data/local/tmp/0844c61b800a480d875feef6da6484f8') #删除安装包目录
    print("----------------------运行APP-------------------------")
    cmdExec(r'hdc shell aa start -a EntryAbility -b com.example.myapplication') #运行APP

    print("----------------------休眠一段时间收集日志-------------------------")
    time.sleep(20)

    


    print("------------------------------------收集到的日志-----------------------------")
    print(globallog)
    is_error = "NO"
    if(globallog != ""):
        print("--------------------------有异常---------------------")
        is_error = "YES"
    

    print("----------------------开始截图-------------------------")
    cmdExec(r'hdc shell snapshot_display -f /data/local/tmp/0.jpeg')

    print("----------------------保存截图到本地-------------------------")
    filename = generate_random_string(10) +  r'.jpeg'
    cmdExec(''' hdc file recv /data/local/tmp/0.jpeg    D:\jietu\{}'''.format(filename))


    data = ("1",pathid,code,"NO",globallog,is_error,filename)
    cursor.execute('''
            INSERT INTO fuzz_record (type,path,driver_code,mutation_info,fuzz_log,is_error,remark) VALUES (?, ?,?, ?,?, ?, ?)
            ''', data)
    # 提交事务
    conn.commit()
    globallog = ""
    return code




def dynamic_format(template, data):
    import re
    # 正则表达式用于匹配 {...}
    pattern = re.compile(r"\{(\w+)\}")
    
    def replacer(match):
        key = match.group(1)
        return str(data.get(key, match.group(0)))  # 如果 key 不在 data 中则返回原样输出
    
    return pattern.sub(replacer, template)




data_template = r'''
      **task requirements**: You are an expert in fuzz testing driver variation, able to generate new driver code based on the known driver code [driver_code] (HarmonyOS's arkts syntax) and the seed list of APIs included in the driver [seed_ist], with the following requirements.
    [Instruction]
    1.Do not change the code structure, otherwise the program may not compile properly. Simply mutate the code in onPageShow() and the sub methods it calls in the driver code based on contextual information.
    2.Keep the first line of code in onPageShow() as this. keepScreenOn (true); Do not make any modifications to him, as he can keep the screen constantly on, making it easier for the driver to continue executing.
    3. Based on the API description in the document and the seed list [seed_ist] (seed_ist is JSON data, key represents the name of the API, and value represents the possible parameters of the API), mutate the driver [driver_comode]
    4. It is possible to adjust the order of API calls in the original driver code [driver_comde] and the values of APIs in the mutated [seed_stist] appropriately, and generate drivers that are as diverse as possible.
    5.The generated drivers should not be duplicated with the current driver list[current_driver_list]. The generation of drivers should be as diverse as possible to test potential vulnerabilities in the system.
    6. Your output only includes the code itself and does not contain any other content.
    [document]
    {document}

    [driver_code]
    ```code
    {code}
    ```
    [seed_list]
    {seed_list}

    [current_driver_list]
    {current_driver_list}
    [output]


'''



def logjianting():
    process = subprocess.Popen(['hdc', 'shell', "hilog  -L  E "], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, universal_newlines=True)
    read_output(process)


t = threading.Thread(target=logjianting)
t.start()

import re

#提取两个字符串中间的内容
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
cursor = conn.cursor()


#封装驱动变异提示词
cursor.execute('''select * FROM seed_info_ds;''') 
rows = cursor.fetchall()
seed_gen_prompts = []

ecoh_driver_num = 3;  #每一组驱动变异次数
ecoh_driver_list = []

num = 0;
startIndex = 35

for row in rows:
    ecoh_driver_list = []
    if num < startIndex:
        print(num)
        num = num + 1
        continue

    pathid = row[1]
    cursor.execute("select * FROM driver_info_ds where driver_name = " + "'{}'".format(pathid)) 
    #print("select * FROM driver_info_ds where driver_name = " + "'{}'".format(pathid))
    rows1= cursor.fetchall()
    rows2 = rows1[0]
    document_data = rows2[5]
    

    code = rows2[6]   #驱动信息
    document_data = extract_between(document_data,"[document]","[Instruction]").strip("[document]")  #原始文档信息
    seeds = row[2]    #种子信息

    ecoh_driver_list.append(code)
    recordPeekMemory();
    
    for enum in range(ecoh_driver_num):
        result = '##驱动:\n'
        for item in ecoh_driver_list:
            result += str(item) + '##驱动:\n'
        result = result.rstrip('##驱动:\n')
        p = {'document' : document_data,"code" : code, "seed_list" : seeds,"current_driver_list" :  result}
        res = dynamic_format(data_template,p)
        print("-----------------------------驱动生成提示词:")  
        print(res)
        #exit()
        #seed_gen_prompts.append((res,row[1]))
        tempcode = driverGen1(pathid,res,cursor)
        #print(res)
        #exit()
        ecoh_driver_list.append(tempcode)


    num = num + 1;
    #print(res)
    #exit()


# 关闭连接
cursor.close()
conn.close()




