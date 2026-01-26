# import requests,os
# import base64,time

 
# def image_to_base64(filepath):
#     with open(filepath, "rb") as image_file:
#         byte_content = image_file.read()
#         base64_content = base64.b64encode(byte_content)
#         return base64_content.decode('utf-8')
# # Flask 服务的 URL
# url = 'http://123.60.15.219:7001/upload'


# while True:
#     # 要发送的文件路径
#     try:
#         file_path = r'D:\\桌面整理\\20250108\\鸿蒙\\doc\\docs\\en\\application-dev\\graphics\\figures\\overdraw-demo-enable.png'

#         data = {'type': "image", 'text': "Describe this picture","image" : image_to_base64(file_path)}
#             #data = {'type': 'video', 'text': 'Describe this video.'}
#             # 发送 POST 请求
#         response = requests.post(url, data=data,timeout=60)
#     except:
#         print("网络异常")
#         pass
#     # 打印响应内容
#     print(response.text)


# def gif2mp4(gifPath,mp4filepath):
#     #ffmpeg -f gif -i input.gif  -crf 0 output.mp4
#     command = f"ffmpeg -y -f gif -i {gifPath}  -crf 0 {mp4filepath}"  
#     exit_code = os.system(command)



# gif2mp4(r'D:\桌面整理\20250108\test1\input.gif',r'D:\桌面整理\20250108\test1\output1.mp4')


# def appendContent(file_path,images,imagesdes):
#     sum = ""
#     append_title = "#The following is a description of the image (format: png/jpg/jpeg/gif) that appeared in the previous text: \n"
#     sum = sum + append_title
    
#     for i in range(len(images)):
#         image_name  =  "##Image Name: {}\n".format(images[i])
#         image_des   =  "###Image description: {}\n".format(imagesdes[i])
#         sum = sum + image_name + image_des
    
#     #file_path = "example.txt"
#     with open(file_path, 'a',encoding='utf-8') as file:
#         file.write(sum)

# images = ["1.png","2.png"]
# imagesdes = ["i am 1.png","2.png"]

# appendContent("example.txt",images,imagesdes)


#GPT4接口封装


import requests
import json,time

def getMessageID(prompt):
    url = 'https://www.chatgp4.com/api/gpt/chat/sendMessage'
    headers = {
        'accept': 'application/json',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-type': 'application/json',
        'cookie': '_ga=GA1.1.1356203443.1737082635; gptSessionId=7b6d708c-687e-4f82-ac30-c090bf391ed9; _ga_C8Z1RNL7H7=GS1.1.1737347914.13.0.1737347914.0.0.0',
        'origin': 'https://www.chatgp4.com',
        'referer': 'https://www.chatgp4.com/gpt/',
        'sec-ch-ua': '";Not A Brand";v="99", "Chromium";v="94"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 SE 2.X MetaSr 1.0'
    }
    data = {"chatId":95306,"type":"gpt4","prompt":prompt,"image":[]}
    response = requests.post(url,headers=headers,json=data,timeout=20)
    #print(response.text)
    dictionary = json.loads(response.text)
    return dictionary["messages"][1]["id"]



def  getMessage(ID):
    url = 'https://www.chatgp4.com/api/gpt/chat/prompt'
    headers = {
        'accept': 'application/json',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-type': 'application/json',
        'cookie': '_ga=GA1.1.1356203443.1737082635; gptSessionId=7b6d708c-687e-4f82-ac30-c090bf391ed9; _ga_C8Z1RNL7H7=GS1.1.1737347914.13.0.1737347914.0.0.0',
        'origin': 'https://www.chatgp4.com',
        'referer': 'https://www.chatgp4.com/gpt/',
        'sec-ch-ua': '";Not A Brand";v="99", "Chromium";v="94"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 SE 2.X MetaSr 1.0'
    }
    data = {"chatId":95306,"messageId":ID}
    response = requests.post(url,headers=headers,json=data,timeout=20)
    response.encoding = 'utf-8'  # 明确指定编码方式

    #print(response.text)
    return response.text

