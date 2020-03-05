# -*- coding: utf-8 -*-

#@author: Lilyheasamiko
#!pip install ortools

from __future__ import print_function
#from ortools.sat.python import cp_model
from ortools.linear_solver import pywraplp
import numpy as np
from random import sample 
#Compute MaxScore for every unassigned library dynamically
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

def Maxscore():
    Check = []
    MaxScore = [] 
    SolID = []
    LibId =[]
    Dt = []
    maxScore = 0

    LibChoice = list(set(range(L)) - set(LibId[:]))
    while np.size(LibChoice, 0) > 0:
        for l in LibChoice:
            Sum = 0
            Choice = list(set(Sid_sort[l][:]) - set(Check[:]))
            if np.size(Choice, 0) > 0:
                Comp = min([(D-T[l])*M[l], N[l], np.size(Choice, 0)])
                for nb in Choice[0:Comp]:
                    Sum += S_sort[l][nb]
                if Sum > maxScore:
                    maxScore = Sum
                    solId = Choice[0:Comp]
                    Check.append(solId[:])
                    libId = l
        MaxScore.append(maxScore)
        SolID.append(solId)
        LibId.append(libId)
        Dt.append(D-T[np.argmax(libId)])  
        LibChoice = list(set(range(L)) - set(LibId[:]))

def main():
    filepath = '//ad.tuni.fi/home/he/StudentDocuments/Desktop/hcode copy/a_example.txt'
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

    #usage of OR tools
    #create the solver
    solver = pywraplp.Solver('SolveAssignmentProblemMIP',
                           pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)
    #Create the data
    num_books = B
    num_libs = L
    num_days = D
    presign_days = T
    all_books = Sid_sort
    all_libs = range(num_libs)
    all_days = range(num_days)
    scans_scores = S_sort 
#    scans = np.zeros((B, D, L))
    # Creates the model.
    #model = cp_model.CpModel()

# Creates scan variables.
    # scans[(l, d, b)]: library 'l' scan book 'b' on day 'd'. (too large)
    # scans[l, d]: library 'l' scan book 'b' on day 'd'.
    scans = {}
    for l in all_libs:    
    #    for b in all_books[l]:
            # Each library in D days can scan maximal D- T[l] days.
    #        for d in range(all_days[l], D):
        for b in range(B):
              scans[(l, b)] = solver.BoolVar('x%i%i' % (l, b))    
         
    #            scans[b, d, l] = model.NewBoolVar('scan_%id%id%id' % (l, d, b))
    #            scans[(l, b)] = solver.BoolVar('x[%i, %i]' % (l, b))
    
  # Create constraints
    # Each library has N[l] books in all
              ct = solver.Constraint(0, min(N[l],M[l]*(D - all_days[l])), 'ct')
              if b in all_books[l]:
    #for l in all_libs:
    #    solver.Add(solver.Sum(scans[l, b] for b in all_books[l]) <= N[l])
    # Each library can scan maximal M[l] books per day, with scanning days D-T[l]        
       # One loosened condition: Each book scanned at most one library and on one day counted(Non-repitition)
                  ct.SetCoefficient(scans[(l, b)], S[b])
              else:
                  ct.SetCoefficient(scans[(l, b)], 0)   
    for b in range(B):
        for l in all_libs:
             ct.SetCoefficient(scans[(l, b)], 1)         
    #objective function : maxScore 
    #solver.Maximize(solver.Sum(scans_scores[l][b] * scans[l, b]))

    # Invoke the solver
    # Creates the solver and solve.
    objective = solver.Objective()
    for l in all_libs:
          for b in all_books[l]: 
                objective.SetCoefficient(scans[(l, b)], S[b])
    objective.SetMaximization()

    sol = solver.Solve()
    print('Total score = ', solver.Objective().Value())
    print(solver.Sum(solver.Sum(solver.Value(scans[l, b]) for b in all_books)>0 for l in all_libs))
    for l in all_libs:
        if solver.Sum(solver.Sum(scans[l, b]) for b in all_books)>0 :
            print(l, ' ', solver.Sum(scans[l, b] for b in all_books),'\n')
            print(all_books[l]*scans[l, b], '\n')
#    for l in all_libs:
#        print('Day', d)
#        for b in all_books:
#            for d in range(D - all_days[l]):
#                if solver.Value(shifts[(b, d, l)]) == 1:
#                    if scans[(b, d, l)] == 1:
#                        print('Nurse', n, 'works shift', s, '(requested).')
#                    else:
#                        print('Nurse', n, 'works shift', s, '(not requested).')
#        print()
#    for l in all_libs:
#        print(sum(scans[(b, d, l)] for d in all_days[all_days[l] != 0]), sum(scans[(b, d, l)] for b in all_books[all_books[l] != 0]), '\n')
#        while scans[(b, d, l)]== 1: print(b) 
    # Statistics
    print()
    print('Statistics')
    print('  - wall time       : %f ms' % solver.WallTime())

if __name__ == '__main__':
    main()
