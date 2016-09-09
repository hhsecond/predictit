import os, threading, time, logging, sys, datalist
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

filecount = 0

path = 'ODI.yaml/'
info_keys = {'match_type', 'outcome', 'dates', 'overs', 'gender',
	'toss', 'player_of_match', 'venue', 'teams'}

lock = threading.Lock()
features = np.empty((0,12))


def file_process(path, self):
	global features
	featurelist = []

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
			winner = info['outcome']['winner']
		except KeyError as e:
			print('exception: ', e)
			exit()
		venue = info['venue']
		try:
			player_of_match = ' '.join(info['player_of_match'])
		except KeyError:
			player_of_match = ''
		print(self.count, dates, path)


		if gender.strip() == 'male':
			host_country = datalist.venue_list[venue]
			featurelist = [path.split('/')[1], dates, team1, team2, host_country, toss_winner, toss_decision, winner]

			#assertion for innings
			try:
				assert len(innings) == 2, 'two innings per match'
				assert isinstance(innings, list), 'innings is not a list'
				#TODO
			except AssertionError as e:
				loge('AssertionError - innings part: ' + path + ' ' + str(e))
			for key in innings:
				total_score = 0
				total_wickets = 0
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
					total_score += total_per_ball

					if wickettype:
						total_wickets += 1
				
				if team == team1:
					team1score = total_score
					team1wickets = total_wickets
				elif team == team2:
					team2score = total_score
					team2wickets = total_wickets
				else:
					raise("team names are not matched: " + path)

			featurelist.append(team1score)
			featurelist.append(team2score)
			featurelist.append(team1wickets)
			featurelist.append(team2wickets)

			features = np.append(features, [featurelist], axis=0)
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
	if not count%2:
		logd('waiting for reducing the load')
		logi('Number of threads: ' + str(threading.active_count()))
		time.sleep(1)
while (threading.active_count() - 1):
	time.sleep(10)


np.save('features.npy', features)

