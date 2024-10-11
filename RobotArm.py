from adafruit_servokit import ServoKit
import time
import math

class RobotArm:
	def __init__(self, debug=False):
		self.debug = debug
		
		self.straight_up = [90, 90, 45, 90, 110, 0]
		self.theta = [0, 0, 0, 90, 0]
		self.x = 0
		self.y = 0
		self.z = 0
		self.r = 0
		self.rf_x = 0
		self.rf_y = 0
		self.rf_z = 0
		self.l1 = 90
		self.l2 = 100
		self.l3 = 127.5
		self.l4 = 125
		self.cur_ang = []*5
		self.kit = ServoKit(channels=16, address=0x41)
		self.kit.servo[0].set_pulse_width_range(550, 2350)
		self.kit.servo[1].set_pulse_width_range(720, 2520)
		self.kit.servo[2].set_pulse_width_range(550, 2350)
		self.kit.servo[3].set_pulse_width_range(550, 2450)
		self.kit.servo[4].set_pulse_width_range(625, 2525)
		self.kit.servo[7].set_pulse_width_range(900, 1500)
		
		if self.debug: print("Homing...")
		self.home()
		time.sleep(1)
		if self.debug: print("Starting!")
		
	def test_motors(self, i):
		self.kit.servo[i].angle = 0
		time.sleep(2)
		self.kit.servo[i].angle = 180
		
	def home(self):
		home = self.cur_ang = [90, 160, 170, 90, 20]
		for i in range(5):
			self.kit.servo[i].angle = home[i]
		self.kit.servo[7].angle = 0
			
		time.sleep(1)	
		self.kit.servo[3].angle = None
		self.kit.servo[4].angle = None
		self.kit.servo[7].angle = None
		
	def map_angles(_, theta):
		new_angles = theta
		new_angles[0] = self.straight_up[0] - theta[0]
		new_angles[2] = self.straight_up[2] - theta[2]
		new_angles[4] = self.straight_up[4] + theta[4]
		return new_angles
		
	def move_to_angles(self, speed=1):
		if self.debug: print("\nMoving...")
		start_time = time.time()
		for i in range(5):
			if self.cur_ang[i] < 0: self.cur_ang[i] = 0;
			if self.cur_ang[i] > 180: self.cur_ang[i] = 180;
			self.kit.servo[i].angle = self.cur_ang[i]
			
		reached_position = [False for x in range(5)]
		while True:
			for i in range(5):
				d = self.theta[i] - self.cur_ang[i]
				if d != 0: s = d/abs(d) * speed;
				else: s = speed;
								
				if abs(d) > abs(s):
					self.kit.servo[i].angle += s
				else:
					self.kit.servo[i].angle = self.theta[i]
					reached_position[i] = True
									
				self.cur_ang[i] = self.kit.servo[i].angle
				
			if reached_position == [True for x in range(5)]:
				if self.debug: print("Movement Completed!")
				print("Movement Time:", time.time()-start_time)
				break		
		
		self.kit.servo[3].angle = None
		self.kit.servo[4].angle = None
				
	def get_theta1(self, t2, phi, p_m):
		t1_a = math.atan((self.z-self.l4*math.sin(math.radians(phi)))/(self.r-self.l4*math.cos(math.radians(phi))))
		t1_b = math.atan((self.l3*math.sin(math.radians(t2)))/(self.l2+self.l3*math.cos(math.radians(t2))))
		if p_m: return  math.degrees(t1_a + t1_b);
		else: return math.degrees(t1_a - t1_b);
		
	def try_equations(self, t2, phi):
		if self.debug: print("\nAquiring angles...")
		trys = [[0 for x in range(len(self.theta))] for x in range(4)]
		for x in range(4):
			for y in range(5):
				trys[x][y] = self.theta[y]
		
		trys[0][2] = -t2
		trys[0][1] = self.get_theta1(-t2, phi, True)
		trys[0][4] = phi - trys[0][2] - trys[0][1]
		
		trys[1][2] = t2
		trys[1][1] = self.get_theta1(t2, phi, True)
		trys[1][4] = phi - trys[1][2] - trys[1][1]
		
		trys[2][2] = -t2
		trys[2][1] = self.get_theta1(-t2, phi, False)
		trys[2][4] = phi - trys[2][2] - trys[2][1]
		
		trys[3][2] = t2
		trys[3][1] = self.get_theta1(t2, phi, False)
		trys[3][4] = phi - trys[3][2] - trys[3][1]
		
		for a in range(4):
			new_angles = self.map_angles(trys[a])
			if self.debug: print(f"try {a}", new_angles)
			for b in range(len(self.theta)):
				if trys[a][b] >= 0 and trys[a][b] <= 180:
					continue
				elif trys[a][b] > -10 and trys[a][b] < 0:
					trys[a][b] = 0
					continue
				elif trys[a][b] < 190 and trys[a][b] > 180:
					trys[a][b] = 180
					continue
				else:
					new_angles = None
					break
			if new_angles != None and new_angles[1] > 10:
				return new_angles
							
	def move_to_position(self, x, y, z, phi=-45):
		self.x = x + self.rf_x
		self.y = y + self.rf_y
		self.z = z + self.rf_z
		
		self.y += 15
		if self.x == 0: self.x = 0.001;
		self.theta[0] = math.degrees(math.atan(self.x/self.y))
			
		self.r = math.sqrt(math.pow(self.x, 2) + math.pow(self.y, 2))
				
		a = (math.pow(self.r, 2) + math.pow(self.z, 2) + math.pow(self.l4, 2) - math.pow(self.l3, 2) - math.pow(self.l2, 2) -
				2*self.l4*(self.r*math.cos(math.radians(phi)) + self.z*math.sin(math.radians(phi))))
		
		t2 = math.degrees(math.acos(a / (2 * self.l2 * self.l3)))
		
		self.theta = self.try_equations(t2, phi)
		
		if self.debug:
			print("Chosen angles to go to:")
			for i in range(5):
				print(i, self.theta[i])

		self.move_to_angles()
		
	def move_ref_frame(self, x, y, z):
		self.rf_x = x
		self.rf_y = y
		self.rf_z = z
		
	def open_close(self, o_c=True):
		if o_c:
			self.kit.servo[7].angle = 180
			time.sleep(0.5)
			self.kit.servo[7].angle = None
		else:
			self.kit.servo[7].angle = 0
			time.sleep(0.5)
			
	def release(self):
		for i in range(5):
			self.kit.servo[i].angle = None
		self.kit.servo[7].angle = None
