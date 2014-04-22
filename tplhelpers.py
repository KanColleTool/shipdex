def speed_string(stat):
	if stat >= 10:
		return "Fast"
	return "Slow"

def range_string(stat):
	if stat >= 4:
		return "V.Long"
	elif stat == 3:
		return "Long"
	elif stat == 2:
		return "Medium"
	elif stat <= 1:
		return "Short"
	return "??? (%s)" % stat
