#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 18:29:42 2020

@author: LilyHeAsamiko
"""
import numpy as np
from random import * 

#def getAll(list, num):
#    return filter(lambda a: list[a] == num , range(0, len(list)))

def getAll(list, ID, num):
    start_at = -1
    locs = []
    while True:
        try:
            loc = list.index(num, start_at+1)
        except ValueError:
            break
        else:
            locs.append(ID[loc])
            start_at = loc

    return locs

def Maxidxlist(idx, list):
    A = np.array(list, dtype = int)
    Max = 0
    for i in range(min(np.size(idx, 0), np.size(list, 0))):
        if A[i]>= Max:
            Max = A[i]
    return Max
    
def Sumidxlist(idx, list):
    A = np.array(list, dtype = int)
    Sum = 0
    for i in range(min(np.size(idx, 0), np.size(list, 0))):
        Sum += A[i]
    return Sum

#def Appendlist(sublist, list):
#    for elem in sublist:
#        list.append(elem)
#    return list

def AddSol(Sid_sort, S_sort, l, Choice, Check, S, Comp, Score, SolID, D, T):
#            Sum = Sumidxlist(Choice[range(Comp)], S_sort[l][:])
#            Sum = Sumidxlist(Choice[0:Comp], S_sort[l][:])
#            BkId.append(Choice[0:Comp])                           
    Score.append(Sumidxlist(Choice[0:Comp], S_sort[l][:]))
    SolID.append(Choice[0:Comp])
#    print(Choice[0:Comp])
#    print(SolID)
    for elem in Choice[0:Comp]:
        Check.append(elem)       
    LibId.append(l)
    Dt.append(D-T[l])
    return [Score, SolID, Check, LibId, Dt]

def Solve(LibChoice, Sid_sort, S_sort, Choice, Check, S, Comp, Score, SolID, D, T, L, B):
    for l in LibChoice:
        Sum = 0
        BkId = []
        Choice = list(set(Sid_sort[l][:]) - set(np.unique(Check[:])))
        print(Choice)
        if np.size(Choice, 0) > 0:
            if Maxidxlist(Choice,  S_sort[l][:])  >= sum(np.array(S, dtype = int))/len(S):
                Comp = min((D-T[l])*M[l], np.size(Choice, 0))
    #            Sum = Sumidxlist(Choice[range(Comp)], S_sort[l][:])
    #            Sum = Sumidxlist(Choice[0:Comp], S_sort[l][:])
    #            BkId.append(Choice[0:Comp])   
                Output = AddSol(Sid_sort, S_sort, l, Choice, Check, S, Comp, Score, SolID, D, T)                       
            elif l == L-1:
                if np.size(Check, 0) == B:
                    break
                else:
                    LibChoice = list(set(range(L)) - set(LibId))
                    Output = Solve(LibChoice, Sid_sort, S_sort, Choice, Check, S, Comp, Score, SolID, D, T, L, B)
            if np.size(Check, 0) == B:
                break
            if np.size(Output, 0) > 0:
                Score = Output[0]
                SolID = Output[1]
                Check = Output[2]       
                LibId = Output[3]
                Dt = Output[4]  
        LibChoice = list(set(range(L)) - set(LibId))        
    return [Score, SolID, Check, LibId, Dt]

#filepath = '/content/a_example.txt'
#filepath = '/content/b_read_on.txt'
#filepath = '/content/c_incunabula.txt'
#filepath = '/content/d_tough_choices.txt'
filepath = '/content/e_so_many_books.txt'
#filepath = '/content/f_libraries_of_the_world.txt'

N = []
T = []
M = []
ID = []
with open(filepath) as f: 

    first_line = f.readline().split() 
    
    B = int(first_line[0]) 

    L = int(first_line[1]) 
    
    D = int(first_line[2]) 
#    print('M: {}'.format(M)) 

#    print('N: {}'.format(N)) 
    ls = f.readlines()
    
S = ls[0].split()

for i in range(B): 
   S[i] = int(S[i])     
#for i in range(1, 2, 2*L-1):

for i in np.linspace(1, 2*L-1, L):
#    temp = ls[int(i)].split()
    temp = ls[int(i)].split()
    #books can be scanned after once signed up
    N.append(int(temp[0]))
    #days for signed up
    T.append(int(temp[1]))
    #books sent for scanning after once signed up
    M.append(int(temp[2]))
    temp2 = ls[int(i+1)].split() 
    Id = []
    for tp in range(int(temp[0])):
        Id.append(int(temp2[tp])) 
    ID.append(Id)
    
#pre-compute
Sid = []
S_sort = []
Sid_sort = []
for l in range(L):
    temp = []
    Sid.append(ID[l][0:N[l]]) 
    for Id in ID[l][0:N[l]]:
        temp.append(int(S[Id]))
    S_sort.append(np.sort(temp)[::-1])
    temp2 = []
    for tp in list(np.unique(np.sort(temp)[::-1])):
        temp2 += getAll(list(np.sort(temp)[::-1]), ID[l][0:N[l]], tp)[:]
    if np.size(temp2, 0) == 1:
        Sid_sort.append(temp2[0])
    else:
        
        Sid_sort.append(temp2[:])
  
#    for tp in list(np.sort(temp)[::-1]):
#            tempSid_sort.append(list(temp).index(tp))
#            tempSid_sort.append([i for i, v in enumerate(list(temp)) if v == tp ])

#max Score for every library
MaxScore = [] 
for l in range(L):
    Sum = 0
    Comp = min((D-T[l])*M[l], N[l])
    for nb in range(Comp):
       Sum += S_sort[l][nb]
    MaxScore.append(Sum)  

#(Notused)Sort by libraryID
#MaxScore_sort = np.sort(MaxScore)[::-1]
#MaxScoreID_sort = np.argsort(MaxScore)[::-1]
    
#find library by Sorted BookID
#for bs in np.unique(S):
#    Lib_sorted.append(getAll(list(np.sort(S)[::-1]), list(range(B)), bs)[:])

# solution: assgin books for library according to MaxScore decreasingly(Check availability dynamically) 
Check = []
SolID = []
LibId =[]
Score = []
Dt = []
BkId = []

#The first library assigned without extra condition
LibId.append(np.argmax(MaxScore))
Score.append(max(MaxScore))
Dt.append(D-T[np.argmax(MaxScore)])
Comp = min((D-T[np.argmax(MaxScore)])*M[np.argmax(MaxScore)], N[np.argmax(MaxScore)])
for bn in range(Comp):
    BkId.append(Sid_sort[np.argmax(MaxScore)][bn])  
SolID.append(BkId)              
Check = BkId
LibChoice = list(set(range(L)) - set(LibId))
print(SolID)
#Solve(LibChoice, Sid_sort, S_sort, Choice, Check, S, Comp, Score, SolID, D, T, L, B):
for l in LibChoice:
    Sum = 0
    if np.size(Sid_sort[l]) == 1:
        Choice = list(set([Sid_sort[l]]) - set(Check[:]))
    else:
        Choice = list(set(Sid_sort[l][:]) - set(Check[:]))
#    print(Choice)
    if np.size(Choice, 0) > 0:
        if Maxidxlist(Choice,  S_sort[l][:])  >= sum(np.array(S, dtype = int))/len(S):
            Comp = min((D-T[l])*M[l], np.size(Choice, 0))
#            Sum = Sumidxlist(Choice[range(Comp)], S_sort[l][:])
#            Sum = Sumidxlist(Choice[0:Comp], S_sort[l][:])
#            BkId.append(Choice[0:Comp])   
            Output = AddSol(Sid_sort, S_sort, l, Choice, Check, S, Comp, Score, SolID, D, T)                       
            Score = Output[0]
            SolID = Output[1]
            Check = Output[2]       
            LibId = Output[3]
            Dt = Output[4] 
            LibChoice = list(set(range(L)) - set(LibId))
        elif l == LibChoice[-1]:
            if np.size(Check, 0) == B:
                break
            else:
                LibChoice = list(set(range(L)) - set(LibId))
                for l in LibChoice:
                    Sum = Score[l]
                    if np.size(Sid_sort[l]) == 1:
                        Choice = list(set([Sid_sort[l]]) - set(Check[:]))
                    else:
                        Choice = list(set(Sid_sort[l][:]) - set(Check[:]))#                    print(Choice)
                    if np.size(Choice, 0) > 0:
                        Comp = min((D-T[l])*M[l], np.size(Choice, 0))
#            Sum = Sumidxlist(Choice[range(Comp)], S_sort[l][:])
#            Sum = Sumidxlist(Choice[0:Comp], S_sort[l][:])
#            BkId.append(Choice[0:Comp])   
                        Output = AddSol(Sid_sort, S_sort, l, Choice, Check, S, Comp, Score, SolID, D, T)                       
                        Score = Output[0]
                        SolID = Output[1]
                        Check = Output[2]       
                        LibId = Output[3]
                        LibChoice = list(set(range(L)) - set(LibId))
                    if np.size(Check, 0) == B & l == LibChoice[-1]: 
                        break   
        if np.size(Check, 0) == B: 
            break;    
            
print(sum(Score))
LibN = sum(np.array(Score) > 0)        


#output: sort by start_scanning day
#StartDay_sort = np.sort(Dt)
StartDayID_sort = np.argsort(Dt)

with open('/content/202202outd.txt', 'w') as f:
    f.write("%s\n" % str(LibN))    
#library index of valid solutions    
    for l in  range(LibN):
        if np.array(Score)[l] > 0:
            f.write("%s " % str(LibId[l]))
            f.write("%s \n" % str(np.size(SolID[l][0:N[l]], 0)))
#            f.write("%s \n" % str(np.array(SolID[l][:], dtype = int)))
            f.write("%s \n" % str(SolID[l][0:N[l]]))
