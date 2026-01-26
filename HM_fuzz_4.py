# -*- coding: utf-8 -*-
import os
import subprocess
from openai import OpenAI

import os,time
import json
import requests,threading
import paho.mqtt.publish as publish
import selectors






def get_response(userPrompt):
    print("----------------------提示词-------------------------")
    print(userPrompt)
    data = {'data': userPrompt}
    #print(data)
    code = requests.post("http://123.60.15.219:6003/getRes", data=data)
    return   code.text



#执行CMD命令
def cmdExec(command):
    # 使用subprocess.run来执行命令
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    # 输出命令的执行结果
    print(result.stdout,result.stderr)
    return result.stdout, result.stderr


#设置环境变量
cmdExec('set "DEVECO_SDK_HOME"="D:/hm/DevEco Studio/sdk"')

#0.用codeql对鸿蒙源码进行静态分析


testNum = 0;


globallog = ""
def read_output(process, timeout=5):
    global globallog
    """
    读取子进程的输出，并在超时后停止
    """
    globallog = "";
    last_data_time = time.time()
    output_activity = threading.Event()  # 用于标记是否有新数据

    def reader():
        global globallog
        nonlocal last_data_time
        while True:
            line = process.stdout.readline()
            if not line:
                break  # 子进程输出结束
            print(line, end='')
            globallog = globallog + line;
            last_data_time = time.time()  # 更新最后接收到数据的时间
            output_activity.set()  # 标记有新数据

    # 启动读取线程
    thread = threading.Thread(target=reader)
    thread.daemon = True  # 设置为守护线程，主程序退出时自动终止
    thread.start()

    try:
        while True:
            # 等待是否有新数据
            output_activity.wait(timeout=1)  # 最多等待 1 秒

            # 检查是否超时
            if time.time() - last_data_time > timeout:
                print("5秒内没有新数据，退出监听")
                #cmdExec(r'hdc shell aa force-stop com.example.myapplication')
                break

            output_activity.clear()  # 重置事件，等待下一次数据

    except KeyboardInterrupt:
        print("\n监听被手动终止")
    finally:
        # 确保子进程被正确关闭
        process.stdout.close()
        process.terminate()
        process.wait()
    print("结束")


