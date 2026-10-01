# Import necessary modules from machine and time libraries for hardware and delay control
from machine import Pin, PWM
from time import sleep

# Turn ON the built-in LED on the Raspberry Pi Pico to indicate power status
LED = Pin("LED", Pin.OUT)
LED.on()

# Configure Motor A PWM pin for speed control and digital pin for direction
e1 = PWM(Pin(28))
m1 = Pin(27, Pin.OUT)

# Configure Motor B PWM pin for speed control and digital pin for direction
e2 = PWM(Pin(26))
m2 = Pin(22, Pin.OUT)

# Set PWM frequency to 1000 Hz for smooth motor operation
e1.freq(1000)
e2.freq(1000)

# Function to stop both motors and pause execution for 1 second
def stop():
    e1.duty_u16(0)
    e2.duty_u16(0)
    sleep(1)

# Function to move the robot forward at 50 percent speed for 2 seconds
def forward():
    m1.value(1)
    m2.value(1)
    e1.duty_u16(32767)
    e2.duty_u16(32767)
    sleep(2)        
    stop()

# Function to move the robot backward at 50 percent speed for 2 seconds
def backward():
    m1.value(0)
    m2.value(0)
    e1.duty_u16(32767)
    e2.duty_u16(32767)
    sleep(2)
    stop()

# Function to turn the robot left by adjusting motor speeds for 0.8 seconds
def turn_left():
    m1.value(1)
    m2.value(1)
    e1.duty_u16(65535)
    e2.duty_u16(32767)
    sleep(0.8)        
    stop()

# Function to turn the robot right by adjusting motor speeds for 0.8 seconds
def turn_right():
    m1.value(1)
    m2.value(1)
    e1.duty_u16(32767)
    e2.duty_u16(65535)
    sleep(0.8)        
    stop()

# Function to perform a 180-degree turn by doubling the turn duration
def turn_180():
    m1.value(1)
    m2.value(1)
    e1.duty_u16(65535)
    e2.duty_u16(32767)
    sleep(0.8 * 2)        
    stop()


# Dictionary mapping text commands from file to their respective Python functions
command_actions = {
    "FORWARD": forward,
    "BACKWARD": backward,
    "TURN_LEFT": turn_left,
    "TURN_RIGHT": turn_right,
    "TURN_180": turn_180,
    "STOP": stop
}

# Function to read movement instructions line by line from an external text file
def run_robot_from_file(filename="instructions.txt"):
    print(f"Reading movement instructions from {filename}...")
    try:
        # Open the instruction file in read mode
        with open(filename, "r") as file:
            # Iterate through each line in the file
            for line in file:
                # Clean whitespace and convert command text to uppercase
                cmd = line.strip().upper()
                # Skip empty lines or comment lines starting with '#'
                if not cmd or cmd.startswith("#"):
                    continue
                
                # Check if the command exists in our dictionary and execute it
                if cmd in command_actions:
                    print(f"Executing: {cmd}")
                    command_actions[cmd]()
                else:
                    print(f"Unknown command: {cmd}")
                    
        print("All instructions executed successfully!")
    except FileNotFoundError:
        # Handle error gracefully if the instruction file is missing
        print(f"Error: File '{filename}' not found.")

# Main entry point to run the file-based robot instruction sequence
if __name__ == "__main__":
    run_robot_from_file()
