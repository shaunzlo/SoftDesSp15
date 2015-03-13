""" Analyzes the word frequencies in a book downloaded from
	Project Gutenberg """

import string
import operator

def get_word_list(file_name):
	""" Reads the specified project Gutenberg book.  Header comments,
		punctuation, and whitespace are stripped away.  The function
		returns a list of the words used in the book as a list.
		All words are converted to lower case.
	"""
	fp = open(file_name, 'r')
	words = []
	for line in fp:
		for word in line.split():
			words.append(word)
	
	for i in range(len(words)):
		words[i] = words[i].translate(None, ",./;'[]<?:{}=>-+_)(*&^%$#@!")
		words[i] = words[i].lower()
	return words
	pass

def get_top_n_words(word_list, n):
	""" Takes a list of words as input and returns a list of the n most frequently
		occurring words ordered from most to least frequently occurring.

		word_list: a list of words (assumed to all be in lower case with no
					punctuation
		n: the number of words to return
		returns: a list of n most frequently occurring words ordered from most
				 frequently to least frequentlyoccurring
	"""

	temp = {}
	top_n = []
	final = {}

	for word in word_list:
		temp[word] = temp.get(word,0) + 1

	top_n = sorted(temp, key = temp.get, reverse = True)[:n]

	for word in top_n:
		for i in range(len(temp)):
			if word == temp.keys()[i]:
				final[word] = temp.values()[i]
	
	sorted_words = sorted(final.items(), key = operator.itemgetter(1))
	sorted_words.reverse()

	return sorted_words

sorted_word_list = get_word_list("Oliver.txt")
print get_top_n_words(sorted_word_list, 100)