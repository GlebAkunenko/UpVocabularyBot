from random import shuffle


class Lesson:
	def __init__(self, exercises: dict[str, list[str]]):
		words = list(exercises.keys())
		self.words = []
		self.exercises = {}
		for word in words:
			if len(word) == 1:
				self.words.append(word[0])
				self.exercises[word[0]] = exercises[word]
			else:
				for subword in word:
					self.words.append(subword)
					self.exercises[subword] = exercises[word]
		self.right_answers = 0
		shuffle(self.words)

	def is_empty(self):
		return len(self.words) == 0

	@property
	def current_question(self):
		return self.words[0]

	def check_answer(self, answer: str):
		return answer in self.exercises[self.current_question]

	@property
	def answers_count(self):
		return len(self.exercises[self.current_question])

	def is_question_completed(self):
		return self.right_answers == self.answers_count

	def complete_question(self):
		self.words.pop(0)
		self.right_answers = 0