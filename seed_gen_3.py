import requests
 
log = "fail, The replaced value cannot exceed 100"

data_template = r'''
    Generate a batch of initial seeds for fuzz testing for each API based on the following documentation and code
    
    [document]
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
   
    
    [code]
    ```code
        import cardEmulation from '@ohos.nfc.cardEmulation';

        var hceService = new cardEmulation.HceService();

        // Start HCE with AID list
        hceService.startHCE([
            "F0010203040506", "A0000000041010"
        ])
        .then(() => {
            console.log('HCE started successfully');
            // Subscribe to HCE commands
            hceService.on("hceCmd", (err, res) => {
                if (err) {
                    console.log('callback => Operation hceCmd failed. Cause: ' + err);
                } else {
                    console.log('callback => Operation hceCmd succeeded. Data: ' + JSON.stringify(res));
                    // Send response APDU
                    // Send response APDU
                    hceService.sendResponse([0x00, 0xa4, 0x04, 0x00, 0x0e, 0x32, 0x50, 0x41, 0x59, 0x2e, 0x53, 0x59, 0x53, 0x2e, 0x44, 0x44, 0x46, 0x30, 0x31, 0x00]);
                }
            });
        })
        .catch((error) => {
            console.log('Failed to start HCE. Error: ' + error);
            console.log('Failed to start HCE. Error: ' + error);
        });

        // Stop HCE at the end
        hceService.stopHCE()
        .then(() => {
            console.log('HCE stopped successfully');
        })
        .catch((error) => {
            console.log('Failed to stop HCE. Error: ' + error);
        });

    ```

    [Instruction]
    
    Generate an initial seed list for each API in the code based on the documentation, with the output format in JSON format and the api name as the key. and the seed list as the value. For example:
     ```json
    {
        "hceService.startHCE" : [[
            "123", "456"
        ],[
            "789", "111213"
        ]]
    }
    ```
'''

data = {'data': data_template}
print(data)
r = requests.post("http://159.138.133.44:6003/getRes", data=data)
 
print(r.text)