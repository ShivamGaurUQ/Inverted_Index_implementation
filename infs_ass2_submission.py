
# coding: utf-8

# In[2]:


# coding: utf-8

# In[5]:



# coding: utf-8

# In[ ]:


#1. tokenize each doc
import glob			#python library to read open multiple files and read data from them
import re			#python library to comprehend regular expression
import os			#python library used to delete a file
from collections import Counter			#python library used to count tokens
from collections import defaultdict
import sys
import pickle


class text_transform:
    
    unique_tokens=[]
    index_address=""
    
 
    
  
    
        
    def __init__(self):		#class constructor to read address of dataset and common words in the file
        
        self.all_tokens=[]
        self.tokens=[]
        self.stop_words=[]
        self.tokens_wo_stopwords=[]
        self.unique_tokens=[]
        self.inverted_index={}
        self.inner_index={}
        self.keywords=[]
        self.doc_list=[]
        self.term_search={}
        
        
        #choice=input("Press 1 to create inverted index or 2 to search using keywords")
        #if int(choice)==1:            
        self.prereq_inverted_index()        
                
        #else:
        #self.search_index()
            
            
    def prereq_inverted_index(self):
        
        directory_name=input("Enter corpus directory path ")
 
        if os.path.isdir(directory_name):
            print("Directory found. Creating inverted index.")
            self.data_address=directory_name+'\cranfieldDocs\cranfield*'  										#also used to read address of file which stores data temporarily from all files in the dataset      
            self.address_com_words=directory_name+'\common_words.txt'
            text_transform.index_address=directory_name+"\inverted_index.pickle"
            self.process_data()
        else:
            print("Wrong directory address!")
            
            
    
            
    def process_data(self):										#function to read data from all the files in the dataset and copy all data into one duplicate file temporarily
        data_files=sorted(glob.glob(self.data_address))		#uses glob library to open all files one by one
        for data_file in data_files:
            info=open(data_file,"r")
            if info.mode=='r':
                contents=info.read()
                sgml_tags = re.sub('<[^<]+>', "", contents)
                info.close()
                with open(data_file, "w") as remove_tag:
                    remove_tag.write(sgml_tags)
                    remove_tag.close()
                    
                    
                self.stop_words.clear()
                self.tokens_wo_stopwords.clear()					#the function also removes common words from the tokens obtained in task 1
                with open(self.address_com_words) as com_words_file:
                    for sentence in com_words_file:
                        for com_word in re.findall(r'\w+', sentence):
                            self.stop_words.append(com_word.lower())
                
                
                self.tokens.clear()
                with open(data_file,"r") as doc_file:		
                    for sentence in doc_file:
                        for alpha_num_token in re.findall(r'\w+', sentence):		#Uses 're' library to identify alphanumeric tokens
                            self.tokens.append(alpha_num_token.lower())
                    doc_file.close()
                
                self.tokens_wo_stopwords=self.tokens.copy()
                for com_word in list(self.tokens_wo_stopwords):
                    if com_word in self.stop_words:
                        self.tokens_wo_stopwords.remove(com_word)
                
                
                with open(data_file, "w") as write_token:
                    for each_token in self.tokens_wo_stopwords:
                        self.all_tokens.append(each_token)
                        write_token.write(each_token)
                        write_token.write("\n")
                    write_token.close()
            
        self.unique_tokens=set(list(self.all_tokens))
        self.create_inverted_index()
            
    def create_inverted_index(self):
        
        data_files=sorted(glob.glob(self.data_address))		#uses glob library to open all files one by one
        
        temp_list=[]
        doc_num=0
        
        for data_file in data_files:
            
            self.inner_index.clear()
            info=open(data_file,"r")
            if info.mode=='r':
                doc_num=doc_num+1                
                for newline in info:
                    newline=newline.rstrip()
                    wordlist=newline.split()
                    
                    for word in wordlist:
                        if word in self.unique_tokens:                                
                            self.inner_index[word]=self.inner_index.get(word,0) + 1
                            
               
                
                for word, count in self.inner_index.items():
                    if word in self.inverted_index:
                       
                        temp_list=self.inverted_index[word]
                       
                        tple=(doc_num,count)
                        temp_list.append(tple)
                        self.inverted_index[word]=temp_list                      
                        
                                                
                        
                        
                    else:
                        
                        tple=(doc_num,count)
                        self.inverted_index[word]=list(tple)
                                     
               
            
                
                
            
            
            
            info.close()
        print('Inverted index created. Writing index to file.')
        write_index_to_file=open(text_transform.index_address,"wb")
        pickle.dump(self.inverted_index,write_index_to_file)
        write_index_to_file.close()
        
        text_transform.unique_tokens=self.unique_tokens.copy()
        
            
 



class search:
        
    def __init__(self):
        self.keywords=[]
        self.doc_list=[]
        self.index={}
        read_inverted_index=open(text_transform.index_address,"rb")
        self.index=pickle.load(read_inverted_index)
        self.term_search={}
        self.search_index()
    
    def search_index(self):               
        self.keywords.clear()
        self.doc_list.clear()
        num_of_keywords=input("Enter number of keywords for search (max 3)")
        
        i=0
        self.term_search.clear()
        while i<int(num_of_keywords):
            keyword=input('Enter keyword ')
            self.keywords.append(keyword)
            i=i+1
            
        for term in self.keywords:
            
            if term in text_transform.unique_tokens:
                
                self.doc_list=self.index[term]
                
           
                self.term_search[self.doc_list[0]]=self.term_search.get(self.doc_list[0],0)+self.doc_list[1]
           
                var=self.doc_list.pop(0)
                var=self.doc_list.pop(0)
            
            
            
            
            
            
                for doc_freq in self.doc_list:
                    doc,frequency=doc_freq
                
                    self.term_search[doc]=self.term_search.get(doc,0)+frequency
                    
                
        
        sorted_docs=sorted(self.term_search.items(), key=lambda x : x[1], reverse=True)
        if len(sorted_docs)>0:
            print('\nTop 10 documents containing input keywords \n')
            print(sorted_docs[0:10])
        else:
            print('No records found')
        


        
   
if __name__=='__main__':
    create_inverted_index=text_transform()
    while(True):
        search_query=input("Press 1 to search query or 2 to exit")
        if int(search_query)==1:
            search_qry=search()
        else:
            break
        if int(search_query)==2:
            break
        
    
    
   



