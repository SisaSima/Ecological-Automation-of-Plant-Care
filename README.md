# Ecological-Automation-of-Plant-Care
We are currently facing many environmental challenges, such as global warming and water scarcity, which pose great challenges for effective sustainable plant cultivation. Traditional methods of irrigation and care often lead to insufficient watering or, conversely, to overflowing the plants, which not only wastes water, but can also cause soil rot, which can later appear on the products.

 
 In the future, an innovative solution to these problems may be ecological automation of plant care, which combines automated irrigation based on machine learning and recycling of excess water.

 
 The main goal of the work is to create an automated system that monitors and controls soil irrigation, while responding to environmental factors such as air humidity and ambient temperature. An important part of the project is also efficient water management through its recycling. Excess water is captured, filtered and reused, which significantly contributes to reducing consumption and promotes sustainability.

 
 This work describes in detail the individual steps of the development of this device from the design to the implementation of sensors and machine learning algorithms.


# Hardware
Circut diagram and PCB were made in KiCAD.

Used electroparts:
- Raspberry pi Pico W - https://techfun.sk/produkt/raspberry-pi-pico-w/
- SHT30 - https://techfun.sk/produkt/senzor-teploty-a-vlhkosti-vzduchu-sht30/
- Capacitive Soil Humidity sensor - https://techfun.sk/produkt/kapacitny-senzor-vlhkosti-pody/
- OLED 1.3" display 128x64 - https://techfun.sk/produkt/oled-1-3-display-128x64/
- Water Level sensor (homemade)
- Small Water Pump - https://techfun.sk/produkt/mala-vodna-pumpa/
- Battery
- Charging Module - https://techfun.sk/produkt/nabijaci-modul-pre-litiove-baterie-tp4056-ochranny-obvod-rozne-typy/


![image](https://github.com/user-attachments/assets/eedb83a2-ca62-448c-ba7a-b21b84b948e6)

![image](https://github.com/user-attachments/assets/a57c8f23-9203-4a7f-9593-deeb4754fe72)


# Code
#### To run the code on the Raspberry pi Pico W, you need to install circuitpython on it. Detailed instructions for its installation can be found [here](https://learn.adafruit.com/welcome-to-circuitpython/installing-circuitpython).

#### Then you just transfer the files from the code folder to the device. In order for the programs to run, it is necessary to move the "lib" folder, in which all used libraries are stored, to the device.

#### To immediately, automatically start the program after starting, it is necessary to name the required file "code.py" (this step is already done). The program is still under development, so there are two versions of the code.py code in the folder.


# 3d Model
#### I shared a 'box_model.3mf' file, ready to be printed on 3d printer. The model should look like this:

##### Insert a model image

#### There is a place left for the battery and charging module. I powered it from micro USB-B (connected directly to Raspberry pi Pico W).
#### WARNING! UPPER HOLE FOR USB CABLE is too small. The hole needs to be enlarged after printing (I used a drill).

# notes
- https://github.com/khristinakokolus/smart_flowerpot inspiration
- https://github.com/pop-os/shell
