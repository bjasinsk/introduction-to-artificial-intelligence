# Introduction-to-Artificial-Intelligence lab-4

Exercise 4

The aim of the lab is to implement a random forest algorithm and perform classification for a given dataset.

## Assumptions

- The task of classifying the admission of children to kindergarten based on information about the structure and finances of the family. The set is formed by 12960 observations - 5 classes of which 3 of them have similar abundance (more than 4000 observations) and 2 are rare (2 and 328 observations).
- In the random forest algorithm, the id3 algorithm was used to create a single tree
- All measurements were performed using the same seed of randomness when selecting the split between the training and testing set
- The random tree in the applied id3 algorithm generates as many levels in the tree as it receives attributes in the set D passed as a parameter. There are therefore no repetitions in the nodes of the same attributes.
- In the random forest algorithm, I varied and studied the effect of depth, i.e. the parameter n_d, which is the number of attributes drawn from the main set D without repetitions (the set D consists of all attributes present in the shared file nursery.data:`'parents', 'has_nurs', 'form', 'children', 'housing', 'finance', 'social', 'health'`).
- To run the program, place the file nursery.data, which is the data on which the algorithm operates, in the same directory
