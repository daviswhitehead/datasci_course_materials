import sys
import json


def process_sentiment_file(f):
    sentiment_scores = {}
    for line in f:
        term, score = line.split('\t')
        sentiment_scores[term] = int(score)

    return sentiment_scores


def score_tweet_text(text, sentiment_scores):
    d = {}
    score = 0
    for word in text.split():
        word = word.lower()
        if word in sentiment_scores:
            score += sentiment_scores[word]
        else:
            d[word] = 0
    for word in d:
        d[word] = score

    return score, d


def process_twittersteam_file(f, sentiment_scores):
    non_sentiment_words = {}
    for line in f:
        tweet = json.loads(line)
        if 'text' in tweet:
            score, d = score_tweet_text(tweet['text'], sentiment_scores)
            for word in d:
                if word in non_sentiment_words:
                    non_sentiment_words[word].append(d[word])
                else:
                    non_sentiment_words[word] = [d[word], ]

    return non_sentiment_words


def score_non_sentiment_words(non_sentiment_words):
    for word in non_sentiment_words:
        l = non_sentiment_words[word]
        scores = []
        for score in l:
            # remove messages without a score
            if score != 0:
                scores.append(score)
        try:
            avg_score = sum(scores) / float(len(scores))
        # if there are no relevant scores, then the avg_score is set to zero
        except ZeroDivisionError:
            avg_score = 0

        print word, avg_score


def main():
    sentiment_file = open(sys.argv[1], 'r')
    twittersteam_file = open(sys.argv[2], 'r')
    sentiment_scores = process_sentiment_file(sentiment_file)
    non_sentiment_words = process_twittersteam_file(twittersteam_file, sentiment_scores)
    score_non_sentiment_words(non_sentiment_words)


if __name__ == '__main__':
    main()
