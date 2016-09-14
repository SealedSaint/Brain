from FileWriter import write

class InputReceiver:

	def __init__(self):
		self.inputs = []

	def receive(self):
		while True:
			new = input('--> ')
			self.inputs.append(new)

	def return_inputs(self):
		new_inputs = self.inputs
		self.inputs = []
		return new_inputs