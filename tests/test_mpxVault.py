import brownie

from brownie import chain

def test_allocateTokens(mpxVault, accounts, tokens):
	(mpx, token1) = tokens
	account = accounts[0]
	beneficiary = accounts[1]

	account = accounts[0]
	beneficiary = accounts[1]
	amount = 100e18
	initialBalance = mpx.balanceOf(beneficiary)
	initialmpxVaultBalance = mpx.balanceOf(mpxVault)

	mpxVault.allocateTokens(beneficiary, amount, {"from": account})
	assert mpxVault.allocatedTokens(beneficiary) == amount
	assert mpx.balanceOf(beneficiary) == initialBalance + amount
	assert mpx.balanceOf(mpxVault) == initialmpxVaultBalance - amount

	mpxVault.allocateTokens(beneficiary, amount, {"from": account})
	assert mpxVault.allocatedTokens(beneficiary) == amount*2
	assert mpx.balanceOf(beneficiary) == initialBalance + amount*2
	assert mpx.balanceOf(mpxVault) == initialmpxVaultBalance - amount*2

	with brownie.reverts("Ownable: caller is not the owner"):
		mpxVault.allocateTokens(beneficiary, amount, {"from": beneficiary})

def test_batchAllocateTokens(mpxVault, accounts, tokens):
	(mpx, token1) = tokens
	account = accounts[0]
	beneficiary = [accounts[1], accounts[2], accounts[3]]
	amounts = [100e18, 10e18, 20e18]

	initialBalance = mpx.balanceOf(accounts[1])
	initialBalance1= mpx.balanceOf(accounts[2])
	initialBalance2 = mpx.balanceOf(accounts[3])
	initialmpxVaultBalance = mpx.balanceOf(mpxVault)

	mpxVault.batchAllocateTokens(beneficiary, amounts, {"from": account})
	assert mpxVault.allocatedTokens(accounts[1]) == 100e18
	assert mpxVault.allocatedTokens(accounts[2]) == 10e18
	assert mpxVault.allocatedTokens(accounts[3]) == 20e18

	assert mpx.balanceOf(accounts[1]) == initialBalance + 100e18
	assert mpx.balanceOf(accounts[2]) == initialBalance1 + 10e18
	assert mpx.balanceOf(accounts[3]) == initialBalance2 + 20e18
	assert mpx.balanceOf(mpxVault) == initialmpxVaultBalance - 130e18

	mpxVault.batchAllocateTokens(beneficiary, amounts, {"from": account})
	assert mpxVault.allocatedTokens(accounts[1]) == 100e18 * 2
	assert mpxVault.allocatedTokens(accounts[2]) == 10e18 * 2
	assert mpxVault.allocatedTokens(accounts[3]) == 20e18 * 2

	assert mpx.balanceOf(accounts[1]) == initialBalance + 100e18*2
	assert mpx.balanceOf(accounts[2]) == initialBalance1 + 10e18*2
	assert mpx.balanceOf(accounts[3]) == initialBalance2 + 20e18*2
	assert mpx.balanceOf(mpxVault) == initialmpxVaultBalance - 130e18*2

	with brownie.reverts("Ownable: caller is not the owner"):
		mpxVault.batchAllocateTokens(beneficiary, amounts, {"from": accounts[1]})
	with brownie.reverts("beneficiary should match amounts"):
		mpxVault.batchAllocateTokens(beneficiary, [10, 20], {"from": account})



