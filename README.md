# fog-computing-TUBerlin
Fog Computing Course project


**1. In order to get this working:**

- Make sure to have Python 3 and pip3 installed.
```
pip3 install pyzmq
pip3 install paho-mqtt
```
**2. Start the sensors:**

- You can choose between LOW, MED and HIGH intensity for simulation.  It represents the number of cars passing the sensor in each lane.
```
python3 SensorLane1.py <DESIRED INTENSITY>
python3 SensorLane2.py <DESIRED INTENSITY>
```
- The sensors use MQTT to publish the data to a broker, which in our case is located in the cloud. For ease in testing, each sensor is taken as a different topic.

**3. Start the Edge Device**
```
python3 EdgeDevice.py
```
- This edge device is subscribed to both sensor's topics on the MQTT broker. It recieves the data as soon as it connects to the broker.
- One of the functions grabs the data and calculates a basic average of the cars that passed in a certain period of time. 

*Ensuring reliability at Edge node*
- At the same we are connected to an AWS server using a basic ZeroMQ REQ/RES mode. A thread is used to run this on top of the MQTT subscriptions. Every 10 seconds it calculates the average of cars that were passed in that time and sends it to the AWS server, and awaits for a response until it can send more. This ensures reliability.

**4. Cloud Server**

- AWS server keeps collecting the data received from edge nodes then returns a message back suggesting which route to prioritize. This prioritization is based on simple logic 'if traffic is higher on a route then prioritize it'.

*Ensuring Reliability at Cloud node*
If the AWS server goes down, it keeps collecting sensor data and then returns a message to edge node suggesting which route to prioritize, once it comes back online.

*For Testing Putposes*
<br />
Your local machine coulc mimic cloud instance. You can run this file locally for tests.
```
python3 CloudServer.py
```

*For actual implementation on Cloud (AWS)*
<br />
4.1. Inside EdgeDevice.py file on your local machine, make sure to update the IP pointing to public IP of your AWS EC2 instance.
```
AWS_INSTANCE = "tcp://<YOUR PUBLIC IP ADDRESS>:5555"
```
4.2. Your AWS security group should allow access to this incoming TCP traffic.
```
5555	TCP	0.0.0.0/0	launch-wizard-1-SecurityGroup
```
4.3. Now run the script inside your EC2 instance.
```
python3 CloudServer.py
```
