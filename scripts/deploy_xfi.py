from brownie import *

import os
from dotenv import load_dotenv
load_dotenv()

def main():
	accounts.from_mnemonic(os.getenv("mnemonic"))
	account = accounts[0]

	token = Token.deploy("test", "test", 2e26, {"from": account}) # token for test purposes. should change to test mpx

	vault = MpxVault.deploy(token.address, {"from": account}) # mpx giver contract.

	# need to fill vault with tokens.
