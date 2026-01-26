#递归读取某个文件下所有的json内容
import os
import json
import sqlite3,json,re,time
from openai import OpenAI
conn = sqlite3.connect('auth.db')

# 创建一个Cursor:
cursor = conn.cursor()
#cursor.execute('''''') 

def gpt4Test(prompt):
    num1 = 0;
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
            num1 = num1 + 1
            if(num1 > 5):
                return None;
            print("获取msg异常")
            time.sleep(0.1)
            continue

def dynamic_format(template, data):
   
    # 正则表达式用于匹配 {...}
    pattern = re.compile(r"\{(\w+)\}")
    
    def replacer(match):
        key = match.group(1)
        return str(data.get(key, match.group(0)))  # 如果 key 不在 data 中则返回原样输出
    
    return pattern.sub(replacer, template)


#提取 TypeScript 代码
def extract_typescript_code(text):
    # 使用正则表达式匹配 ``` 包裹的内容，忽略代码语言标识
    pattern = r"```(?:\w+\n)?(.*?)```"
    code_blocks = re.findall(pattern, text, re.DOTALL)
    return code_blocks





#读取当前的漏洞列表
cursor.execute('''select * FROM hm_current_cve_bug_list;''') 
row_current_bugs = cursor.fetchall()
#print(row_current_bugs)

#读取当前工程分析的漏洞数据
cursor.execute('''select * FROM cwe_analysis_bug;''') 
row_current_project_bugs = cursor.fetchall()
#print(row_current_project_bugs)


# 获取列名
columns = [description[0] for description in cursor.description]
# 将结果转换为字典列表
row_current_project_bugs = [dict(zip(columns, row)) for row in row_current_project_bugs]
 

data_template = r'''
    **task requirements**: You are a vulnerability assessment expert who can determine whether it is a 0-day vulnerability, a 1-day vulnerability, or a nday vulnerability based on the known HarmonyOS vulnerability CVE list (current_hm_cve_bugs) and the analysis results of the current tool. The analysis results of the current tool include the original driver code (driver_code), the possible vulnerability code in the driver (driver_code_delect), the possible vulnerability type (cwe_id), the possible vulnerability type description (cwe_describe), the possible vulnerability basis log (log_delect), the possible vulnerability description (bug_des), and the basis for tool analysis of this possible vulnerability (analysis),Your output result is JSON data, in the following format：
    ```json
        {
            "type" : "",    //0-day,1-day, nday  
            "analysis" : "",   //Your analysis basis
        }
    ```
    [driver_code]
     ```code
    {driver_code}
    ```


    [driver_code_select]
    ```code
    {driver_code_select}
    ```

    [cwe_id]
    {cwe_id}

    [cwe_describe]
    {cwe_describe}

    [log_select]
    {log_select}

    [bug_des]
    {bug_des}


    [analysis]
    {analysis}

    [current_hm_cve_bugs]
     ```json
    {current_hm_cve_bugs}
    ```


    [output]


'''

#开始逐条分析漏洞数据
num = 0
endnum = 57;
for row_current_project_bug in row_current_project_bugs:
    flag = True;
     #print(row)
    if(num < endnum):
        num = num + 1;
        continue
    print("当前分析到第" + str(num) + "条日志")
    #print(row_current_project_bug)
    #exit()
    #You are a vulnerability assessment expert who can determine whether it is a 0-day vulnerability, a 1-day vulnerability, or a nday vulnerability based on the known HarmonyOS vulnerability CVE list (current_hm_cve_bugs) and the analysis results of the current tool. The analysis results of the current tool include the original driver code (driver_code), the possible vulnerability code in the driver (driver_code_delect), the possible vulnerability type (cwe_id), the possible vulnerability type description (cwe_describe), the possible vulnerability basis log (log_delect), the possible vulnerability description (bug_des), and the basis for tool analysis of this possible vulnerability (analysis),Your output result is JSON data, in the following format：
    driver_code = row_current_project_bug["driver_code"] 
    driver_code_select = row_current_project_bug["driver_code_select"] 
    cwe_id = row_current_project_bug["cwe_id"]
    cwe_describe = row_current_project_bug["cwe_describe"] 
    log_select = row_current_project_bug["log_select"] 
    bug_type = row_current_project_bug["bug_type"] 
    bug_des = row_current_project_bug["bug_des"] 
    analysis = row_current_project_bug["analysis"]
    pid =  row_current_project_bug["id"]
    
    
    for i in  range(11):
        current_bugs_fragments = row_current_bugs[i * 6 : (i + 1) * 6]
        current_bugs_fragments_jsondata = [json.loads(row[-2]) for row in current_bugs_fragments]
        json_package = json.dumps(current_bugs_fragments_jsondata, indent=4, ensure_ascii=False);

        p = {'driver_code' : driver_code,"driver_code_select" : driver_code_select,"cwe_id" : cwe_id,"cwe_describe" : cwe_describe,"log_select" : log_select,"bug_des" : bug_des,"analysis" : analysis,'current_hm_cve_bugs' : json_package}
        res = dynamic_format(data_template,p)
        #print(res)

        #开始分析
        response =  gpt4Test(res)
        if(response == None):
            #num = num + 1;
            #continue
            flag = False;
            break;
        response = extract_typescript_code(response)

        if(len(response) > 0):
            response = json.loads(response[0]);
            print(response)
            data = (response["type"],response["analysis"],pid)
            cursor.execute('''
            INSERT INTO final_analysis_result (type,analysis,pid) VALUES (?, ?,?)
            ''', data)
            conn.commit()
    if(flag == False):
        print("网络错误：当前分析到第" + str(num) + "条日志")
        break
           
    num = num + 1;



# num = 0;
# endnum = 889;
# for row in rows:
#     #print(row)
#     if(num < endnum):
#         num = num + 1;
#         continue



#     print("当前第 {} 条".format(num))
#     type1 = row[1];
#     path = row[2];
#     driver_code = row[3];
#     fuzz_log = row[6];

#     p = {'code' : driver_code,"logcat" : fuzz_log}
#     res = dynamic_format(data_template,p)

#     #print(res)
    

#     #开始分析
#     response =  gpt4Test(res)
#     if(response == None):
#         num = num + 1;
#         continue
#     response = extract_typescript_code(response)

#     if(len(response) > 0):
#         response = json.loads(response[0]);
#         print(response)
#         for r in response:
#             data = (type1,path,driver_code,fuzz_log,r["driver_code"],r["cwe_id"],r["cwe_describe"],r["log"])
#             cursor.execute('''
#             INSERT INTO log_cwe_analysis (type,path,driver_code,fuzz_log,driver_code_select,cwe_id,cwe_describe,log_select) VALUES (?, ?,?, ?,?, ?, ?,?)
#             ''', data)
#             conn.commit()
#     num = num + 1;


# 关闭连接
cursor.close()
conn.close()

