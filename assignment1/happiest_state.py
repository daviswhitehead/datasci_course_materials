import sys
import json
import geocoder

"""
g = geocoder.google([45.15, -75.14], method='reverse')
>>> g.state
"""


def states_dict():
    states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
    }
    return states


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
