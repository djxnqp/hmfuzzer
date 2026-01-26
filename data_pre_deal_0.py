import os
import requests
import re,time

import base64
 
def image_to_base64(filepath):
    with open(filepath, "rb") as image_file:
        byte_content = image_file.read()
        base64_content = base64.b64encode(byte_content)
        return base64_content.decode('utf-8')

#获取所有鸿蒙md文件
def get_md_files(directory):
    md_files = []
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            if file_path.endswith('.md'):
                md_files.append(file_path)
                #print(file_path)
        else:
            md_files.extend(get_md_files(file_path))
    return md_files

folder_path = r'D:\桌面整理\20250108\鸿蒙\doc\docs\en\application-dev'
paths = get_md_files(folder_path)

print("原文件夹下md文件个数:{}".format(len(paths)))


#过滤掉c++相关的文件
def filterCPPFile(paths):
    res = []
    for path in  paths:
        with open(path, 'r',encoding='utf-8',errors='ignore') as file:
            # 读取文件内容
            content = file.read()
            #print(content)
            if ("```c" in content) or   ("```c++" in content) or ("```cpp" in content):
                pass
            elif "```ts" in content:
                res.append(path)
    return res

paths = filterCPPFile(paths)
print("过滤掉C相关的md文件个数:{}".format(len(paths)))
#将过滤和处理好的数据拷贝到指定文件夹


#---------------------------------------------将数据拷贝到新的路径-----------------------------------------------
import shutil
import os
def create_directory_if_not_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"The directory {path} was successfully created.")
    else:
        print(f"The directory {path} already exists.")
 

def copy_file(source_path, destination_folder):
    """
    将文件从source_path复制到destination_folder。
    """
    shutil.copy2(source_path, destination_folder)
for path in paths:
    filePath = os.path.dirname(path)
    filePath = filePath.replace("application-dev","okmddir")
    print(filePath)
    create_directory_if_not_exists(filePath)
    copy_file(path, filePath)
exit()

#---------------------------------------------多模态数据处理(处理完成后进行上面数据的拷贝)-----------------------------------------------

#找出包含图片的md文件
def findImagesMds(paths):
    res = []
    for path in paths:
        with open(path, 'r',encoding='utf-8',errors='ignore') as file:
            # 读取文件内容
            content = file.read()
            #print(content)
            if (".png" in content) or   (".jpg" in content) or   (".gif" in content) or   (".jpeg" in content):
                res.append(path)
                
    return res


paths = findImagesMds(paths)
print("包含图片的md文件个数:{}".format(len(paths)))

#利用大语言模型将图片数据替换为文本(gif转为视频后再上传，其它以文件的形式进行上传)
#def replaceImageUsetextByVlm(paths):


def gif2mp4(gifPath,mp4filepath):
    #ffmpeg -f gif -i input.gif  -crf 0 output.mp4
    command = f"ffmpeg -y -f gif -i {gifPath}  -crf 0 {mp4filepath}"  
    exit_code = os.system(command)



#提取文件中图片的全名
def find_image_filenames(text):
    # 正则表达式匹配文件全名，包括路径，但只提取文件名部分
    pattern = r'[^\\/]+?\.(?:jpg|png|jpeg|gif)\b'
    # 在文本中查找所有匹配的文件全名
    image_filenames = re.findall(pattern, text, re.IGNORECASE)
    return image_filenames



def image2image(type1,file_path,text):
    # Flask 服务的 URL
    url = 'http://123.60.15.219:7001/upload'

    # 要发送的文件路径
    #file_path = r'D:\桌面整理\20250108\鸿蒙\doc\docs\en\application-dev\ai\mindspore\figures\01.jpg'
    #file_path = r'D:\桌面整理\20250108\test1\output.mp4'
    # 打开文件并以二进制模式读取
    while True:
        #with open(file_path, 'rb') as f:
        data = {'type': type1, 'text': text,"image" : image_to_base64(file_path)}
        # 发送 POST 请求
        try:
            response = requests.post(url, data=data,timeout=300)
            if(response.text == "error"):
                print("GPU 内存异常")
                time.sleep(10)
                continue
            break
        except Exception as e:
            print("网络异常，重新请求: " + file_path)
            print(e)
            time.sleep(0.1)
            continue


    # 打印响应内容
    print(response.text)
    return response.text

#获取文件中图片的路径(下面这些文件包含图片数据，需要用多模态大模型转换为文本数据)
res = {}
for path in paths:
    pngs = []
    with open(path, 'r',encoding='utf-8',errors='ignore') as file:
        # 读取文件内容
        content = file.read()
        medias = find_image_filenames(content)
        for media in medias:
            pngtemp = os.path.join(os.path.join(os.path.dirname(path),"figures"), media)
            if os.path.exists(pngtemp): #文件存在
                pngs.append(pngtemp)
    res[path] = pngs
    #print(res[path])

#开始使用多模态大模型进行识别
def appendContent(file_path,images,imagesdes):
    sum = ""
    append_title = "#The following is a description of the image (format: png/jpg/jpeg/gif) that appeared in the previous text: \n"
    sum = sum + append_title
    
    for i in range(len(images)):
        image_name  =  "##Image Name: {}\n".format(images[i])
        image_des   =  "###Image description: {}\n".format(imagesdes[i])
        sum = sum + image_name + image_des
    
    #file_path = "example.txt"
    with open(file_path, 'a',encoding='utf-8',errors='ignore') as file:
        file.write(sum)


startFile = "ohos-arkui-advanced-TabTitleBar"
flag = False

num = 0
for mdfile in res.keys():
    #print(mdfile)
    #print(res[mdfile])
    mdfiletemp = mdfile
    print(mdfiletemp)


    num = num + 1
    print("当前第{}文档,总共:{}".format(num,len(res.keys())))
    if not flag:
        if(startFile in mdfile):
            flag = True
            print("找到第一个文件")
        else:
            print("未找到第一个文件")
            continue
    


    images = []
    imagesdes = []
    if len(res[mdfile]) > 0:
        for png in res[mdfile]:
            filename, file_extension = os.path.splitext(png)
            fileNamesingle = os.path.basename(png)
            text = ""
            filepath = ""
            type1 =  ""
            if file_extension == ".gif":
                print((png,filename + ".mp4",fileNamesingle))
                #gif2mp4(png,filename + ".mp4");
                #text = "Describe this video."
                #type1 =  "video"
                #filepath = filename + ".mp4"
            else:
                print((png,fileNamesingle))
                text = "Describe this image."
                type1 =  "image"
                filepath = png
                #---先不考虑gif---
                des = image2image(type1,filepath,text)  #将这个描述追加到mdfile中
                images.append(fileNamesingle)
                imagesdes.append(eval(des)[0])
        if len(images) > 0:
            print("追加文件: " + mdfiletemp)
            appendContent(mdfiletemp,images,imagesdes)









    
    







