from cmd import PROMPT
import gymnasium as gym
from gymnasium import spaces
import numpy as np
import torch
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.results_plotter import load_results, ts2xy
from stable_baselines3.common.callbacks import BaseCallback
import math


'''
目标：利用强化学习生成能够编译通过的多样化测试驱动

1.动作的定义
1）提前构建一批提示词模板
2）android测试用例的收集
3）鸿蒙测试用例的提取   

'''

PROMPTS = [
    '''
   Context: As an experienced fuzz testing driver code designer, your task is to generate a unique fuzz testing driver code by analyzing the provided example code and API documentation to enhance software testing.
Role: Fuzz Testing Driver Code Designer
Intent: Design a unique fuzz testing driver code that is functional and adheres to constraints.
Skill: Proficient in fuzz testing, code design, API documentation interpretation, and generating diverse driver codes.
Purpose: Introduce variations in API calls and parameters to create a unique and functional driver code.
Examples:
{Examples}
documentation:
{documentation}
    '''
    ,
    '''
    Context: As an experienced fuzz testing driver code designer, your task is to generate a unique fuzz testing driver code by analyzing the provided example code and API documentation to enhance software testing.
Role: Fuzz Testing Driver Code Designer
Intent: Design a unique fuzz testing driver code that is functional and adheres to constraints.
Skill: Proficient in fuzz testing, code design, API documentation interpretation, and generating diverse driver codes.
Purpose: Introduce variations in API calls and parameters to create a unique and functional driver code.
Examples:
{Examples}
documentation:
{documentation}
    '''
     ,
    '''
   Context: As a fuzz testing driver code designer, your goal is to generate a unique fuzz testing driver code by analyzing the provided example code and API documentation to enhance the effectiveness of software testing.
Objective: Design a unique fuzz testing driver code that is functional and adheres to constraints.
Skill: Proficient in fuzz testing, code design, API documentation interpretation, and generating diverse driver codes.
Task: Analyze the example code and API documentation, identify potential variations in API calls and parameters, and design a unique and functional driver code by introducing diversity.
Examples:
{Examples}
documentation:
{documentation}
    '''
     ,
    '''
  Context: In software testing, fuzz testing is a crucial method. Your task is to design a unique fuzz testing driver code using the provided example code and API documentation to improve the efficiency and effectiveness of software testing.
Objective: Design a unique fuzz testing driver code that is functional and adheres to constraints based on the provided example code and API documentation.
Skill: Proficient in fuzz testing, code design, API documentation interpretation, and generating diverse driver codes.
Task: Analyze the example code and API documentation, identify potential variations in API calls and parameters, and design a unique and functional driver code by introducing diversity.
Examples:
{Examples}
documentation:
{documentation}
    '''
     ,
    '''
   Task: As a fuzz testing driver code designer, your task is to design a unique fuzz testing driver code by analyzing the provided example code and API documentation.
Audience: Software testers and developers
Style: Professional, accurate, and technical
Tone: Confident and authoritative
Examples:
{Examples}
documentation:
{documentation}
    '''
    ,
     
    '''
  Task: Design a unique fuzz testing driver code using the provided example code and API documentation to enhance the effectiveness of software testing.
Audience: Software testers and developers
Style: Professional, accurate, and technical
Tone: Confident and authoritative
Examples:
{Examples}
documentation:
{documentation}
    '''
     ,
    '''
   Action: Design a unique fuzz testing driver code
Location: In a software testing environment
Intent: Generate a unique fuzz testing driver code by analyzing the provided example code and API documentation to enhance the effectiveness of software testing
Need: Proficiency in fuzz testing, code design, API documentation interpretation, and generating diverse driver codes
Goal: Design a unique and functional driver code that adheres to constraints
Examples:
{Examples}
documentation:
{documentation}
    '''
     ,
    '''
 Action: Design a unique fuzz testing driver code based on the example code and API documentation
Location: In a software testing environment
Intent: Introduce variations in API calls and parameters to create a unique and functional driver code
Need: Proficiency in fuzz testing, code design, API documentation interpretation, and generating diverse driver codes
Goal: Design a unique and functional driver code that adheres to constraints
Examples:
{Examples}
documentation:
{documentation}
    '''
     ,
    '''
Role: Fuzz Testing Driver Code Designer
Task: Design a unique fuzz testing driver code by analyzing the provided example code and API documentation
Goal: Design a unique fuzz testing driver code that is functional and adheres to constraints
Output: The generated driver code
Examples:
{Examples}
documentation:
{documentation}
    '''
     ,
    '''
   Role: Fuzz Testing Driver Code Design Expert
Task: Design a unique fuzz testing driver code using the provided example code and API documentation
Goal: Design a unique fuzz testing driver code that is functional and adheres to constraints based on the provided example code and API documentation
Output: The generated driver code
Examples:
{Examples}
documentation:
{documentation}
    '''
]

#奖励函数权重
W = [0.2, 0.5, 0.5, 0.4, 0.7, 0.3, 0.2]

#最大时间模糊测试时间
T_max = 0;

# 自定义网格环境
class GridWorldEnv(gym.Env):
    def __init__(self):
        super(GridWorldEnv, self).__init__()
        self.size = 10
        self.state = [0] # 初始位置
        #self.goal = [3, 3]  # 目标位置
       
        self.action_space = spaces.Discrete(10)  # 10个提示词
        self.observation_space = spaces.Box(low=0, high=self.size - 1, shape=(1,), dtype=np.int32)

    def reset(self, *, seed=None, options=None):
        super().reset(seed=seed)
        self.state = [0]
        return np.array(self.state), {}

    def step(self, action):
        p = PROMPTS[action]
        datas = myLlmDriverGen(p)   #大语言模型根据提示词进行驱动生成，返回是否生成成功
        
        if(datas[6] > T_max):
            T_max = datas[6]

        reward = W[0]*datas[0] -  W[1]*math.log(1 + datas[1])  -  W[2]*math.log(1 + datas[2])  -  W[3]*math.log(1 + datas[3])  -  W[4]*math.log(1 + datas[4])  -  W[5]*math.log(1 + datas[5])  - W[6]  *  datas[6]/T_max 

        return np.array(self.state), reward, done, False, {}

    def render(self, mode='console'):
        pass

# 回调函数用于实时保存TensorBoard日志
class TensorboardCallback(BaseCallback):
    def __init__(self, verbose=0):
        super(TensorboardCallback, self).__init__(verbose)

    def _on_step(self) -> bool:
        # 在每一步记录奖励
        self.logger.record("reward", self.locals["rewards"][0])
        return True

# 创建环境
env = GridWorldEnv()
env = Monitor(env)  # 用于记录日志
vec_env = make_vec_env(lambda: env, n_envs=1)

# 检查是否有可用的 GPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# 创建模型并指定设备
model = PPO("MlpPolicy", vec_env, verbose=1, tensorboard_log="./gridworld_tensorboard/", device=device)

# 训练模型
time_steps = 100000
model.learn(total_timesteps=time_steps, callback=TensorboardCallback())

# 保存模型
model.save("gridworld_model")

# 测试模型
obs, info = env.reset()
for i in range(100):
    action, _states = model.predict(obs)
    obs, rewards, dones, truncated, info = env.step(action)
    env.render()
    if dones:
        break

# 启动TensorBoard
# 在终端运行以下命令：
# tensorboard --logdir=./gridworld_tensorboard/