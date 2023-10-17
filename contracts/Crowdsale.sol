pragma solidity 0.8.13;


import "@OpenZeppelin/contracts/token/ERC20/IERC20.sol";
import "@uniswap/v3-core/contracts/interfaces/callback/IUniswapV3SwapCallback.sol";
import "@uniswap/v3-core/contracts/interfaces/IUniswapV3Factory.sol";
import "@uniswap/v3-core/contracts/interfaces/IUniswapV3Pool.sol";
import "@uniswap/v3-core/contracts/libraries/TickMath.sol";
import "@OpenZeppelin/contracts/token/ERC20/utils/SafeERC20.sol";

contract Crowdsale is IUniswapV3SwapCallback
{
	using SafeERC20 for IERC20;
	IUniswapV3Factory public factory;
	IERC20 public stablecoin;

	address public team;

	uint256 public multiplier;

	uint256 public tokensSold;

	event BoughtTokens(uint256 indexed tokensAmount, address indexed buyer, address indexed beneficiary, uint256 spentAmount);

	mapping (address => uint256) public allocatedTokens;

	constructor(address _stablecoin, uint256 _multiplier, address _team, IUniswapV3Factory _factory) 
	{
		stablecoin = IERC20(_stablecoin);
		multiplier = _multiplier;
		team = _team;
		factory = _factory;
	}

	/// @notice Buy tokens for stablecoin.
	function buyTokens(address beneficiary, uint256 spentAmount) external
	{
		uint256 tokensAmount = spentAmount * multiplier;

		stablecoin.transferFrom(msg.sender, address(this), spentAmount);

		allocatedTokens[beneficiary] += tokensAmount;
		tokensSold += tokensAmount;

		emit BoughtTokens(tokensAmount, msg.sender, beneficiary, spentAmount);
	}

	function buyWithUniswap(address inputToken, address beneficiary, uint256 initialAmount, uint24 fee) external returns (uint256 tokensAmount)
	{
		IUniswapV3Pool pool = IUniswapV3Pool(factory.getPool(inputToken, address(stablecoin), fee));
		require(address(pool) != address(0), "Pool does not exist");
		bool zeroForOne = inputToken < address(stablecoin);
		IERC20(inputToken).safeIncreaseAllowance(address(pool), initialAmount);

		(int256 amount0, int256 amount1) = pool.swap(
			address(this),
			zeroForOne,
			int256(initialAmount),
			zeroForOne ? TickMath.MIN_SQRT_RATIO + 1 : TickMath.MAX_SQRT_RATIO - 1,
			abi.encode(inputToken, address(stablecoin), fee)
		);
		uint256 spentAmount = uint256(-(zeroForOne ? amount1 : amount0));
		tokensAmount = spentAmount * multiplier;
		tokensSold += tokensAmount;

		emit BoughtTokens(tokensAmount, msg.sender, beneficiary, spentAmount);
	}

	function uniswapV3SwapCallback(int256 amount0Delta, int256 amount1Delta, bytes calldata data) external override {
		(address source, address destination, uint24 fee) = abi.decode(data, (address, address, uint24));
		require(msg.sender == factory.getPool(source, destination, fee), "Invalid caller");
		require((source < destination ? amount0Delta : amount1Delta) != 0, "Unsuccessful swap");
	}

	/// @notice get all stablecoin to team.
	function getFunds(IERC20 token) external
	{
		uint256 amount = token.balanceOf(address(this));
		token.transfer(team, amount);
	}
}

