/* * * * * * * * * * * * * * * * * * * * * *
 * SELF-BALANCING ROBOT
 * =========================================
 *
 * Code by: Simon Bluett
 * Email: hello@chillibasket.com
 * Website: wired.chillibasket.com
 *
 * 7/10/15, Version 2.0
 *
 * Here are some hints when you try to use this code:
 *
 *  > Ensure pin-mapping is correct for your robot (line 54)
 *  > Ensure calibration values are correct for your sensor (line 181)
 *  > Uncomment (line 700) in order to see if your sensor is working
 *  > Play with your PID values on (line 93)
 *  > Ensure that your left & right motors aren't inverted (line 355)
 *  > Confirm whether you want the Pitch ypr[1] or Roll ypr[2] sensor readings!
 * * * * * * * * * * * * * * * * * * * * * */


/* * * * * * * * * * * * * * * * * * * * * *
 *  This Demo makes use of the I2Cdev and MPU6050 libraries, and the demonstration
 *  sketch written by (Jeff Rowberg <jeff@rowberg.net>), modified to work
 *  with the Intel Galileo Development Board:
 *  -- -- -- -- -- -- -- -- -- -- -- -- -- --
 *  I2Cdev device library code is placed under the MIT license
 *  Copyright (c) 2012 Jeff Rowberg
 *  Permission is hereby granted, free of charge, to any person obtaining a copy
 *  of this software and associated documentation files (the "Software"), to deal
 *  in the Software without restriction, including without limitation the rights
 *  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 *  copies of the Software, and to permit persons to whom the Software is
 *  furnished to do so, subject to the following conditions:
 *
 *  The above copyright notice and this permission notice shall be included in
 *  all copies or substantial portions of the Software.
 * * * * * * * * * * * * * * * * * * * * * */



// I2Cdev and MPU6050 must be installed as libraries, or else the .cpp/.h files
// for both classes must be in the include path of your project
#include <I2Cdev.h>
#include <MPU6050_6Axis_MotionApps20.h>
#include <Wire.h>

// Specific I2C addresses may be passed as a parameter here
MPU6050 mpu;              // Default: AD0 low = 0x68


// Define the pin-mapping
// -- -- -- -- -- -- -- -- -- -- -- -- -- --
#define DIR_A 12                // Direction Pin, Motor A
#define DIR_B 13                // Direction Pin, Motor B
#define PWM_A 3                 // PWM, Motor A (Left Motor)
#define PWM_B 11                // PWM, Motor B (Right Motor)
#define BRK_A 9                 // Brake, Motor A
#define BRK_B 8                 // Brake, Motor B

#define BTN_1 10                 // On/Off Button
#define BTN_2 7                 // Set Centre of Gravity Button

#define LED_1 5                 // Low-battery Warning LED
#define LED_2 4                // Current mode LED


// Max PWM parameters
#define MAX_TURN 30


// MPU Control/Status
// -- -- -- -- -- -- -- -- -- -- -- -- -- --
bool dmpReady = false;          // Set true if DMP init was successful
uint8_t devStatus;              // Return status after device operation (0 = success, !0 = error)
uint8_t mpuIntStatus;           // Holds actual interrupt status byte from MPU
uint16_t packetSize;            // Expected DMP packet size (default is 42 bytes)
uint16_t fifoCount;             // Count of all bytes currently in FIFO
uint8_t fifoBuffer[64];         // FIFO storage buffer


// Orientation/Motion
// -- -- -- -- -- -- -- -- -- -- -- -- -- --
Quaternion q;                   // [w, x, y, z]       Quaternion Container
VectorFloat gravity;            // [x, y, z]            Gravity Vector
int16_t gyro[3];                // [x, y, z]            Gyro Vector
float ypr[3];                   // [yaw, pitch, roll]   Yaw/Pitch/Roll & gravity vector
float averagepitch[50];         // Used for averaging pitch value


