# pumpfun_listener.py
# यह कोड Pump.fun पर नए टोकन डिटेक्ट करने का बेसिक उदाहरण है
# ध्यान रखें: इसमें कोई प्राइवेट की या पैसे का ट्रांजैक्शन नहीं है, बस सुनता है

import asyncio
import json
from solana.rpc.async_api import AsyncClient
from solana.rpc.websocket_api import connect as ws_connect
from solana.publickey import PublicKey

# Pump.fun का फैक्ट्री अकाउंट (उदाहरण)
PUMP_FACTORY_ACCOUNT = PublicKey("6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P")

RPC_HTTP = "https://api.mainnet-beta.solana.com"
RPC_WS = "wss://api.mainnet-beta.solana.com/"

async def main():
    client = AsyncClient(RPC_HTTP)
    async with ws_connect(RPC_WS) as ws:
        await ws.logs_subscribe(filter={"mentions": [str(PUMP_FACTORY_ACCOUNT)]})
        print("🎧 Pump.fun पर नए टोकन सुन रहे हैं...")
        while True:
            msg = await ws.recv()
            data = json.loads(msg)
            params = data.get("params", {})
            result = params.get("result", {})
            signature = result.get("signature")
            if signature:
                print("🔹 नया ट्रांजैक्शन मिला:", signature)

if __name__ == "__main__":
    asyncio.run(main())
