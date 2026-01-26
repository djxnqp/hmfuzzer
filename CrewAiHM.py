import os
from crewai import Agent, Task, Crew, Process,LLM
from langchain.tools import DuckDuckGoSearchRun
search_tool = DuckDuckGoSearchRun()

llm = LLM(
    model="openai/deepseek-chat",
    api_key="sk-5d46850eed3c411b8d61d6caa1dd2fee",
    base_url="https://api.deepseek.com"
)

# 驱动编写智能体
coder = Agent(  
  role='模糊测试驱动编写工程师',  
  goal='根据上下文编写对应的驱动代码',  
  backstory=
  """
    你是一个模糊测试驱动编写工程师，能够根据上下文信息编写对应的Arkts鸿蒙应用代码。
  """,  
  verbose=True,  
  allow_delegation=False,  
  llm = llm  
)

# 驱动代码修复智能体
repairer = Agent(  
  role='模糊测试驱动代码语法修复者',  
  goal='根据上下文信息修复驱动代码的语法错误',  
  backstory=
  """
    你是一个模糊测试驱动语法错误修复工程师，能够根据上下文错误等信息修复对应驱动代码的语法错误。
  """,  
  verbose=True,  
  allow_delegation=False,  
  llm = llm  
)



# 日志分析智能体
loger = Agent(  
  role='日志分析工程师',  
  goal='能够分析模糊测试驱动的执行结果',  
  backstory=
  """
    你是一个模糊测试驱动执行日志的分析工程师，能够分析模糊测试过程中产生的日志。
  """,  
  verbose=True,  
  allow_delegation=False,  
  llm = llm  
)


# 为您的代理创建任务
task1 = Task(  
  description="""根据你已有的知识编写一份贪吃蛇的需求文档""", 
  expected_output='一份贪吃蛇的需求文档',
  agent=jiagoushi
)


# 实例化您的团队并采用顺序处理
crew = Crew( agents=[jiagoushi, coder,shenji],  tasks=[task1, task2,task3,task4],  verbose=True, # 您可以将其设置为1或2以获得不同的日志记录级别
)

# 开始工作！
result = crew.kickoff()


