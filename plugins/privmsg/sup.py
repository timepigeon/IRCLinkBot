def main(data):
	sups = ["hello", "gday", "good morning", "good night"]
	for sup in sups:
		if ":"+sup in data['recv'].lower():
			args = argv(sup, data['recv'])
			if len(args['argv']) == 1:
				data['api'].say(args['channel'], sup)
