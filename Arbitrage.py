from itertools import permutations
alphabetConvert = ['A','B','C','D','E']

initAsset = 5 #initially have 5 units of tokenB


liquidity = {
    ("tokenA", "tokenB"): (17, 10),
    ("tokenA", "tokenC"): (11, 7),
    ("tokenA", "tokenD"): (15, 9),
    ("tokenA", "tokenE"): (21, 5),
    ("tokenB", "tokenC"): (36, 4),
    ("tokenB", "tokenD"): (13, 6),
    ("tokenB", "tokenE"): (25, 3),
    ("tokenC", "tokenD"): (30, 12),
    ("tokenC", "tokenE"): (10, 8),
    ("tokenD", "tokenE"): (60, 25),
}

liquidity_list0 = [
    [0,17,11,15,21],
    [10,0,36,13,25],
    [7,4,0,30,10],
    [9,6,12,0,60],
    [5,3,8,25,0]
]

def optimalPay(remain1, remain2):
    return (remain1*remain2)**0.5-remain1

def getE1E2(path, index, R1, R2, R3, R4):
    E1 = R1*R3/(R3+R2)
    E2 = R2*R4/(R3+R2)
    if (index == len(path)-3):
        return (E1, E2)
    else:
        return getE1E2(path,index+1, E1, E2,liquidity_list0[path[index+2]][path[index+3]], liquidity_list0[path[index+3]][path[index+2]])


def uniswapV2(token1, token2, pay): #Put in token1 in exchange for token2
    oldToken1 = liquidity_list0[token1][token2]  #amount of token1 in pool(1,2)
    oldToken2 = liquidity_list0[token2][token1]
    k = oldToken1 * oldToken2
    newToken1 = oldToken1 + pay
    newToken2 = k/newToken1
    liquidity_list0[token1][token2] = newToken1
    liquidity_list0[token2][token1] = newToken2
    gain = oldToken2 - newToken2
    return gain

def uniswapE1E2(E1, E2, payment):
    gain = E2*payment/(E1+payment)
    profit = gain - payment
    return profit

def arbitrage(path, initPay): #path is a list
    currentGain = uniswapV2(path[0], path[1], initPay)
    for i in range(1,len(path)-1):
        currentGain = uniswapV2(path[i], path[i+1], currentGain)

    balance = currentGain-initPay+initAsset
    return balance

maxbalance = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
# def dfs(steps, start, end, goal, pay, liquidity):
#     if (end == goal and steps == 1):

def cycle1Swap():
    perm = permutations([0,2,3,4])
    paths = [[1] + list(perm) + [1] for perm in perm]
    # paths = [[1,0,4,3,2,1]]
    # paths += perm[0]
    profit = 0
    for i in range(0,len(paths)):
        profit = 0
        E1E2 = getE1E2(paths[i], 0, liquidity_list0[paths[i][0]][paths[i][1]], liquidity_list0[paths[i][1]][paths[i][0]], liquidity_list0[paths[i][1]][paths[i][2]], liquidity_list0[paths[i][2]][paths[i][1]])
        if (E1E2[1] > E1E2[0]):
            payment = (E1E2[0]*E1E2[1])**0.5-E1E2[0]
            # print("payment:", payment)
            delta = payment
            profit = uniswapE1E2(E1E2[0],E1E2[1],payment)
            if (profit > 15):
                # print ("path:", paths[i])
                # print ("profit", profit)
                for j in range(0,len(paths[i])-1):
                    # print("delta:", delta)
                    delta = uniswapV2(paths[i][j], paths[i][j+1], delta)
                # print("delta:", delta);
                print("path: ", end="")
                for j in range(len(paths[i])-1):
                    print(alphabetConvert[paths[i][j]], "->", end="", sep="")
                print(alphabetConvert[paths[i][-1]], end=", ")
                ans = (delta-payment+initAsset)
                print("TokenB balance=:", ans,".",sep="")
        else:
            continue;

        



cycle1Swap()
# paths = [[1,0,2,1],[1,3,2,1],[1,0,3,1],[1,2,0,1],[1,0,3,1],[1,3,2,1]]
# for i in range(0,len(paths)):
#     E1E2 = getE1E2(paths[i], 0, liquidity_list0[paths[i][0]][paths[i][1]], liquidity_list0[paths[i][1]][paths[i][0]], liquidity_list0[paths[i][1]][paths[i][2]], liquidity_list0[paths[i][2]][paths[i][1]])
#     payment = (E1E2[0]*E1E2[1])**0.5-E1E2[0]
#     print("payment:", payment)
#     delta = payment
#     for j in range(0,len(paths[i])-2):
#         delta = uniswapV2(paths[i][j], paths[i][j+1], delta, liquidity_list0)
#     profit += (delta-payment)

# print(profit+initAsset)
# print(uniswapE1E2(E1E2[0], E1E2[1], payment)+initAsset)
# print(arbitrage(path, 4.0386946))
    

# print(uniswapV2(1,0,4.0386))
# print(uniswapV2(0,2,uniswapV2(1,0,4.0386)))
# print(uniswapV2(2,1,uniswapV2(0,2,uniswapV2(1,0,4.0386))))
# print(arbitrage([1,0,2,1], 4.0386946084697115))