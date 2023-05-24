from unittest import TestCase
import Model


class DictionaryTests(TestCase):

	def test_init_one_to_one(self):
		input = [
			[["w1"], ["k1"]],
			[["w2"], ["k2"]],
			[["w3"], ["k3"]]
		]
		my_dict = Model.Dictionary(input)
		actual_direct = my_dict.direct
		actual_reverse = my_dict.reverse
		expected_direct = {
			("w1",): ("k1",),
			("w2",): ("k2",),
			("w3",): ("k3",)
		}
		expected_reverse = {
			("k1",): ("w1",),
			("k2",): ("w2",),
			("k3",): ("w3",)
		}
		self.assertEqual(expected_direct, actual_direct)
		self.assertEqual(expected_reverse, actual_reverse)

	def test_init_one_to_many(self):
		input = [
			[["w1"], ["k11", "k12", "k13"]],
			[["w2"], ["k21", "k22", "k23"]],
			[["w3"], ["k31", "k32", "k33"]]
		]
		my_dict = Model.Dictionary(input)
		actual_direct = my_dict.direct
		actual_reverse = my_dict.reverse
		expected_direct = {
			("w1",): ("k11", "k12", "k13"),
			("w2",): ("k21", "k22", "k23"),
			("w3",): ("k31", "k32", "k33")
		}
		expected_reverse = {
			("k11", "k12", "k13"): ("w1",),
			("k21", "k22", "k23"): ("w2",),
			("k31", "k32", "k33"): ("w3",)
		}
		self.assertEqual(expected_direct, actual_direct)
		self.assertEqual(expected_reverse, actual_reverse)

	def test_init_many_to_one(self):
		input = [
			[["w11", "w12", "w13"], ["k1"]],
			[["w21", "w22", "w23"], ["k2"]],
			[["w31", "w32", "w33"], ["k3"]]
		]
		my_dict = Model.Dictionary(input)
		actual_direct = my_dict.direct
		actual_reverse = my_dict.reverse
		expected_direct = {
			("w11", "w12", "w13"): ("k1",),
			("w21", "w22", "w23"): ("k2",),
			("w31", "w32", "w33"): ("k3",)
		}
		expected_reverse = {
			("k1",): ("w11", "w12", "w13"),
			("k2",): ("w21", "w22", "w23"),
			("k3",): ("w31", "w32", "w33")
		}
		self.assertEqual(expected_direct, actual_direct)
		self.assertEqual(expected_reverse, actual_reverse)

	def test_init_many_to_many(self):
		input = [
			[["w11", "w12", "w13"], ["k11", "k12", "k13"]],
			[["w21", "w22", "w23"], ["k21", "k22", "k23"]],
			[["w31", "w32", "w33"], ["k31", "k32", "k33"]]
		]
		my_dict = Model.Dictionary(input)
		actual_direct = my_dict.direct
		actual_reverse = my_dict.reverse
		expected_direct = {
			("w11", "w12", "w13"): ("k11", "k12", "k13"),
			("w21", "w22", "w23"): ("k21", "k22", "k23"),
			("w31", "w32", "w33"): ("k31", "k32", "k33")
		}
		expected_reverse = {
			("k11", "k12", "k13"): ("w11", "w12", "w13"),
			("k21", "k22", "k23"): ("w21", "w22", "w23"),
			("k31", "k32", "k33"): ("w31", "w32", "w33")
		}
		self.assertEqual(expected_direct, actual_direct)
		self.assertEqual(expected_reverse, actual_reverse)


class DictionaryParserTests(TestCase):

	def test_parse_one_to_one(self):
		input = """
		k1 - v1\n
		k2-v2\n
		k3- v3\n
		k4 -v4
		"""
		actual_dictionary = Model.DictionaryParser.parse_from_string(input)
		expected_dictionary = Model.Dictionary([
			[["k1"], ["v1"]],
			[["k2"], ["v2"]],
			[["k3"], ["v3"]],
			[["k4"], ["v4"]]]
		)
		self.assertEqual(expected_dictionary, actual_dictionary)

	def test_parse_one_to_many(self):
		input = """
		k1 - a1, a2, a3\n
		k2 - b1,b2,b3\n
		k3- c1
		"""
		actual_dictionary = Model.DictionaryParser.parse_from_string(input)
		expected_dictionary = Model.Dictionary([
			[["k1"], ["a1", "a2", "a3"]],
			[["k2"], ["b1", "b2", "b3"]],
			[["k3"], ["c1"]]]
		)
		self.assertEqual(expected_dictionary, actual_dictionary)

	def test_parse_many_to_many(self):
		input = """
		k1, k2 - a1, a2, a3\n
		"""
		actual_dictionary = Model.DictionaryParser.parse_from_string(input)
		expected_dictionary = Model.Dictionary([
			[["k1", "k2"], ["a1", "a2", "a3"]]]
		)
		self.assertEqual(expected_dictionary, actual_dictionary)
