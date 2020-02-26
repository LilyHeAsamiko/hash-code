''''''
LilyHeAsamiko
''''''''''''''''''''''''''''''''
import numpy as np
from random import * 

filepath = 'C:/Users/he/Downloads/c_medium.in' 


#def imprvdGreedy(S, M, N, p):
#    sum = 0
#    idx = list(range(N))
#    idx1 = sample(range(N), k = int(N*p))
#    solidx = []
#    sol = []
#    check = [];
##    if sum(np.array(S[idx1]))< M 
#    for i in idx:
#        
#        if i in idx1:
#            solidx.append(i)
#            sol.append(S[i])
#            check.append(i)
#            sum += S[i]        
#            if sum == M:
#                print(len(sol),sol)
##                return [len(sol),sol]
#            elif sum > M:
#                solidx.pop(i)
#                sol.pop(S[i])
#        elif len(check) == len(idx1):
#            if i not in idx1:
#                solidx.append(i)
#                sol.append(S[i])
#                check.append(i)
#                sum += S[i]        
#                if sum == M:
#                    print(len(sol),sol)
##                    return [len(sol),sol]
#                elif sum > M:
#                    solidx.pop(j)
#                    sol.pop(S[j])
#                if i == idx[-1]:
#                    sol = []
#                    solidx = []
#                    print(check)
#                    check = []
#                    imprvdGreedy(S, N, p)
#                    print('false')
#                    return false


def imprvdGreedy2(S, M, N, idx, idx1):
    Sum = 0
    solidx = []
    sol = []
    check = [];
    for i in idx:        
        if i in idx1:
            solidx.append(i)
            sol.append(S[i])
            check.append(i)
            Sum += S[i]        
            if Sum == M:
                print(len(sol),sol, Sum)
  #              return list([len(sol),sol, Sum])
  #              return sol
            elif Sum > M:
                solidx.pop(i)
                sol.pop(S[i])
        elif len(check) == len(idx1):
            if i not in idx1:
                solidx.append(i)
                sol.append(S[i])
                check.append(i)
                Sum += S[i]        
                if Sum == M:
                    print(len(sol),sol, Sum)
#                    return  list([len(sol),sol, Sum])
#                    return sol
                elif Sum > M:
                    solidx.pop(j)
                    sol.pop(S[j])
                if i == idx[-1]:
                    print(check)
#                    shuffle
#                    imprvdGreedy(S, M, N, idx, idx1)
                    print('false')
#                    return list([len(sol),sol, Sum])  
#                    return sol

with open(filepath) as f: 

    first_line = f.readline().split() 

    M = int(first_line[0]) 

    N = int(first_line[1]) 

    print('M: {}'.format(M)) 

    print('N: {}'.format(N)) 

     

    S = f.readline().split() 

for i in range(N): 

    S[i] = int(S[i]) 

#        print('S[{}]: {}'.format(i, S[i])) 

 
p = 0.8
#    imprvdGreedy(S, M, N, p)
idx = list(range(N))
idx1 = sample(range(N), k = int(N*p))
Nsol = 0
Sol = []
Msol = 0
T = 1000
while T > 0:
    Soltemp = imprvdGreedy2(S, M, N, idx, idx1)
#        [Ntemp, Soltemp, Mtemp] = imprvdGreedy2(S, M, N, idx, idx1)
        
 #       if Mtemp > Msol & Mtemp != M:
#            Nsol = Ntemp
#            Sol = Soltemp            
#        elif Mtemp == Msol:
#            break
#        T -= 1            
    if sum(Soltemp) > Msol & sum(Soltemp) != M:
       Msol = sum(Soltemp)
       Sol = Soltemp            
    elif Mtemp == Msol:
       Nsol = len(Soltemp)
       Sol = Soltemp  
       break
    T -= 1
