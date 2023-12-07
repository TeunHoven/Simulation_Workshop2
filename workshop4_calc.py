import pandas
import numpy as np

# Returns the Beta matrix
def getBeta(X, Y):
    beta = pandas.DataFrame(np.dot(np.dot(X.getT(), X).getI(), np.dot(X.getT(), Y)))
    return beta

## Gets the estimated covariance
def getEstimatedCovariance(Y):
    cov_full = []

    tests = len(Y[0])-1

    for i in range(len(Y)):
        cov_row = []
        yi = Y[i][tests]
        const = 1/((tests-1)*(tests-2)) 
        for j in range(len(Y)):
            yj = Y[j][tests]
            cov = 0
            for l in range(10):
                cov += (Y[i][l]-yi)*(Y[j][l]-yj)
            cov = const*cov
            cov_row.append(cov)
        cov_full.append(cov_row)

    return pandas.DataFrame(np.matrix(cov_full))

#
#   READ DATA
#

data1 = pandas.read_csv("Data/4,4,DISTRIBUTION.EXPONENTIAL(25_0),DISTRIBUTION.EXPONENTIAL(40_0),DISTRIBUTION.EXPONENTIAL(40_0),(False_0)/data.csv")
x1 = [4, 4, 25, 0, 40, 0, 40, 0]
ydata1 = data1['avg queue length'].loc[0:10]
y1 = data1['avg queue length'].loc[10]
std1 = data1['std dev queue'].loc[10]
data2 = pandas.read_csv("Data/4,4,DISTRIBUTION.EXPONENTIAL(25_0),DISTRIBUTION.EXPONENTIAL(40_0),DISTRIBUTION.UNIFORM(30_50),(False_0)/data.csv")
x2 = [4, 4, 25, 0, 40, 0, 30, 50]
ydata2 = data2['avg queue length'].loc[0:10]
y2 = data2['avg queue length'].loc[10]
std2 = data2['std dev queue'].loc[10]
data3 = pandas.read_csv("Data/4,5,DISTRIBUTION.UNIFORM(20_30),DISTRIBUTION.EXPONENTIAL(40_0),DISTRIBUTION.UNIFORM(30_50),(False_0)/data.csv")
x3 = [4, 5, 20, 30, 40, 0, 30, 50]
ydata3 = data3['avg queue length'].loc[0:10]
y3 = data3['avg queue length'].loc[10]
std3 = data3['std dev queue'].loc[10]
data4 = pandas.read_csv("Data/4,5,DISTRIBUTION.UNIFORM(20_30),DISTRIBUTION.UNIFORM(30_50),DISTRIBUTION.UNIFORM(30_50),(False_0)/data.csv")
x4 = [4, 5, 20, 30, 30, 50, 30, 50]
ydata4 = data4['avg queue length'].loc[0:10]
y4 = data4['avg queue length'].loc[10]
std4 = data4['std dev queue'].loc[10]
data5 = pandas.read_csv("Data/5,4,DISTRIBUTION.UNIFORM(20_25),DISTRIBUTION.EXPONENTIAL(40_0),DISTRIBUTION.EXPONENTIAL(40_0),(False_0)/data.csv")
x5 = [5, 4, 20, 25, 40, 0, 40, 0]
ydata5 = data5['avg queue length'].loc[0:10]
y5 = data5['avg queue length'].loc[10]
std5 = data5['std dev queue'].loc[10]
data6 = pandas.read_csv("Data/5,4,DISTRIBUTION.UNIFORM(20_25),DISTRIBUTION.UNIFORM(30_50),DISTRIBUTION.EXPONENTIAL(40_0),(False_0)/data.csv")
x6 = [5, 4, 20, 25, 30, 50, 40, 0]
ydata6 = data6['avg queue length'].loc[0:10]
y6 = data6['avg queue length'].loc[10]
std6 = data6['std dev queue'].loc[10]
data7 = pandas.read_csv("Data/5,5,DISTRIBUTION.EXPONENTIAL(22.5_0),DISTRIBUTION.UNIFORM(30_50),DISTRIBUTION.EXPONENTIAL(40_0),(False_0)/data.csv")
x7 = [5, 5, 22.5, 0, 30, 50, 40, 0]
ydata7 = data7['avg queue length'].loc[0:10]
y7 = data7['avg queue length'].loc[10]
std7 = data7['std dev queue'].loc[10]
data8 = pandas.read_csv("Data/5,5,DISTRIBUTION.UNIFORM(20_30),DISTRIBUTION.UNIFORM(30_50),DISTRIBUTION.UNIFORM(30_50),(False_0)/data.csv")
x8 = [5, 5, 20, 30, 30, 50, 30, 50]
ydata8 = data8['avg queue length'].loc[0:10]
y8 = data8['avg queue length'].loc[10]
std8 = data8['std dev queue'].loc[10]

