import re
import math

def call_gearcalc(self, e):
	calculator = GearCalc(e.input)
	e.output = e.nick + ', ' + calculator.solve()
	return e
call_gearcalc.command = "!gearcalc"

class GearCalc:

	default_wheel_circumference = 2098
	mps_to_mph = 2.23694
	mps_to_kph = 3.6
	mps_constant = 0.000016674592
	mph_to_mps = 0.44704
	kph_to_mps = 0.27778
	parameter_meta_data = {
		'cadence': {
			'name': 'Cadence',
			'examples': ['90rpm']
		},
		'speed': {
			'name': 'Speed',
			'examples': ['20mph', '32kph', '9mps']
		},
		'front_teeth': {
			'name': 'Chainring Size',
			'examples': ['53x11', '50x?']
		},
		'rear_teeth': {
			'name': 'Cog Size',
			'examples': ['53x11', '?x11']
		}
	}

	def __init__(self, calc_string):
		self.tokens = self.tokenize(calc_string)
		self.cadence = self.findCadence()
		self.speed = self.findSpeed();
		self.front_teeth = self.findFrontTeeth()
		self.rear_teeth = self.findRearTeeth()
		self.wheel_circumference = self.findErto()
		self.metric = self.findMetric()

	def getParameterMetaData(self, parameter, dataType):
		return self.parameter_meta_data[parameter][dataType]

	def getListMetaDataFromParameters(self, parameters, dataType):
		return_list = []
		for parameter in parameters:
			value = self.getParameterMetaData(parameter, dataType)
			if value is not None:
				if type(value) is list:
					for item in value:
						return_list.append(item)
				else:
					return_list.append(value)
		return return_list

	def tokenize (self, calc_string):
		return re.split('\s', calc_string)

	def solve (self):
		if self.isAlreadySolved():
			return "You already know your answer, think about it."
		elif self.isSolvable():
			solution_parameter = self.findMissingParameter()
			if solution_parameter == 'cadence':
				return self.solveCadence()
			elif solution_parameter == 'speed':
				return self.solveSpeed()
			elif solution_parameter == 'front_teeth':
				return self.solveFrontTeeth()
			elif solution_parameter == 'rear_teeth':
				return self.solveRearTeeth()
			else:
				return "Sorry I can't yet solve for " + self.getParameterMetaData(solution_parameter, 'name')
		else:
			return "I need more information try some of the following: " + ', '.join(str(v) for v in self.getListMetaDataFromParameters(self.findMissingParameters(), 'name')) + " Eg.) " + ', '.join(str(v) for v in self.getListMetaDataFromParameters(self.findMissingParameters(), 'examples'))

	def solveCadence (self):
		try:
			return str(round(self.speed / (self.mps_constant * self.wheel_circumference * self.solveGearRatio()), 1)) + ' rpm'
		except ZeroDivisionError:
			return "nice try, trying to divide by zero are you?"

	def solveSpeed (self):
		mps = (self.mps_constant * self.wheel_circumference * self.solveGearRatio() * self.cadence);
		if self.metric: 
			return str(round(mps * self.mps_to_kph, 1)) + ' kph';
		else:
			return str(round(mps * self.mps_to_mph, 1)) + ' mph';

	def solveFrontTeeth (self):
		try:
			return str(int(round(((self.speed / (self.mps_constant * self.wheel_circumference * self.cadence)) * (self.rear_teeth))))) + ' tooth chainring'
		except ZeroDivisionError:
			return "nice try, trying to divide by zero are you?"


	def solveRearTeeth (self):
		try:
			return str(int(round((self.mps_constant * self.wheel_circumference * self.cadence * self.front_teeth) / (self.speed)))) + ' tooth cog'
		except ZeroDivisionError:
			return "nice try, trying to divide by zero are you?"

	def solveGearRatio (self):
		try:
			return self.front_teeth / self.rear_teeth
		except ZeroDivisionError:
			return "nice try, trying to divide by zero are you?"

	def isSolvable(self):
		missing_parameters = self.findMissingParameters()
		if len(missing_parameters) == 1:
			return True
		else:
			return False

	def isAlreadySolved(self):
		missing_parameters = self.findMissingParameters()
		if len(missing_parameters) == 0:
			return True
		else:
			return False

	def findMissingParameter(self):
		missing_parameters = self.findMissingParameters()
		if missing_parameters:
			return missing_parameters.pop(0)

	def findMissingParameters(self):
		missing_parameters = []
		object_values = vars(self)
		for key in object_values:
			if object_values[key] is None and key != 'metric':
				missing_parameters.append(key)
		return missing_parameters


	def findCadence(self):
		for token in self.tokens:
			m = re.match(r"^(\d+)rpm$", token)
			if m:
				return int(m.group(1))

	def findSpeed(self ):
		for token in self.tokens:
			m = re.match(r"^([\d.]+)mph$", token)
			if m:
				return float(m.group(1)) * self.mph_to_mps
			m = re.match(r"^([\d.]+)kph$", token)
			if m:
				return float(m.group(1)) * self.kph_to_mps
			m = re.match(r"^([\d.]+)mps$", token)
			if m:
				return float(m.group(1))

	def findFrontTeeth(self):
		for token in self.tokens:
			m = re.match(r"^([\d\?]+)x[\d\?]+$", token)
			if m:
				if m.group(1) != '?':
					return int(m.group(1))

	def findRearTeeth(self):
		for token in self.tokens:
			m = re.match(r"^[\d\?]+x([\d\?]+)$", token)
			if m:
				if m.group(1) != '?':
					return int(m.group(1))

	def findMetric(self):
		for token in self.tokens:
			m = re.match(r"^metric$", token)
			if m:
				return True

	def findErto(self):
		for token in self.tokens:
			m = re.match(r"^(\d{2})-(\d{3})$", token)
			if m:
				return self.calculateErtro(int(m.group(1)), int(m.group(2)))
		return self.default_wheel_circumference

	def calculateErtro(self, tire_width, rim_diameter):
		return int(round(float(rim_diameter + (tire_width * 2)) * math.pi))
