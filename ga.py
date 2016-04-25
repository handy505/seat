#!/usr/bin/env python3
#-*- coding: UTF-8 -*-

def test():
    print("geneic test")
        
class GA(object):
    
    def __init__(self):
        pass
        
    def next_generation(self):
        pass
        
    __generation = 0
    @property
    def generation(self):
        return self.__generation
    