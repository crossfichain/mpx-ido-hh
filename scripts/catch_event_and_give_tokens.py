import brownie, web3, time
from brownie import *

import os
from dotenv import load_dotenv
load_dotenv()

def main():
	accounts.from_mnemonic(os.getenv("mnemonic"))
	account = accounts[0]

	# token = Token.deploy("name", "symbol", 2e26, {"from": account}) # token for test purposes.
	# crowdsale = Crowdsale.deploy(token, 10, account, {"from": account}) # mpx seller contract.

	spentAmount = 10e18 # 10000000000000000000
	anotherAddress = "0x090BD9F68670FA4788BE057fBD55F05ecD7Da5b9"

	startBlock = web3.eth.blockNumber
	endBlock = 0

	# repeat everything.
	while True:

	### starts from choosed network.
		token = Token.at("0x74cD4787F5aABda9F02eE33493A7fD18BF7F764d") # stable on chosen chain
		crowdsale = Crowdsale.at("0x61A595815Ba0E701d88e9aa9DD899F38f6291A5f") # contract address on chosen chain

		# call events for tests
		# token.approve(crowdsale, spentAmount, {"from": account})
		# crowdsale.buyTokens(anotherAddress, spentAmount, {"from": account})
		# token.approve(crowdsale, spentAmount + 20e18, {"from": account})
		# crowdsale.buyTokens(account, spentAmount+20e18, {"from": account})
		# token.approve(crowdsale, spentAmount+1e18, {"from": account})
		# crowdsale.buyTokens("0x000000000000FA4788BE057fBD55F05ecD000000", spentAmount+1e18, {"from": account})

		endBlock = web3.eth.blockNumber # last block to scan for events.

		# get all events from start to last block.
		event = crowdsale.events.get_sequence(from_block=startBlock, to_block=endBlock, event_type="BoughtTokens")

		i = 0
		amounts = []
		beneficiary = []
		print(len(event))
		for i in range(len(event)):
			amounts.append(event[i]['args']['tokensAmount'])
			beneficiary.append(event[i]['args']['beneficiary'])
			print(amounts[i])
			print(beneficiary[i])
			i += 1

		print(amounts)
		print(beneficiary)
		print(web3.eth.blockNumber)
		# startBlock += 10
		startBlock = web3.eth.blockNumber

	### disconnect and connect to xfi.
		brownie.network.disconnect()
		brownie.network.connect('xfi-test')
		accounts.from_mnemonic(os.getenv("mnemonic"))
		account = accounts[0]
	###

		vault = MpxVault.at("0x3284aCCE00DAd27CFB22c6f5fe6FBEB2a809F901") # mpx vault address on xfi.
		vault.batchAllocateTokens(beneficiary, amounts, {"from": account}) # give mpx on xfi

	### disconnect and connect to goerli
		brownie.network.disconnect()
		brownie.network.connect('goerli')
		accounts.from_mnemonic(os.getenv("mnemonic"))
		account = accounts[0]
	###
		time.sleep(30) # should set to needed amount of time to skip.

