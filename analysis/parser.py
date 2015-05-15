import pprint
import json

class CodeNest(object):
	
	def __init__(self, name, stars):
		self.name        = name
		self.stars       = stars
		self.result_set  = {}
		self.variance    = 0
		self.mean        = 0
		self.sample_size = 0
	
	def add_result(self, indent_level, count):
		self.result_set[indent_level] = count
	
	def calculate_mean(self):
		summed = 0
		for indent_level, count in self.result_set.iteritems():
			summed += count * indent_level

		self.mean = float(summed) / self.sample_size

	def calculate_variance(self):
		summed = 0
		for indent_level, count in self.result_set.iteritems():
			summed += count * (indent_level - self.mean) ** 2

		self.variance = float(summed) / self.sample_size



	def calculate_statistics(self):
		self.sample_size = reduce( (lambda x, y: x + y), self.result_set.values())

		self.calculate_mean()
		self.calculate_variance()
	
	def __repr__(self):
		return "Name: %s, Mean: %s, Variance: %s, Sample Size: %s" % \
			(self.name, self.mean, self.variance, self.sample_size)

# read the file one supposes
results = None
with open('results.json') as data:
	results = json.load(data)

for result in results:
	name        = result['name']
	stars       = result['stargazers_count']
	frequencies = result['frequency']
	nest = CodeNest(name, stars)
	for frequency in frequencies:
		nest.add_result(frequency['indent'], frequency['value'])

	nest.calculate_statistics()
	print nest
