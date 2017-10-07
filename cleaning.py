import count_freqs

# reads in file and adds each line as an element
def process_file(filename):
    """
    Pass a file as input and this function returns
    the file contents as a list
    """
    file_contents = []
    for i in open(filename):
        file_contents.append(i)
    return file_contents


def clean_file(file_contents):
    cleaned_words = []
    for i in file_contents:
        if len(i) < 2:
            cleaned_words.append(i)
        else:
            cleaned_words.append(i.split()[0])
    return cleaned_words

# returns words in file without duplicates
def get_unique_words(cleaned_words):
    return set(cleaned_words)


#  returns dictionary with counts
def count_words(word_set, cleaned_words):
    unique_words_dict = {}
    for i in word_set:
        unique_words_dict[i] = 0
    for i in cleaned_words:
        unique_words_dict[i] = unique_words_dict[i] + 1
    return unique_words_dict


# replaces word with RARE if < 5
def replace_rare(file_contents, count_words):
    f2 = open('4_1.txt', 'w')
    for i in file_contents: 
        if len(i.strip()) == 0:
            pass
        elif count_words[i.split()[0]] < 5: 
            f2.write("_RARE_ " + "".join(i.split()[1:])+"\n") # NewLine
        else:
            f2.write(i)
    f2.close()


if __name__ == '__main__':
	file_contents = process_file("./ner_train.dat")
	cleaned_words = clean_file(file_contents)
	word_set = get_unique_words(cleaned_words)
	unique_words_dict = count_words(word_set, cleaned_words)
	replace_rare(file_contents, unique_words_dict)
	# After classifying the words as _RARE_
	# Re-run the count_freqs.py
	# It creates file named 'out.count'
	count_freqs.main('4_1.txt')