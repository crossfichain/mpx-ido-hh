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

	crowdsale.getFunds({"from": account})

	assert stablecoin.balanceOf(accounts[3]) == initialTeamBalance + spentAmount
	assert stablecoin.balanceOf(crowdsale) == initialCrowdsaleBalance - spentAmount

