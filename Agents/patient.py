from spade import agent
from Behaviors.requestBehav import RequestBehav
from Behaviors.replyBehav import ReplyBehav

class PatientAgent(agent.Agent):

    async def setup(self):
        print("Agent {}".format(str(self.jid)) + " starting...")
        a = RequestBehav()
        b = ReplyBehav()
        self.add_behaviour(a)
        self.add_behaviour(b)