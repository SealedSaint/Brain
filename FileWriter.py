def write(text=''):
	with open('output.txt', 'a') as out:  # 'a' opens for appending
		out.write(text + '\n')