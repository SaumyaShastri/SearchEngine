from typing import Tuple

#Creating a trie structure and it's node
class TrieNode(object):  
    def __init__(self, char: str):
        self.char = char
        self.children = []
        #the last character of the word.`
        self.word_finished = False
        #counter for this character
        self.counter = 1
        #list of all the occurences of the prefix in the documents 
        self.OccurrenceList={}
    
#Initialize the root of the trie    
root = TrieNode('*')

#Adding a word in the trie structure
def insert(root, word: str,document):
        node = root
        for char in word:
            found_in_child = False
            # Search for the character in the children of the present `node`
            for child in node.children:
                if child.char == char:
                    #the char of the word to be inserted is already present in trie; increment the counter of this char 
                    child.counter += 1
                    # move the pointer to the node's child to continue the insertion of the rest of the word
                    node = child
                    found_in_child = True
                    break
            # this char has never been inserted before, create node and insert it
            if not found_in_child:
                new_node = TrieNode(char)
                node.children.append(new_node)
                # And then point node to the new child
                node = new_node
                
        # At this point, word is inserted- we mark the end of this word
        node.word_finished = True
        if document not in node.OccurrenceList:  #If document is not in OccurenceList for that word
            node.OccurrenceList[document]=1     # Create a new key with document name
        node.OccurrenceList[document]= node.OccurrenceList[document]+1 # We append the position in the document      
        
#Performing the search in our files for the input word, using the trie structure we created above
#We will first check for the word's existence, if it exists- return file name and occurence number 
def find_prefix(root, prefix: str) -> Tuple[bool, int]:
    node = root
    #handling the case of an empty trie ie the root node has no children
    if not root.children:
        return False, 0
    for char in prefix:
        char_not_found = True
        # Search through all the children of the node the pointer is pointing to
        for child in node.children:
            if child.char == char:
                #the char of the input word exists in trie
                char_not_found = False
                # increment the pointer to go further down the trie to check for the remaining chars in prefix
                node = child
                break
    #letting the user know that the input word of prefix doesn't exist in the trie 
    if char_not_found:
        print("Word Not Found: " +prefix)
    #input word found, return the found status, along the files in which it exists
    else:    
        print("Word Found: " +prefix)
    return True,node.OccurrenceList

#for scrapping words from website
from bs4 import BeautifulSoup
import nltk
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
import string
stop_words = set(stopwords.words('english'))
stop_words.update(string.punctuation) 
import os

#selecting file for scrapping into fdata->files
#please change the dircectory to run on your device
fdata = r"./input/"
files=os.listdir(fdata)
#cleaning the text in every every file from punctuations, stop words, digits, words less than length 2 and other symbols
for file in files:  
    fname=file  #called later, while associating word with the file it exists in for insertion in trie
    file=open(fdata+str(file), encoding="utf8")
    soup = BeautifulSoup(file.read(), 'html.parser')
    #filter the soup
    [script.extract() for script in soup.findAll('script')]
    [style.extract() for style in soup.findAll('style')]
    #gather words from filtered soup
    words = word_tokenize(soup.get_text())
    # remove the words containing punctuation
    words = [i for i in words if all(j not in string.punctuation for j in i)]
    #filtering words and cleaning the data to insert in trie
    for word in words:
        if word.lower() not in stop_words and len(word) > 2 and word.isdigit() == False:
                # build compressed trie tree
                try:
                    # remove the words whcih can't encode to ascII
                    word = word.lower().strip().encode('ascII')
                except:
    #                             print word
                    a = 1
                else:
                #inserting words into tree
                     insert(root, word.decode("utf-8"), fname)
                
# Asking the user for input word that we search                    
Enter = input("Please enter what you would like to search for: ")
#In case if multiple word search
inp = Enter.split(' ')
rank = {}
#searching for each word of the input
for word in inp:
    #search in trie, store the result in dic
    boolw,dic = find_prefix(root, word.lower())
#ranking the files in which the word was present
    for key in dic:
        if key not in rank:
            rank[key] = dic[key]
        else:
            rank[key] = rank[key] + dic[key]
#ranking website based on number of time word present - sort them in acsending order and reversing them so we display 
# the websites in order of relevance
items=[(v,k) for k,v in rank.items()]
items.sort()
items.reverse()
#displaying search results
if not items:
    print("No results")
else:
    print("Results : ")
#printing all the files the input was found in, in order of maximum occurences    
    for key in items:
        print(key)
        