// For PID Controller
// -- -- -- -- -- -- -- -- -- -- -- -- -- --
float Kp = 8;                   // (P)roportional Tuning Parameter
float Ki = 2;         // (I)ntegral Tuning Parameter        
float Kd = 5;         // (D)erivative Tuning Parameter       
float lastpitch;                // Keeps track of error over time
float iTerm;                  // Used to accumulate error (integral)
float targetAngle = 2.1;        // Can be adjusted according to centre of gravity 

// You can Turn off YAW control, by setting
// the Tp and Td constants below to 0.
float Tp = 0.6;             // Yaw Proportional Tuning Parameter
float Td = 0.1;         // Yaw Derivative Tuning Parameter
float targetYaw = 0;            // Used to maintain the robot's yaw
float lastYawError = 0;

float PIDGain = 0;        // Used for soft start (prevent jerking at initiation)


// Motor Control
// -- -- -- -- -- -- -- -- -- -- -- -- -- --
int direction_A = 0;            // 0 - Forwards, 1 - Backwards
int direction_B = 0;            //
int brake_A = 1;                // 1 - On, 0 - Off
int brake_B = 1;                //


// Runtime variables
// -- -- -- -- -- -- -- -- -- -- -- -- -- --
int modeSelect = 1;             // System Mode (0 = off, 1 = normal, 2 = guided)
bool initialised = true;        // Is the balancing system on?

char inchar = 0;                // Hold any incoming characters
float angular_rate = 0;         // Used to make sure rate is ~0 when balance mode is initiated

bool newCalibration = false;  // If set TRUE, the target angles are recalibrated


// Variables used for timing control
// Aim is 10ms per cycle (100Hz)
// -- -- -- -- -- -- -- -- -- -- -- -- -- --
#define STD_LOOP_TIME 9

unsigned long loopStartTime = 0;
unsigned long lastTime;             // Time since PID was called last (should be ~10ms)

// 0 = Off, 1 = On
int modes = 0;



// ------------------------------------------------------------------
//                INITIAL SETUP
// ------------------------------------------------------------------

void setup() {

    Wire.begin();

    // Initialize serial communication for debugging
    Serial.begin(115200);
  
   // Configure LED for output
    pinMode(LED_1, OUTPUT);
    pinMode(LED_2, OUTPUT);

    digitalWrite(LED_1, LOW);
    digitalWrite(LED_2, LOW);

    // Set as input, internal pullup for buttons
    pinMode(BTN_1, INPUT_PULLUP);
    pinMode(BTN_2, INPUT_PULLUP);

    // Configure Motor I/O
    pinMode(DIR_A, OUTPUT);     // Left Motor Direction
    pinMode(DIR_B, OUTPUT);     // Right Motor Direction
    pinMode(BRK_A, OUTPUT);     // Left Motor Brake
    pinMode(BRK_B, OUTPUT);     // Right Motor Brake

    // Initialize MPU6050
    mpu.initialize();
    Serial.println("Testing MPU connection:");

    Serial.println(mpu.testConnection() ? "> MPU6050 connection successful" : "> MPU6050 connection failed");
    Serial.println("Initialising DMP");
    devStatus = mpu.dmpInitialize();

    /* * * * * * * * * * * * * * * * * * * *
     * IMPORTANT!
     * Supply your own MPU6050 offsets here
     * Otherwise robot will not balance properly.
     * * * * * * * * * * * * * * * * * * * */
    mpu.setXGyroOffset(16362);
    mpu.setYGyroOffset(37);
    mpu.setZGyroOffset(31);
    mpu.setXAccelOffset(-1487);
    mpu.setYAccelOffset(1879);
    mpu.setZAccelOffset(1675);

    // Make sure it worked (returns 0 if so)
    if (devStatus == 0) {
        Serial.println("Enabling DMP");
        mpu.setDMPEnabled(true);
        mpuIntStatus = mpu.getIntStatus();

        // Set our DMP Ready flag so the main loop() function knows it's okay to use it
        Serial.println("DMP Ready! Let's Proceed.");
        Serial.println("Robot is now ready to balance. Hold the robot steady");
        Serial.println("in a vertical position, and the motors should start.");
        dmpReady = true;
        packetSize = mpu.dmpGetFIFOPacketSize();

    } else {
    // In case of an error with the DMP
        if(devStatus == 1) Serial.println("> Initial Memory Load Failed");
        else if (devStatus == 2) Serial.println("> DMP Configuration Updates Failed");
    }

}



