from spade.behaviour import CyclicBehaviour


class ReplyBehav(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=10)
        if msg:
            performative = msg.get_metadata("performative")
            if performative == "confirm":
                print("Agent {}:".format(str(self.agent.jid)) + " Rescue successful!")
            elif performative == "refuse":
                print("Agent {}:".format(str(self.agent.jid)) + " No emergency vehicles or hospitals available")
            else:
                print("Agent {}:".format(str(self.agent.jid)) + " Message not understood!")

            self.kill()

        else:
            print("Agent {}:".format(str(self.agent.jid)) + "Did not receive any message after 10 seconds")

    async def on_end(self):
        await self.agent.stop()