def gpt4Test(prompt):
    ID = getMessageID(prompt)
    return getMessage(ID)


questions = [
    "模糊测试是什么？",
    "模糊测试的主要目的是什么？",
    "为什么需要进行模糊测试？",
    "模糊测试和传统测试有什么区别？",
    "常见的模糊测试工具有哪些？",
    "如何选择合适的模糊测试工具？",
    "模糊测试的基本原理是什么？",
    "什么是基于变异的模糊测试？",
    "基于变异的模糊测试有哪些优缺点？",
    "什么是基于生成的模糊测试？",
    "基于生成的模糊测试与基于变异的模糊测试有何不同？",
    "如何设计有效的模糊测试用例？",
    "模糊测试在软件开发生命周期中的最佳实践是什么？",
    "模糊测试可以应用于哪些类型的软件？",
    "如何评估模糊测试的效果？",
    "模糊测试能否完全替代传统测试方法？",
    "如何将模糊测试与自动化测试相结合？",
    "模糊测试在云环境中的应用有哪些挑战？",
    "如何对模糊测试结果进行分析和处理？",
    "模糊测试如何帮助发现软件中的安全漏洞？",
    "在进行模糊测试时，如何避免产生过多的无效测试用例？",
    "如何提高模糊测试的效率和覆盖率？",
    "模糊测试在嵌入式系统中的应用有哪些特点？",
    "如何对模糊测试工具进行定制和扩展？",
    "模糊测试在大数据环境下的应用前景如何？",
    "如何利用人工智能技术提升模糊测试的效果？",
    "模糊测试在物联网设备中的应用有哪些难点？",
    "如何对模糊测试过程进行监控和管理？",
    "模糊测试能否发现所有类型的软件缺陷？",
    "如何将模糊测试融入持续集成/持续部署流程中？",
    "模糊测试在移动应用测试中的应用有哪些优势？",
    "如何对模糊测试生成的日志进行有效分析？",
    "模糊测试在Web应用安全测试中的作用是什么？",
    "如何对模糊测试工具进行性能优化？",
    "模糊测试在开源软件中的应用现状如何？",
    "如何利用模糊测试进行协议测试？",
    "模糊测试在金融软件中的应用有哪些特殊要求？",
    "如何对模糊测试结果进行复现和定位？",
    "模糊测试在医疗软件中的应用前景如何？",
    "如何利用模糊测试进行文件格式测试？",
    "模糊测试在游戏软件测试中的应用有哪些挑战？",
    "如何对模糊测试工具进行多线程优化？",
    "模糊测试在通信软件中的应用有哪些特点？",
    "如何利用模糊测试进行数据库测试？",
    "模糊测试在航空软件中的应用现状如何？",
    "如何对模糊测试结果进行分类和统计？",
    "模糊测试在汽车电子软件中的应用有哪些难点？",
    "如何利用模糊测试进行API测试？",
    "模糊测试在工业控制系统软件中的应用有哪些风险？",
    "如何对模糊测试工具进行分布式部署？",
    "模糊测试在教育软件中的应用有哪些优势？",
    "如何利用模糊测试进行图像处理软件测试？",
    "模糊测试在智能家居软件中的应用前景如何？",
    "如何对模糊测试结果进行可视化展示？",
    "模糊测试在区块链软件中的应用有哪些挑战？",
    "如何利用模糊测试进行音频处理软件测试？",
    "模糊测试在智能交通软件中的应用有哪些特点？",
    "如何对模糊测试工具进行插件化开发？",
    "模糊测试在智能穿戴设备软件中的应用现状如何？",
    "如何利用模糊测试进行视频处理软件测试？",
    "模糊测试在智能安防软件中的应用有哪些优势？",
    "如何对模糊测试结果进行关联分析？",
    "模糊测试在智能电网软件中的应用有哪些难点？",
    "如何利用模糊测试进行自然语言处理软件测试？",
    "模糊测试在智能物流软件中的应用前景如何？",
    "如何对模糊测试工具进行代码优化？",
    "模糊测试在智能农业软件中的应用现状如何？",
    "如何利用模糊测试进行机器学习软件测试？",
    "模糊测试在智能医疗设备软件中的应用有哪些风险？",
    "如何对模糊测试结果进行深度挖掘？",
    "模糊测试在智能金融软件中的应用有哪些特点？",
    "如何利用模糊测试进行智能教育软件测试？",
    "模糊测试在智能旅游软件中的应用前景如何？",
    "如何对模糊测试工具进行内存优化？",
    "模糊测试在智能环保软件中的应用现状如何？",
    "如何利用模糊测试进行智能建筑软件测试？",
    "模糊测试在智能体育软件中的应用有哪些优势？",
    "如何对模糊测试结果进行智能分析？",
    "模糊测试在智能娱乐软件中的应用有哪些难点？",
    "如何利用模糊测试进行智能办公软件测试？",
    "模糊测试在智能政务软件中的应用前景如何？",
    "如何对模糊测试工具进行安全加固？",
    "模糊测试在智能法律软件中的应用现状如何？",
    "如何利用模糊测试进行智能人力资源软件测试？",
    "模糊测试在智能社交软件中的应用有哪些风险？",
    "如何对模糊测试结果进行精准定位？",
    "模糊测试在智能媒体软件中的应用有哪些特点？",
    "如何利用模糊测试进行智能广告软件测试？",
    "模糊测试在智能电子商务软件中的应用前景如何？",
    "如何对模糊测试工具进行性能评估？",
    "模糊测试在智能供应链软件中的应用现状如何？",
    "如何利用模糊测试进行智能能源软件测试？",
    "模糊测试在智能工业软件中的应用有哪些优势？",
    "如何对模糊测试结果进行有效反馈？",
    "模糊测试在智能研发软件中的应用有哪些难点？",
    "如何利用模糊测试进行智能测试软件测试？",
    "模糊测试在智能运维软件中的应用前景如何？",
    "如何对模糊测试工具进行功能扩展？",
    "模糊测试在智能监控软件中的应用现状如何？",
    "如何利用模糊测试进行智能预警软件测试？",
    "模糊测试在智能决策软件中的应用有哪些风险？",
    "如何对模糊测试结果进行综合评估？",
    "模糊测试在智能分析软件中的应用有哪些特点？",
    "如何利用模糊测试进行智能优化软件测试？",
    "模糊测试在智能调度软件中的应用前景如何？",
    "如何对模糊测试工具进行兼容性测试？",
    "模糊测试在智能仿真软件中的应用现状如何？",
    "如何利用模糊测试进行智能设计软件测试？",
    "模糊测试在智能制造软件中的应用有哪些优势？",
    "如何对模糊测试结果进行持续跟踪？",
    "模糊测试在智能研发管理软件中的应用有哪些难点？",
    "如何利用模糊测试进行智能项目管理软件测试？",
    "模糊测试在智能知识管理软件中的应用前景如何？",
    "如何对模糊测试工具进行稳定性测试？",
    "模糊测试在智能文档管理软件中的应用现状如何？",
    "如何利用模糊测试进行智能档案管理软件测试？",
    "模糊测试在智能信息检索软件中的应用有哪些风险？",
    "如何对模糊测试结果进行质量评估？",
    "模糊测试在智能搜索引擎软件中的应用有哪些特点？",
    "如何利用模糊测试进行智能推荐系统软件测试？",
    "模糊测试在智能问答系统软件中的应用前景如何？",
    "如何对模糊测试工具进行压力测试？",
    "模糊测试在智能语音识别软件中的应用现状如何？",
    "如何利用模糊测试进行智能语言翻译软件测试？",
    "模糊测试在智能文本编辑软件中的应用有哪些优势？",
    "如何对模糊测试结果进行可靠性评估？",
    "模糊测试在智能代码编辑软件中的应用有哪些难点？",
    "如何利用模糊测试进行智能数据库管理软件测试？",
    "模糊测试在智能网络管理软件中的应用前景如何？",
    "如何对模糊测试工具进行可用性测试？",
    "模糊测试在智能安全防护软件中的应用现状如何？",
    "如何利用模糊测试进行智能防火墙软件测试？",
    "模糊测试在智能入侵检测软件中的应用有哪些风险？",
    "如何对模糊测试结果进行安全性评估？",
    "模糊测试在智能杀毒软件中的应用有哪些特点？",
    "如何利用模糊测试进行智能数据备份软件测试？",
    "模糊测试在智能数据恢复软件中的应用前景如何？",
    "如何对模糊测试工具进行用户体验测试？",
    "模糊测试在智能办公自动化软件中的应用现状如何？",
    "如何利用模糊测试进行智能电子表格软件测试？",
    "模糊测试在智能演示文稿软件中的应用有哪些优势？",
    "如何对模糊测试结果进行性能评估？",
    "模糊测试在智能绘图软件中的应用有哪些难点？",
    "如何利用模糊测试进行智能排版软件测试？",
    "模糊测试在智能印刷软件中的应用前景如何？",
    "如何对模糊测试工具进行界面测试？",
    "模糊测试在智能图形设计软件中的应用现状如何？",
    "如何利用模糊测试进行智能动画制作软件测试？",
    "模糊测试在智能视频编辑软件中的应用有哪些风险？",
    "如何对模糊测试结果进行功能评估？",
]


