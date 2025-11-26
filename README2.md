markdown

# Solaflex: Real-Time Pump.fun Rug Pull Detector 🚀

[![GitHub stars](https://img.shields.io/github/stars/elplaya86-ai/Solaflex)](https://github.com/elplaya86-ai/Solaflex/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/elplaya86-ai/Solaflex)](https://github.com/elplaya86-ai/Solaflex/network)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)

Solaflex is a sophisticated, open-source tool designed to monitor new token launches on [Pump.fun](https://pump.fun) in real-time. It identifies common patterns and red flags associated with "rug pulls" and scam tokens on the Solana blockchain. The tool provides customizable alerts and a framework for community-driven analysis to help protect investors from potential scams.

## Key Features
- **Real-Time Monitoring**: Uses WebSockets to detect new Pump.fun launches instantly.
- **Rug Pull Detection**:
  - Checks if mint authority is revoked (prevents unlimited token minting).
  - Verifies if freeze authority is revoked (prevents token freezing).
  - Detects if liquidity pool (LP) tokens are burned (prevents liquidity rugs).
- **Actionable Alerts**: Console outputs with good signs (✅) and red flags (🚩), plus links to Solscan, Pump.fun, and Dexscreener.
- **Extensible**: Easy to add more checks, like honeypot detection or scammer wallet blacklists.
- **Solana Integration**: Built with the Solana Python SDK for reliable blockchain interaction.

## How It Works
Solaflex subscribes to logs from the Pump.fun program on Solana's mainnet. When a new token "create" event is detected:
1. Fetches transaction details.
2. Identifies the token mint and creator.
3. Performs rug pull checks on authorities and liquidity.
4. Outputs alerts with risk assessment.

This helps users quickly evaluate if a new token is "safer" or a "high risk" rug pull candidate.

## Quick Start
1. Clone the repo:

   git clone https://github.com/elplaya86-ai/Solaflex.git
   cd Solaflex

2. Install dependencies:

   pip install solana solders asyncio

3. (Optional) Set a fast RPC (e.g., from Helius):

   export SOLANA_RPC="https://your-rpc-url"

4. Run the detector:

   python pump_detector.py

### Example Output

 Solaflex: Pump.fun Rug Detector STARTED
 RPC: https://api.mainnet-beta.solana.com
 Listening for new Pump.fun tokens... NEW PUMP.FUN LAUNCH DETECTED!
 Transaction: https://solscan.io/tx/[signature]
 Pump.fun: https://pump.fun/[signature] Token Mint: [mint_address]
 Creator: [creator_address]
 Dexscreener: https://dexscreener.com/solana/[mint] GOOD SIGNS:
   Mint authority REVOKED (cannot mint more tokens)
   Freeze authority REVOKED (cannot freeze holders' tokens)
   Liquidity Pool tokens BURNED (liquidity cannot be rugged) RED FLAGS:
   None detected so far SAFER TOKEN (but always DYOR!)

## Configuration
- **RPC_URL**: Defaults to public mainnet. Upgrade to a paid provider for production to avoid rate limits.
- Extend `pump_detector.py` for custom features (e.g., Telegram bots or database logging).

## Roadmap
- 📱 Add Telegram/Discord notifications.
- 🛡️ Integrate honeypot and blacklist checks.
- 📈 Web dashboard for live monitoring.
- 🤝 Community contributions welcome!

## Contributing
Fork the repo, make your changes, and submit a pull request. Focus on new detection features or UI improvements. See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## License
This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

## Disclaimer
Solaflex is for educational and informational purposes only. It does not guarantee detection of all scams. Always do your own research (DYOR) before investing. Cryptocurrency carries high risk.

Built with ❤️ by [elplaya86-ai](https://github.com/elplaya86-ai). Powered by Grok (xAI).  
*Last updated: November 26, 2025*