// -------------------------------------------------------------------
//       PID CONTROLLER
// -------------------------------------------------------------------

int PID(float pitch) {            

    // Calculate time since last time PID was called (~10ms)
    // -- -- -- -- -- -- -- -- -- -- -- -- -- --
    unsigned long thisTime = millis();
    float timeChange = float(thisTime - lastTime);

    // Calculate Error
    float error = targetAngle - pitch;


    // Calculate our PID terms
    // PID values are multiplied/divided by 10 in order to allow the
    // constants to be numbers between 0-10.
    // -- -- -- -- -- -- -- -- -- -- -- -- -- --
    float pTerm = Kp * error * 10;
    iTerm += Ki * error * timeChange / 10;  
    float dTerm = Kd * (pitch - lastpitch) / timeChange * 100; 
  
  if (Ki == 0) iTerm = 0;
    lastpitch = pitch;
    lastTime = thisTime;


    // Obtain PID output value
    // -- -- -- -- -- -- -- -- -- -- -- -- -- --
    float PIDValue = pTerm + iTerm - dTerm;

    // Set a minimum speed (motors will not move below this - can help to reduce latency)
    //if(PIDValue > 0) PIDValue = PIDValue + 10;
    //if(PIDValue < 0) PIDValue = PIDValue - 10;

  // Limit PID value to maximum PWM values
    if (PIDValue > 255) PIDValue = 255;
    else if (PIDValue < -255) PIDValue = -255; 

    return int(PIDValue);

}



// -------------------------------------------------------------------
//       YAW CONTROLLER
// -------------------------------------------------------------------

int yawPD(int yawError) {            


    // Calculate our PD terms
    // -- -- -- -- -- -- -- -- -- -- -- -- -- --
    float pTerm = Tp * yawError;
    float dTerm = Td * (yawError - lastYawError) / 10; 
  
    lastYawError = yawError;

    // Obtain PD output value
    // -- -- -- -- -- -- -- -- -- -- -- -- -- --
    int yawPDvalue = int(-pTerm + dTerm);

  // Limit PD value to maximum
    if (yawPDvalue > MAX_TURN) yawPDvalue = MAX_TURN;
    else if (yawPDvalue < -MAX_TURN) yawPDvalue = -MAX_TURN; 

    //Serial.print("Error: ");
    //Serial.print(yawError);
    //Serial.print(" - PD: ");
    //Serial.println(yawPDvalue);
    return yawPDvalue;

}



// -------------------------------------------------------------------
//        MOVEMENT CONTROLLER
// -------------------------------------------------------------------
// This function calculate the PWM output required to keep the robot 
// balanced, to move it back and forth, and to control the yaw.

