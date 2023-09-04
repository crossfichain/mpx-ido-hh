from brownie import *
from brownie.network import priority_fee

def main(is_need_to_publish = True):
	priority_fee("auto")
	mnemonik = ""
	accounts.from_mnemonic(mnemonik)
	account = accounts[0]

	usdt = ""
	team = ""     # team address

	token = Token.deploy("name", "symbol", 2e26, {"from": account}, publish_source=is_need_to_publish) # token for test purposes.

	crowdsale = Crowdsale.deploy(usdt, 10, team, {"from": account}, publish_source=is_need_to_publish) # mpx seller contract.
