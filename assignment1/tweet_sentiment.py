import sys
import json


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
    target_file = open('tweet_sentiment_output.txt', 'w')
    for line in f:
        tweet = json.loads(line)
        if 'text' in tweet:
            score = score_tweet_text(tweet['text'], sentiment_scores)
            target_file.write('{}\n'.format(score))
        else:
            score = 0
            target_file.write('{}\n'.format(score))


def main():
    sentiment_file = open(sys.argv[1], 'r')
    twittersteam_file = open(sys.argv[2], 'r')
    sentiment_scores = process_sentiment_file(sentiment_file)
    process_twittersteam_file(twittersteam_file, sentiment_scores)


if __name__ == '__main__':
    main()