void MoveControl(int pidValue, float yaw){
  
    // Set both motors to this speed
    int left_PWM = pidValue;
    int right_PWM = pidValue;


    /* YAW CONTROLLER */

    // Check if turning left or right is faster
    // -- -- -- -- -- -- -- -- -- -- -- -- -- --
    int leftTurn, rightTurn;

    float newYaw = targetYaw;

    if((yaw > 0) && (newYaw < 0)){
        rightTurn = yaw + abs(newYaw);
        leftTurn = (180 - yaw) + (180 - abs(newYaw));

    } else if ((yaw < 0) && (newYaw > 0)){
        rightTurn = (180 - abs(yaw)) + (180 - newYaw);
        leftTurn = abs(yaw) + newYaw;

    } else if (((yaw > 0) && (newYaw > 0)) || ((yaw < 0) && (newYaw < 0))){
        rightTurn = newYaw - yaw;

        if (rightTurn > 0){
            leftTurn = rightTurn;
            rightTurn = 360 - leftTurn;
        } else if (rightTurn < 0){
            rightTurn = abs(rightTurn);
            leftTurn = 360 - abs(rightTurn);
        } else if (rightTurn == 0){
            rightTurn = leftTurn = 0;
        }
    }

    // Apply yaw PD controller to motor output
    // -- -- -- -- -- -- -- -- -- -- -- -- -- --
    if ((leftTurn == 0) && (rightTurn == 0)){
        // Do nothing
    } else if (leftTurn <= rightTurn){
      leftTurn = yawPD(leftTurn);
        left_PWM = left_PWM - leftTurn;
        right_PWM = right_PWM + leftTurn;

    } else if (rightTurn < leftTurn){
        rightTurn = yawPD(rightTurn);
        left_PWM = left_PWM + rightTurn;
        right_PWM = right_PWM - rightTurn;
        
    }


    // Limits PID to max motor speed
    // -- -- -- -- -- -- -- -- -- -- -- -- -- --
    if (left_PWM > 255) left_PWM = 255;
    else if (left_PWM < -255) left_PWM = -255; 
    if (right_PWM > 255) right_PWM = 255;
    else if (right_PWM < -255) right_PWM = -255; 

    // Send command to left motor
    if (left_PWM >= 0) Move(0, 0, int(left_PWM));     // '0' = Left-motor, '1' = Right-motor
    else Move(0, 1, (int(left_PWM) * -1));
  // Send command to right motor
    if (right_PWM >= 0) Move(1, 1, int(right_PWM));   // '0' = Forward, '1' = Backward
    else Move(1, 0, (int(right_PWM) * -1));    

}



// -------------------------------------------------------------------
//       MOTOR CONTROLLER
// -------------------------------------------------------------------

void Move(int motor, int direction, int speed) {            

  // Left Motor
  // -- -- -- -- -- -- -- -- -- -- -- -- -- --
  if (motor == 0){
  
    // Set motor direction (only if it is currently not that direction)
    if (direction == 0){
            if (direction_A == 1) digitalWrite(DIR_A, HIGH);    // Forwards
      direction_A = 0;
    } else {
      if (direction_A == 0)  digitalWrite(DIR_A, LOW);    // Backwards
      direction_A = 1;
    }
        
    // Release brake (only if brake is active)
    if (brake_A == 1){
      digitalWrite(BRK_A, LOW);
      brake_A = 0;
    }
    
    // Send PWM data to motor A
    analogWrite(PWM_A, speed);


    // Right Motor
  // -- -- -- -- -- -- -- -- -- -- -- -- -- --
    } else if (motor == 1){
  
    // Set motor direction (only if it is currently not that direction)
    if (direction == 0){
      if (direction_B == 1) digitalWrite(DIR_B, HIGH);    // Forwards
      direction_B = 0;
    } else {
      if (direction_B == 0)  digitalWrite(DIR_B, LOW);    // Backwards
      direction_B = 1;
    }
        
    // Release brake (only if brake is active)
    if (brake_B == 1){
      digitalWrite(BRK_B, LOW);
      brake_B = 0;
    }
    
    // Send PWM data to motor A
    analogWrite(PWM_B, speed);


    // Stop both motors
  // -- -- -- -- -- -- -- -- -- -- -- -- -- --
    } else if (motor = 3){  

        analogWrite(PWM_A, 0);
        analogWrite(PWM_B, 0);
        digitalWrite(BRK_A, HIGH);
        digitalWrite(BRK_B, HIGH);
        brake_A = 1;
        brake_B = 1;

    }
}



// -------------------------------------------------------------------
//       READ INPUT FROM SERIAL
// -------------------------------------------------------------------

