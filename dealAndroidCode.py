import sqlite3,os
conn = sqlite3.connect('auth.db')
# 创建一个Cursor:
cursor = conn.cursor()


#获取所有的java文件
def get_java_files(directory):
    md_files = []
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            if file_path.endswith('.java'):
                md_files.append(file_path)
                #print(file_path)
        else:
            md_files.extend(get_java_files(file_path))
    return md_files



#dirs = [r"D:\androidlizi\coursera-android\Examples",r"D:\androidlizi\Android"]
dirs = [r"D:\androidlizi\Android"]
for d in dirs:
    mulu = get_java_files(d);
    for m in mulu:
        #print(m)
        file_splits = m.split("\\")
        module_name = file_splits[3]
        file_name = file_splits[-1]
        #code = 
        with open(m, 'r',encoding='utf-8',errors='ignore') as file:
            # 读取文件内容
            content = file.read()
        data = (module_name,file_name,content)
        cursor.execute('''
            INSERT INTO android_example (module_name,file_name,file_content) VALUES (?, ?, ?)
            ''', data)
        conn.commit()
            

    exit()

# 关闭连接
cursor.close()
conn.close()
