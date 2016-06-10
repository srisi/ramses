'''
From http://stackoverflow.com/questions/8870261/how-to-split-text-without-spaces-into-list-of-words
I still don't understand how this works...
It somehow first works forward through the string to create the cost function
And then backwards to create the actual string.
Really weird but extremely efficient.

'''

from math import log

# Build a cost dictionary, assuming Zipf's law and cost = -math.log(probability).
words = open("words-by-frequency.txt").read().split()
wordcost = dict((k, log((i+1)*log(len(words)))) for i,k in enumerate(words))
maxword = max(len(x) for x in words)

def infer_spaces(s):
    """Uses dynamic programming to infer the location of spaces in a string
    without spaces."""

    # Find the best match for the i first characters, assuming cost has
    # been built for the i-1 first characters.
    # Returns a pair (match_cost, match_length).
    def best_match(i):

        candidates = enumerate(reversed(cost[max(0, i - maxword):i]))
        print "candidates", [c for c in candidates]

        candidates = enumerate(reversed(cost[max(0, i - maxword):i]))
        print "wordcost", [
            (c + wordcost.get(s[i - k - 1:i], 9e999), k + 1, wordcost.get(s[i - k - 1:i], 9e999), s[i - k - 1:i]) for
            k, c in candidates]

        candidates = enumerate(reversed(cost[max(0, i-maxword):i]))
        return min((c + wordcost.get(s[i-k-1:i], 9e999), k+1) for k,c in candidates)

    # Build the cost array.
    cost = [0]
    for i in range(1,len(s)+1):
        c,k = best_match(i)
        print "best match: {}, {} \n".format(c, k)
        cost.append(c)

    print "cost: {} \n\n".format(cost)

    # Backtrack to recover the minimal-cost string.
    out = []
    i = len(s)
    while i>0:
        c,k = best_match(i)
        assert c == cost[i]
        out.append(s[i-k:i])

        print c, k, s[i-k:i]
        print
        i -= k

    return " ".join(reversed(out))

if __name__ == "__main__":

    s = 'theis'

    print infer_spaces(s)