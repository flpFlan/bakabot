class PipeLine:
    def check(self,evt)->bool:
        ...
    async def pre_process(self,evt):
        ...

class GroupPipeLine(PipeLine):
    group_id:int
    def check(self,evt)->bool:
        if not hasattr(evt,"group_id"):
            return False
        return evt.group_id==self.group_id