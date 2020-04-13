class Declaration:
	def __init__(self, players: list) -> None:
		self.players = players
		self.declarations = []
		self.trump = None
		self.trump_player = None
		self.trump_player_initial_declaration = -1

	def find_trump(self, largest_number=5) -> None:
		# TODO: make pygame friendly
		print("bid a number lower than the highest number to pass")
		for player in self.players:
			print(player.name)
			number = int(input("number: "))
			if number >= largest_number:
				declaration_suit = int(input("1: Clubs\n2: Diamonds\n3: Hearts\n4: Spades\n\n: "))
				if declaration_suit == 1:
					self.trump = "Clubs"
				elif declaration_suit == 2:
					self.trump = "Diamond"
				elif declaration_suit == 3:
					self.trump = "Hearts"
				elif declaration_suit == 4:
					self.trump = "Spades"

				self.trump_player = self.players.index(player)
				self.trump_player_initial_declaration = number
				largest_number = number

			print("\n\n")

	def final_declarations(self):
		# TODO: make pyqt5 friendly
		def shift(arr, new_first):
			head_arr = arr[new_first:]
			tail_arr = arr[:new_first]
			return head_arr + tail_arr

		self.players = shift(self.players, self.trump_player)
		print("Final Declarations!!!")
		print("Trump: " + self.trump)
		for i in range(len(self.players)):
			print(self.players[i].name)
			declaration = int(input("declaration: "))
			if i == 0:
				while declaration < self.trump_player_initial_declaration:
					print("minimum: " + str(self.trump_player_initial_declaration))

					declaration = int(input("declaration: "))

			self.declarations[i] = declaration

			print("\n\n")

	def show_declaration(self):
		# used for debugging
		print("Trump: " + self.trump)
		print(f"| {self.players[0].name}:{self.declarations[0]} |")
		print(f"| {self.players[1].name}:{self.declarations[1]} |")
		print(f"| {self.players[2].name}:{self.declarations[2]} |")
		print(f"| {self.players[3].name}:{self.declarations[3]} |")
