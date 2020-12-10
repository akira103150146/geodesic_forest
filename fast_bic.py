import numpy as np
import pandas as pd
import random
import statistics 

def diff_var(n1, n2, w1, w2, sigma1, sigma2):
    if n1 == 1 or n2 == 1:
        return 0
    c1 = n1 * np.log(w1) - (n1/2) * np.log(2*np.pi*sigma1)
    c2 = n2 * np.log(w2) - (n2/2) * np.log(2*np.pi*sigma2)
    return -2 * (c1 + c2)

def parameters(array):
    n = len(array) # length of array
    mean = np.mean(array)# mean
    
    # variance
    if len(array) == 1:
        var = 0
    else:
        var = np.var(array, ddof=1)
    return n, mean, var

def fast_bic(array):
    n = len(array) # length of all elements
    cluster1 = list()
    cluster2 = list()
    
    cluster1.append(array[0])
    cluster1.append(array[1])
    
    mu1 = np.mean(cluster1)# put first element in cluster1
    cluster2 = array[2:]
    mu2 = np.mean(cluster2)
    
    n1, mean1, var1 = parameters(cluster1)
    n2, mean2, var2 = parameters(cluster2)
    w1, w2 = n1/n, n2/n # proportion
    var_combine = (var1*n1 + var2*n2) / n

    if var1 == 0 or 0.0:
        var1 = np.Inf
    if var2 == 0 or 0.0:
        var2 = np.Inf  

    BIC_diff_var = diff_var(n1, n2, w1, w2, var1, var2)
    BIC_same_var = diff_var(n1, n2, w1, w2, var_combine, var_combine)
    BIC_curr = min(BIC_diff_var, BIC_same_var)
    minBIC = BIC_diff_var 
#     print(minBIC)
#     print("diff, same", BIC_diff_var, BIC_same_var)
#     print("BIC_curr", BIC_curr)
    splitpoint = cluster1[-1]
        
    while len(cluster2) > 2:
        # move one element from cluster2 to cluster1
        cluster1.append(cluster2[0])
        cluster2 = cluster2[1:]
#         print("-----")
#         print("cluster1:", cluster1)
#         print("cluster2:", cluster2)
        
        # parameters
        n1, mean1, var1 = parameters(cluster1)
        n2, mean2, var2 = parameters(cluster2)
        w1, w2 = n1/n, n2/n
        var_combine = (var1*n1 + var2*n2) / n

        if var1 == 0 or 0.0:
            var1 = np.Inf
        if var2 == 0 or 0.0:
            var2 = np.Inf  

        BIC_diff_var = diff_var(n1, n2, w1, w2, var1, var2)
        BIC_same_var = diff_var(n1, n2, w1, w2, var_combine, var_combine)
        BIC_curr = min(BIC_diff_var, BIC_same_var)
#         print("diff, same", BIC_diff_var, BIC_same_var)
#         print("BIC_curr", BIC_curr)
        if BIC_curr < minBIC:
            minBIC = BIC_curr
            splitpoint = cluster1[-1]
            
    return splitpoint, minBIC

# test = list()
# for i in range(0,10):
#     n = random.randint(1,10000)
#     test.append(n)
# test.sort()
# # test = [1, 2,3, 4, 5, 6]
# print(parameters(test))
# print(test)


# splitpoint, minBIC = Fast_BIC(test)
# print(splitpoint, minBIC)