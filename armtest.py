# Used when developing and testing robot arm movement

import time
from adafruit_servokit import ServoKit

kit = ServoKit(channels=16, address=0x41)

# ~ kit.servo[0].angle = 0
# ~ time.sleep(1)
# ~ kit.servo[1].angle = 180

home = [25, 65, 170, 90, 0, 0]
straight_up = [90, 110, 30, 90, 120, 0]
straight2 = [90, 0, 30, 90, 120, 0]
loose = [None, None, None, None, None, None]

def move(pos):
	for i in range(6):
		kit.servo[i].angle = pos[i]
		if i > 2:
			time.sleep(1)
			kit.servo[i].angle = None

# ~ move(straight_up)

# ~ speed = 1
# ~ motor = 4
# ~ kit.servo[motor].angle = 0
# ~ while kit.servo[motor].angle < 180:
	# ~ if kit.servo[motor].angle + speed < 180:
		# ~ kit.servo[motor].angle += speed
	# ~ else:
		# ~ kit.servo[motor].angle = 180
		
# ~ while kit.servo[motor].angle > 0:
	# ~ if kit.servo[motor].angle - speed > 0:
		# ~ kit.servo[motor].angle -= speed
	# ~ else:
		# ~ kit.servo[motor].angle = 0
		
# ~ move(loose)

from RobotArm import RobotArm

time.sleep(1)
ra = RobotArm(debug=True)

# ~ ra.test_motors(7)

# ~ ra.move_to_position(-70, 190, 0, -45)
# ~ ra.open_close(True)
# ~ ra.move_to_position(-75, 75, -60, -90)
# ~ time.sleep(1)
# ~ ra.open_close(False)
# ~ time.sleep(1)
# ~ ra.move_to_position(-75, 75, 0, -90)
# ~ ra.move_to_position(75, 75, 0, -90)
# ~ ra.move_to_position(75, 75, -60, -90)
# ~ time.sleep(1)
# ~ ra.open_close(True)
ra.release()
