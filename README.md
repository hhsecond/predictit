## Predictor
#### Using YAML file from CricSheet
##### Using only ODI now

## Formating of YAML file
dictionary with 3 keys
- Info : information about the game
- Meta : information about creation of file
- Innings : game details ( this is what we are interested in )

## Formating of data in tabular.txt
#### '==' is using as delimter
match_winner==ground winner==toss winner==Year==series_name==match_name==Team1==Team2==Ground==date==time==first batting==score==out==over==second batting==out==over==toss_winner==match_winner

Ex.
1==1==0==1988==west-indies-in-england==eng-vs-wi-2nd-odi-west-indies-in-england==ENGLAND==WEST INDIES==ENGLAND==May 21==01:00 AM  LOCAL==ENGLAND==186==8==55==WEST INDIES==139==10==46==WEST INDIES==ENGLAND==3==
0==0==1==1988==west-indies-in-england==eng-vs-wi-2nd-odi-west-indies-in-england==ENGLAND==WEST INDIES==ENGLAND==May 21==01:00 AM  LOCAL==ENGLAND==186==8==55==WEST INDIES==139==10==46==WEST INDIES==ENGLAND==3==

## records that i avoided
+ Records that has T20 and Test in the url
+ Records that has women, u19, XI in the team name
+ Matches that are abandoned or doesnot have winner name in toss result field
+ matches which stadium name i could not map with a country - almost 800 matches

## Important links to NLP
- https://github.com/nltk/nltk/wiki/Installing-Third-Party-Software
- https://www.quora.com/Could-anyone-give-me-an-example-of-using-Stanford-CoreNLP-sentiment-analysis-with-Python
- http://www.nltk.org/api/nltk.tag.html#module-nltk.tag.stanford
- https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
- www.cortical.io
- https://opennlp.apache.org/
- http://www.nltk.org/book/ch01.html
- https://pypi.python.org/pypi/corenlp-python
