<p align="center"><a href="https://youtu.be/eq8Kj1s_X8E" target="_blank"><img src="https://imgur.com/VabSScN.png"></a></p>

# Tapo100Automation_Laptop

### Introduction:
An application that will automatically turn on/off the Tapo100 plug based on the Laptop battery percentage for Windows 11 machines.

## Table of Contents:

## Prerequisites
#### Python
Python version of 3.10.6 and later should work. Previous version of Python may work but have not been tested.
## Stable Build
[Stable-v1.0.0]() is the latest stable build of the project. If development is going to be done on this project then it is adviced to branc off of any _Stable_ branches because they will **NOT** be changed or updated except for README.md. Any other brances are subjected to change including the main branch.
## Installation
1. First download the latest [TAL-v1.0.0.zip]() from the latest Stable build.
2. Once downloaded extract/unzip the file.
## Tutorial
Once [Installation](#installation) is done then just start the application **TapoAutomationLaptop.exe**. When the application starts it will look like the image below.

| ![Application Started](https://imgur.com/9kAHRXc.png) |
|:--:|
| *Fig 1: TapoAutomationLaptop.exe Started* |

Let me explain what each part of the application does from the image below.

| ![Application Started](https://imgur.com/zMnjGLX.png) |
|:--:|
| *Fig 2: TapoAutomationLaptop.exe* |

- a. **Battery Charge Value:** This is the current battery charge value of the laptop. It will keep updating once per second to reflect the laptop's battery charge.
- b. **Battery Charge Status:** This icon shows the current status of the battery which is if the battery is being charged or NOT. If the icon is a battery with a lightning bolt in it then it means the battery is being charged. If the icon is a battery with no lightning bolt in it then it means the battery is NOT being charged.
- c. **Tapo Connection Status:** This icon will only appear once the Tapo device has been connected.
- d. **Min:** The minimum threshold value. Once the battery charge value reaches the minimum threshold value then TapoAutomationLaptop will turn on the Tapo device and the laptop will start charging. The minimum value can be any value from 0 to 100. Also once a new value is given and the setting has been saved then the updated value will be shown on the label as well, in this case it is 20% in the label **Min (%) -> 20%**.
- e **Max:** The maximum threshold value. Once the battery charge value reaches the maximum threshold value then TapoAutomationLaptop will turn off the Tapo device and the laptop will stop charging. The maximum value can be any value from 0 to 100. Also once a new value is given and the setting has been saved then the updated value will be shown on the label as well, in this case it is 80% in the label **Max (%) -> 80%**.
- f. **IP:**
