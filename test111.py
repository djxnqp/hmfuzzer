import random

def generate_numbers():
    while True:
        # 随机生成第一个和第五个数，范围在18到19之间
        num1 = random.randint(18, 19)
        num5 = random.randint(18, 19)
        
        # 随机生成第二个、第三个和第四个数，范围在0到20之间
        num2 = random.randint(0, 20)
        num3 = random.randint(0, 20)
        num4 = random.randint(0, 20)
        
        # 检查这五个数的总和是否为100
        if num1 + num2 + num3 + num4 + num5 == 92:
            return [num1, num2, num3, num4, num5]

# 生成满足条件的五个数
result = generate_numbers()
print("生成的五个数为：", result)