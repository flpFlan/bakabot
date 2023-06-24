from adapter import CQHTTPAdapter

client=CQHTTPAdapter.Adapter.test_client()

class User:
    def __init__(self,qq_number:int,nickname:str):
        self.qq_number=qq_number
        self.nickname=nickname

    def say_private(self,to:int,msg:str):
        ...
    def say_at_group(self,group_id:int,msg:str):
        ...

class Group:
    def __init__(self,id:int,name:str):
        self.id=id
        self.name=name
        self.members:list[User]=[]
    
    def add_member(self,user:User):
        self.members.append(user)