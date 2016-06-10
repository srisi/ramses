from math import log

# Build a cost dictionary, assuming Zipf's law and cost = -math.log(probability).
words = open("words-by-frequency.txt").read().split()
wordcost = dict((word, log((index+1)*log(len(words)))) for index, word in enumerate(words))
#maxword = max(len(x) for x in words)

# max word is longest word allowed
maxword = 10

print wordcost['a']
print wordcost.get('a', 9e999)
#print wordcost

def infer_spaces(s):
    """Uses dynamic programming to infer the location of spaces in a string
    without spaces."""

    # Find the best match for the i first characters, assuming cost has
    # been built for the i-1 first characters.
    # Returns a pair (match_cost, match_length).
    def best_match(i):

        '''
        cost is a list with initial entry [0].
        i = 1
        cost[max(0, i-maxword):i] = cost[max(0, 1-10): 1] = cost[0]
        enumerate -> idx and value

        if we're at position 20, we do not need to consider characters before position 10.
        '''

        candidates = enumerate(reversed(cost[max(0, i-maxword):i]))

        print "candidates", [k for k in candidates]



        candidates = enumerate(reversed(cost[max(0, i - maxword):i]))
        print "wordcost", [(c + wordcost.get(s[i - k - 1:i], 9e999), k + 1, wordcost.get(s[i-k-1:i], 9e999), s[i-k-1:i]) for k, c in candidates]

        candidates = enumerate(reversed(cost[max(0, i-maxword):i]))

        '''
        Let's say candidates = [(0,0)]
        k = c = 0
        c + wordcost.get(s[i-k-1 : i]) = 0 + wordcost.get(s[1-0-1 : 1]) = wordcost.get("a") = 3.849
        '''


        # 9e999 (inf) is default
        return min((c + wordcost.get(s[index-k-1:index], 9e999), k+1) for index, c in candidates)

    # Build the cost array.
    cost = [0]
    # for every index in the length of the string:
    for i in range(1,len(s)+1):
        print "cost", cost
        c,k = best_match(i)
        print "best match", c, k,  "\n"
        cost.append(c)

    print "\n\n"
    print "cost", cost

    # Backtrack to recover the minimal-cost string.
    out = []
    i = len(s)

    '''
    Start at very end of the string, (pos 31 in test string)
    Find length with minimal cost. 4 ("good") for test string.
    Then, move towards the start of the string by the number of words added and repeat.
    Here, new i=27. -> "a"
    Then i=26

    '''
    while i>0:



        c,k = best_match(i)

        print i, c, k, s[i-k:i]

        assert c == cost[i]
        out.append(s[i-k:i])
        i -= k

        print out


    return " ".join(reversed(out))


if __name__ == "__main__":

    s = "AndIbelieve,ifIcouldgiveyouagood"

    s = ["words there rri ght be one or two or one or two or three",
         "over a period of t i me i n 2008 and 2009",
         "And I bel i eve, i f I coul d gi ve you a good",
         "date for t he Q i va case, I was asked t o serve as a",
         "consultant on that case in late June of 2009. But that"
         ]

    s = 'overaperiod'

    infer_spaces(s)