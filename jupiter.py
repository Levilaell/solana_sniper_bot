import base64
import logging

import httpx
from solana.rpc.async_api import AsyncClient
from solana.rpc.commitment import Confirmed
from solana.rpc.types import TxOpts
from solders.message import to_bytes_versioned
from solders.transaction import VersionedTransaction

from config_manager import JUPITER_CONFIG, RPC_ENDPOINT, config
from wallet import load_keypair

logger = logging.getLogger(__name__)

SOL_MINT_ADDRESS = "So11111111111111111111111111111111111111112"


# ---------- helper: token listado? ------------------------------------------
async def is_token_supported(mint: str) -> bool:
    if not hasattr(is_token_supported, "_cache"):
        async with httpx.AsyncClient(timeout=10) as c:
            r = await c.get("https://token.jup.ag/all")
            r.raise_for_status()
            is_token_supported._cache = r.json()
    return any(d.get("address") == mint for d in is_token_supported._cache)


# ---------- núcleo -----------------------------------------------------------
async def buy_token(dest_mint: str) -> str | None:
    if not await is_token_supported(dest_mint):
        logger.warning("Mint %s não listado na Jupiter.", dest_mint)
        return None
    if config is None:
        logger.error("Config ausente.")
        return None

    kp = load_keypair()
    if not kp:
        return None

    api = JUPITER_CONFIG["api_url"]
    lamports = int(float(JUPITER_CONFIG.get("amount", 0.01)) * 1_000_000_000)
    slippage = JUPITER_CONFIG.get("slippageBps", 50)

    # ---------- quote ----------
    qparams = {
        "inputMint": SOL_MINT_ADDRESS,
        "outputMint": dest_mint,
        "amount": lamports,
        "slippageBps": slippage,
        "onlyDirectRoutes": "false",
        "asLegacyTransaction": "false",
    }
    async with httpx.AsyncClient(timeout=20) as h:
        qr = await h.get(f"{api}/quote", params=qparams)
        qr.raise_for_status()
        quote = qr.json()
        if not quote.get("routePlan"):
            logger.warning("Sem rota para %s", dest_mint)
            return None

        sp = {
            "quoteResponse": quote,
            "userPublicKey": str(kp.pubkey()),
            "wrapAndUnwrapSol": True,
        }
        sr = await h.post(f"{api}/swap", json=sp)
        sr.raise_for_status()
        swap = sr.json()

    if "swapTransaction" not in swap:
        logger.error("swapTransaction ausente.")
        return None

    # ---------- desserializa & assina ----------
    vtx = VersionedTransaction.from_bytes(base64.b64decode(swap["swapTransaction"]))

    # assina mensagem
    msg_bytes = to_bytes_versioned(vtx.message)
    sig = kp.sign_message(msg_bytes)
    vtx.signatures[0] = sig  # 1ª assinatura = pagador

    raw_tx = bytes(vtx)

    # ---------- envia ----------
    async with AsyncClient(RPC_ENDPOINT, commitment=Confirmed) as c:
        try:
            logger.info("Enviando swap…")
            tx_sig = await c.send_raw_transaction(
                raw_tx, opts=TxOpts(skip_preflight=True, preflight_commitment="confirmed")
            )
            logger.info("Swap enviado! Sig: %s", tx_sig.value)
            return str(tx_sig.value)
        except Exception as e:
            logger.error("Falha ao enviar tx: %s", e)
            return None
