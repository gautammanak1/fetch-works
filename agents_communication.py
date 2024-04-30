from uagents import Agent, Bureau, Context, Model # type: ignore
 
class Message(Model):
    message: str
 
sigmar = Agent(name="sigmar", seed="sigmar recovery phrase")
slaanesh = Agent(name="slaanesh", seed="slaanesh recovery phrase")
 
@sigmar.on_interval(period=3.0)
async def send_message(ctx: Context):
   await ctx.send(slaanesh.address, Message(message=" Hlo there is gautam manak "))
 
@sigmar.on_message(model=Message)
async def sigmar_message_handler(ctx: Context, sender: str, msg: Message):
    ctx.logger.info(f"Received message from {sender}: {msg.message}")
 
@slaanesh.on_message(model=Message)
async def slaanesh_message_handler(ctx: Context, sender: str, msg: Message):
    ctx.logger.info(f"Received message from {sender}: {msg.message}")
    await ctx.send(sigmar.address, Message(message="I am your agent "))
 
bureau = Bureau()
bureau.add(sigmar)
bureau.add(slaanesh)
if __name__ == "__main__":
    bureau.run()