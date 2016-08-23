import os, threading, time, logging, sys
from yaml import load, dump

flog = open('data_from_yaml.log', 'w+')
root = logging.getLogger('Root')
root.setLevel(logging.INFO)
lhandler = logging.StreamHandler(flog)
#lhandler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s [%(levelname)s] : %(message)s',
	'%Y-%m-%d %H:%M:%S')
lhandler.setFormatter(formatter)
root.addHandler(lhandler)
logd = root.debug
logi = root.info
logw = root.warning
logc = root.critical
loge = root.error




path = 'ODI.yaml/'
info_keys = {'match_type', 'outcome', 'dates', 'overs', 'gender',
	'toss', 'player_of_match', 'venue', 'teams'}

def file_process(path):
	logd('opening' + path)
	with open(path) as f:
		yaml_out = load(f)
		info = yaml_out['info']
		innings = yaml_out['innings']

		
		#assertions for the whole file
		try:
			assert len(yaml_out) == 3, 'yaml file basically have 3'\
			 'values in the dictionary'
			assert isinstance(info, dict), 'info returns dictionary'
			assert isinstance(innings, list)
		except AssertionError:
			loge('AssertionError - whole file part: ' + path)

		#assertion for info
		try:
			dont_have_value = info_keys - set(info.keys()).intersection(info_keys)
			if dont_have_value:
				logw(path + ' doesnt have ' + str(dont_have_value))
		except AssertionError:
			loge('AssertionError - info part: ' + path)


		#assertion for innings
		try:
			assert len(innings) == 2, 'two innings per match'
			assert isinstance(innings, list)
			#TODO
		except AssertionError:
			loge('AssertionError - innings part: ' + path)
		for key in innings:
			assert len(key) == 1, 'each innings is single dictionary'
			each_innings, top_details = key.popitem()
			print(each_innings)

			team = top_details['team']
			deliveries = top_details['deliveries']
			
			for delivery in deliveries:
				ball, details = delivery.popitem()
				print(ball)

				assert len(details) < 6, 'bowler, batsman, nonstriker, runs and wicket'
				bowler = details.pop('bowler')
				batsman = details.pop('batsman')
				non_striker = details.pop('non_striker')
				runs = details.pop('runs')
				try:
					wicket = details.pop('wicket')
					wickettype = wicket.pop('kind')
					wicketperson = wicket.pop('player_out')
				except KeyError:
					wickettype = ''
					wicketperson = ''
				extras = runs.pop('extras')
				runbybat = runs.pop('batsman')
				total_per_ball = runs.pop('total')

				print(
					'team: ', team,
					'bowler: ', bowler,
					'batsman: ', batsman,
					'non_striker: ', non_striker,
					'extras: ', extras,
					'runbybat: ', runbybat,
					'total_per_ball: ', total_per_ball,
					'wicketperson: ', wicketperson,
					'wickettype: ', wickettype
					)
				print('\n\n')




class process(threading.Thread):
	"""Class process each file saperatly in a thread"""
	def __init__(self, path):
		threading.Thread.__init__(self)
		self.path = path

	def run(self):
		logd('Next Tread')
		file_process(self.path)
		
count = 0
for file in os.listdir(path):
	count += 1
	process(path+file).start()
	if not count%5:
		logd('waiting for reducing the load')
		logi('Number of threads: ' + str(threading.active_count()))
		time.sleep(1)
