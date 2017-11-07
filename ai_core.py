import numpy
import pickle
from pybrain3.datasets import SupervisedDataSet, UnsupervisedDataSet
from pybrain3.structure import LinearLayer
from pybrain3.supervised.trainers import BackpropTrainer
from pybrain3.tools.shortcuts import buildNetwork


class Tools:
	# region Constants
	# Weekdays
	SUN = 0b1000000
	MON = 0b0100000
	TUE = 0b0010000
	WED = 0b0001000
	THU = 0b1000100
	FRI = 0b1000010
	SAT = 0b1000001
	ANY = 0b1111111
	NEV = 0b0000000

	# Map of categories with ids
	cat_map = [
		{'name': 'default', 'code': 0, 'time': 8, 'day': ANY},
		{'name': 'morning', 'code': 1, 'time': 7, 'day': ANY},
		{'name': 'hiking', 'code': 2, 'time': 9, 'day': ANY ^ SUN},
		{'name': 'game', 'code': 3, 'time': 14, 'day': SAT | SUN},
		{'name': 'movie', 'code': 4, 'time': 20, 'day': THU | FRI | SAT},
		{'name': 'club', 'code': 5, 'time': 22, 'day': FRI | SAT | SUN},
	]

	# endregion

	@staticmethod
	def objdump(dmp_obj, dmp_filename):
		dump = open(dmp_filename, 'wb')
		pickle.dump(dmp_obj, dump)
		dump.close()

	@staticmethod
	def objrecv(dmp_filename):
		dump = open(dmp_filename, 'rb')
		dmp_obj = pickle.load(dump)
		dump.close()
		return dmp_obj


class CategoryAdvisor:
	# region Notes on using this class
	# In order to use dataset, history must contain >2*OBSERVE_LENGTH (which is >20)
	# endregion

	# region Constants
	NETWORK_FILENAME = 'networkdump.txt'
	DATASET_FILENAME = 'datasetdump.txt'

	OBSERVE_LENGTH = 5
	PREDICT_LENGTH = 1

	# endregion

	# region Variables
	bprnetw = None
	dataset = None

	# endregion

	@staticmethod
	def create(network, dataset):
		res = CategoryAdvisor()

		if network is None:
			res.bprnetw = buildNetwork(CategoryAdvisor.OBSERVE_LENGTH, 20, CategoryAdvisor.PREDICT_LENGTH, outclass=LinearLayer, bias=True, recurrent=True)
		else:
			res.bprnetw = network

		if dataset is None:
			res.dataset = SupervisedDataSet(CategoryAdvisor.OBSERVE_LENGTH, CategoryAdvisor.PREDICT_LENGTH)
		else:
			res.dataset = dataset

		return res

	def retrain_complete(self, history_complete):
		if len(history_complete) >= CategoryAdvisor.OBSERVE_LENGTH:
			self.dataset.clear()

			data_length = len(history_complete)

			for n in range(data_length):
				if n + (CategoryAdvisor.OBSERVE_LENGTH - 1) + CategoryAdvisor.PREDICT_LENGTH < data_length:
					self.dataset.addSample(history_complete[n:n + CategoryAdvisor.OBSERVE_LENGTH], history_complete[n + 1:n + 1 + CategoryAdvisor.PREDICT_LENGTH])

			trainer = BackpropTrainer(self.bprnetw, self.dataset)
			trainer.trainEpochs(100)

			return True
		else:
			return False

	def retrain_single(self, value):
		inp = numpy.append(self.dataset['input'][-1][1:], self.dataset['target'][-1])
		self.dataset.addSample(inp, [value])

		trainer = BackpropTrainer(self.bprnetw, self.dataset)
		trainer.trainEpochs(100)

	def calculate(self):
		ts = UnsupervisedDataSet(CategoryAdvisor.OBSERVE_LENGTH, )
		ts.addSample(self.dataset['input'][-1])
		return int(self.bprnetw.activateOnDataset(ts)[0][0])


advisors = {}


def ai_predict_time(username, category_id):
	category = None
	for _ctg in Tools.cat_map:
		if _ctg['code'] == category_id:
			category = _ctg
			break
	if category is None or username is None or username is '':
		return -1

	time = 0
	# TODO: Use CategoryAdvisor for each category, run threads on training. Calculate next value and return
	return time
