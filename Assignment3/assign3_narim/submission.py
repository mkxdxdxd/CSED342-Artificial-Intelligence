import shell
import util
import wordsegUtil



############################################################
# Problem 1: Word Segmentation

# Problem 1a: Solve the word segmentation problem under a unigram model

class WordSegmentationProblem(util.SearchProblem):
    def __init__(self, query, unigramCost):
        self.query = query
        self.unigramCost = unigramCost

    def startState(self):
        # BEGIN_YOUR_ANSWER (our solution is 1 lines of code, but don't worry if you deviate from this)
        return 0
        # END_YOUR_ANSWER

    def isEnd(self, state):
        # BEGIN_YOUR_ANSWER (our solution is 1 lines of code, but don't worry if you deviate from this)
        return state == len(self.query)
        # END_YOUR_ANSWER

    def succAndCost(self, state):
        # BEGIN_YOUR_ANSWER (our solution is 5 lines of code, but don't worry if you deviate from this)
        results = []
        for i in range(state + 1, len(self.query) + 1):
            action = self.query[state:i]
            results.append((action, i, self.unigramCost(action)))
        return results
        # END_YOUR_ANSWER

def segmentWords(query, unigramCost):
    if len(query) == 0:
        return ''

    ucs = util.UniformCostSearch()
    ucs.solve(WordSegmentationProblem(query, unigramCost))

    # BEGIN_YOUR_ANSWER (our solution is 1 lines of code, but don't worry if you deviate from this)
    return ' '.join(ucs.actions)
    # END_YOUR_ANSWER

# Problem 1b: Solve the k-word segmentation problem under a unigram model

class KWordSegmentationProblem(util.SearchProblem):
    def __init__(self, k, query, unigramCost):
        self.k = k
        self.query = query
        self.unigramCost = unigramCost

    def startState(self):
        # BEGIN_YOUR_ANSWER (our solution is 1 lines of code, but don't worry if you deviate from this)
        return (0, 0)
        # END_YOUR_ANSWER

    def isEnd(self, state):
        # BEGIN_YOUR_ANSWER (our solution is 1 lines of code, but don't worry if you deviate from this)
        return state[0] == len(self.query) and state[1] == self.k
        # END_YOUR_ANSWER

    def succAndCost(self, state):
        # BEGIN_YOUR_ANSWER (our solution is 7 lines of code, but don't worry if you deviate from this)
        results = []
        for i in range(state[0] + 1, len(self.query) + 1):
            action = self.query[state[0]:i]
            if state[1] + 1 <= self.k and i <= len(self.query):
                results.append((action, (i, state[1] + 1), self.unigramCost(action)))
        return results
        # END_YOUR_ANSWER

def segmentKWords(k, query, unigramCost):
    if len(query) == 0:
        return ''

    # BEGIN_YOUR_ANSWER (our solution is 3 lines of code, but don't worry if you deviate from this)
    ucs = util.UniformCostSearch()
    ucs.solve(KWordSegmentationProblem(k, query, unigramCost))
    return ' '.join(ucs.actions)
    # END_YOUR_ANSWER

############################################################
# Problem 2: Vowel Insertion

# Problem 2a: Solve the vowel insertion problem under a bigram cost

class VowelInsertionProblem(util.SearchProblem):
    def __init__(self, queryWords, bigramCost, possibleFills):
        self.queryWords = queryWords
        self.bigramCost = bigramCost
        self.possibleFills = possibleFills

    def startState(self):
        # BEGIN_YOUR_ANSWER (our solution is 1 lines of code, but don't worry if you deviate from this)
        return wordsegUtil.SENTENCE_BEGIN, 0
        # END_YOUR_ANSWER

    def isEnd(self, state):
        # BEGIN_YOUR_ANSWER (our solution is 1 lines of code, but don't worry if you deviate from this)
        return state[1] == len(self.queryWords)
        # END_YOUR_ANSWER

    def succAndCost(self, state):
        # BEGIN_YOUR_ANSWER (our solution is 9 lines of code, but don't worry if you deviate from this)
        prev_word, count = state
        results = []
        _actions = self.possibleFills(self.queryWords[count])

        if(len(_actions)>0):
            actions = self.possibleFills(self.queryWords[count])
        else:
            actions = self.queryWords[count]

        #_actions = self.possibleFills(self.queryWords[count]) #find for next state, it's set of next state
        #actions = self.possibleFills(self.queryWords[count]) if len(_actions) > 0 else {self.queryWords[count]}

        for action in actions:
            results.append((action, (action, count + 1), self.bigramCost(prev_word, action)))

        return results
        # END_YOUR_ANSWER

