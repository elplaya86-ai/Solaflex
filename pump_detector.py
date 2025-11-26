# =============================================
# Pump.fun Real-time Rug Pull Detector (2025)
# 
# This script monitors the Solana blockchain in real-time for new Pump.fun token launches.
# It detects potential rug pulls by checking key indicators:
#   - Mint authority revocation (prevents unlimited token minting)
#   - Freeze authority revocation (prevents token freezing)
#   - Liquidity pool (LP) token burns (prevents liquidity rugs)
# 
# Key Features:
#   - Uses WebSockets for real-time detection (no polling delays)
#   - Filters specifically for Pump.fun program interactions
#   - Fetches and analyzes transaction details asynchronously
#   - Provides actionable alerts with links to Solscan, Pump.fun, and Dexscreener
# 
# Requirements:
#   - Python 3.8+
#   - pip install solana solders asyncio
# 
# Usage:
#   - Set SOLANA_RPC environment variable for a custom RPC (e.g., Helius/QuickNode)
#   - Run: python pump_detector.py
# 
# Limitations:
#   - Public RPC may have rate limits; use a paid provider for production
#   - This is for educational purposes; always DYOR before trading
# 
# Author: elplaya86-ai (powered by Grok from xAI)
# Date: November 26, 2025
# =============================================

import os
import asyncio
import json
from solana.rpc.async_api import AsyncClient
from solana.rpc.commitment import Confirmed
from solana.publickey import PublicKey
from solders.pubkey import Pubkey

# === Configuration ===
RPC_URL = os.getenv("SOLANA_RPC", "https://api.mainnet-beta.solana.com")  # Use Helius/QuickNode for better performance

# Program IDs
PUMP_FUN_PROGRAM = PublicKey("6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P")  # Pump.fun program ID
RAYDIUM_AMM = PublicKey("675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8")  # Raydium AMM for LP detection
TOKEN_PROGRAM = PublicKey("TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA")  # SPL Token program

async def main():
    async with AsyncClient(RPC_URL) as client:
        print("🚀 Solaflex: Pump.fun Rug Detector STARTED")
        print(f"📡 RPC: {RPC_URL}")
        print("👀 Listening for new Pump.fun tokens...\n")

        # Subscribe to logs for Pump.fun program
        logs_sub = await client.logs_subscribe(
            filters={"mentions": [str(PUMP_FUN_PROGRAM)]},
            commitment=Confirmed
        )

        async for msg in logs_sub:
            try:
                logs = msg.value.logs
                signature = msg.value.signature

                # Detect Pump.fun 'create' events
                if any("create" in log.lower() for log in logs):
                    print(f"\n🎉 NEW PUMP.FUN LAUNCH DETECTED!")
                    print(f"📄 Transaction: https://solscan.io/tx/{signature}")
                    print(f"🔗 Pump.fun: https://pump.fun/{signature[:44]}")  # Approximate Pump.fun link

                    # Fetch full transaction details
                    tx_resp = await client.get_transaction(
                        signature,
                        encoding="jsonParsed",
                        max_supported_transaction_version=0
                    )
                    if not tx_resp.value:
                        print("⏭️ Skipping: No transaction data available")
                        continue

                    tx = tx_resp.value
                    instructions = tx.transaction.transaction.message.instructions
                    post_token_balances = tx.meta.post_token_balances or []
                    creator = tx.transaction.transaction.message.account_keys[0].pubkey

                    # Find the new token mint (Pump.fun mints 1B tokens initially)
                    mint = None
                    for bal in post_token_balances:
                        if bal.ui_token_amount.amount == "1000000000":  # 1B tokens
                            mint = bal.mint
                            break

                    if not mint:
                        print("⏭️ Skipping: Could not identify mint address")
                        continue

                    mint_pubkey = PublicKey(mint)

                    # === Perform Rug Pull Checks ===
                    alerts = []
                    good_signs = []

                    # Fetch mint account info
                    mint_account_resp = await client.get_account_info(mint_pubkey)
                    mint_account = mint_account_resp.value
                    if mint_account and mint_account.data:
                        data = mint_account.data

                        # Check mint authority (bytes 4-36)
                        if len(data) >= 36:
                            mint_auth_bytes = data[4:36]
                            mint_auth = Pubkey.from_bytes(mint_auth_bytes)
                            if mint_auth == Pubkey.default():
                                good_signs.append("Mint authority REVOKED (cannot mint more tokens)")
                            else:
                                alerts.append(f"Mint authority ACTIVE: {mint_auth} (high risk - dev can dilute supply)")

                        # Check freeze authority (bytes 36-68)
                        if len(data) >= 68:
                            freeze_auth_bytes = data[36:68]
                            freeze_auth = Pubkey.from_bytes(freeze_auth_bytes)
                            if freeze_auth == Pubkey.default():
                                good_signs.append("Freeze authority REVOKED (cannot freeze holders' tokens)")
                            else:
                                alerts.append(f"Freeze authority ACTIVE: {freeze_auth} (high risk - dev can freeze wallets)")

                    else:
                        alerts.append("Could not fetch mint account info")

                    # Check for LP token burn (look for burn logs related to Raydium)
                    burned_lp = any("Burn" in log and "Raydium" in log for log in logs)
                    if burned_lp:
                        good_signs.append("Liquidity Pool tokens BURNED (liquidity cannot be rugged)")
                    else:
                        alerts.append("LP tokens NOT burned (high risk - dev can pull liquidity)")

                    # === Output Results ===
                    print(f"\n💎 Token Mint: {mint}")
                    print(f"👤 Creator: {creator}")
                    print(f"📊 Dexscreener: https://dexscreener.com/solana/{mint}")

                    print("\n✅ GOOD SIGNS:")
                    for sign in good_signs:
                        print(f"   {sign}")

                    print("\n🚩 RED FLAGS:")
                    if alerts:
                        for alert in alerts:
                            print(f"   {alert}")
                    else:
                        print("   None detected so far")

                    if not alerts:
                        print("\n🟢 SAFER TOKEN (but always DYOR!)")
                    else:
                        print("\n🔴 HIGH RISK – POSSIBLE RUG")

                    print("=" * 80)

            except Exception as e:
                print(f"⚠️ Error processing transaction {signature}: {e}")
                continue

if __name__ == "__main__":
    asyncio.run(main())
