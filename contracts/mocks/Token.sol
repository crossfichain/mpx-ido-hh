pragma solidity 0.8.13;

// SPDX-License-Identifier: MIT

import "@OpenZeppelin/contracts/token/ERC20/ERC20.sol";
import "@OpenZeppelin/contracts/access/Ownable.sol";

contract Token is ERC20, Ownable
{
	constructor(string memory name, string memory symbol, uint256 initialSupply) ERC20(name, symbol)
	{
		_mint(msg.sender, initialSupply);
	}
}