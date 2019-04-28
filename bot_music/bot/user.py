import discord

class User():
    def __init__(self, Id: int, Channel, State: bool):
        self.Id = Id
        self.Channel = Channel
        self.State = State

    def __del__(self):
        print("clear session")

    def cprint(self):
        print("User = (Id: {0}), (chId: {1}), (State: {2}) \n".format(self.Id, self.Channel, self.State))

    def get_users(self, users):
        print("------------------------------------------Users appended------------------------------------------------")
        for user in users:
            if user.voice:
               u = User(user.id, user.voice.channel, False)
            else:
                u = User(user.id, None, False)
            self.Users.append(u)
            u.cprint()
        print("------------------------------------------------------------------------------------------------------")	

    def get_owner_id(self):
    	for x in self.Users:
    		if x.State == True:
    			return x.Id

    def get_owner_channel(self):
    	for x in self.Users:
    		if x.State == True:
    			if x.Channel is not None:
    				return x.Channel

    def set_owner(self,Id):
    	for x in self.Users:
            if x.Id == Id:
                x.State = True
                print("owner_id set to:" + str(x.Id))

    def upd_user_channel(self,Id,Channel):
    	for x in self.Users:
            if x.Id == Id:
                x.Channel = Channel
                print("Channel set to:" + str(x.Channel))

    def clr_owner(self):
    	for x in self.Users:
    		x.State = False
    	print("Owner is clear")


    def print_users(self):
    	print("-----------------------------Users-----------------------------------------")
    	for user in self.Users:
    		user.cprint()
    	print("-----------------------------------------------------------------------------------")
