import os, threading, time, logging, sys
import numpy as np
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

#remove after use
player_name = []
filecount = 0

path = 'ODI.yaml/'
info_keys = {'match_type', 'outcome', 'dates', 'overs', 'gender',
	'toss', 'player_of_match', 'venue', 'teams'}


features = np.array()

def file_process(path, self):
	#remove after need
	global player_name

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
		dates = info['dates'][0]
		gender = info['gender']
		team1 = info['teams'][0]
		team2 = info['teams'][1]
		toss_winner = info['toss']['winner']
		toss_decision = info['toss']['decision']
		try:
			outcome = info['outcome']['by']
		except KeyError:
			outcome = ''
		venue = info['venue']
		try:
			player_of_match = ' '.join(info['player_of_match'])
		except KeyError:
			player_of_match = ''
		print(self.count, dates)

		if gender.strip() == 'male':
			#assertion for innings
			try:
				assert len(innings) == 2, 'two innings per match'
				assert isinstance(innings, list), 'innings is not a list'
				#TODO
			except AssertionError as e:
				loge('AssertionError - innings part: ' + path + ' ' + str(e))
			for key in innings:
				assert len(key) == 1, 'each innings is single dictionary'
				each_innings, top_details = key.popitem()

				team = top_details['team']
				deliveries = top_details['deliveries']
				
				for delivery in deliveries:
					ball, details = delivery.popitem()
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
					if extras:
						extras_type = list(details.pop('extras'))[0]
					else:
						extras_type = ''
					runbybatsman = runs.pop('batsman')
					total_per_ball = runs.pop('total')


					detail_dict = {
						'team: ', team,
						'bowler: ', bowler,
						'batsman: ', batsman,
						'non_striker: ', non_striker,
						'extras: ', extras,
						'runbybatsman: ', runbybatsman,
						'total_per_ball: ', total_per_ball,
						'wicketperson: ', wicketperson,
						'wickettype: ', wickettype,
						'extras_type: ', extras_type
						}
					player_name.append(bowler)
					player_name.append(batsman)
					player_name = list(set(player_name))
		else:
			logi('Female game: ' + str(dates) + ' ' + team1 + team2 +gender)




class process(threading.Thread):
	"""Class process each file saperatly in a thread"""
	def __init__(self, path):
		threading.Thread.__init__(self)
		self.path = path

	def run(self):
		global filecount
		filecount += 1
		self.count = filecount
		logd('Next Tread')
		file_process(self.path, self)
		
count = 0
for file in os.listdir(path):
	count += 1
	process(path+file).start()
	if not count%5:
		logd('waiting for reducing the load')
		logi('Number of threads: ' + str(threading.active_count()))
		time.sleep(2)
while (threading.active_count() - 1):
	time.sleep(10)
for val in player_name:
	print(val)