X = np.matrix([x1, x2, x3, x4, x5, x6, x7, x8])
Y = np.matrix([[y1], [y2], [y3], [y4], [y5], [y6], [y7], [y8]])

Y_cov = [ydata1, ydata2, ydata3, ydata4, ydata5, ydata6, ydata7, ydata8]


print(f"Covariance: \n{getEstimatedCovariance(Y_cov)}")

print(Y)
print(f"{std1} {std2} {std3} {std4} {std5} {std6} {std7} {std8}")

beta = getBeta(X, Y)

std = np.std([std1, std2, std3, std4, std5, std6, std7, std8])

cov_beta = pandas.DataFrame(np.dot(X.getT(), X).getI() * std)

all_index_removals = []

print(beta)

found = True

while found:
    i = 0
    found = False
    beta = getBeta(X, Y)
    remove_index = []

    for b in beta.loc[:, 0]:
        rounded = round(b, 1)
        print(f"Beta: {b}")
        print(f"Rounded: {rounded}")

        if rounded <= 0.1 and rounded >= -0.1:
            found = True
            remove_index.append(i)

        i += 1

    remove_index.reverse()

    for idx in remove_index:
        x1.pop(idx)
        x2.pop(idx)
        x3.pop(idx)
        x4.pop(idx)
        x5.pop(idx)
        x6.pop(idx)
        x7.pop(idx)
        x8.pop(idx)

    if len(remove_index) != 0:
        all_index_removals.append(remove_index)
    print(all_index_removals)
    X = np.matrix([x1, x2, x3, x4, x5, x6, x7, x8])
    Y = np.matrix([[y1], [y2], [y3], [y4], [y5], [y6], [y7], [y8]]) 


data9 = pandas.read_csv("Data/4,5,DISTRIBUTION.EXPONENTIAL(22.5_0),DISTRIBUTION.UNIFORM(30_50),DISTRIBUTION.EXPONENTIAL(40_0),(False_0)/data.csv")
std9 = data9['std dev queue'].loc[10]
avg9 = data9['avg queue length'].loc[10]
x9 = [4, 5, 22.5, 0, 30, 50, 40, 0]

data10 = pandas.read_csv("Data/4,4,DISTRIBUTION.UNIFORM(20_25),DISTRIBUTION.EXPONENTIAL(40_0),DISTRIBUTION.UNIFORM(30_50),(False_0)/data.csv")
std10 = data10['std dev queue'].loc[10]
avg10 = data10['avg queue length'].loc[10]
x10 = [5, 5, 20, 25, 40, 0, 30, 50]

for indices in all_index_removals:
    for idx in indices:
        x9.pop(idx)
        x10.pop(idx)

x9 = np.matrix(x9)
x10 = np.matrix(x10)

std = np.std([std1, std2, std3, std4, std5, std6, std7, std8])

cov_beta = pandas.DataFrame(np.dot(X.getT(), X).getI() * std)

print(cov_beta)
print(beta)

#### Test the model

y_test9 = np.dot(x9, beta)
y_test10 = np.dot(x10, beta)

sim_value9 = avg9
sim_value10 = avg10

print(f"Test 9 - Predicted: {y_test9} || Sim Value: {sim_value9}")
print(f"\tStd: {std9} || CI_lower: {sim_value9-1.96*(std9/np.sqrt(10))} || CI_lower: {sim_value9+1.96*(std9/np.sqrt(10))}")
print(f"Test 10 - Predicted: {y_test10} || Sim Value: {sim_value10} ")
print(f"\tStd: {std10} || CI_lower: {sim_value10-1.96*(std10/np.sqrt(10))} || CI_lower: {sim_value10+1.96*(std10/np.sqrt(10))}")

z9 = (sim_value9 - y_test9)/np.sqrt(np.sqrt(std9)-np.sqrt(np.std(y_test9)))
z10 = (sim_value10 - y_test10)/np.sqrt(np.sqrt(std9)-np.sqrt(np.std(y_test10)))

print(f"Test 9 - Z-value: {z9}")
print(f"Test 10 - Z-value: {z10}")
