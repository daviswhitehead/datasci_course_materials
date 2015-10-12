import sys
import json


def process_twittersteam_file(f):
    d = {}
    total = 0
    for line in f:
        tweet = json.loads(line)
        if 'text' in tweet:
            words = tweet['text'].split()
            for word in words:
                if word in d:
                    d[word] += 1
                    total += 1
                else:
                    d[word] = 1
                    total += 1

    return d, total


def print_word_frequencies(frequencies, total):
    for word in frequencies:
        print word, float(frequencies[word]) / float(total)


def main():
    twittersteam_file = open(sys.argv[1], 'r')
    frequencies, total = process_twittersteam_file(twittersteam_file)
    print_word_frequencies(frequencies, total)


if __name__ == '__main__':
    main()
