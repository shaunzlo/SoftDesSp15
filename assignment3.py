"""

Name: Zi Liang, Ong
Mini Project 3

Description: Prints the frequency of each word as well as the top 10 words being used in acsending order

"""
import operator

def extract_words(filename):
	fp = open(filename, 'r')
	words = []
	for line in fp:
		for word in line.split():
			words.append(word)
	return words

def remove_punctuation(words):
	for i in range(len(words)):
		words[i] = words[i].translate(None, ",./;'[]<?:{}=>-+_)(*&^%$#@!")
		words[i] = words[i].lower()
	return get_words

def top_ten_used_words(s):
	temp = {}
	top_ten = []
	final = {}
	i = 0

	for word in s:
		temp[word] = temp.get(word,0) + 1

	print temp

	top_ten = sorted(temp, key = temp.get, reverse = True)[:10]

	for word in top_ten:
		for i in range(len(temp)):
			if word == temp.keys()[i]:
				final[word] = temp.values()[i]
	
	sorted_final = sorted(final.items(), key = operator.itemgetter(1))
	return sorted_final

get_words = extract_words("Oliver.txt") 		#get_words is in list
removed_punc = remove_punctuation(get_words) 	#removed_punc is in list format
print top_ten_used_words(removed_punc)			#prints the top 10 words used in ascending order 
