import uuid
from typing import Tuple
import requests
from pydantic import BaseModel, Field  # Ensure BaseModel is imported from pydantic
# from some_context_library import Context  # Replace with the actual import path
# from some_protocol_library import Protocol  # Replace with the actual import path

# Mock imports for ai_engine since the actual module is not specified.
from ai_engine import UAgentResponse, UAgentResponseType  # Ensure this is the correct import

class GeoCode(BaseModel):
    address: str = Field(description="Address of a location to find lat and long of.")

URL = "https://maps.googleapis.com/maps/api/geocode/json"

# You should replace this with a real API key.
API_KEY = ""

if API_KEY == "":
    raise Exception("You need to provide an API key for Google Maps API to use this example")

geocode_protocol = Protocol("GeoCode")

def get_data(address: str) -> Tuple or None:
    """
    Returns the latitude and longitude of a location using the Google Maps Geocoding API.
    Args:
        address (str): The address of the location.
    Returns:
        tuple: A tuple containing the latitude and longitude of the location.
    """
    query_params = {"key": f"{API_KEY}", "address": f"{address}"}
    response = requests.get(URL, params=query_params)
    data = response.json()
    if data['status'] == 'OK':
        latitude = data['results'][0]['geometry']['location']['lat']
        longitude = data['results'][0]['geometry']['location']['lng']
        return latitude, longitude
    else:
        return None

@geocode_protocol.on_message(model=GeoCode, replies=UAgentResponse)
async def on_message(ctx: Context, sender: str, msg: GeoCode):
    ctx.logger.info(f"Received message from {sender}.")
    try:
        data = get_data(msg.address)
        if data is not None:
            latitude, longitude = data
            option = f"Location for {msg.address} is: \nlatitude={latitude}, longitude={longitude}"
            request_id = str(uuid.uuid4())
            ctx.storage.set(request_id, option)
            await ctx.send(
                sender,
                UAgentResponse(
                    message=option,
                    type=UAgentResponseType.FINAL,
                    request_id=request_id
                ),
            )
        else:
            await ctx.send(
                sender,
                UAgentResponse(
                    message="No geo coordinates are available for this context",
                    type=UAgentResponseType.FINAL
                ),
            )
    except Exception as exc:
        ctx.logger.error(exc)
        await ctx.send(
            sender,
            UAgentResponse(
                message=str(exc),
                type=UAgentResponseType.ERROR
            )
        )

# Assuming 'agent' is an instance of the Agent class
agent.include(geocode_protocol)