#1.根据静态分析结果、适应度、执行日志 -> 生成驱动代码
def  driverGen(log):
    global testNum,globallog
    #log = "fail, The replaced value cannot exceed 100"
    testNum = testNum + 1
    #1.驱动合成
    print("----------------------利用大模型分析日志生成驱动和初始种子-------------------------")
    data_template = r'''
        [describe]
        Replace<SPAN>in the code([code]) according to [require]，The value range of the replaced<SPAN>is 0-1000,Your output only contains source code,Excluding any other description
        
        [code]
        import contact from '@ohos.contact';
        import geoLocationManager from '@ohos.geoLocationManager';
        import { BusinessError } from '@kit.BasicServicesKit';
        import { MqttAsync, MqttConnectOptions, MqttMessage, MqttResponse, MqttSubscribeOptions } from '@ohos/mqtt';
        import { MqttClient } from '@ohos/mqtt';
        import socket from '@ohos.net.socket';
        import { hilog } from '@kit.PerformanceAnalysisKit';
        @Entry
        @Component
        struct Index {
        @State message: string = "";
        @State status:number = <SPAN>;
        @State status1:string = "hello world";

        onPageShow(): void {
            this.netConnect();

            if(this.status > 100) {
                hilog.error(0x0000, 'testTag1', 'fail, The replaced value cannot exceed 100')
                this.status1 = 'fail, The replaced value cannot exceed 100'
            }
            else{
                hilog.info(0x0000, 'testTag1', 'success，Please replace a random number based on the range')
                this.status1 = 'success，Please replace a random number based on the range'
            }

        }

        onPageHide(): void {
        }

        netConnect(){

            let mqttAsyncClient = MqttAsync.createMqtt({
            url: "123.60.15.219:9698",
            clientId: "e5fatos4jh3l79lndb0bs",
            persistenceType: 1,
            })

            let options: MqttConnectOptions = {
            //set userName and password
            userName: "",
            password: "",
            connectTimeout: 30,
            };
            mqttAsyncClient.connect(options, (err: Error, data: MqttResponse) => {
            // to do Something
            console.log(JSON.stringify(err),JSON.stringify(data))
            });


            let subscribeOption: MqttSubscribeOptions = {
            topic: "domotopic",
            qos: 2
            }
            mqttAsyncClient.subscribe(subscribeOption, (err: Error, data: MqttResponse) => {
            // to do Something
            console.log(JSON.stringify(err),JSON.stringify(data))
            });

            mqttAsyncClient.messageArrived((err: Error, data: MqttMessage) => {
            // to do Something
            console.log(JSON.stringify(err),JSON.stringify(data))
                this.message = data.payload
            });

        }

        
        build() {
            Column({space:10}) {
                Text("当前替换值: " + this.status + "\n"  + "APP日志：" + this.status1).fontSize(25)
                Text("当前测试种子: " +  this.message).fontSize(25)
            }.justifyContent(FlexAlign.Center)
            .height('100%')
            .width('100%')
        }
        }

        [require]
        1.#log#
        3.You can only replace<SPAN>in the code（[code]）, do not modify other parts of the code（[code]）
    '''.replace("#log#",str(testNum))  
    

    data_template = '''
        
      import common from '@ohos.app.ability.common';
        import window from '@ohos.window';

        @Entry
        @Component
        struct KeepScreenOn {
        @State message: string = '常亮状态##1##2123123123 贾飞:11111 ' 
        @State isScreenOn: boolean = false
        private context: common.BaseContext = getContext(this) as common.BaseContext

        async keepScreenOn(status:boolean) {
            let windowClass = await window.getLastWindow(this.context) //获取窗口实例
            await windowClass.setWindowKeepScreenOn(status) //设置窗口常亮或取消
            this.isScreenOn = await windowClass.getWindowProperties().isKeepScreenOn//查看屏幕常亮状态
        }

        onPageShow(): void {

            this.keepScreenOn(true)
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


    '''.replace("##1##",str(testNum))


    #code = get_response(data_template)
    code =  data_template
    print("----------------------大模型生成的代码-------------------------")
    print(code)
    #将驱动代码写入鸿蒙项目的指定文件
    file = open(r"C:\Users\36132\DevEcoStudioProjects\MyApplication19\entry\src\main\ets\pages\Index.ets", "w",encoding = 'utf-8')
    file.write(code)
    file.close()

    #2.驱动代码语法校验（编译） 可以加一个修复智能体
    print("----------------------编译APP-------------------------")
    os.chdir(r"C:\\Users\\36132\\DevEcoStudioProjects\\MyApplication19")
    cmdExec(r'"D:\hm\DevEco Studio\tools\node\node.exe" "D:\hm\DevEco Studio\tools\hvigor\bin\hvigorw.js" --mode module -p module=entry@default -p product=default -p requiredDeviceType=phone assembleHap --analyze=normal --parallel --incremental --daemon')

    #3.将编译生成的APP包上传虚拟机/真机
    print("----------------------停止运行当前的APP-------------------------")
    cmdExec(r'hdc shell aa force-stop com.example.myapplication')  #停止运行当前的APP
    print("----------------------删除虚拟机上原先的安装包-------------------------")
    cmdExec(r'hdc shell rm -rf data/local/tmp/0844c61b800a480d875feef6da6484f8')
    print("----------------------在虚拟机上新建一个文件夹，用于上传安装包-------------------------")
    cmdExec(r'hdc shell mkdir data/local/tmp/0844c61b800a480d875feef6da6484f8')  #新建一个目录用于放置编译好的APP
    print("----------------------将本地编译好的安装包上传虚拟机-------------------------")
    cmdExec(r'hdc file send C:\Users\36132\DevEcoStudioProjects\MyApplication19\entry\build\default\outputs\default\entry-default-signed.hap "data/local/tmp/0844c61b800a480d875feef6da6484f8"') #将编译好的包上传
    print("----------------------安装安装包-------------------------")
    cmdExec(r'hdc shell bm install -p data/local/tmp/0844c61b800a480d875feef6da6484f8') #安装APP
    cmdExec(r'hdc shell rm -rf data/local/tmp/0844c61b800a480d875feef6da6484f8') #删除安装包目录
    print("----------------------运行APP-------------------------")
    cmdExec(r'hdc shell aa start -a EntryAbility -b com.example.myapplication') #运行APP

    print("----------------------发送种子数据-------------------------")
    #def func():
    #    for i in range(10):
            #publish.single("domotopic", payload="seed" + str(i), hostname="123.60.15.219",port=9698)
    #        time.sleep(0.5)
    #    cmdExec(r'hdc shell aa force-stop com.example.myapplication')
        #print("----------------------产生崩溃-------------------------")

    #t = threading.Thread(target=func)
    #t.start()


    #5.收集日志  -》 日志精简（利用大模型）
    print("----------------------开启子进程收集日志-------------------------")
    res = cmdExec('''for /f "tokens=1" %a in ('hdc shell ps ^| findstr myapplication') do @echo %a''')
    c = "hdc shell hilog -P " + res[0].strip()
    # 启动子进程，执行命令，收集模拟器日志
    process = subprocess.Popen(['hdc', 'shell', 'hilog','-P',res[0].strip()], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,encoding='utf-8')
    log = "fail, The replaced value cannot exceed 100"

    read_output(process)
    print("------------------------------------结果")
    print(globallog)

    
    return log

    #6.计算适应度函数

    #7.执行步骤1




log = "success，Please replace a random number based on the range"
while True:
    print("----------------------当前日志 :{}-------------------------".format(log))
    log = driverGen(log)
    