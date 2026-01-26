import requests

import requests
import json,time

cookie = "_ga=GA1.1.1356203443.1737082635; gptSessionId=7b6d708c-687e-4f82-ac30-c090bf391ed9; _ga_C8Z1RNL7H7=GS1.1.1737347914.13.0.1737347914.0.0.0"

def getMessageID(prompt):
    global cookie
    url = 'https://www.chatgp4.com/api/gpt/chat/sendMessage'
    headers = {
        'accept': 'application/json',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-type': 'application/json',
        'cookie': cookie,
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
    global cookie
    url = 'https://www.chatgp4.com/api/gpt/chat/prompt'
    headers = {
        'accept': 'application/json',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-type': 'application/json',
        'cookie': cookie,
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

 
data_template = r'''
    The following is a description of the NFC cardSimulation API for HarmonyOS ArkTS standard
    #Import module
    ```typescript 
        import cardEmulation from '@ohos.nfc.cardEmulation';
    ```
    #cardEmulation.isSupported
    ```typescript 
    isSupported(feature: number): boolean  //Does it support some type of card emulation
    ```
    
    ##System capability：
    ###SystemCapability.Communication.NFC

    ##return value： 
    | type | describe |
    |----|----|
    | boolean | true: Support simulation of this type of card, false: This type of card simulation is not supported. | 

    
    #HceService
    Manage HCE card simulation. Before calling the HceService interface, it is necessary to first pass the new cardSimulation HceService () creates an instance.

    ```typescript 
    startHCE(aidList: string[]): boolean //Start using HCE capability.
    ```

    ##parameter：
    | Parameter Name | type | Required | describe | 
    |----|----|
    | aidList | string[] | yes | List of Aid registrations for card simulation |

    
    #stopHCE
    ```typescript 
    stopHCE(): boolean //Stop using HCE capability.
    ```
    ##Permission required：ohos.permission.NFC_CARD_EMULATION
    ##System capability： SystemCapability.Communication.NFC
    
    #on
    ```typescript 
    on(type: "hceCmd", callback: AsyncCallback<number[]>): void; //After startHCE, subscribe to messages from the peer device.
    ```
    ##Permission required：ohos.permission.NFC_CARD_EMULATION
    ##System capability： SystemCapability.Communication.NFC

    ##parameter：
    | Parameter Name | type | Required | describe | 
    |----|----|
    | type | string | yes | Fixed input of 'hceCmd' string |
    | callback | AsyncCallback<number[]> | yes | Fixed input of 'hceCmd' string|

    #sendResponse
    ```typescript 
    sendResponse(responseApdu: number[]): void; //Send data to the peer device.
    ```
    ##Permission required：ohos.permission.NFC_CARD_EMULATION
    ##System capability： SystemCapability.Communication.NFC

    ##parameter：
    | Parameter Name | type | Required | describe | 
    |----|----|
    | responseApdu | number[] | yes | The data to be sent to the other end is a data array that complies with the APDU protocol |

    ##Example:
     ```typescript 
        var hceService = new cardEmulation.HceService();
        hceService.startHCE([
            "F0010203040506", "A0000000041010"
        ])
        hceService.stopHCE();
        hceService.on("hceCmd", (err, res) => {
            if(err.data === 0) {
                console.log('callback => Operation hceCmd succeeded. Data: ' + JSON.stringify(res));
                hceService.sendResponse([0x00,0xa4,0x04,0x00,
                0x0e,0x32,0x50,0x41,0x59,0x2e,0x53,0x59,0x53,0x2e,0x44,0x44,
                0x46,0x30,0x31,0x00]);
            } else {
                console.log('callback => Operation hceCmd failed. Cause: ' + err.data);
            }
        })
        
    ```
    # Instruction
    Connect the device with AID 123456 for data transmission and reception.The requirements are as follows.
    1.**Model output requirements**： The output only contains typescript code and does not include any other descriptions
    2.**API call order**:Send data after successful subscription,Call Stop HCE at the end of the code
    
    

'''.replace("#log#",log)  

data = {'data': data_template}
print(data)
r = requests.post("http://123.60.15.219:6003/getRes", data=data)
 
print(r.text)