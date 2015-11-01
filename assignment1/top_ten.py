import sys
import json
from collections import defaultdict


def process_sentiment_file(f):
    sentiment_scores = {}
    for line in f:
        term, score = line.split('\t')
        sentiment_scores[term] = int(score)

    return sentiment_scores


def score_tweet_text(text, sentiment_scores):
    score = 0
    for word in text.split():
        word = word.lower()
        if word in sentiment_scores:
            score += sentiment_scores[word]

    return score


def process_twittersteam_file(f, sentiment_scores):
    d = defaultdict(int)
    for line in f:
        tweet = json.loads(line)
        # check if tweet meets our criteria
        if ('entities' in tweet
        and tweet['entities']['hashtags']):
            for hashtag in tweet['entities']['hashtags']:
                d[hashtag['text']] += 1

    return d


def print_counts_descending(d):
    sort = sorted(d.items(), key=lambda kv: kv[1], reverse=True)
    for item in sort:
        print item[0], item[1]


def main():
    sentiment_file = open(sys.argv[1], 'r')
    twittersteam_file = open(sys.argv[2], 'r')
    sentiment_scores = process_sentiment_file(sentiment_file)
    hashtag_scores = process_twittersteam_file(
        twittersteam_file, sentiment_scores
    )
    print_counts_descending(hashtag_scores)


if __name__ == '__main__':
    main()
