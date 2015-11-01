import sys
import json
import geocoder
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
    d = defaultdict(list)
    for line in f:
        tweet = json.loads(line)
        # check if tweet meets our criteria
        if ('text' in tweet
        and 'coordinates' in tweet
        and tweet['coordinates']):
            # get geo
            lng = tweet['coordinates']['coordinates'][0]
            lat = tweet['coordinates']['coordinates'][1]
            g = geocoder.google([lat, lng], method='reverse')
            if g.country == 'US':
                # add to dict
                score = score_tweet_text(tweet['text'], sentiment_scores)
                d[g.state].append(score)

    return d


def get_state_averages(scores):
    d = defaultdict(float)
    for k, v in scores.items():
        d[k] = sum(v) / float(len(v))

    return d


def print_highest_average(averages):
    sort = sorted(averages.items(), key=lambda kv: kv[1], reverse=True)
    # print state score
    print sort[0][0], sort[0][1]


def main():
    sentiment_file = open(sys.argv[1], 'r')
    twittersteam_file = open(sys.argv[2], 'r')
    sentiment_scores = process_sentiment_file(sentiment_file)
    state_scores = process_twittersteam_file(
        twittersteam_file, sentiment_scores
    )
    state_score_averages = get_state_averages(state_scores)
    print_highest_average(state_score_averages)


if __name__ == '__main__':
    main()