java_interview_questions = [
    "1. 什么是JVM，JRE和JDK？",
    "2. Java的基本数据类型有哪些？",
    "3. 什么是自动装箱和拆箱？",
    "4. Java中的String和StringBuffer有什么区别？",
    "5. 什么是Java中的异常处理机制？",
    "6. 什么是多态？请举例说明。",
    "7. 什么是接口（Interface），与抽象类的区别是什么？",
    "8. 什么是构造函数？",
    "9. 什么是匿名内部类？",
    "10. 解释Java中的继承。",
    "11. 什么是Java集合框架？",
    "12. ArrayList和LinkedList有什么区别？",
    "13. 什么是哈希表（HashMap）？",
    "14. 什么是Java中的同步？",
    "15. 什么是死锁，如何避免死锁？",
    "16. 描述Java中的线程生命周期。",
    "17. 什么是Java中的volatile关键字？",
    "18. 对象的引用和对象的内存是什么关系？",
    "19. 什么是Java中的lambda表达式？",
    "20. 什么是Stream API？",
    "21. 解释Java中的反射机制。",
    "22. 什么是Java的枚举类型？",
    "23. 请说明final、finally和finalize的区别。",
    "24. 在Java中如何实现单例模式？",
    "25. Java中的强引用、弱引用、软引用与虚引用有什么区别？",
    "26. 垃圾回收机制是如何工作的？",
    "27. 什么是Java中的性质和方法的重载？",
    "28. Java中的设计模式有哪些？",
    "29. 什么是Spring框架？",
    "30. 解释JUnit是什么？",
    "31. 什么是RESTful Web服务？",
    "32. 什么是构建工具，如Maven和Gradle？",
    "33. Java的访问修饰符有哪些？",
    "34. 请说明Runnable接口和Thread类的区别。",
    "35. 什么是Java中的注解（Annotation）？",
    "36. Java中的Callable和Runnable有什么区别？",
    "37. 什么是Java中的方法引用？",
    "38. 解释Java中的进程与线程的区别。",
    "39. 解释什么是操作符重载。",
    "40. 什么是设计模式中的MVC模式？",
    "41. 什么是Java中的Comparator和Comparable接口？",
    "42. Java是如何处理多线程的？",
    "43. 解释Java中的IoC和DI。",
    "44. 什么是HQL和SQL，它们有什么区别？",
    "45. 什么是Java中的JDBC？",
    "46. 解释Java中的事务管理。",
    "47. 解释什么是类加载器（Class Loader）。",
    "48. Java中的正则表达式如何使用？",
    "49. 如何在Java中处理日期和时间？",
    "50. 什么是Java中的定时任务？",
    "51. Java中的禁止子类化是通过什么实现的？",
    "52. ClassNotFoundException和NoClassDefFoundError有什么区别？",
    "53. 解释什么是Java中的装饰器模式。",
    "54. 为什么使用集成测试？",
    "55. 解释在Java中如何处理文件IO。",
    "56. 什么是Java中的Socket编程？",
    "57. Java中的优先队列（Priority Queue）有什么特点？",
    "58. 什么是垃圾回收器（Garbage Collector）？",
    "59. 解释什么是设计模式中的策略模式。",
    "60. Java中的Synchronized关键字怎么使用？",
    "61. SQL注入是什么，如何防止？",
    "62. Java中如何创建一个只读属性？",
    "63. Java中的动态代理是什么？",
    "64. 解释什么是DSN和ODBC。",
    "65. Java中的集合的线程安全如何实现？",
    "66. Spring中的AOP是如何工作的？",
    "67. Java中的数据结构有哪些常见的实现？",
    "68. 什么是Java中的基本异常和检查异常的区别？",
    "69. Java中的构造器链是什么？",
    "70. 解释Java中的代理模式。",
    "71. Java如何实现序列化？",
    "72. 什么是构造函数重载？",
    "73. Java中的Executor框架是什么？",
    "74. Java的核心库有哪些？",
    "75. RestTemplate在Spring中如何使用？",
    "76. 解释Java中的动态数组。",
    "77. Java中的JDBC连接如何实现？",
    "78. 什么是设计模式中的代理模式？",
    "79. Java中的懒加载是什么？",
    "80. Java的异常层次结构是怎样的？",
    "81. 什么是设计模式中的观察者模式？",
    "82. Java中的动态类型和静态类型有什么区别？",
    "83. 解释Java中的监听器模式。",
    "84. 什么是常量池（Constant Pool）？",
    "85. Java中如何使用注解进行配置？",
    "86. 解释什么是Hessian与JSON的区别？",
    "87. 什么是Java中的时间复杂度与空间复杂度？",
    "88. Java中的CopyOnWriteArrayList与ArrayList有什么区别？",
    "89. 解释Java中的方法引用。",
    "90. 什么是Java中的关键字final？",
    "91. 什么是Java中的深拷贝与浅拷贝？",
    "92. 解释Java的类加载机制。",
    "93. Java中的可变参数如何使用？",
    "94. 解释Java中的类和结构体的区别。",
    "95. 如何理解Java中的工厂模式？",
    "96. 在Java中如何处理多线程问题？",
    "97. 解释Java中的线程池有什么优势。",
    "98. 什么是Java中的自动关闭资源（try-with-resources语句）？",
    "99. Java中的DAG与树形结构有什么区别？",
    "100. 解释Java虚拟机内存结构。"
]

