import sqlite3
import re,json,time
from openai import OpenAI
conn = sqlite3.connect('auth.db')
cursor = conn.cursor()


def gpt4Test(prompt):
    num1 = 0;
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



data_template = r'''
    **task requirements**: You are a HarmonyOS arkui (arkts syntax) vulnerability analysis expert, able to describe vulnerabilities based on contextual information (including source code [driver_code], fuzz test log [fuzz_log], cweid [cwe_id], cwe description [cwe_des], possible vulnerability code [select_comde], and the basis for determining possible vulnerability code logs [select_log]). Your analysis criteria are not limited to [select_code] and [select_log], but can also come from other content of contextual information. The returned content is JSON, which is described as follows:
    ```json
        [                                   //You can analyze multiple vulnerabilities
            {
                "bug_type" : "",         //You analyze the types of vulnerabilities
                "bug_des" : "",         //Description of this vulnerability
                "analysis" : ""        //Basis for vulnerability analysis
            },
            {
                "bug_type" : "",         //You analyze the types of vulnerabilities
                "bug_des" : "",         //Description of this vulnerability
                "analysis" : ""        //Basis for vulnerability analysis
            }
        ]
    ```
    You need to carefully check if the output format complies with JSON syntax. If not, please modify it yourself before outputting.
    [driver_code]
    ```code
    {driver_code}
    ```
    [fuzz_log]
    {fuzz_log}

    [select_code]
    ```code
    {select_code}
    ```
    [cwe_id]
    {cwe_id}

    [cwe_des]
    {cwe_des}

    [select_log]
    {select_log}

     [screenshot]
    {screenshot}
    [output]



'''

#读取模糊测试日志
cursor.execute('''select * FROM log_cwe_analysis;''') 
rows = cursor.fetchall()

num = 0;
endnum = 153;
for row in rows:
    #print(row)
    if(num < endnum):
        num = num + 1;
        continue



    print("当前第 {} 条".format(num))
    driver_code = row[3];
    fuzz_log = row[4];
    select_code = row[5];
    cwe_id = row[6];
    cwe_des = row[7];
    select_log =  row[8];


    p = {'driver_code' : driver_code,"fuzz_log" : fuzz_log,"select_code" : select_code,"cwe_id" : cwe_id,"cwe_des" : cwe_des,"select_log" : select_log}
    res = dynamic_format(data_template,p)


    #print(res)
    #exit();

    #开始分析
    response =  gpt4Test(res)
    if(response == None):
        num = num + 1;
        continue
    response = extract_typescript_code(response)



    if(len(response) > 0):
        response = json.loads(response[0]);
        #print(response)
        for r in response:
            print(r)
            data = (row[0],driver_code,fuzz_log,select_code,cwe_id,cwe_des,select_log,r["bug_type"],r["bug_des"],r["analysis"])
            cursor.execute('''
            INSERT INTO cwe_analysis_bug (pid,driver_code,fuzz_log,driver_code_select,cwe_id,cwe_describe,log_select,bug_type,bug_des,analysis) VALUES (?, ?,?, ?,?, ?, ?,?, ?,?)
            ''', data)
            conn.commit()
    #exit();
    num = num + 1;


# 关闭连接
cursor.close()
conn.close()

