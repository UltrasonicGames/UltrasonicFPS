from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import serial

ser = serial.Serial('/dev/cu.usbserial-1420', 9600)  # Change this to the correct port

app = Ursina()

# create a large-scale map
ground = Entity(
    model='plane',
    texture='grass',
    scale=(1000, 1, 1000),
    collider='box'
)
# Create some walls
wall1 = Entity(model='cube', scale=(1,100,1000), position=(-500,1,0), texture='brick', collider='box')
wall2 = Entity(model='cube', scale=(1,100,1000), position=(500,1,0), texture='brick', collider='box')
wall3 = Entity(model='cube', scale=(1000,100,1), position=(0,1,-500), texture='brick', collider='box')
wall4 = Entity(model='cube', scale=(1000,100,1), position=(0,1,500), texture='brick', collider='box')
# create a player entity with a weapon
player = FirstPersonController(
    position=(0, 1, 0),
    model='cube',
    color=color.white,
    scale=(0.5, 1, 0.5),
    speed=10,
    jump_height=1,
    gravity=0,
    collider='box'
)

# Create Text objects for displaying sensor readings
front_back_text = Text(text='Distance front/back: ', position=(-0.6, 0), origin=(0, 0), scale=1)
left_right_text = Text(text='Distance left/right: ', position=(0, 0), origin=(0, 0), scale=1)


# create a moving enemy entity

# front_threshold = 30
# # back_threshold = 30
# left_threshold = 30
# right_threshold = 30

threshold = 20
maxx = 120
# thresholdspeed = 10

def update():
    global front_back_text, left_right_text
    if ser.in_waiting > 0:
        sensor_data = ser.readline().decode().strip().split(',')
        distance_front_back = int(sensor_data[0])
        distance_left_right = int(sensor_data[1])
        
        
        
        # Update Text objects with sensor readings
        front_back_text.text = 'Distance front/back: ' + str(distance_front_back)
        left_right_text.text = 'Distance left/right: ' + str(distance_left_right)
        
        
        
        
        
        # player.x += 0
        # player.z += 0
        # Calculate movement based on sensor data
        if distance_front_back == 0 or distance_front_back > 170 and distance_left_right == 0:
            x_movement = 0
            z_movement = 0
            player.z += z_movement
            player.x += x_movement
        else:
            
            
            
            if distance_front_back < 15 and distance_front_back < 80:
                z_movement = 1
                x_movement = 0
                player.z += z_movement
                player.x += x_movement 
                
            
            elif distance_front_back > 15 and distance_front_back < 80:
                z_movement = -1
                x_movement = 0
                player.z += z_movement
                player.x += x_movement
            
            
            
            
                
       
                
                
            elif distance_left_right < 15:
                x_movement = -1
                z_movement = 0
                player.x += x_movement
                player.z += z_movement
                
            
                
            elif distance_left_right > 15:
                x_movement = 1
                z_movement = 0
                player.x += x_movement
                player.z += z_movement
                
            else:
                x_movement = 0
                z_movement = 0
                player.z += z_movement
                player.x += x_movement
            
        # Limit movement to avoid excessive speed
        # x_movement = max(min(x_movement, 0.1), -0.1)
        # z_movement = max(min(z_movement, 0.1), -0.1)
        
        # Move player
        # player.x += x_movement
        # player.z += z_movement
app.run()
