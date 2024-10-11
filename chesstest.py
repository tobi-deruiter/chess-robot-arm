import chess
import chess.engine
import time

engine = chess.engine.SimpleEngine.popen_uci(r"/home/rarm/Stockfish-sf_15/src/stockfish")

board = chess.Board()
print(board)
while not board.is_game_over():
 result = engine.play(board, chess.engine.Limit(time=0.1))
 print(result.move)
 board.push(result.move)
 print(board)
 time.sleep(3)
 

engine.quit()
