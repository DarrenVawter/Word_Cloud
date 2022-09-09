# -*- coding: utf-8 -*-
"""
Created on Thu Sep  8 16:06:20 2022

@author: Darren Vawter
"""

from Helper_Functions import Get_Orthogonal_Estimate;

class Sentence_Trie:
    
    def __init__(self):
        
        self.root = self.Node("", 0);   
        self.dictionary = {};
        
    def Insert_Sentence(self, sentence_tokens):
        
        self.root.total += 1;
        
        current_node = self.root;
        
        for token in sentence_tokens:
            
            if(token not in current_node.children_map):
                current_node.children_map[token] = len(current_node.children);
                child = self.Node(token, current_node.depth+1);
                current_node.children.append(child);
            else:            
                child = current_node.children[current_node.children_map[token]];
                
            child.total += 1;                
            
            if(token not in self.dictionary):
                self.dictionary[token] = (0, []);
                
            self.dictionary[token][1].append(current_node);
            
            current_node = child;
            
    def Seed_Relations(self, token):
        
        for node in self.dictionary[token][1]:
            
            for child in node.children:
                
                if(child.token == token):
                    continue;
                    
                    #TODO: change this
                self.dictionary[child.token] = (self.dictionary[child.token][0]+child.depth*child.total, self.dictionary[child.token][1]);
                    
    class Node:
        
        def __init__(self, token, depth):
            
            self.token = token;
            self.depth = depth;
            self.total = 0;
            self.children_map = {};
            self.children = [];                   
                            
trie = Sentence_Trie();
trie.Insert_Sentence(["hello"]);
trie.Insert_Sentence(["hello"]);
trie.Insert_Sentence(["hello"]);
trie.Insert_Sentence(["the","bat","flew"]);
trie.Insert_Sentence(["the","bat","flew"]);
trie.Insert_Sentence(["the","frog","lept"]);
trie.Insert_Sentence(["the","frog","lept"]);
trie.Insert_Sentence(["the","frog","swam"]);
trie.Insert_Sentence(["bat","man"]);

trie.Seed_Relations("bat")
for token in trie.dictionary:
    print(token,trie.dictionary[token][0])

                
                
                
                
                
                
                
                
                
                
                
                
                