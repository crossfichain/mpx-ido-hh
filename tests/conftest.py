import pytest
import brownie

from brownie import chain

@pytest.fixture(scope="function", autouse=True)

def isolate(fn_isolation):

	# perform a chain rewind after completing each test, to ensure proper isolation
	# https://eth-brownie.readthedocs.io/en/v1.10.3/tests-pytest-intro.html#isolation-fixtures
	pass


@pytest.fixture(scope="module")
def crowdsale(accounts, Crowdsale, tokens):
	(mpx, stablecoin) = tokens

	crowdsale = Crowdsale.deploy(stablecoin, 10, accounts[3], {"from": accounts[0]})

	return crowdsale

@pytest.fixture(scope="module")
def mpxVault(MpxVault, accounts, tokens):
	(mpx, stablecoin) = tokens

	vault = MpxVault.deploy(mpx.address, {"from": accounts[0]})
	mpx.transfer(vault, 1e25, {"from": accounts[0]})

	return vault

@pytest.fixture(scope="module")
def tokens(accounts, Token):

	mpx = Token.deploy("name", "symbol", 2e26, {"from": accounts[0]})
	stablecoin = Token.deploy("name1", "symbol1", 2e26, {"from": accounts[0]})

	mpx.transfer(accounts[1], 4e25, {"from": accounts[0]})
	mpx.transfer(accounts[2], 4e25, {"from": accounts[0]})

	return (mpx, stablecoin)