void readSerial() {

    // Initiate all of the variables
    // -- -- -- -- -- -- -- -- -- -- -- -- -- --
  int changestate = 0;    // Which action needs to be taken?
  int no_before = 0;      // Numbers before decimal point
  int no_after = 0;     // Numbers after decimal point
  bool minus = false;     // See if number is negative
  inchar = Serial.read();   // Read incoming data

    if (inchar == 'P') changestate = 1;
    else if (inchar == 'I') changestate = 2;
    else if (inchar == 'D') changestate = 3;

    // Tell robot to calibrate the Centre of Gravity
    else if (inchar == 'G') calibrateTargets();


    // Records all of the incoming data (format: 00.000)
    // And converts the chars into a float number
    if (changestate > 0){
        if (Serial.available() > 0){

            // Is the number negative?
            inchar = Serial.read();
            if(inchar == '-'){
                minus = true;
                inchar = Serial.read();
            }
            no_before = inchar - '0';

            if (Serial.available() > 0){
                inchar = Serial.read();

                if (inchar != '.'){
                    no_before = (no_before * 10) + (inchar - '0');

                    if (Serial.available() > 0){
                        inchar = Serial.read();
                    }
                }

                if (inchar == '.'){
                    inchar = Serial.read();
                    if (inchar != '0'){
                        no_after = (inchar - '0') * 100;
                    }

                    if (Serial.available() > 0){
                        inchar = Serial.read();
                        if (inchar != '0'){
                            no_after = no_after + ((inchar - '0') * 10);
                        }

                        if (Serial.available() > 0){
                            inchar = Serial.read();
                            if (inchar != '0'){
                                no_after = no_after + (inchar - '0');
                            }
                        }
                    }
                }
            }

            // Combine the chars into a single float
            float answer = float(no_after) / 1000;
            answer = answer + no_before;
            if (minus) answer = answer * -1;

            // Update the PID constants
            if (changestate == 1){
                Kp = answer;
                Serial.print("P - ");
            } else if (changestate == 2){
                Ki = answer;
                Serial.print("I - ");
            } else if (changestate == 3){ 
                Kd = answer;
                Serial.print("D - ");
            }
            Serial.print("Constant Set: ");
            Serial.println(answer, 3);

        } else {
            changestate = 0;
        }
    }
}



// -------------------------------------------------------------------
//       RECALIBRATE TARGET VALUES
// -------------------------------------------------------------------
// Takes a number of readings and gets new values for the target angles.
// Robot must be held upright while this process is being completed.

void calibrateTargets(){

  targetAngle = 0;
  targetYaw = 0;
  
    for(int calibrator = 0; calibrator < 50; calibrator++){
  
    accelgyroData();
    targetAngle += pitch();
    targetYaw += yaw();
    delay(10);
  }
  
  // Set our new value for Pitch and Yaw
  targetAngle = targetAngle / 50;
  targetYaw = targetYaw / 50;
  Serial.print("Target Pitch: ");
  Serial.print(targetAngle, 3);
  Serial.print(", Target Yaw: ");
  Serial.print(targetYaw, 3);

  newCalibration = false;
}



// -------------------------------------------------------------------
//       GET PITCH AND YAW VALUES
// -------------------------------------------------------------------
// This simply converts the values from the accel-gyro arrays into degrees.

float pitch(){
  return (ypr[1] * 180/M_PI);
}

float yaw(){
  return (ypr[0] * 180/M_PI);
}

float angRate(){
  return -((float)gyro[1]/131.0);
}



// -------------------------------------------------------------------
//       GET ACCEL_GYRO DATA
// -------------------------------------------------------------------

