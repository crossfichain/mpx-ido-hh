import brownie

from brownie import chain


def test_buyTokens(crowdsale, accounts, tokens):
	(token, stablecoin) = tokens

	account = accounts[0]
	beneficiary = accounts[1]
	spentAmount = 100e18
	multiplier = crowdsale.multiplier()
	initialBalance = stablecoin.balanceOf(account)
	initialCrowdsaleBalance = stablecoin.balanceOf(crowdsale)


	stablecoin.approve(crowdsale, spentAmount, {"from": account})
	crowdsale.buyTokens(beneficiary, spentAmount, {"from": account})

	assert stablecoin.balanceOf(account) == initialBalance - spentAmount
	assert stablecoin.balanceOf(crowdsale) == initialCrowdsaleBalance + spentAmount

	assert crowdsale.tokensSold() == spentAmount * multiplier


def test_allocatedTokens(crowdsale, accounts, tokens):
	(token, stablecoin) = tokens

	account = accounts[0]
	beneficiary = accounts[1]
	spentAmount = 100e18
	multiplier = crowdsale.multiplier()

	stablecoin.approve(crowdsale, spentAmount, {"from": account})
	crowdsale.buyTokens(beneficiary, spentAmount, {"from": account})
	assert crowdsale.allocatedTokens(beneficiary) == spentAmount * multiplier

	stablecoin.approve(crowdsale, spentAmount, {"from": account})
	crowdsale.buyTokens(beneficiary, spentAmount, {"from": account})
	assert crowdsale.allocatedTokens(beneficiary) == spentAmount * multiplier *2


def test_getFunds(crowdsale, accounts, tokens):
	(token, stablecoin) = tokens

	account = accounts[0]
	beneficiary = accounts[1]
	spentAmount = 100e18
	initialTeamBalance = token.balanceOf(accounts[3])

	stablecoin.approve(crowdsale, spentAmount, {"from": account})
	crowdsale.buyTokens(beneficiary, spentAmount, {"from": account})

	initialCrowdsaleBalance = stablecoin.balanceOf(crowdsale)

	crowdsale.getFunds(stablecoin, {"from": account})

	assert stablecoin.balanceOf(accounts[3]) == initialTeamBalance + spentAmount
	assert stablecoin.balanceOf(crowdsale) == initialCrowdsaleBalance - spentAmount

# mainnet-fork test
def test_buyWithUniswap(crowdsaleFork, accounts):

	account = "0x6B175474E89094C44Da98b954EedeAC495271d0F" # account for fork test with tokens.
	stablecoin = brownie.Contract.from_explorer("0xdAC17F958D2ee523a2206206994597C13D831ec7") # usdt
	beneficiary = accounts[1]
	spentAmount = 100e18
	multiplier = crowdsaleFork.multiplier()
	# initialBalance = stablecoin.balanceOf(account)
	# initialCrowdsaleBalance = stablecoin.balanceOf(crowdsale)

	inputToken = brownie.Contract.from_explorer("0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48") # usdc
	fee = 100

	stablecoin.approve(crowdsaleFork, spentAmount, {"from": account})
	crowdsaleFork.buyWithUniswap(inputToken, beneficiary, spentAmount, fee, {"from": account})


	assert crowdsaleFork.tokensSold() == spentAmount * multiplier