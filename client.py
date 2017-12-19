import zmq
import Board
import bot

# ==== PLAYER ====

def get_array(string) :
	array = []
	string_list = string.split(";")
	for i in string_list :
		temp = i.split(",")
		array.append(temp)
	# print array
	return array


if __name__ == '__main__':
	

	choice = raw_input("Do you want to be Player 1 ? [y/n] : ")
	is_player_one = choice == "y"
	port_number = 5555
	if not is_player_one :
		port_number = 5556

	context = zmq.Context()
	socket = context.socket(zmq.REQ)
	socket.connect("tcp://localhost:"+str(port_number))

	# get server's permission to join game
	print "Asking server to let me play..."
	socket.send_string("Can I play?")
	reply = socket.recv_string()

	permission = str(reply).split()
	print permission
	if permission[0] == "No" :
		print "Sorry, someone was already playing..."
		exit(0)
	color = permission[1]
	opponent_color = permission[2]
	max_col = int(permission[3])
	max_row = int(permission[4])
	print "My color is", color

	board = Board.Board(max_col, max_row, color, opponent_color)
	player = bot.Connect_Four_Bot(board, color, 7, True)


	print "Waiting other player..."

	while True :
		socket.send_string(str(port_number))

		state = socket.recv_string()
		if "Game Complete!" in str(state) :
			break
		# print state
		array = get_array(str(state))
		# print "assigning this state to my local state"
		board.set_board_array(array)
		board.print_board()
		print "thinking of my move..."
		col = player.make_a_move()
		
		move = ""
		move += str(port_number) + " "
		move += str(col) + " "
		move += color
		socket.send_string(move)

		#  Get the reply.
		reply = socket.recv_string()
		# print "Received reply", reply
	winner = str(state).split()[-1]
	print winner
	if color == winner :
		print "You win!"
	elif opponent_color == winner :
		print "Opponent won!"
	else :
		print "Game Draw!"