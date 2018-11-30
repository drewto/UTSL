import re
import json
from progress.bar import Bar

emoticons_str = r"""
	(?:
		[:=;] # Eyes
		[oO\-]? # Nose (optional)
		[D\)\]\(\]/\\OpP] # Mouth
	)"""
 
regex_str = [
	emoticons_str,
	r'<[^>]+>', # HTML tags
	r'(?:@[\w_]+)', # @-mentions
	r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
	r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
 
	r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
	r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
	r'(?:[\w_]+)', # other words
	r'(?:\S)' # anything else
]
	
tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)
 
def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def tokenize(s):
	return tokens_re.findall(s)
 
def find_url(string): 
    # findall() has been used  
    # with valid conditions for urls in string 
    url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+] |[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', string) 
    return url 

def preprocess(s, lowercase=False):
	tokens = tokenize(s)
	if lowercase:
		tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
	
	# Now that we have the tokens, lets do what we want with it all
	
	# First, remove all of the stop terms (tokenized items we do not want)
	f = open("preprocess_stop_terms.txt", "r")
	stop_terms = []
	for line in f:
		stop_terms.append(line.rstrip())
	for term in stop_terms:
		term_in_tokens = 1
		while(term_in_tokens == 1):
			if term in tokens:
				tokens.remove(term)
			else:
				term_in_tokens = 0

	# Remove the URLs
	url_in_tokens = 1
	while url_in_tokens == 1:
		url_in_tokens = 0
		for token in tokens:
			if len(find_url(token)) > 0:
				tokens.remove(token)
				url_in_tokens = 1

	# Remove mentions 
	mention_in_tokens = 1
	while mention_in_tokens == 1:
		mention_in_tokens = 0
		for token in tokens:
			if token[0] == '@':
				tokens.remove(token)
				mention_in_tokens = 1

	for i in range(len(tokens)):
		if tokens[i][0] == '#':
			tokens[i] = tokens[i][1:]

	return tokens
 	


def main():
	file_length = file_len("scraped_tweets.json")
	file = open("scraped_tweets.json", "r")
	bar = Bar('Pre-processing tweets...', max=file_length)
	outfile = open("preprocessed_tweets.json", "w")
	for tweet in file:
		tweet_data = json.loads(tweet)
		text = tweet_data['text']
		new_text = preprocess(text)
		tweet_data['text'] = " ".join(new_text)
		outfile.write(json.dumps(tweet_data))
		bar.next()

	bar.finish()

if __name__ == '__main__':
	main()