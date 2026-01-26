import os
from crewai import Agent, Task, Crew, Process,LLM
from langchain.tools import DuckDuckGoSearchRun
search_tool = DuckDuckGoSearchRun()

llm = LLM(
    model="openai/deepseek-chat",
    api_key="sk-5d46850eed3c411b8d61d6caa1dd2fee",
    base_url="https://api.deepseek.com"
)

# 定义具有角色和目标的代理
jiagoushi = Agent(  
  role='架构师',  
  goal='编写一份贪吃蛇的需求文档',  
  backstory="""你在一个游戏公司的架构师。
  你擅长编写游戏开发的需求文档。
  擅长Python语言
  """,  
  verbose=True,  
  allow_delegation=False,  
 # tools=[search_tool],
  llm = llm  
)
coder = Agent(  
    role='软件开发人员',  
    goal='根据架构师提出的需求文档编写python代码',  
    backstory="""你是一名python游戏开发者，能够使用pygame开发游戏""",  
    verbose=True,  
    allow_delegation=False,  
    llm = llm  
)

shenji = Agent(  
    role='代码审计人员',  
    goal='审计软件开发人员编写的代码',  
    backstory="""你是一名python代码的审计人员，能够发现代码漏洞和代码不规范的地方""",  
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
task2 = Task(  
  description="""根据架构师提出的需求文档编写python代码""", 
  expected_output='python代码',
  agent=coder
)

task3 = Task(  
  description="""审计软件开发人员编写的代码""", 
  expected_output='详细的修改意见',
  agent=shenji
)

task4 = Task(  
  description="""根据审计人员修改意见修改代码""", 
  expected_output='python代码',
  agent=coder
)


# 实例化您的团队并采用顺序处理
crew = Crew( agents=[jiagoushi, coder,shenji],  tasks=[task1, task2,task3,task4],  verbose=True, # 您可以将其设置为1或2以获得不同的日志记录级别
)

# 开始工作！
result = crew.kickoff()


