import sqlite3
conn = sqlite3.connect('auth.db')

# 创建一个Cursor:
cursor = conn.cursor()
#cursor.execute('''''') 

#select count(1) FROM driver_info_ds  where driver_is_success = 'success';
#DELETE FROM driver_info_ds;
# 执行SQL语句，创建user表:
#DELETE FROM driver_info;
#cursor.execute('''CREATE TABLE IF NOT EXISTS driver_info 
#(
#    id INTEGER PRIMARY KEY AUTOINCREMENT,
#    driver_name VARCHAR(256),
#    driver_compile_num VARCHAR(8),
#    driver_is_success VARCHAR(128),
#    driver_compile_output text,
#    driver_document_info text,
#    driver_code text
#)
#''')

#cursor.execute('''CREATE TABLE IF NOT EXISTS seed_info_ds 
#(
#    id INTEGER PRIMARY KEY AUTOINCREMENT,
#    path VARCHAR(256),
#    seeds text
#)
#''')




#cursor.execute('''CREATE TABLE IF NOT EXISTS   fuzz_record 
#(
#    id INTEGER PRIMARY KEY AUTOINCREMENT,
#    type VARCHAR(128),
#    path VARCHAR(512),
#    driver_code text,
#    seed_code text,
#    mutation_info text,
#    fuzz_log text,
#    usage_info text,
#    is_error VARCHAR(128),
#    is_bug  VARCHAR(128),
#    remark text
#)
#''')




# cursor.execute('''CREATE TABLE IF NOT EXISTS   fuzz_record 
# (
#    id INTEGER PRIMARY KEY AUTOINCREMENT,
#    type VARCHAR(128),
#    path VARCHAR(512),
#    driver_code text,
#    seed_code text,
#    mutation_info text,
#    fuzz_log text,
#    usage_info text,
#    is_error VARCHAR(128),
#    is_bug  VARCHAR(128),
#    remark text
# )
# ''')


# cursor.execute('''CREATE TABLE IF NOT EXISTS   log_cwe_analysis 
# (
#    id INTEGER PRIMARY KEY AUTOINCREMENT,
#    type VARCHAR(128),
#    path VARCHAR(512),
#    driver_code text,
#    fuzz_log text,
#    driver_code_select text,
#    cwe_id text,
#    cwe_describe text,
#    log_select text
# )
# ''')


# cursor.execute('''CREATE TABLE IF NOT EXISTS   cwe_analysis_bug 
# (
#    id INTEGER PRIMARY KEY AUTOINCREMENT,
#    pid INTEGER,
#    driver_code text,
#    fuzz_log text,
#    driver_code_select text,
#    cwe_id text,
#    cwe_describe text,
#    log_select text,
#    bug_type text,
#    bug_des text,
#    analysis text
# )
# ''')

# cursor.execute('''CREATE TABLE IF NOT EXISTS   hm_current_cve_bug_list 
# (
#    id INTEGER PRIMARY KEY AUTOINCREMENT,
#    product text,
#    vendor text,
#    status text,
#    version text,
#    dateReserved text,
#    datePublished text,
#    dateUpdated text,
#    descriptions text
# )
# ''')


# cursor.execute('''CREATE TABLE IF NOT EXISTS   final_analysis_result 
# (
#    id INTEGER PRIMARY KEY AUTOINCREMENT,
#    type text,
#    analysis text
# )
# ''')


# cursor.execute('''CREATE TABLE IF NOT EXISTS   final_analysis_result_check 
# (
#    id INTEGER PRIMARY KEY AUTOINCREMENT,
#    type text,
#    analysis text,
#    is_effective text,
#    pid INTEGER
# )
# ''')

cursor.execute('''CREATE TABLE IF NOT EXISTS   android_example 
(
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   module_name text,
   file_name text,
   file_content text
)
''')




#rows = cursor.fetchall()
#print(rows)
# 提交事务
conn.commit()
# 关闭连接
cursor.close()
conn.close()
