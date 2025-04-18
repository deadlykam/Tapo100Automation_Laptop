<p align="center"><a href="https://youtu.be/eq8Kj1s_X8E" target="_blank"><img src="https://imgur.com/VabSScN.png"></a></p>

# Tapo100Automation_Laptop

### Introduction:
An application that will automatically turn on/off the Tapo100 plug based on the Laptop battery percentage for Windows 11 machines.

## Table of Contents:

## Prerequisites
#### Python
Python version of 3.10.6 and later should work. Previous version of Python may work but have not been tested.
#### Tapo Device
The Tapo deviced used for testing is the [Tapo100 Plug](https://www.tapo.com/uk/product/smart-plug/tapo-p100/). Also the Tapo100 Plug Firmware version of 1.2.5 Build 240411 should work. Later and previous version have not been tested.
#### Operating System
For now it works in windows 11. Other OS have not been tested in.
## Stable Build
[Stable-v1.0.0](https://github.com/deadlykam/Tapo100Automation_Laptop/tree/Stable-v1.0.0) is the latest stable build of the project. If development is going to be done on this project then it is adviced to branc off of any _Stable_ branches because they will **NOT** be changed or updated except for README.md. Any other brances are subjected to change including the main branch.
## Installation
1. First download the latest [TAL-v1.0.0.zip](https://github.com/deadlykam/Tapo100Automation_Laptop/releases/tag/v1.0.0) from the latest Stable build.
2. Once downloaded extract/unzip the file.
## Tutorial
Once [Installation](#installation) is done then just start the application **TapoAutomationLaptop.exe**. When the application starts it will look like the image below.

| ![Application Started](https://imgur.com/9kAHRXc.png) |
|:--:|
| *Fig 1: TapoAutomationLaptop.exe Started* |

Let me explain what each part of the application does from the image below.

| ![Application Started](https://imgur.com/uyyOep8.png) |
|:--:|
| *Fig 2: TapoAutomationLaptop.exe* |

- a. **Battery Charge Value:** This is the current battery charge value of the laptop. It will keep updating once per second to reflect the laptop's battery charge value.
- b. **Battery Charge Status:** This icon shows the current status of the battery which is if the battery is being charged or NOT. If the icon is a battery with a lightning bolt in it then it means the battery is being charged. If the icon is a battery with no lightning bolt in it then it means the battery is NOT being charged.
- c. **Tapo Connection Status:** This icon will only appear once the Tapo device has been connected.
- d. **Min:** The minimum threshold value. Once the battery charge value reaches the minimum threshold value then **TapoAutomationLaptop** will turn on the Tapo device and the laptop will start charging. The minimum value can be any value from 0 to 100. Also once a new value is given and the setting has been saved then the updated value will be shown on the label as well, in this case it is 20% in the label **Min (%) -> 20%**.
- e **Max:** The maximum threshold value. Once the battery charge value reaches the maximum threshold value then **TapoAutomationLaptop** will turn off the Tapo device and the laptop will stop charging. The maximum value can be any value from 0 to 100. Also once a new value is given and the setting has been saved then the updated value will be shown on the label as well, in this case it is 80% in the label **Max (%) -> 80%**.
- f. **IP:** The local IP address of the Tapo device. It is needed to find the Tapo device in the local network. When the local IP address has been given it will be shown on the label as well after saving.
- g. **Email:** The email address of your Tapo account. It is needed to login and access the Tapo device. When the email address is given it will be shown on the label as well after saving.
- h. **Password:** The password of your Tapo account. It is needed to login and access the Tapo device.
- i. **Save:** This button will save the current setting of the **TapoAutomationLaptop**. That way you do NOT need to re-enter all the details again when you re-open the application again.
- j. **Connect:** This button will connect to the Tapo device. It is first recommended to give the correct login details of the Tapo before connecting to the Tapo device otherwise the application will NOT work.
- k. **Toggle Tapo:** This button toggles the Tapo device. This means if the Tapo device is on then clicking this button will turn it off and vice versa.
- l. **Auto Connect:** If enabled, this flag will auto connect to the Tapo device when the TapoAutomationLaptop starts.
- m. **Dark Theme:** If enabled, this will show the dark theme of the application. Disabling it again will show the light theme of the application, which is the one shown in the images.

After starting **TapoAutomationLaptop** then you need to fill up all the details, especially f, g and h in _Fig 2_. You can also change the min and max value, d and e, and once you are satisfied then click the **Save** button, i in _Fig 2_. This will save all the setting values and the new settings will also be shown in their respected labels, except for the password. Finally click the **Connect** button, j in _Fig 2_. Once you are connected the **Connect** button, j in _Fig 2_, will disappear and the **Tapo Connection Status** icon will be shown, c in _Fig 2_. Now the **TapoAutomationLaptop** application will automatically charge and discharge the laptop's battery using the min and max value you provided. If you want to update the min and max values then you can do so and then press the **Save** button again.
## Updates
1. Connecting to a Tapo device.
2. Turn on/off Tapo device automatically when thresholds have been reached.
3. Auto connect when starting the application.
4. Dark and Light theme.
5. Toggling the Tapo device on and off.
## Versioning
The project uses [Semantic Versioning](https://semver.org/). Available versions can be seen in [tags on this repository](https://github.com/deadlykam/Tapo100Automation_Laptop/tags).
***
## Authors
- Syed Shaiyan Kamran Waliullah 
  - [Kamran Wali Github](https://github.com/deadlykam)
  - [Kamran Wali Twitter](https://twitter.com/KamranWaliDev)
  - [Kamran Wali Youtube](https://www.youtube.com/channel/UCkm-BgvswLViigPWrMo8pjg)
  - [Kamran Wali Website](https://deadlykam.github.io/)
***
## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE) file for details.
***
