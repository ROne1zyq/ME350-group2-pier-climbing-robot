# ME350-group2-pier-climbing-robot

# Bridge-Pier Climbing Robot

## Project Overview
This project implements an autonomous climbing robot capable of ascending and descending along a vertical bridge pier.  
The robot is controlled by a **Raspberry Pi 4**, equipped with an **ultrasonic distance sensor** for height measurement, and powered by a **12V DC battery pack**.  
It uses four **370 DC geared motors** driven by an **L298N motor driver** to provide sufficient torque for vertical climbing.

The control program enables the robot to climb to a predefined height, maintain its position for a fixed duration, and then descend back to the starting point.

---

## Hardware Components
- **Raspberry Pi 4** – Main controller, communicates with sensors and motor driver  
- **370 DC Geared Motors ×4** – Provide climbing torque (two motors per vehicle)  
- **L298N Motor Driver** – Controls motor direction and speed  
- **HC-SR04 Ultrasonic Sensor** – Measures climbing height in real time  
- **12V 2800mAh Battery Pack** – Powers motors and driver  
- **Computer (SSH connection)** – For remote programming, monitoring, and control  

---

## Features
- **Autonomous Climbing** – Controlled ascent and descent based on distance measurement  
- **Top Hold Function** – Maintains position for 60 seconds at target height  
- **Remote Control via SSH** – Allows code deployment, debugging, and monitoring without a local display  
- **Speed Adjustment** – Switches between high and low climbing speed near the target height for precise stopping  

---

## How It Works
1. **Initialization** – Motors and sensors are set up, and target height is defined.  
2. **Climbing Up** – Robot ascends at high speed until it approaches the target height, then slows down.  
3. **Holding at Top** – Motors stop, and the robot holds position for 60 seconds.  
4. **Climbing Down** – Robot descends until reaching a safe ground clearance.  
5. **Stop & Shutdown** – Motors stop and GPIO resources are released.  

---