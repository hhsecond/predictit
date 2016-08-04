## Predictor


How to use the fetch_data_script:

There are some issues with the lxml installation but other than that all other installations in virtualenv should be fine

This was done using python2.7

### Setup the environment in ubuntu

Install PYTHON3:
sudo apt-get install python-software-properties
sudo add-apt-repository ppa:fkrull/deadsnakes
sudo apt-get update
sudo apt-get install python3.5

get pip:
wget https://bootstrap.pypa.io/get-pip.py
sudo python3.5 get-pip.py

setup virtual env:
sudo apt-get install python-dev libxml2-dev libxslt1-dev zlib1g-dev libffi-dev libssl-dev
virtualenv -p python3.5 py3_venv
source py3_venv/bin/activate
pip install Scrapy
scrapy docs can be found here
http://doc.scrapy.org/en/latest/intro/install.html

installing dependencies
pip install -r fetching_data_scripts/requirements.txt

##Formating of data in tabular.txt
#### '==' is using as delimter
match_winner==ground winner==toss winner==Year==series_name==match_name==Team1==Team2==Ground==date==time==first batting==score==out==over==second batting==out==over==toss_winner==match_winner

Ex.
1==1==0==1988==west-indies-in-england==eng-vs-wi-2nd-odi-west-indies-in-england==ENGLAND==WEST INDIES==ENGLAND==May 21==01:00 AM  LOCAL==ENGLAND==186==8==55==WEST INDIES==139==10==46==WEST INDIES==ENGLAND==3==
0==0==1==1988==west-indies-in-england==eng-vs-wi-2nd-odi-west-indies-in-england==ENGLAND==WEST INDIES==ENGLAND==May 21==01:00 AM  LOCAL==ENGLAND==186==8==55==WEST INDIES==139==10==46==WEST INDIES==ENGLAND==3==

##records that i avoided
+ Records that has T20 and Test in the url
+ Records that has women, u19, XI in the team name
+ Matches that are abondoned or doesnot have winner name in toss result field
+ matches which stadium name i could not map with a country - almost 800 matches

##Important links to NLP
- https://github.com/nltk/nltk/wiki/Installing-Third-Party-Software
- https://www.quora.com/Could-anyone-give-me-an-example-of-using-Stanford-CoreNLP-sentiment-analysis-with-Python
- http://www.nltk.org/api/nltk.tag.html#module-nltk.tag.stanford
- https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
- www.cortical.io
- https://opennlp.apache.org/
- http://www.nltk.org/book/ch01.html
- https://pypi.python.org/pypi/corenlp-python