def insertVowels(queryWords, bigramCost, possibleFills):
    # BEGIN_YOUR_ANSWER (our solution is 3 lines of code, but don't worry if you deviate from this)
    ucs = util.UniformCostSearch(verbose=0)
    ucs.solve(VowelInsertionProblem(queryWords, bigramCost, possibleFills))

    return ' '.join(ucs.actions)
    # END_YOUR_ANSWER

# Problem 2b: Solve the limited vowel insertion problem under a bigram cost

class LimitedVowelInsertionProblem(util.SearchProblem):
    def __init__(self, impossibleVowels, queryWords, bigramCost, possibleFills):
        self.impossibleVowels = impossibleVowels
        self.queryWords = queryWords
        self.bigramCost = bigramCost
        self.possibleFills = possibleFills

    def startState(self):
        # BEGIN_YOUR_ANSWER (our solution is 1 lines of code, but don't worry if you deviate from this)
        return wordsegUtil.SENTENCE_BEGIN, 0
        # END_YOUR_ANSWER

    def isEnd(self, state):
        # BEGIN_YOUR_ANSWER (our solution is 1 lines of code, but don't worry if you deviate from this)
        return state[1] == len(self.queryWords)
        # END_YOUR_ANSWER

    def succAndCost(self, state):
        # BEGIN_YOUR_ANSWER (our solution is 10 lines of code, but don't worry if you deviate from this)
        prev_word, count = state
        results = []
        query_word = self.queryWords[count]

        _actions = self.possibleFills(query_word)
        actions = set(action for action in _actions if not any(v in self.impossibleVowels for v in action))

        if len(actions) == 0:
            actions = {query_word}
    
        for action in actions:
            if any(v in self.impossibleVowels for v in action):
                continue
            new_state = (action, count + 1)
            cost = self.bigramCost(prev_word, action)
            results.append((action, new_state, cost))

        return results
        # END_YOUR_ANSWER

def insertLimitedVowels(impossibleVowels, queryWords, bigramCost, possibleFills):
    # BEGIN_YOUR_ANSWER (our solution is 3 lines of code, but don't worry if you deviate from this)
    ucs = util.UniformCostSearch(verbose=0)
    try:
        ucs.solve(LimitedVowelInsertionProblem(impossibleVowels, queryWords, bigramCost, possibleFills))
    except:
        return 'Impossible'

    return ' '.join(ucs.actions)
    # END_YOUR_ANSWER

############################################################
# Problem 3: Putting It Together

# Problem 3a: Solve the joint segmentation-and-insertion problem

class JointSegmentationInsertionProblem(util.SearchProblem):
    def __init__(self, query, bigramCost, possibleFills):
        self.query = query
        self.bigramCost = bigramCost
        self.possibleFills = possibleFills

    def startState(self):
        # BEGIN_YOUR_ANSWER (our solution is 1 lines of code, but don't worry if you deviate from this)
        return wordsegUtil.SENTENCE_BEGIN, 0
        # END_YOUR_ANSWER

    def isEnd(self, state):
        # BEGIN_YOUR_ANSWER (our solution is 1 lines of code, but don't worry if you deviate from this)
        return state[1] == len(self.query)
        # END_YOUR_ANSWER

    def succAndCost(self, state):
        # BEGIN_YOUR_ANSWER (our solution is 8 lines of code, but don't worry if you deviate from this)
        prev_word, count = state
        results = []
        for i in range(count + 1, len(self.query) + 1):
            for action in self.possibleFills(self.query[count:i]):
                results.append((action, (action, i), self.bigramCost(prev_word, action)))
        return results
        # END_YOUR_ANSWER

def segmentAndInsert(query, bigramCost, possibleFills):
    if len(query) == 0:
        return ''

    # BEGIN_YOUR_ANSWER (our solution is 3 lines of code, but don't worry if you deviate from this)
    ucs = util.UniformCostSearch(verbose=0)
    ucs.solve(JointSegmentationInsertionProblem(query, bigramCost, possibleFills))
    return ' '.join(ucs.actions)
    # END_YOUR_ANSWER

############################################################
# Problem 4: A* search

# Problem 4a: Define an admissible but not consistent heuristic function

