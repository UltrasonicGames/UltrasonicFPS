from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import serial

ser = serial.Serial('/dev/cu.usbserial-1420', 9600)  # Change this to the correct port

app = Ursina()

# create a large-scale map
ground = Entity(
    model='plane',
    texture='grass',
    scale=(100, 1, 100),
    collider='box'
)
# Create some walls
wall1 = Entity(model='cube', scale=(1,10,100), position=(-50,1,0), texture='brick', collider='box')
wall2 = Entity(model='cube', scale=(1,10,100), position=(50,1,0), texture='brick', collider='box')
wall3 = Entity(model='cube', scale=(100,10,1), position=(0,1,-50), texture='brick', collider='box')
wall4 = Entity(model='cube', scale=(100,10,1), position=(0,1,50), texture='brick', collider='box')
# create a player entity with a weapon
player = FirstPersonController(
    position=(0, 1, 0),
    model='cube',
    color=color.white,
    scale=(0.5, 1, 0.5),
    speed=10,
    jump_height=1,
    gravity=1,
    collider='box'
)



# create a moving enemy entity

# front_threshold = 30
# # back_threshold = 30
# left_threshold = 30
# right_threshold = 30

threshold = 50
maxx = 120


def update():
    if ser.in_waiting > 0:
        sensor_data = ser.readline().decode().strip().split(',')
        distance_front_back = int(sensor_data[0])
        distance_left_right = int(sensor_data[1])
        # player.x += 0
        # player.z += 0
        # Calculate movement based on sensor data
        x_movement = 0
        z_movement = 0
        if distance_front_back == 0 and distance_left_right == 0:
            x_movement = 0
            z_movement = 0
            
        else:
            
            if distance_front_back < threshold and distance_front_back < maxx:
                z_movement = 0.1
            
            elif distance_front_back > threshold and distance_front_back < maxx:
                z_movement = -0.1
            
            elif distance_left_right < threshold and distance_left_right < maxx:
                x_movement = -0.1

            elif distance_left_right > threshold and distance_left_right < maxx:
                x_movement = 0.1

            else:
                x_movement = 0
                z_movement = 0
            
        # Limit movement to avoid excessive speed
        # x_movement = max(min(x_movement, 0.1), -0.1)
        # z_movement = max(min(z_movement, 0.1), -0.1)
        
        # Move player
        player.x += x_movement
        player.z += z_movement
app.run()
