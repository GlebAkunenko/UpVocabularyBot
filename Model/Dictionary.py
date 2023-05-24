class Dictionary:
	def __init__(self, content: list[list[list]]):
		self.direct = {}
		self.reverse = {}
		for element in content:
			direct = tuple(element[0])
			reverse = tuple(element[1])
			self.direct[direct] = reverse
			self.reverse[reverse] = direct

	def remove_direct(self, line):
		del self.reverse[self.direct[line]]
		del self.direct[line]

	def remove_reverse(self, line):
		del self.direct[self.reverse[line]]
		del self.reverse[self.direct[line]]

	def __eq__(self, other: "Dictionary"):
		return self.direct == other.direct and self.reverse == other.reverse


class Parser:
	@staticmethod
	def parse_from_string(string: str) -> Dictionary:
		lines = string.strip().split("\n")
		content = []
		for line in lines:
			if line == "":
				continue
			keys, values = line.replace('—', '-').split("-")
			keys = keys.split(",")
			values = values.split(",")
			func = lambda s: s.strip()
			keys = list(map(func, keys))
			values = list(map(func, values))
			content.append([keys, values])
		return Dictionary(content)