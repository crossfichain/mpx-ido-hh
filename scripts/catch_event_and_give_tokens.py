import brownie, web3, time
from brownie import *

import os
from dotenv import load_dotenv
load_dotenv()

def main():
	accounts.from_mnemonic(os.getenv("mnemonic"))
	account = accounts[0]

	spentAmount = 10e18 # 10000000000000000000
	anotherAddress = "0x090BD9F68670FA4788BE057fBD55F05ecD7Da5b9"

	startBlock = web3.eth.blockNumber
	endBlock = 0

	# repeat everything.
	while True:

	### starts from choosed network.
		token = Token.at("0x74cD4787F5aABda9F02eE33493A7fD18BF7F764d") # stable on chosen chain
		crowdsale = Crowdsale.at("0x61A595815Ba0E701d88e9aa9DD899F38f6291A5f") # contract address on chosen chain

		# # call events for tests
		# token.approve(crowdsale, spentAmount, {"from": account})
		# crowdsale.buyTokens(anotherAddress, spentAmount, {"from": account})

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

		startBlock = web3.eth.blockNumber + 1

	### disconnect and connect to xfi.
		brownie.network.disconnect()
		brownie.network.connect('xfi-test')
		accounts.from_mnemonic(os.getenv("mnemonic")) # connect to wallet with mpx
		account = accounts[0]
	###
		mpx = Token.at("0x10D1A6c0C2f4f1AB1924f7271B2Cc95e94e8a223") # token for test purposes. should change to mpx
		# mpx = Contract.from_explorer("") # mpx address

		for i in range(len(beneficiary)):
			mpx.approve(beneficiary[i], amounts[i], {"from": account})
			mpx.transfer(beneficiary[i], amounts[i], {"from": account})

	### disconnect and connect to goerli
		brownie.network.disconnect()
		brownie.network.connect('goerli')
		accounts.from_mnemonic(os.getenv("mnemonic"))
		account = accounts[0]
	###
		time.sleep(30) # should set to needed amount of time to skip.

