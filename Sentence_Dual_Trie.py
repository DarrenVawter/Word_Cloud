# -*- coding: utf-8 -*-
"""
Created on Thu Sep  8 16:06:20 2022

@author: Darren Vawter
"""

class Sentence_Dual_Trie:
    
    def __init__(self):
        
        # Root of forward trie
        self.forward_root = self.Node("", 0);   
        # Root of backward trie
        self.backward_root = self.Node("", 0);   
        # Dictionary of Token_Data objects
        self.dictionary = {};
        
    def Insert_Sentence(self, sentence_tokens):
        
        # Insert sentence into forward trie
        
        # Increment total sentence count at root
        self.forward_root.count += 1;
        
        # Initialize traversal at root
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
            token_data.instances[current_node] = (current_node, child.count);
            
            # Increment the token count
            token_data.count += 1;
                
            # Update node for next traversal step
            current_node = child;

    """
    def Seed_Relations(self, token):
        
        for node in self.dictionary[token][1]:
            
            for child in node.children:
                
                if(child.token == token):
                    continue;
                    
                    #TODO: change this
                self.dictionary[child.token] = (self.dictionary[child.token][0]+child.depth*child.count, self.dictionary[child.token][1]);
    """
                    
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
trie.Insert_Sentence(["hello"]);
trie.Insert_Sentence(["hello"]);
trie.Insert_Sentence(["hello"]);
trie.Insert_Sentence(["the","bat","flew"]);
trie.Insert_Sentence(["the","bat","flew"]);
trie.Insert_Sentence(["the","frog","lept"]);
trie.Insert_Sentence(["the","frog","lept"]);
trie.Insert_Sentence(["the","frog","swam"]);
trie.Insert_Sentence(["bat","man"]);

"""
trie.Seed_Relations("bat")
for token in trie.dictionary:
    print(token,trie.dictionary[token][0])
"""
                
                
                
                
                
                
                
                
                
                
                
                
                