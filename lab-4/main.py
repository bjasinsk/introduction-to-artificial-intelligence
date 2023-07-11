import math
import random
import matplotlib.pyplot as plt
import seaborn as sns
from Tree import Tree
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.model_selection import train_test_split
import pandas as pd


def print_tree(node, indent=0):
    print("  " * indent + str(node.type))
    if node.value:
        print("  " * (indent+1) + "Attribute: " + str(node.attribute))
        print("  " * (indent+1) + "Value: " + str(node.value))
        print("  " * (indent+1) + "Class Value: " + str(node.class_value))
    else:
        print("  " * (indent + 1) + "Class Value: " + str(node.class_value))

    for child in node.children:
        print_tree(child, indent+1)

def predict(tree, x):
    if tree.type == "leaf":
        return tree.class_value
    else:
        attribute = tree.attribute
        value = x[attribute]

        for child in tree.children:
            if child.value == value:
                return predict(child, x)

        y_values = frequency_dictionary(tree.dataset)

        max_value = max(y_values.values())
        for y in y_values:
            if y_values[y] == max_value:
                return y


def frequency_dictionary(u):
    y_values = {}
    for x, y in u:
        if y not in y_values:
            y_values[y] = 1
        else:
            y_values[y] += 1
    return y_values

def entropy(u):
    y_values = frequency_dictionary(u)
    result = 0.0
    n = len(u)

    for class_value in y_values:
        v = y_values[class_value] / n
        result -= v * math.log2(v)
    return result

def entropy_subsets(u, d):
    frequency_attributes = {}
    for x, y in u:
        if x[d] not in frequency_attributes:
            frequency_attributes[x[d]] = [(x, y)]
        else:
            frequency_attributes[x[d]].append((x, y))

    result = 0.0
    n = len(u)

    for v in frequency_attributes.values():
        simple_calculation = len(v) / n
        result += simple_calculation * entropy(v)

    return result

def information_gain(u, d):
    return entropy(u) - entropy_subsets(u, d)

def leaf_most_frequent_class(matrix, u):
    y_values = frequency_dictionary(u)

    max_value = max(y_values.values())
    for y in y_values:
        if y_values[y] == max_value:
            return leaf_with_class(matrix, y)


def leaf_with_class(matrix, y):
    selected_data = []
    for row in matrix:
        if row[-1] == y:
            selected_data.append(row)

    return Tree("leaf", None, None, selected_data, None, y)

def id3(matrix, y, d, u, value=None, d_attribute=None):
    y_count = frequency_dictionary(u)

    for y_simple in y:
        if y_simple in y_count and y_count[y_simple] == len(u):
            return leaf_with_class(matrix, y_simple)

    if len(d) == 0:
        return leaf_most_frequent_class(matrix, u)

    max_gain = float('-inf')
    max_attribute = None
    for simple_d in d:
        gain = information_gain(u, simple_d)
        if gain > max_gain:
            max_gain = gain
            max_attribute = simple_d

    d_to_divide = max_attribute

    u_j = {}
    for x, y in u:
        if x[d_to_divide] not in u_j:
            u_j[x[d_to_divide]] = [(x, y)]
        else:
            u_j[x[d_to_divide]].append((x, y))

    sub_trees = []
    for dj, u_j_set in u_j.items():
        sub_trees.append(id3(matrix, y, d - {d_to_divide}, u_j_set, dj, d_to_divide))

    if d_attribute == None and value == None:
        return Tree("root", d_to_divide, None, u, sub_trees)
    else:
        return Tree("node", d_to_divide, value, u, sub_trees)

def random_forest(matrix, y, d, u, b_trees):
    F = []
    n_u = int(0.75*len(u))
    #n_d = math.floor(math.sqrt(len(d)))
    n_d = 6
    for i in range(b_trees):
        ub = random.choices(u, k=n_u)
        db = set(random.sample(list(d), n_d))
        tree_id3 = id3(matrix, y, db, ub)

        print_tree(tree_id3)
        F.append(tree_id3)

    return F

def predict_random_forest(x, F):
    C = []
    for f in F:
        C.append(predict(f, x))
    return max(set(C), key=C.count)

if __name__ == '__main__':

    df = pd.read_csv('nursery.data')
    matrix = df.values

    X_train, X_test, y_train, y_test = train_test_split(matrix[:,:-1], matrix[:,-1], test_size=0.2, random_state=46)


    x_labels = ['parents', 'has_nurs', 'form', 'children', 'housing', 'finance', 'social', 'health']
    y_labels = ['not_recom', 'recommend', 'very_recom', 'priority', 'spec_prior']

    forest = random_forest(list(zip(X_train, y_train)), set(y_train), set(range(X_train.shape[1])), list(zip(X_train, y_train)), 100)

    print("len(X_test) = ", len(X_test))

    predictions = []
    for x in X_test:
        predictions.append(predict_random_forest(x, forest))

    y_true = y_test
    y_pred = predictions

    labels = ['not_recom', 'recommend', 'very_recom', 'priority', 'spec_prior']
    cm = confusion_matrix(y_true, y_pred, labels=labels)
    sns.heatmap(cm, annot=True, cmap='Blues', fmt='g',xticklabels=['not_recom', 'recommend', 'very_recom', 'priority', 'spec_prior'],yticklabels=['not_recom', 'recommend', 'very_recom', 'priority', 'spec_prior'])
    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.show()
    print(cm)

    accuracy = accuracy_score(y_true, y_pred)

    precision = precision_score(y_true, y_pred, average='weighted', zero_division=0)

    recall = recall_score(y_true, y_pred, average='weighted', zero_division=0)

    print("accuracy: ", accuracy)
    print("precision: ", precision)
    print("recall: ", recall)