class SimpleProblem(util.SearchProblem):
    def __init__(self):
        # BEGIN_YOUR_ANSWER (our solution is 4 lines of code, but don't worry if you deviate from this)
         self.actions = {'a': [('b', 'b', 1), ('c', 'c', 1)],
                        'b': [('d', 'd', 1)],
                        'c': [('d', 'd', 2)],
                        'd': [('e', 'e', 1000)]}
        # END_YOUR_ANSWER

    def startState(self):
        # BEGIN_YOUR_ANSWER (our solution is 1 lines of code, but don't worry if you deviate from this)
        return 'a'
        # END_YOUR_ANSWER

    def isEnd(self, state):
        # BEGIN_YOUR_ANSWER (our solution is 1 lines of code, but don't worry if you deviate from this)
        return state == 'e'
        # END_YOUR_ANSWER

    def succAndCost(self, state):
        # BEGIN_YOUR_ANSWER (our solution is 3 lines of code, but don't worry if you deviate from this)
        return self.actions[state]
        # END_YOUR_ANSWER

def admissibleButInconsistentHeuristic(state):
    # BEGIN_YOUR_ANSWER (our solution is 2 lines of code, but don't worry if you deviate from this)
    h_costs = {'a': 0, 'b': 1001, 'c': 0, 'd': 0, 'e': 0}
    return h_costs[state]
    # END_YOUR_ANSWER

# Problem 4b: Apply a heuristic function to the joint segmentation-and-insertion problem

def makeWordCost(bigramCost, wordPairs):
    """
    :param bigramCost: learned bigram cost from a training corpus
    :param wordPairs: all word pairs in the training corpus
    :returns: wordCost, which is a function from word to cost
    """
    # BEGIN_YOUR_ANSWER (our solution is 4 lines of code, but don't worry if you deviate from this)
    # Implement a unigram cost function using the given bigramCost
    costs = {}
    for word1, word2 in wordPairs:
        cost = bigramCost(word1, word2)
        #if word2 not in costs or cost < costs[word2]:
        #    costs[word2] = cost
        costs[word2] = min(cost ,costs.get(word2, cost))

    def wordCost(word):
        return costs.get(word, bigramCost(wordsegUtil.SENTENCE_UNK, word))

    return wordCost
    # END_YOUR_ANSWER

class RelaxedProblem(util.SearchProblem):
    def __init__(self, query, wordCost, possibleFills):
        self.query = query
        self.wordCost = wordCost
        self.possibleFills = possibleFills

    def startState(self):
        # BEGIN_YOUR_ANSWER (our solution is 1 lines of code, but don't worry if you deviate from this)
        return None, 0
        # END_YOUR_ANSWER

    def isEnd(self, state):
        # BEGIN_YOUR_ANSWER (our solution is 1 lines of code, but don't worry if you deviate from this)
        return state[1] == len(self.query)
        # END_YOUR_ANSWER

    def succAndCost(self, state):
        # BEGIN_YOUR_ANSWER (our solution is 5 lines of code, but don't worry if you deviate from this)
        results = []
        for i in range(state[1] + 1, len(self.query) + 1):
            #substr = self.query[state[1]:i]
            for action in self.possibleFills(self.query[state[1]:i]):
                results.append((None, (None, i), self.wordCost(action)))
        return results
        # END_YOUR_ANSWER

def makeHeuristic(query, wordCost, possibleFills):
    # BEGIN_YOUR_ANSWER (our solution is 2 lines of code, but don't worry if you deviate from this)
    dp = util.DynamicProgramming(RelaxedProblem(query, wordCost, possibleFills))
    h = [dp((None, i)) for i in range(len(query) + 1)]

    #value = []
    #for i in range(len(query)+1):
    #    value.append(dp((None, i)))

    #def heuristic(state):
    #   return value[state[1]]

    #return heuristic

    return lambda state: h[state[1]]

    #h = [dp((None, i)) for i in range(len(query) + 1)]
    #def heuristic(state):
    #    return h[state[1]]

    #return heuristic
    # END_YOUR_ANSWER

def fastSegmentAndInsert(query, bigramCost, wordCost, possibleFills):
    if len(query) == 0:
        return ''

    # BEGIN_YOUR_ANSWER (our solution is 4 lines of code, but don't worry if you deviate from this)
    ucs = util.UniformCostSearch(verbose=0)
    heuristic = makeHeuristic(query, wordCost, possibleFills)
    ucs.solve(JointSegmentationInsertionProblem(query, bigramCost, possibleFills), heuristic)
    return ' '.join(ucs.actions)
    # END_YOUR_ANSWER

############################################################

if __name__ == '__main__':
    shell.main()