pragma solidity 0.8.13;


import "@OpenZeppelin/contracts/token/ERC20/IERC20.sol";

contract Crowdsale
{
	IERC20 public stablecoin;

	address public team;

	uint256 public multiplier;

	uint256 public tokensSold;

	event BoughtTokens(uint256 indexed tokensAmount, address indexed buyer, address indexed beneficiary, uint256 tokensSold, uint256 spentAmount);

	mapping (address => uint256) public allocatedTokens;

	constructor(address _stablecoin, uint256 _multiplier, address _team) 
	{
		stablecoin = IERC20(_stablecoin);
		multiplier = _multiplier;
		team = _team;
	}

	/// @notice Buy tokens for stablecoin.
	function buyTokens(address beneficiary, uint256 spentAmount) external
	{
		uint256 tokensAmount = spentAmount * multiplier;

		stablecoin.transferFrom(msg.sender, address(this), spentAmount);

		allocatedTokens[beneficiary] += tokensAmount;
		tokensSold += tokensAmount;

		emit BoughtTokens(tokensAmount, msg.sender, beneficiary, tokensSold, spentAmount);
	}

	/// @notice get all stablecoin to team.
	function getFunds() external
	{
		uint256 amount = stablecoin.balanceOf(address(this));
		stablecoin.transfer(team, amount);
	}
}

