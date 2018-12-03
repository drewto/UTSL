from itertools import zip_longest
import json
from progress.bar import Bar
from progress.counter import Counter
from process_tweets import preprocess, generate_stop_terms
import nltk
from nltk.corpus import stopwords

def generate_vocabulary(training_data, stopwords_file_name):
	# This function iterates through the training data and makes a
	# list of all of the words excluding stopwords
	stopwords_file = open(stopwords_file_name, "r")
	stopwords = {} # Create a dict to hold all of the unique values
	for stopword in stopwords_file:
		stopwords[stopword] = 0

	bar = Bar("Generating vocabulary...", max=len(training_data))
	vocabulary = {}
	for (tweet, rating) in training_data.items():
		words_in_line = tweet.split(" ")
		for word in words_in_line:
			if word not in stopwords:
				vocabulary[word.rstrip()] = 0
		bar.next()
	bar.finish()
	return sorted(vocabulary.keys())

def load_tweets():
	training_data_load_file = open("data_files/perceptron_traindata.json", "r")
	training_data = json.load(training_data_load_file)
	preprocessed_training_data = {}
	stop_terms = generate_stop_terms("config_files/preprocess_stop_terms.txt")
	counter = Counter("Loading tweets...")
	for (tweet, rating) in training_data.items():
		new_tweet = preprocess(tweet, stop_terms)
		new_tweet_text = " ".join(new_tweet)
		preprocessed_training_data[new_tweet_text] = rating
		counter.next()
	counter.finish()
	return preprocessed_training_data


def generate_features(fortune_text, vocabulary):
	words = fortune_text.split(" ")
	features = []
	for vocab in vocabulary:
		if vocab in words:
			features.append(1)
		else:
			features.append(0)
	return features

def generate_weight_vector(vocabulary, weights):
	weight_vector = {}
	i = 0
	for vocab in vocabulary:
		weight_vector[vocab] = weights[i]
		i += 1
	return weight_vector

def classify(weights, text, features):
	calculation = 0
	size = len(features)
	classification = 0
	for i in range(0, size):
		calculation += (features[i] * weights[i])
	if calculation > 0:
		classification = 1 # Future
	else:
		classification == 0 # Wise
	return classification

def compute_accuracy(weights, training_data, vocab):
	size = len(vocab)
	mistakes = 0
	item_count = 0
	for (text, label) in training_data.items():
		text = text.rstrip()
		features = generate_features(text, vocab)
		classification = classify(weights, text, features)
		if classification != label:
			mistakes += 1
		item_count += 1
	return 1 - (float(mistakes)/float(item_count))

def standard_perceptron(vocab, training_data):
	training_iterations = 20
	learning_rate = 1
	size = len(vocab)
	weights = [0] * size
	mistakes_per_iteration = []
	training_accuracy_per_iteration = []
	testing_accuracy_per_iteration = []	
	bar = Bar("Computing standard perceptron on training data...", max=training_iterations, suffix = '%(percent).1f%% - %(eta)ds') 
	for x in range(0,training_iterations):
		mistakes = 0
		for text,label in training_data.items():
			text = text.rstrip()
			features = generate_features(text, vocab)
			classification = classify(weights, text, features)
			
			y = 0
			if label == 0:
				y = -1
			if label == 1:
				y = 1

			if label != classification:
				# Mistake was made, update weights
				mistakes += 1
				for i in range(0, size):
					weights[i] += learning_rate * y * features[i]
		bar.next()
		mistakes_per_iteration.append(mistakes)
		training_accuracy_per_iteration.append(compute_accuracy(weights, training_data, vocab))
	bar.finish()
	outfile = open("data_files/perceptron_analysis.csv", "w+")
	outfile.write("iteration,mistake_count,training_accuracy,testing_accuracy\n")
	for x in range(0,training_iterations):
		#print("Iteration: " + str(x+1))
		#print("   Training accuracy: " + str(int(training_accuracy_per_iteration[x] * 100)) + "%")
		#print("   # of mistakes: " + str(mistakes_per_iteration[x]))
		outstr = str(x+1)+","+str(mistakes_per_iteration[x])+","+str(int(training_accuracy_per_iteration[x] * 100)) + "%\n"
		outfile.write(outstr)
	print(weights)
	weight_vector = generate_weight_vector(vocab, weights)
	weights_file = open("data_files/perceptron_weights.json", "w+")
	weights_file.write(json.dumps(weight_vector))



def main():
	training_data = load_tweets()
	vocabulary = generate_vocabulary(training_data, "config_files/perceptron_stop_list.txt")
	standard_perceptron(vocabulary, training_data)

if __name__ == "__main__":
	main()