import requests

udatarl = 'http://10.60.81.153:25701/post_params'
data = {'param1':'''



Execute [instruction] based on [document]
[document]
# AccessibilityExtensionAbility

Accessibility Kit provides accessibility extension capabilities based on AccessibilityExtensionAbility in the ExtensionAbility framework. You can develop your accessibility extension services by applying the AccessibilityExtensionAbility template.

## Creating an Accessibility Extension Service

You can create an accessibility extension service by creating a project from scratch or adding the service to an existing project. Only one accessibility extension service can be created for a project.
This example creates an accessibility extension service that implements the following functions:
When the accessibility function is enabled, a right-then-down gesture obtains all nodes on the current screen, and a following left-then-down gesture obtains all nodes.

### Creating a Project

To create an independent accessibility extension service, create a project in the stage model of API version 9 or later in DevEco Studio.

### Creating an AccessibilityExtAbility.ets File

In the **ets** folder of a project, add the **AccessibilityExtAbility** folder and then create the **AccessibilityExtAbility.ets** file in the folder. You can implement some callbacks in the file to add service processing logic.

```ts
import { AccessibilityExtensionAbility, AccessibilityEvent } from '@kit.AccessibilityKit';
import AccessibilityManager from './AccessibilityManager';

class AccessibilityExtAbility extends AccessibilityExtensionAbility {
    onConnect() {
        console.info(`AccessibilityExtAbility onConnect`);
        // Initialize the service logic.
        AccessibilityManager.getInstance().onStart(this.context);
    }

    onDisconnect() {
        console.info(`AccessibilityExtAbility onDisconnect`);
        // Reclaim resources and exit the service logic.
        AccessibilityManager.getInstance().onStop();
    }

    onAccessibilityEvent(accessibilityEvent: AccessibilityEvent) {
        console.info(`AccessibilityExtAbility onAccessibilityEvent: ${JSON.stringify(accessibilityEvent)}`);
        // Process the service logic based on the event information.
        AccessibilityManager.getInstance().onEvent(accessibilityEvent);
    }
}

export default AccessibilityExtAbility;
```

The APIs defined in the file are as follows.

| Name| Description|
| ---- | ---- |
| onConnect(): void | Called when a connection with the extension service is set up.|
| onDisconnect(): void | Called when the connection with the extension service is severed.|
| onAccessibilityEvent(event: AccessibilityEvent): void | Called when an accessibility event occurs|

Create the **AccessibilityManager.ets** file for storing the service logic code.
```ts
import {
  AccessibilityElement,
  AccessibilityEvent,
  AccessibilityExtensionContext,
  ElementAttributeKeys
} from '@kit.AccessibilityKit';

interface Rect {
  left: number,
  top: number,
  width: number,
  height: number,
}

// Attribute information to be queried
let wantedAttribute: ElementAttributeKeys[] = ['bundleName', 'text', 'description', 'windowId'];
type attributeValues = string | number | boolean | AccessibilityElement | AccessibilityElement[] | string[] | Rect;

export default class AccessibilityManager {
  private static instance: AccessibilityManager;
  accessibleContext?: AccessibilityExtensionContext;
  currentPageElementArray: Array<AccessibilityElement> | null = null;

  static getInstance(): AccessibilityManager {
    if (!AccessibilityManager.instance) {
      AccessibilityManager.instance = new AccessibilityManager();
    }
    return AccessibilityManager.instance;
  }

  onStart(context: AccessibilityExtensionContext) {
    console.info(`AccessibilityManager onStart`);
    this.accessibleContext = context;
  }

  onStop() {
    console.info(`AccessibilityManager onStop`);
    this.accessibleContext = undefined;
  }

  onEvent(accessibilityEvent: AccessibilityEvent): void {
    console.info(`AccessibilityManager onEvent`);
    switch (accessibilityEvent.eventType) {
      case 'rightThenDown':
      // Obtain all nodes on the current screen.
        this.getCurrentPageAllElement();
        break;
      case 'leftThenDown':
      // Obtain all nodes.
        this.printAllElementInfo();
        break;
      default:
        break;
    }
  }

  async getCurrentPageAllElement(): Promise<void> {
    console.info(`AccessibilityManager getCurrentPageAllElement`);
    let rootElement: AccessibilityElement;
    if(!this.accessibleContext){
      console.error(`AccessibilityManager accessibleContext undefined`);
      return;
    }
    try {
      rootElement = await this.accessibleContext?.getWindowRootElement();
      this.currentPageElementArray = await this.getAttributeValue(rootElement, 'children') as AccessibilityElement[];
    } catch (error) {
      console.error(`AccessibilityExtAbility Failed to getWindowRootElement. Cause:${JSON.stringify(error)}`);
    }
  }

  async getElementWantedInfo(accessibilityElement: AccessibilityElement, wantedAttribute: ElementAttributeKeys[]):
    Promise<string | null> {
    console.info(`AccessibilityUtils getElementAllInfo`);
    if (accessibilityElement === null) {
      console.error(`AccessibilityUtils accessibilityElement is null`);
      return null;
    }

    let info = '';
    let value: attributeValues | null;
    for (let name of wantedAttribute) {
      value = await this.getAttributeValue(accessibilityElement, name);
      info = info.concat(name + ': ' + value + ' ');
    }
    return info;
  }

  async getAttributeValue(accessibilityElement: AccessibilityElement, key: ElementAttributeKeys):
    Promise<attributeValues | null> {
    console.info(`AccessibilityUtils getAttributeValue`);
    let value: attributeValues;
    let keys = await accessibilityElement.attributeNames();
    let isExit = false;
    for (let keyString of keys) {
      if (key == keyString) {
        isExit = true;
      }
    }
    if (isExit) {
      try {
        value = await accessibilityElement.attributeValue(key);
        return value;
      } catch (error) {
        console.error(`AccessibilityUtils Failed to get attributeValue of ${key} . Cause:  ${JSON.stringify(error)}`);
      }
    }
    return null;
  }

  async printAllElementInfo(): Promise<void> {
    console.info(`AccessibilityManager printAllElementInfo`);
    if (this.currentPageElementArray === null || this.currentPageElementArray.length === 0) {
      console.error(`AccessibilityManager currentPageElementArray is null`);
      return;
    }
    let info: string | null = null;
    for (let index = 0; index < this.currentPageElementArray.length; index++) {
      info = await this.getElementWantedInfo(this.currentPageElementArray[index], wantedAttribute);
      console.info(`AccessibilityManager element information: ${info}`);
    }
  }
}
```

## Processing an Accessibility Event

You can process the service logic for accessibility events through the **onAccessibilityEvent()** API. For details about the events, see [AccessibilityEvent](../reference/apis-accessibility-kit/js-apis-application-accessibilityExtensionAbility.md#accessibilityevent). In this example, the **rightThenDown** gesture is used.

```ts
onAccessibilityEvent(accessibilityEvent: AccessibilityEvent) {
    console.info('AccessibilityExtAbility onAccessibilityEvent: ' + JSON.stringify(accessibilityEvent));
    if (accessibilityEvent.eventType === 'rightThenDown') {
        console.info('AccessibilityExtAbility onAccessibilityEvent: rightThenDown');
        // TODO: Develop custom logic.
    }
}
```
For an accessibility event, you can use the APIs of the [AccessibilityExtensionContext](../reference/apis-accessibility-kit/js-apis-inner-application-accessibilityExtensionContext.md) module to configure the concerned information, obtain root information, and inject gestures.

You can also process physical key events in the accessibility extension service. For details, see [onKeyEvent](../reference/apis-accessibility-kit/js-apis-application-accessibilityExtensionAbility.md#accessibilityextensionabilityonkeyevent).

## Declaring the Capabilities of Accessibility Extension Service

After developing the custom logic for an accessibility extension service, you must add the configuration information of the service to the corresponding module-level **module.json5** file in the project directory.

The **srcEntry** tag indicates the path to the **extensionAbility**.
The **label** tag indicates the name of the **extensionAbility** displayed in the list of installed extension services.
The **description** tag indicates the help information about the **extensionAbility** displayed on the details page of the installed extension service.
Make sure the value of the **type** tag is fixed at **accessibility**. Otherwise, the connection to the service will fail.

```json
"extensionAbilities": [
  {
    "name": "AccessibilityExtAbility",
    "srcEntry": "./ets/AccessibilityExtAbility/AccessibilityExtAbility.ets",
    "label": "$string:MainAbility_label",
    "description": "$string:MainAbility_desc",
    "type": "accessibility",
    "metadata": [
      {
        "name": "ohos.accessibleability",
        "resource": "$profile:accessibility_config"
      }
    ]
  }
]
```
In addition, **accessibility_config** is the specific configuration of the accessibility extension service. You need to create the **accessibility_config.json** file in **resources/base/profile/** and declare the [capability type](../reference/apis-accessibility-kit/js-apis-accessibility.md#capability) of the accessibility extension service in the file. In this example, the following declaration is required:
```json
{
  "accessibilityCapabilities": [
    "retrieve",
    "gesture",
    "touchGuide"
  ]
}
```
## Enabling a Custom Accessibility Extension Service

You can enable or disable a custom accessibility extension service through the device settings.

1. From the device settings screen, access the list of installed extended services under accessibility. If an extended service is not installed, it is grayed out, and "No service" is displayed.

2. Locate the target extension service, and toggle on or off the switch to enable or disable it.

3. If you opt to enable a service, a security reminder is displayed. Wait until the countdown ends and then select the check box indicating that you are aware of and willing to assume the listed risks. After that, you can toggle off the switch to the extended service.

[Instruction]
1.**import requirements**：  Import the corresponding package based on [document]
2.**Drive requirements**:Generate a fuzzy test driver that covers all APIs of [document] as much as possible
3.**Driver calling**: We need to provide an example of driver invocation that meets the following requirements:
##1.Import the corresponding package at the//package position in the following ts code，Check not to import packages repeatedly
##2.Insert the fuzz test driver call code at thev//code position in the following ts code
```ts
    import common from '@ohos.app.ability.common';
    import window from '@ohos.window';
    //package

    @Entry
    @Component
    struct KeepScreenOn {
    @State message: string = '常亮状态 : '
    @State isScreenOn: boolean = false
    private context: common.BaseContext = getContext(this) as common.BaseContext

    async keepScreenOn(status:boolean) {
        let windowClass = await window.getLastWindow(this.context) //获取窗口实例
        await windowClass.setWindowKeepScreenOn(status) //设置窗口常亮或取消
        this.isScreenOn = await windowClass.getWindowProperties().isKeepScreenOn//查看屏幕常亮状态
    }

    onPageShow(): void {
        this.keepScreenOn(true)
        //code
    }

    build() {
        Row() {
        Column() {
            Text(this.message + this.isScreenOn)
            .fontSize(50)
            .fontWeight(FontWeight.Bold)
        }
        .width('100%')
        }
        .height('100%')
        }
    }
```
4.**code requirements**: The generated content only includes the code itself and does not contain any other content
5.**Debugging information requirements**: If the generated driver code contains debugging output information such as
Both console.info () and console.error() use hilog.error() and hilog.info(), and their function declarations are as follows
```ts
/**
* Outputs error-level logs.
*
* @param { number } domain Indicates the service domain, which is a hexadecimal integer ranging from 0x0 to 0xFFFF
* @param { string } tag Identifies the log tag, length cannot exceed 32 bytes.
* @param { string } format Indicates the log format string.
* @param { any[] }args Indicates the log parameters.
* @syscap SystemCapability. HiviewDFX.HiLog
* @crossplatform
* @atomicservice
* @since 11
*/
function error(domain: number, tag: string, format: string, ...args: any[]): void;

/**
* Outputs info-level logs.
*
* @param { number } domain Indicates the service domain, which is a hexadecimal integer ranging from 0x0 to 0xFFFF
* @param { string } tag Identifies the log tag, length cannot exceed 32 bytes.
* @param { string } format Indicates the log format string.
* @param { any[] }args Indicates the log parameters.
* @syscap SystemCapability. HiviewDFX.HiLog
* @crossplatform
* @atomicservice
* @since 11
*/
function info(domain: number, tag: string, format: string, ...args: any[]): void;

For example:
hilog.error(0x0000, 'testTag', 'Failed to load the content. Cause: % {public}s ',  JSON.stringify(err) ?? '');
hilog.info(0x0000, 'testTag', 'Succeeded in loading the content.');
```




''', 'param2': 'value2'}
#response = requests.post(udatarl, data=data)

#print(response.status_code)  # 打印状态码
#print(response.text)  # 打印响应内容

import requests
def gpt4Test(prompt):
    url = 'http://159.138.133.44:6009/predict'
    data = {'text': prompt}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=data, headers=headers)

    #print(response.status_code)  # 打印状态码
    return response.text  # 打印响应内容

print(gpt4Test("写一个冒泡排序算法，输出只包含代码"))