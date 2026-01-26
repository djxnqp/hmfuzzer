#递归读取某个文件下所有的json内容
import os
import json
import sqlite3,json,re,time
from openai import OpenAI
conn = sqlite3.connect('auth.db')

# 创建一个Cursor:
cursor = conn.cursor()




#读取当前的漏洞列表
cursor.execute('''

WITH RankedData AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY pid, type
            ORDER BY id DESC  -- 假设id是唯一标识每一行的字段，且越大的id表示越“后”的行
        ) AS rn
    FROM final_analysis_result
)
SELECT
   type,analysis,pid
FROM RankedData
WHERE rn = 1;

''') 
row_current_bugs = cursor.fetchall()


for  row_current in row_current_bugs:
    #print(row_current)
    data = (row_current[0],row_current[1],"1",row_current[2])
    cursor.execute('''
            INSERT INTO final_analysis_result_check (type,analysis,is_effective,pid) VALUES (?, ?,?,?)
            ''', data)
    conn.commit()
    

# 关闭连接
cursor.close()
conn.close()