void accelgyroData(){

    // Reset interrupt flag and get INT_STATUS byte
    mpuIntStatus = mpu.getIntStatus();

    // Get current FIFO count
    fifoCount = mpu.getFIFOCount();

    // Check for overflow (this should never happen unless our code is too inefficient)
    if ((mpuIntStatus & 0x10) || fifoCount == 1024) {
        // Reset so we can continue cleanly
        mpu.resetFIFO();
        Serial.println("Warning - FIFO Overflowing!");

    // otherwise, check for DMP data ready interrupt (this should happen exactly once per loop: 100Hz)
    } else if (mpuIntStatus & 0x02) {
        // Wait for correct available data length, should be less than 1-2ms, if any!
        while (fifoCount < packetSize) fifoCount = mpu.getFIFOCount();


        // read a packet from FIFO
        mpu.getFIFOBytes(fifoBuffer, packetSize);
        
        // track FIFO count here in case there is > 1 packet available
        // (this lets us immediately read more without waiting for an interrupt)
        fifoCount -= packetSize;

        // Get sensor data
        mpu.dmpGetQuaternion(&q, fifoBuffer);
        mpu.dmpGetGyro(gyro, fifoBuffer);
        mpu.dmpGetGravity(&gravity, &q);
        mpu.dmpGetYawPitchRoll(ypr, &q, &gravity);
        mpu.resetFIFO();

        //Serial.print(ypr[1]);
        //Serial.print(" - ");
        //Serial.println(ypr[0]);
    }
}



// -------------------------------------------------------------------
//       MAIN PROGRAM LOOP
// -------------------------------------------------------------------

void loop() {

  // If the "SET" button is pressed
  // -- -- -- -- -- -- -- -- -- -- -- -- -- --
  if (digitalRead(BTN_2) == LOW){

    digitalWrite(LED_1, HIGH);
      calibrateTargets();

      lastpitch = 0;
      iTerm = 0;

      Serial.println("> Setting new centre of gravity <");

    delay(250);
      mpu.resetFIFO();
      digitalWrite(LED_1, LOW);
  }


  // If the "POWER" button is pressed
  // -- -- -- -- -- -- -- -- -- -- -- -- -- --
  if (digitalRead(BTN_1) == LOW){
      if (modeSelect == 1){
          Serial.println("> Turning off balancing system <");
          initialised = false;
          modeSelect = 0;
          Move(3,0,0);        // Stop both motors from moving
          digitalWrite(LED_2, LOW);
      } else if (modeSelect == 0){
          Serial.println("> Turning on balancing system <");
          initialised = false;
          modeSelect = 1;
          digitalWrite(LED_2, HIGH);
      }
      delay(500);
      mpu.resetFIFO();
  }
    
  // Gather data from MPU6050
  accelgyroData();
    
  // If the Balance System is turned on:
  if (modeSelect == 1){
        
    if (!initialised){

          // Wait until robot is vertical and angular rate is almost zero:
          if ((pitch() < targetAngle+0.1) && (pitch() > targetAngle-0.1) && (abs(angRate()) < 0.3)){
              Serial.println(">>>> Balancing System Active <<<<");
              initialised = true;
              lastpitch = pitch();
              iTerm = 0;
          }
  
      // Otherwise, run the PID controller
    } else {

      // Stop the system if it has fallen over:
      if ((pitch() < -45) || (pitch() > 45)){
          
        // Stop the motors
        Move(3, 0, 0);
        // Reset runtime variables
        lastpitch = 0;
        iTerm = 0;
        initialised = false;
        Serial.println(">>>> Balancing System Stopped <<<<");

      } else {
        // A bit of function-ception happening here:
        //Serial.println(pitch());
        MoveControl(PID(pitch()), yaw());
      }
    }
  }

    if (Serial.available() > 0){    // If new PID values are being sent by the interface
        readSerial();               // Run the read serial method
    }

    // Call the timing function
    // Very important to keep the response time consistent!
    timekeeper();
}



// -------------------------------------------------------------------
//        TIME KEEPER
// -------------------------------------------------------------------

void timekeeper() {

    // Calculate time since loop began
    float timeChange = millis() - loopStartTime;

    // If the required loop time has not been reached, please wait!

    if (timeChange < STD_LOOP_TIME) {
        delay(STD_LOOP_TIME - timeChange);
    } 


    // Update loop timer variables
    loopStartTime = millis();   
}
