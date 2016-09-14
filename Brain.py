import os
import threading
import numpy as np
from InputReceiver import InputReceiver
from FileWriter import write

class Brain:
	OUTPUT_STATES = 10  # 10 digits
	ARRAY_SIZE = (OUTPUT_STATES)
	THINKING_SPEED = 1  # Seconds per thinking loop
	DECAY_RATE = 0.99  # Percent of memories kept at each iteration
	RANDOM_WEIGHT = 0.5
	REINFORCEMENT_RATE = 1
	DISCOURAGEMENT_RATE = 1
	VALID_INPUT = np.arange(10)
	VALID_OUTPUT = np.arange(10)

	def __init__(self):
		self.state = np.zeros(self.ARRAY_SIZE)
		self.thinking = False
		self.input_receiver = InputReceiver()
		threading.Thread(target=self.input_receiver.receive).start()

	# Runs every THINKING_SPEED seconds - skips a thinking loop if last loop is still running. This allows
	#   us to limit thinking speed.
	def live(self):
		threading.Timer(self.THINKING_SPEED, self.live).start()

		# If we are still thinking from last time, skip this run
		if self.thinking: return

		# BEGIN THINKING
		self.thinking = True
		# write()

		# Get input
		inputs = self.get_inputs()

		# Update
		self.update(inputs)

		# Output
		self.output()

		self.thinking = False
		# END THINKING

	def get_inputs(self):
		return self.input_receiver.return_inputs()

	def update(self, inputs):
		self.randomly_mutate()
		self.decay()
		self.learn_from_inputs(inputs)

	def randomly_mutate(self):
		self.state += np.random.uniform(-self.RANDOM_WEIGHT, self.RANDOM_WEIGHT, self.ARRAY_SIZE)

	def decay(self):
		self.state *= self.DECAY_RATE

	def learn_from_inputs(self, inputs):
		for input in inputs:
			alteration = self.map_input_to_alteration(input)
			write(str(alteration))
			self.state += alteration

	def map_input_to_alteration(self, input):
		alteration = np.zeros(self.ARRAY_SIZE)

		try:
			input = int(input)
			if input in self.VALID_INPUT:
				alteration[input] += self.REINFORCEMENT_RATE
			else:
				write('{0} is not a valid input'.format(str(input)))
		except TypeError:
			write('TypeError: {0} is not a valid input'.format(str(input)))

		return alteration

	def output(self):
		# write(str(self.state))
		write(str(np.argmax(self.state)))


if __name__ == '__main__':
	os.remove('output.txt')
	brain = Brain()
	brain.live()
