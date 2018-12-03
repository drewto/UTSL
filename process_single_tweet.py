import sys
from perceptron import generate_features, classify, compute_accuracy, standard_perceptron
from process_tweets import preprocess, generate_stop_terms
import json

def main():
	tweet = sys.argv[1]
	preprocess_stop_terms_filename = "config_files/preprocess_stop_terms.txt"
	stop_terms = generate_stop_terms(preprocess_stop_terms_filename)
	preprocessed_tweet = preprocess(tweet, stop_terms)
	f = open("data_files/perceptron_weights.json")
	a = f.readlines()[0]
	vocab = json.loads(a)
	#self.vocab = json.load("data_files/perceptron_weights.json")
	weights = []
	for (term, weight) in vocab.items():
		weights.append(weight)
	features = generate_features(" ".join(preprocessed_tweet), vocab)
	classification = classify(weights, " ".join(preprocessed_tweet), features)
	print(classification)


if __name__ == '__main__':
	main()