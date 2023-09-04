pragma solidity 0.8.13;


import "@OpenZeppelin/contracts/token/ERC20/IERC20.sol";
import "@OpenZeppelin/contracts/access/Ownable.sol";

/// @notice contract to get MPX tokens bought with crowdsale.
contract MpxVault is Ownable
{
	IERC20 public mpx;

	mapping (address => uint256) public allocatedTokens;

	event tokensAllocated(address indexed beneficiary, uint256 indexed amount);

	constructor(address _mpx)
	{
		mpx = IERC20(_mpx);
	}

	function allocateTokens(address beneficiary, uint256 amount) external onlyOwner
	{
		allocatedTokens[beneficiary] += amount;
		mpx.transfer(beneficiary, amount);

		emit tokensAllocated(beneficiary, amount);
	}

	function batchAllocateTokens(address[] calldata beneficiary, uint256[] calldata amounts) external onlyOwner
	{
		require(beneficiary.length == amounts.length, "beneficiary should match amounts");

		for (uint256 i = 0; i < beneficiary.length; i++)
		{
			allocatedTokens[beneficiary[i]] += amounts[i];
			mpx.transfer(beneficiary[i], amounts[i]);

			emit tokensAllocated(beneficiary[i], amounts[i]);
		}
	}
}