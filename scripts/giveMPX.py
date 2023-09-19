from brownie import *

import os
from dotenv import load_dotenv
load_dotenv()

def main():
	accounts.from_mnemonic(os.getenv("mnemonic"))
	account = accounts[0]

	vault = MpxVault.at("")

	beneficiary = ""
	giveAmount =

	vault.allocateTokens(beneficiary, giveAmount, {"from": account}) # give mpx on xfi
