from RobotArm import RobotArm
import chess.engine
import chess

class ChessBot:
	def __init__(self, rf_x=-70, rf_y=25, rf_z=-60):
		self.engine = chess.engine.SimpleEngine.popen_uci(r"/home/rarm/Stockfish-sf_15/src/stockfish")
		self.board = chess.Board()
		
		self.ra = RobotArm(debug=True)
		
		self.l_to_c = {
			"a": 0,
			"b": 1,
			"c": 2,
			"d": 3,
			"e": 4,
			"f": 5,
			"g": 6,
			"h": 7
		}
		
		self.phi_range = -45 - -95
		
		self.ra.move_ref_frame(rf_x, rf_y, rf_z)
		
	def main(self):
		while not self.board.is_game_over():
			result = self.engine.play(self.board, chess.engine.Limit(time=0.1))
			print(result.move)
			self.board.push(result.move)
			print(self.board)
			
			start, end = self.uci_to_arm_coords(str(result.move))
			
			phi = self.find_phi(start[1])
			print("phi", phi)
			self.ra.move_to_position(start[0], start[1], 60, phi)
			self.ra.open_close(True)
			self.ra.move_to_position(start[0], start[1], 0, phi)
			self.ra.open_close(False)
			self.ra.move_to_position(start[0], start[1], 60, phi)
			
			phi = self.find_phi(end[1])
			print("phi", phi)
			self.ra.move_to_position(end[0], end[1], 60, phi)
			self.ra.move_to_position(end[0], end[1], 0, phi)
			self.ra.open_close(True)
			self.ra.move_to_position(end[0], end[1], 60, phi)
			
	def find_phi(self, dist):
		return -95 + (dist/140*self.phi_range)
			
	def uci_to_arm_coords(self, result):
		start = str(result)[0:2]
		end = str(result)[2:4]
		start_coord = self.chess_loc_to_arm_coord(start)
		end_coord = self.chess_loc_to_arm_coord(end)
		return start_coord, end_coord
		
		
	def chess_loc_to_arm_coord(self, loc):
		coord = [0, 0]
		coord[0] = self.l_to_c[loc[0]] * 20
		coord[1] = (int(loc[1])-1) * 20
		return coord
		
	
if __name__ == "__main__":
	cb = ChessBot()
	cb.main()
	
