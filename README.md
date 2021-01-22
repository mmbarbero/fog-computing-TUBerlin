# fog-computing-TUBerlin
Fog Computing Course project


**In order to get this working:**

- Make sure to have Python 3 and pip3 installed
```
pip3 install pyzmq
pip3 install paho-mqtt
```
**Start the sensors:**
- You can choose between LOW, MED and HIGH intensity for simulation.  It represents the number of cars passing the sensor in each lane.
```
python3 SensorLane1.py <DESIRED INTENSITY>
python3 SensorLane2.py <DESIRED INTENSITY>
```
- The sensors use MQTT to and publish the data to a broker, which in our case is in the cloud for ease of use in testing. Each sensor is a different topic.

**Start the Edge Device**
```
python3 EdgeDevice.py
```
- This device is subscribed to both sensor's topics on the MQTT broker. It recieves the data as soon as it connects to the broker.
- One of the functions grabs the data and calculates a basic average of the cars that passed in a certain period of time. 
- At the same we are connected to an AWS server using a basic ZeroMQ REQ/RES mode. I used a thread to run this on top of the MQTT subscriptions. Every 10 seconds it calculates the average of cars that passed in that time and sends it to the AWS server, and awaits for a response until it can send more.
- If the AWS server goes down, it keeps collecting sensor data and then sends the average once it comes back online. (We need to work on this, make it more reliable)

**Cloud Server**
- I created an AWS ec2 instance and it basically just runs this code. You can just run this file locally for tests.
```
python3 CloudServer.py
```



