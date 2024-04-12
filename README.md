# 2024-Spring-HW2

Please complete the report problem below:

## Problem 1
Provide your profitable path, the amountIn, amountOut value for each swap, and your final reward (your tokenB balance).

> Solution
> 
>Swap(B,A) amountIn:4.151608877446016 amountOut:4.987231595204996\
Swap(A,E) amountIn:4.987231595204996 amountOut:0.9595542289555015\
Swap(E,D) amountIn:0.9595542289555015 amountOut:2.2178059464947353\
Swap(D,C) amountIn:2.2178059464947353 amountOut:4.679637536566986\
Swap(C,A) amountIn:4.679637536566986 amountOut:19.409445452839083\

>Be aware that I still have 5-4.151608877446016 = 0.848391122553984 in my balance before the last swap. Thus I have 20.257836575393068 units of tokenB in the end.

## Problem 2
What is slippage in AMM, and how does Uniswap V2 address this issue? Please illustrate with a function as an example.

> Solution
> Slippage is after a person orders a swap, the price of the wanted token is raised because someone else ordered and finished a swap before your swap was done. i.e the R0, R1 is changed in the following formula for pirce:
$$\frac{R_1r\Delta A}{R_0+r\Delta A}$$
Uniswap has a slippage tolerance system. If the slippage that occured to your swap is more than your set limit, the transaction fails.
```
def calculate_slippage_amount(R_A, R_B, delta_A, slippage_tolerance):

    # Calculate expected amount of token B (delta_B) using constant product formula
    k = R_A * R_B
    R_A_prime = R_A + delta_A
    R_B_prime = k / R_A_prime
    delta_B_expected = R_B - R_B_prime
    
    # Apply slippage tolerance to get the minimum acceptable amount of token B
    delta_B_minimum = delta_B_expected * (1 - slippage_tolerance)
```
>The above function calculates the minimum $\Delta b$ that we can accept. If the resulted swap gets something lower than that, we fail the swap.

## Problem 3
Please examine the mint function in the UniswapV2Pair contract. Upon initial liquidity minting, a minimum liquidity is subtracted. What is the rationale behind this design?

> Solution
> We want to insure that there will always be some liquidity of a token in the pool. This is because the price of our tokens rely heavily on the constant product formula. If the liqudity drops to zero, then there will be a major error in pricing the tokens. Thus, we have the following formula:
$$minted = \sqrt{token1 \times token2} - MINIMUM LIQUIDITY$$

## Problem 4
Investigate the minting function in the UniswapV2Pair contract. When depositing tokens (not for the first time), liquidity can only be obtained using a specific formula. What is the intention behind this?

> Solution
> LP tokens minted= $\frac{Reserve Of Token A}{Deposit Amount Of Token A}\times(TotalSupplyOfLPTokens)$
​
I think this serves 2 very important purposes.
>1. It ensures that the share of LP tokens received is directly proportional to the amount of liquidity a provider adds relative to the existing liquidity in the pool.
>2. It prevents the existing tokens from being diluted after addition of new liquidity. The formula maintains the invariant that the value of one LP token relative to the underlying assets is conserved across any liquidity event.

## Problem 5
What is a sandwich attack, and how might it impact you when initiating a swap?


> Solution
> Basically, the attacker observes the transaction pool, hunting for transactions that may cause substantial slippage(the transaction may be pretty big). Then, the attacker does a transaction by paying higher gas before the big transaction is done. Thus buying before the slippage occurs, and also driving the price up. Then, after the big transaction is done, the victim buys the tokens at an inflated price. The price goes up even more. The attacker now can sell his/her token at a higher price before the slippage. 
>
> This is just my understanding, it may be a bit imprecise.

