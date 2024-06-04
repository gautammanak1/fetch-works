import http.client
import json
from uagents import Agent, Bureau, Context, Model
from uagents.network import wait_for_tx_to_complete
from uagents.setup import fund_agent_if_low

class VehicleDetailsRequest(Model):
    vehicle_number: str
    rapidapi_key: str

class VehicleDetailsResponse(Model):
    details: str

class PaymentRequest(Model):
    wallet_address: str
    amount: int
    denom: str

class TransactionInfo(Model):
    tx_hash: str

AMOUNT = 100
DENOM = "atestfet"

# Agents setup
alice = Agent(name="alice", seed="alice secret phrase")
bob = Agent(name="bob", seed="bob secret phrase")

fund_agent_if_low(bob.wallet.address())
fund_agent_if_low(alice.wallet.address())

def get_vehicle_details(vehicle_number, rapidapi_key):
    conn = http.client.HTTPSConnection("rto-vehicle-information-verification-india.p.rapidapi.com")
    
    payload = json.dumps({
        "reg_no": vehicle_number,
        "consent": "Y",
        "consent_text": "I hereby declare my consent agreement for fetching my information via AITAN Labs API"
    })
    
    headers = {
        'content-type': "application/json",
        'X-RapidAPI-Key': rapidapi_key,
        'X-RapidAPI-Host': "rto-vehicle-information-verification-india.p.rapidapi.com"
    }
    
    conn.request("POST", "/api/v1/rc/vehicleinfo", payload, headers)
    
    res = conn.getresponse()
    data = res.read()
    
    return data.decode("utf-8")

# Alice requests vehicle details
@alice.on_interval(period=10.0)
async def request_vehicle_details(ctx: Context):
    vehicle_number = "GJ01JT0459"  # example vehicle number
    rapidapi_key = "39d8d4a7dbmsh3bff5ad53be4fbcp12bc59jsnb251e5c486c4"
    details = get_vehicle_details(vehicle_number, rapidapi_key)
    await ctx.send(
        bob.address,
        VehicleDetailsRequest(
            vehicle_number=vehicle_number,
            rapidapi_key=rapidapi_key
        )
    )
    ctx.logger.info(f"Requested vehicle details for {vehicle_number}: {details}")

@bob.on_message(model=VehicleDetailsRequest, replies=VehicleDetailsResponse)
async def fetch_vehicle_details(ctx: Context, sender: str, msg: VehicleDetailsRequest):
    ctx.logger.info(f"Received vehicle details request from {sender}")
    details = get_vehicle_details(msg.vehicle_number, msg.rapidapi_key)
    await ctx.send(
        alice.address,
        VehicleDetailsResponse(details=details)
    )
    ctx.logger.info(f"Fetched vehicle details: {details}")

# # Alice requests payment
# @alice.on_interval(period=20.0)
# async def request_funds(ctx: Context):
#     await ctx.send(
#         bob.address,
#         PaymentRequest(
#             wallet_address=str(ctx.wallet.address()), amount=AMOUNT, denom=DENOM
#         ),
#     )

@alice.on_message(model=TransactionInfo)
async def confirm_transaction(ctx: Context, sender: str, msg: TransactionInfo):
    ctx.logger.info(f"Received transaction info from {sender}: {msg}")
    tx_resp = await wait_for_tx_to_complete(msg.tx_hash, ctx.ledger)
    coin_received = tx_resp.events["coin_received"]
    if (
        coin_received["receiver"] == str(ctx.wallet.address())
        and coin_received["amount"] == f"{AMOUNT}{DENOM}"
    ):
        ctx.logger.info(f"Transaction was successful: {coin_received}")

# @bob.on_message(model=PaymentRequest, replies=TransactionInfo)
# async def send_payment(ctx: Context, sender: str, msg: PaymentRequest):
#     ctx.logger.info(f"Received payment request from {sender}: {msg}")
#     transaction = ctx.ledger.send_tokens(
#         msg.wallet_address, msg.amount, msg.denom, ctx.wallet
#     )
#     await ctx.send(alice.address, TransactionInfo(tx_hash=transaction.tx_hash))

bureau = Bureau()
bureau.add(alice)
bureau.add(bob)

if __name__ == "__main__":
    bureau.run()
