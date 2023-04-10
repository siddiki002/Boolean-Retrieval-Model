from nltk.stem import PorterStemmer #PorterStemmer for stemming
from tkinter import *   # library for GUI
import pickle
dictionary = dict()
"""
The dictionary is of following pattern:

term : [term_frequency,{doc_id : [position]}]

Each term is token retrieved after document processing. The term frequency is the number of times the term is repeated in entire collection and
the dictionary in the end is a key:value pair of document ID and it's postion (a list) .

"""
# a simple list of stop words
stopwords = list()

# function to add a term to the dictionary
def add_to_dictionary(word,doc_id,pos):
    # checking if the term is already in dictionary
    if word in dictionary:
        value = dictionary[word]
        value[0]+=1      # incrementing the frequency of the term
        post_dict = value[1] # getting the posting dictionary
        if doc_id in post_dict:
            post_dict[doc_id].append(pos)   # appending the position to the document ID already present
            value[1] = post_dict
        else:
            post_dict[doc_id] = [pos]
            value[1] = post_dict
        dictionary[word] = value
    else:
        dictionary[word] = [1,{doc_id:[pos]}]
    
# simple function to check if the given string contains space or not
def containspace(word):

    for i in range(0,len(word)):
        if word[i]==' ':
            return True
    
    return False
# function to remove symbols and special characters
def remove_symbols(line):
    return ''.join(ch for ch in line if ch.isalnum())

# function that returns posting list
def findPostingList(word):
    if word not in dictionary:
        return []
    else:
        return list(dictionary[word][1].keys())
def positional_query(word1,word2,k):
    result_list = intersection(findPostingList(word1), findPostingList(word2))
    answer = list()
    k = int(k)
    for i in range(0,len(result_list)):
        list1 = dictionary[word1][1]
        list1 = list1[result_list[i]]
        list2 = dictionary[word2][1]
        list2 = list2[result_list[i]]
        m=0
        n=0
        while m<len(list1) and n<len(list2):
            if list1[m]+(k+1) == list2[n]:
                answer.append(result_list[i])
                n+=1
                m+=1
            elif list1[m]+(k+1) < list2[n]:
                m+=k+1
            else:
                n+=k+1
        
    return answer
def makedictionary():

    # porter stemmer    
    ps = PorterStemmer()
    # filling the stopwords() list
    with open("Preprocessing/Stopword-List.txt","r") as stpfile:
        fileData = stpfile.readlines()
        for line in fileData:
            line = line.replace('\n', '')
            line = line.replace(' ', '')
            stopwords.append(line)

    # processing each document to create inverted index

    for doc_id in range(1,31):
        file = open("Dataset/"+str(doc_id)+".txt","r")
        data = file.readlines()
        position = 1
        for line in data:
            word = line.split()
            for i in range(0,len(word)):
                # normalizing the words
                word[i] = remove_symbols(word[i]) # removing symbols and special character from each token
                word[i] = word[i].lower()   #peforming case-folding
                word[i] = word[i].replace("nbsp"," ")   # handling the nbsp problem in the documents
                if containspace(word[i]):
                    subword = word[i].split()
                    word[i] = ps.stem(subword[0])
                    for j in range(1,len(subword)):
                        word.append(ps.stem(subword[j]))

                else:
                    word[i] = ps.stem(word[i])
            # position = 1
            for alphabet in word:   # adding the normalized list of words into the dictionary to create inverted index
                if alphabet not in stopwords:
                    add_to_dictionary(alphabet, doc_id,position)
                position+=1
def write_to_file():
    with open('Preprocessing/Dictionary.txt','wb') as file:
        pickle.dump(dictionary,file)
        file.close()

def read_from_file():
    with open('Preprocessing/Dictionary.txt','rb') as file:
        local_dictionary = pickle.loads(file.read())
        file.close()
        return local_dictionary

            
# function to perform binary NOT operation
def not_operation(word):
    ans_list = findPostingList(word)
    answer = list()
    for i in range(1,31):
        if i not in ans_list:
            answer.append(i)
    
    return answer
# function to perform binary OR operation
def union(list1,list2):
    answer = list()

    for i in list2:
        if i not in list1:
            list1.append(i)
    
    list1.sort()
    answer = list1
    return answer
    
    return answer
# function to perform binary AND operation
def intersection(list1,list2):

    answer = list()

    i = 0
    j = 0

    while (i<len(list1) and j<len(list2)):
        
        if (list1[i] == list2[j]):
            answer.append(list1[i])
            i+=1
            j+=1
        elif list1[i] < list2[j]:
            i+=1
        else:
            j+=1


    
    return answer
# driver code:
def main(query):
    """
    The below function makes dictionary from the document list. Since I have saved the dictionary in file 'Dictionary.txt' therefore the below function is commented
    but could be evaluated for checking the logic

    makedictionary()
    """
    # importing PorterStemmer for stemming of the query
    ps = PorterStemmer()
    # to check if it is a positional query
    if '/' in query:
        query = query.split()
        for i in range(0,len(query)):
            query[i] = remove_symbols(query[i])
            query[i] = query[i].lower()
            query[i] = ps.stem(query[i])
        
        return positional_query(query[0],query[1],query[2])
    query = query.split()

    # performing normalization on the query
    for i in range(0,len(query)):
        query[i] = remove_symbols(query[i])
        query[i] = query[i].lower()
        query[i] = ps.stem(query[i])

    list1 = list()
    list2 = list()
    # perform the binary operation
    for i in range(0,len(query),2):
        if(len(list1)==0):
            list1 = findPostingList(query[i])
            # checking if the query contains only two words and one of them is a 'not' operation
            if len(query) == 2 and query[0] == 'not':
                return not_operation(query[1])
            # to cater single word query
            if i+2 > len(query):
                continue
            list2 = findPostingList(query[i+2])
            # classifiying queries according to the operators
            if query[i+1] == 'and':
                list1 = intersection(list1, list2)
            elif query[i+1] == 'or':
                list1 = union(list1, list2)
            elif query[i+1] == 'not':
                list2 = not_operation(query[i+2])
                list1 = intersection(list1, list2)
        else:
            if i+2 < len(query):
                list2 = findPostingList(query[i+2])
                if query[i+1] == 'and':
                    list1 = intersection(list1, list2)
                elif query[i+1] == 'or':
                    list1 = union(list1, list2)
                elif query[i+1] == 'not':
                    list2 = not_operation(query[i+2])
                    list1 = intersection(list1, list2)
            else:
                continue

    return list1

# reading the dictionary from file
dictionary = read_from_file()
# GUI Code
# using tkinter library for GUI
frame = Tk()
frame.title("IR assignment 01 (20k-0177)")
frame.geometry('1920x1080')
frame.configure(bg='#ADD8E6')


def showquery():
    lbl.configure(text='')
    inp = inputtxt.get(1.0,"end-1c")
    # sending the query to the main function and getting the answer
    inp = main(inp)    
    lbl.configure(height=1000,width=50,font=('Times',10))
    answerText = "The terms are present in following documents:\n"
    for i in range(0,len(inp)):
        answerText+= "Document "+str(inp[i])+"\n"
    if len(inp)==0:
        answerText = "No result exist"
    lbl.configure(text=answerText)
    # lbl.configure(fg=red)

queryLabel = Label(frame,text="Enter Query use '/' for proximity query\nFor e.g qudrat ka nizam will be queried as qudrat nizam /1")
queryLabel.pack()
inputtxt = Text(frame,height=4,width=25)
inputtxt.pack()

search = Button(frame,text="search",command=showquery)
search.pack()

lbl = Label(frame,text="")
lbl.pack()

frame.mainloop()