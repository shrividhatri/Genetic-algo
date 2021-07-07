import json
import requests
from client import *
import random

#secret key
SECRET_KEY = 'phNQbyYl7SruDzXTYojd8MOKKi1csMsFbr3sdEofhjWIyIPfFg'

#initial  vectors
#w1 = [-10, 0, -10, 0 , -10.75214813e-2, -2.29999999e-14,  -10,  +2.335999999e-05, -2.04999999e-06, -1.59811999e-08,  +9.99000000e-10]
#w2 = [0,0,0,0,0,0,0,0,0,0,0]
#w3 = [0.0, -1.45799022e-12, -2.28980078e-13,  4.62010753e-11, -1.75214813e-10, -1.83669770e-15,  8.52944060e-16,  2.29423303e-05, -2.04721003e-06, -1.59792834e-08,  9.98214034e-10]

#variables
no_params = 11  #no of parameters
a = 1           #factor to multiply with t_error
b = 1           #factor to multiply with v_error
population_size = 10
size = (population_size,no_params)  #size of population vector
power = 3
probability = 4    #probability for mutation between 1 and 11
no_of_children = 5  #no of parents to be mated
parents_in_generation = 10 #no of parents taken from parent array
num_generation = 200
#index array
index = [0 for i in range(no_of_children)]

#fitness array
cols = (population_size) 
fitness_parent = [0 for i in range(cols)]
fitness_child = [0 for i in range(cols)]
t_err_parent = [0 for i in range(cols)] 
v_err_parent = [0 for i in range(cols)] 
t_err_child = [0 for i in range(cols)] 
v_err_child = [0 for i in range(cols)] 

#population 2d array
r,c = size
parent_array = [[0 for i in range(c)] for j in range(r)]
child_array = [[0 for i in range(c)] for j in range(r)]
temp_array = [[0 for i in range(c)] for j in range(r)]


def fitness_calc_parent():
    for i in range(population_size):
        t_error, v_error = get_errors(SECRET_KEY,parent_array[i])
        f = a*t_error+b*v_error
        t_err_parent[i] = t_error
        v_err_parent[i] = v_error
        fitness_parent[i] = f
def fitness_calc_child():
    for i in range(population_size):
        t_error, v_error = get_errors(SECRET_KEY,child_array[i])
        f = a*t_error+b*v_error
        t_err_child[i] = t_error
        v_err_child[i] = v_error
        fitness_child[i] = f
def calculate_b():
    x = random.uniform(0,1)
    y = x-0.5
    if(y>=0):
        b = ((2*(1-x))**-1)**((power+1)**-1)
    else:
        b = (2*x)**((power+1)**-1)
    return b

def cross_over(parent_1,parent_2):
    """print()
    print('Mating pool')
    print('parent 1 : ',end ='')
    print(parent_1)
    print('parent 2 : ',end ='')
    print(parent_2)"""
    child_1 = []
    child_2 = []
    factor = calculate_b()
    f1 = (factor+1)/2
    f2 = (1 - factor)/2
    for i in range(no_params):
        child_1.append(parent_1[i]*f1 + parent_2[i]*f2)
        child_2.append(parent_2[i]*f1 + parent_1[i]*f2)
    """print('child 1 : ',end ='')
    print(child_1)
    print('child 2 : ',end ='')
    print(child_2)  
    print()"""
    return child_1,child_2


def mutation(vector):
    for i in range(no_params):
        prob = random.randint(1,11)
        
        if(prob<probability):
            if abs(vector[i]*random.uniform(-0.95,1.05))<=10 :
                if vector[i] ==  0 : 
                    vector[i] = random.uniform(-0.05,0.05)
                else:
                    vector[i] = vector[i]*random.uniform(-0.95,1.05)
            else : 
                vector[i] = random.uniform(-1,1)
    """print('child vector after mutation')
    print(vector)
    print()"""
    return vector

def init_population():
    for i in range(population_size):
        parent_array[i] = mutation(parent_array[i])

    
def create_child_array():
    test_list = fitness_parent
    K = no_of_children
    index = sorted(range(len(test_list)), key = lambda sub: test_list[sub])[:K]
    g = 0
    for i in range(no_of_children):
        p1 = parent_array[random.choice(index)]
        p2 = parent_array[random.choice(index)]
        c1,c2 = cross_over(p1,p2)
        """print('child1 before mutation')
        print(c1)"""
        child_array[g] = mutation(c1)
        """print('child2 before mutation')
        print(c2)"""
        child_array[g+1] = mutation(c2)
        g = g+2

def create_generation():
    test_list = fitness_parent
    K = 5
    index1 = sorted(range(len(test_list)), key = lambda sub: test_list[sub])[:K]
    test_list = fitness_child
    K = population_size-5
    index2 = sorted(range(len(test_list)), key = lambda sub: test_list[sub])[:K]
    k = 0
    for i in index1:
        temp_array[k] = parent_array[i]
        k = k+1
    for j in index2:
        temp_array[k] = child_array[j]
        k = k+1
    for i in range(population_size):
        parent_array[i] = temp_array[i]

if __name__=="__main__":
    init_population()
    for i in range(num_generation):
        print("GENERATION : ",end="")
        print(i)

        print("PARENT ARRAY : ")
        print(parent_array)

        print("FITNESS ARRAY OF PARENT : ")
        fitness_calc_parent()
        print(fitness_parent)
        print("test error of parent : ")
        print(t_err_parent)
        print("validation error of parent : ")
        print(v_err_parent)

        print("CHILD ARRAY : ")
        create_child_array()
        print(child_array)

        print("FITNESS ARRAY OF CHILD ")
        fitness_calc_child()
        print(fitness_child)
        print("test error of child : ")
        print(t_err_child)
        print("validation error of child : ")
        print(v_err_child)

        create_generation()
    

