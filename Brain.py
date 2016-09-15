import os
import threading
import numpy as np
from InputReceiver import InputReceiver
from FileWriter import write

class Brain:
	OUTPUT_STATES = 3  # 10 digits
	ARRAY_SIZE = (OUTPUT_STATES)
	THINKING_SPEED = 1  # Seconds per thinking loop
	DECAY_RATE = 0.99  # Percent of memories kept at each iteration
	RANDOM_WEIGHT = 0.5
	REINFORCEMENT_RATE = 1
	DISCOURAGEMENT_RATE = 1
	VALID_INPUT = np.arange(10)
	VALID_OUTPUT = np.arange(10)

	def __init__(self):
		self.state = None
		self.command_state_memory = {}
		self.last_alteration = None

	def live(self):
		while True:
			print()
			self.state = self.get_neutral_state()

			# Get a command
			command = str(self.get_command())

			# Update brain state based on command
			self.update_from_command(command)
			# print(self.state)

			# Get Feedback based on command
			feedback = self.get_feedback()

			# Learn from feedback
			self.learn(command, feedback)


	def get_neutral_state(self):
		return np.zeros(self.ARRAY_SIZE)

	@staticmethod
	def get_command():
		command = input('Please give me a command: ')
		return command

	def update_from_command(self, command):
		try:
			# We have seen this command before and got good feedback - let's try it again
			self.state = self.command_state_memory[command]
		except KeyError:
			# We don't have a success state for this command - let's try something random and get some feedback
			self.randomly_mutate()

	def randomly_mutate(self):
		alteration = np.random.uniform(-self.RANDOM_WEIGHT, self.RANDOM_WEIGHT, self.ARRAY_SIZE)
		self.state += alteration
		self.last_alteration = alteration

	def get_feedback(self):
		feedback = input('Is this correct? -> {0}\n(y/n) --> '.format(self.output()))
		while feedback not in ['n','y']:
			feedback = input('Please provide feedback as either "y" or "n" --> ')
		return feedback

	def output(self):
		return np.argmax(self.state)

	def learn(self, command, feedback):
		if feedback == 'n':
			print('Ok, so that was not right. Let me try again....')
			self.command_state_memory.pop(command, None)  # Remove any stored success state
		else:
			print('Great! I think I am understanding.')
			self.save_command_state(command, self.state)

	def save_command_state(self, command, success_state):
		self.command_state_memory[command] = np.copy(success_state)
		# print(self.command_state_memory)


	# def get_inputs(self):
	# 	return self.input_receiver.return_inputs()
	#
	# def update(self, inputs):
	# 	self.randomly_mutate()
	# 	self.decay()
	# 	self.learn_from_inputs(inputs)
	#

	#
	# def decay(self):
	# 	self.state *= self.DECAY_RATE
	#
	# def learn_from_inputs(self, inputs):
	# 	for input in inputs:
	# 		alteration = self.map_input_to_alteration(input)
	# 		write(str(alteration))
	# 		self.state += alteration
	#
	# def map_input_to_alteration(self, input):
	# 	alteration = np.zeros(self.ARRAY_SIZE)
	#
	# 	try:
	# 		input = int(input)
	# 		if input in self.VALID_INPUT:
	# 			alteration[input] += self.REINFORCEMENT_RATE
	# 		else:
	# 			write('{0} is not a valid input'.format(str(input)))
	# 	except TypeError:
	# 		write('TypeError: {0} is not a valid input'.format(str(input)))
	#
	# 	return alteration


if __name__ == '__main__':
	brain = Brain()
	brain.live()
