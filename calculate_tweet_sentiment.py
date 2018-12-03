import json
import operator
from progress.bar import Bar

def file_len(fname):
	with open(fname) as f:
		for i, l in enumerate(f):
			pass
	return i + 1

def main():
	term_frequencies_filename = "data_files/term_semantic_orientation.txt"
	tweets_file_filename = "data_files/scraped_tweets.json"
	sentiment_tweets_output_filename = "data_files/tweets_with_sentiment.json"
	term_frequencies = open(term_frequencies_filename, "r")
	term_sentiments = {}
	for line in term_frequencies:
		words = line.split(" ")
		term_sentiments[words[0]] = float(words[1])
	tweet_count = file_len(tweets_file_filename)
	bar = Bar("Determining sentiment for each tweet...", max=tweet_count)
	tweets_file = open(tweets_file_filename, "r")
	output_file = open(sentiment_tweets_output_filename, "w+")
	tweet_sentiment = {}
	overall_sentiment = 0
	for line in tweets_file:
		tweet = json.loads(line)
		text = tweet['text'].split(" ")
		sentiment = 0
		for word in text:
			if word in term_sentiments:
				sentiment += term_sentiments[word]
		overall_sentiment += sentiment
		tweet['sentiment'] = sentiment
		output_file.write(json.dumps(tweet)+'\n')
		tweet_sentiment[tweet['text']] = sentiment
		bar.next()
	bar.finish()
	tweet_sentiment_sorted = sorted(tweet_sentiment.items(),key=operator.itemgetter(1), reverse=True)
	top_pos = tweet_sentiment_sorted[:5]
	top_neg = tweet_sentiment_sorted[-5:]
	top_neg.reverse()
	
	pos_tweet_count = 0
	neg_tweet_count = 0
	sorted_sentiments_file = open("data_files/tweet_texted_sorted_by_sentiment.txt","w+")
	for item in tweet_sentiment_sorted:
		(tweet, rating) = item
		if rating > 1:
			pos_tweet_count += 1
		if rating < -1:
			neg_tweet_count += 1
		new_text = []
		for word in tweet.split(" "):
			if word == '&gt;':
				new_text.append(">")
			if word == '&amp;':
				new_text.append("&")
			if word == '&lt;':
				new_text.append("<")
			else:
				new_text.append(word)
		tweet = " ".join(new_text)
		sorted_sentiments_file.write(str(rating) + ": " + tweet + '\n\n\n')
	print("The overall sentiment regarding your search terms is: " + str(overall_sentiment))
	sorted_sentiments_file.close()

	f_data = open("data_files/perceptron_traindata.json", "w+")
	(pos_tweet, pos_rating) = tweet_sentiment_sorted[0]
	(neg_tweet, neg_rating) = tweet_sentiment_sorted[-1]
	pos_threshold = 1
	neg_threshold = -1
	perceptron_data = {}
	for (tweet,rating) in tweet_sentiment_sorted:
		if rating > pos_threshold:
			perceptron_data[tweet] = 1
		if rating < neg_threshold:
			perceptron_data[tweet] = 0
	f_data.write(json.dumps(perceptron_data))
	f_data.close()

if __name__ == "__main__":
	main()