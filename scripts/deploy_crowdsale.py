from brownie import *
from brownie.network import priority_fee

import os
from dotenv import load_dotenv
load_dotenv()

def main(is_need_to_publish = False):
	priority_fee("auto")
	accounts.from_mnemonic(os.getenv("mnemonic"))
	account = accounts[0]

	usdt = ""
	team = account     # team address

	token = Token.deploy("name", "symbol", 2e26, {"from": account}, publish_source=is_need_to_publish) # token for test purposes.

	crowdsale = Crowdsale.deploy(token, 10, team, {"from": account}, publish_source=is_need_to_publish) # mpx seller contract.
