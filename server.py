import time
import zmq
import Board

# ==== BOARD ====

def get_parameter_from_message(message) :
	param_list = str(message).split()
	print param_list
	return param_list

def get_string(array) :
	string_list = []
	for i in array :
		string_list.append(",".join(i))
	string = ";".join(string_list)
	print string
	return string

if __name__ == '__main__':

	red = "x"
	blue = "o"
	none = "N"
	max_depth = 9
	max_col = 5
	max_row = 4
	board = Board.Board(max_col, max_row, red, blue)
	
	context = zmq.Context()
	socket = context.socket(zmq.REP)
	socket2 = context.socket(zmq.REP)
	socket.bind("tcp://*:5555")
	socket2.bind("tcp://*:5556")

	# waiting for players and assigning them their color
	print "waiting for player 1"
	player_1_game_request = socket.recv_string()
	if player_1_game_request == "Can I play?" :
		socket.send_string("Yes " + str(red) + " " + str(blue) + " " + str(max_col) + " " + str(max_row))
	print "player 1 successfully connected"
	print "waiting for player 2"
	player_2_game_request = socket2.recv_string()
	if player_2_game_request == "Can I play?" :
		socket2.send_string("Yes " + str(blue) + " " + str(red) + " " + str(max_col) + " " + str(max_row))
	print "player 2 successfully connected"

	print "Starting the game now!"


	p1_turn = True
	while not board.is_game_complete() :
		#  Wait for next request from client
		soc = None
		if p1_turn :
			soc = socket
		else :
			soc = socket2
		
		message = soc.recv_string()
		print "Received request: %s" % message
		# Deny any other player after the game has started
		if message == "Can I play?" :
			soc.send_string("No")
			continue

		soc.send_string(get_string(board.get_board_array()))
		
		message = soc.recv_string()
		print "Received request: %s" % message
		# Deny any other player after the game has started
		if message == "Can I play?" :
			soc.send_string("No")
			continue


		#  Do some 'work'
		move_params = get_parameter_from_message(message)
		
		move_successfull = board.put_piece_at(int(move_params[1]), move_params[2])

		board.print_board()
		time.sleep(1)

		#  Send reply back to client
		soc.send_string(str(move_successfull))

		if move_successfull :
			p1_turn = not p1_turn

	message = socket.recv_string()
	socket.send_string("Game Complete! " + str(board.winner))
	message = socket2.recv_string()
	socket2.send_string("Game Complete! " + str(board.winner))
	
		