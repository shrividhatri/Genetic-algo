# Genetic-algo

Team members:

1. Shri Vidhatri M M - 2019113006
2. Anandhini Rajendran - 2019101055

# Genetic algorithm

It is a search-based optimisation technique based on Darwin's principles of Natural selection. It is inspired by genetics and can be used to find near-optimal solutions which are very inefficient when solved in the traditional techniques. Genetic algorithms do not need any derivative information and have very good parallel capabilities thus giving a set of good solutions instead of a single solution.

## Terminologies:

### Population:

A subset of all possible solutions to the problem in that particular state, analogous to the biological term of a population meaning a group of individuals in that current time.

### Chromosomes:

One particular solution given for the problem

### Gene:

One element in the chromosome

### Allele:

The value a gene takes in a particular chromosome

### Generation:

The evolution usually starts from a population of randomly generated individuals and is an iterative process, and the population in each iteration called a generation

### Selection:

The process of selecting parents which mate and recombine to create offsprings

### Offsprings/children:

The new population generated after the mating of parents and mutation if any.

### Mating pool:

The mating pool is formed by candidate solutions that the selection operators deem to have the highest fitness in the current population.

### Mutation:

Mutation is a genetic operator used to maintain genetic diversity from one generation of a population of genetic algorithm chromosomes to the next using random changes.

## The given problem:

We have been given a vector of size 11 which represents the coefficients of features to a dataset currently unknown to us. The vector given corresponds to an overfit model and we are expected to use a genetic algorithm to generalise the model to perform better on unseen data.

Based on the train and validation error output from the dataset, we have attempted varying different hyperparameters (see below) to achieve a better solution than the one we started with.  

## Understanding the algorithm

The basic structure of Genetic algorithm can be understood as:

- initial population( random or seeded by an overfit vector)
- select parents for mating
- apply crossover and mutation operators to generate new offsprings
- offsprings replace the existing individuals in the population

![Images/basic_structure.jpg](Images/basic_structure.jpg)

The algorithm is visually understood from the above image. A generaised psudo-code for the same could be:

```python
Genetic_Algorithm()
   initialize population
   find fitness of the population
   
   while (termination criteria is reached) do
      parent selection
      crossover with probability pc
      mutation with probability pm
      decode and fitness calculation
      survivor selection
      find best
   return best
```

## Various functions:

### Initial population:

```python
def init_population():
    for i in range(population_size):
        parent_array[i] = mutation(parent_array[i])
```

We start the genetic algorithm by an initial population of size defined by the variable ***population_size.***

We have observed that the entire population if initialised using the overfit vector, results in having similar sultions and reduced diversity

Thus we have opted for initialising the parent array with all zero vectors and mutating them according to the mutation probability since it is the diversity in the population that ultimately leads to optimality.

### Fitness function:

```python
def fitness_calc_parent():
    for i in range(population_size):
        t_error, v_error = get_errors(SECRET_KEY,parent_array[i])
        f = a*t_error+b*v_error
        t_err_parent[i] = t_error
        v_err_parent[i] = v_error
        fitness_parent[i] = f
```

 

The fitness function is calculated using the train and validation errors that were obtained from the server requests. The values ***a*** and ***b*** were varied to get a better idea of the errors. The values worked well since both the train errors and validation errors were large and a perfect balance among them enabled us to reduce them simultaneously.

### Mating pool selection & crossover:

Mating pool selection for selecting parents of the next generations can be done in various ways.

One of those ways is fitness proportionate selection where the individual becomes a parent with a probability that is proportional to its fitness enabling the fitter individuals to have higher mating opportunities.

This type of selection can be viewed as Roulette wheel selection which follows the logic of calculating the sum of fitness, generating a random number x below the sum and keep adding the fitness of the individuals until the value of x is crossed and the last individual thus selected is the chosen one. This process is repeated until we get the desired number of parents for mating.

There are many other ways such as stochastic universal sampling, tournament selection, rank selection and so on.

```python
def create_child_array():
    test_list = fitness_parent
    K = no_of_children
    index = sorted(range(len(test_list)), key = lambda sub: test_list[sub])[:K]
    g = 0
    for i in range(no_of_children):
        p1 = parent_array[random.choice(index)]
        p2 = parent_array[random.choice(index)]
        c1,c2 = cross_over(p1,p2)
        child_array[g] = mutation(c1)
        child_array[g+1] = mutation(c2)
        g = g+2
```

In this genetic algorithm code, we have written, we have chosen the rank selection algorithm which was fast and effective.

In this kind of mating pool selection, we have sorted the fitness of all the prospective parents ( a combination of previous generation parents and children) and
