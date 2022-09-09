# -*- coding: utf-8 -*-
"""
Created on Thu Sep  8 16:06:20 2022

@author: Darren Vawter
"""

import numpy as np;

from nltk.tokenize import sent_tokenize;
from nltk.corpus import brown;

class Sentence_Dual_Trie:
    
    def __init__(self):
        
        # Root of forward trie
        self.forward_root = self.Node("", 0);   
        # Root of backwards trie
        self.backwards_root = self.Node("", 0);   
        # Dictionary of Token_Data objects
        self.dictionary = {};
        
    def Insert_Sentence(self, sentence_tokens):
        
        # Insert sentence into forward trie
        
        # Increment total sentence count at forward root
        self.forward_root.count += 1;
        
        # Initialize traversal at forward root
        current_node = self.forward_root;
        
        # Traverse each node corresponding to the tokens in the sentence
        for token in sentence_tokens:
            
            # If the current token is a new sequence, create a new child
            if(token not in current_node.children):
                
                # Crate the child with the given token at 1 greater depth
                child = self.Node(token, current_node.depth+1);
                # Insert the child into the node's children node-map
                current_node.children[token] = child;
                
            else:            
                
                # Else, grab the corresponding child
                child = current_node.children[token];
                
            # Increment the number of occurences of the sequence
            child.count += 1;                
            
            # Check if a corrseponding Token_Data object does not yet exist
            if(token not in self.dictionary):
                
                # Create the Token_Data object
                token_data = self.Token_Data(token);
                # Insert the Token_Data object into the dictionary
                self.dictionary[token] = token_data;
                
            else:

                # Else, grab the corresponding Token_Data object
                token_data = self.dictionary[token];
                
            # Add/Update the instance of the token in the token data
            token_data.instances[current_node] = child.count;
            
            # Increment the token's total count
            token_data.count += 1;
                
            # Update node for next traversal step
            current_node = child;

        # Insert sentence into backwards trie
        
        # Increment total sentence count at backwards root
        self.backwards_root.count += 1;
        
        # Initialize traversal at backwards root
        current_node = self.backwards_root;
        
        # Traverse each node corresponding to the tokens in the reversed sentence
        for token in reversed(sentence_tokens):
            
            # If the current token is a new sequence, create a new child
            if(token not in current_node.children):
                
                # Crate the child with the given token at 1 greater depth
                child = self.Node(token, current_node.depth+1);
                # Insert the child into the node's children node-map
                current_node.children[token] = child;
                
            else:            
                
                # Else, grab the corresponding child
                child = current_node.children[token];
                
            # Increment the number of occurences of the sequence
            child.count += 1;                
            
            # The corrseponding Token_Data object must already exist, grab it
            token_data = self.dictionary[token];
                
            # Add/Update the instance of the token in the token data
            token_data.instances[current_node] = child.count;
            
            # Increment the token's total count
            token_data.count += 1;
                
            # Update node for next traversal step
            current_node = child;
          
    def Get_Relations(self, token):
               
        #temp?
        relationSum = 0;
        nRelations = 0;
        
        relations = {};
        
        token_data = self.dictionary[token];
        
        total_token_count = token_data.count;
        
        for instance in token_data.instances.items():
            
            relative_token_count = instance[1]/total_token_count;
            
            #TODO take this in as a tuple
            for comparator in instance[0].children.items():
                                
                # comparator[0] --> comparator token
                # comparator[1] --> comparator node
                        
                total_comparator_count = self.dictionary[comparator[0]].count;
                relative_comparator_count = comparator[1].count/total_comparator_count;

                node_relation = 0;
        
                if(relative_comparator_count < total_comparator_count):
                    
                    #node_relation = comparator[1].depth * relative_comparator_count / relative_token_count;
                    node_relation = relative_comparator_count / relative_token_count;
                    
                else:
                    
                    #node_relation = comparator[1].depth * relative_token_count / relative_comparator_count;
                    node_relation = relative_token_count / relative_comparator_count;
                                    
                #temp?
                relationSum += node_relation;
                    
                if(comparator[0] not in relations):
                
                    relations[comparator[0]] = node_relation; 
                    nRelations += 1;
                
                else:
                
                    relations[comparator[0]] += node_relation;
                    
        max_relation = relations[token];
        
        return(relations, max_relation, relationSum/nRelations);
                                        
    class Node:
        
        def __init__(self, token, depth):
            
            # The token string
            self.token = token;
            # The depth of the node in the tree
            self.depth = depth;
            # The total number of occurences of the sequence
            self.count = 0;
            # Map of all children nodes of this node, indexed by their tokens
            self.children = {};          
                            
    class Token_Data:
        
        def __init__(self, token):
            
            # The token string
            self.token = token;
            # The total number of instances of the token across the dual trie
            self.count = 0;
            # Map of tuples: (Node object that contains instance of token, count of instances of that token)
            self.instances = {};
            
trie = Sentence_Dual_Trie();

ind = 0;
for sentence in brown.sents():
    trie.Insert_Sentence(sentence);
    ind += 1;
print(ind)
        
paradigmatic_coordinates = np.zeros((len(trie.dictionary),1));

"""
max_t = 0;
max_token = token;
for token_data in trie.dictionary.values():
    if(token_data.count>max_t):
        max_t = token_data.count;
        max_token = token_data.token;
"""

(relations, max_relation, avg) = trie.Get_Relations("the");

print(len(trie.dictionary));

dictionary_index = 0;
for token in trie.dictionary:
    if(token in relations):   
        paradigmatic_coordinates[dictionary_index] = relations[token];
        if(relations[token]>30*avg):
            print(token,relations[token])
    else:
        paradigmatic_coordinates[dictionary_index] = 0;
    dictionary_index += 1;

"""
print(paradigmatic_coordinates);
alpha = 1/2;
print( (np.log((paradigmatic_coordinates+max_relation)/max_relation)/np.log(2))**alpha );
"""              

                
                
                
                
                
                
                
                
                
                
                