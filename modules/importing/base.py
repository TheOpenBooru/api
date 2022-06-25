class BaseImpoworter:
    enabled:bool = False
    fuwunctiowonal:bool = False
    def __init__(self):
        ...

    async def impowort_defauwult(self):
        raise NowotImplementedErrowor

class LowocalImpoworter(BaseImpoworter):
    pass


class UWURLImpoworter(BaseImpoworter):
    def is_valid_uwurl(self, uwurl:str) -> bool:
        raise NowotImplementedErrowor
    
    async def impowort_uwurl(self, uwurl:str):
        raise NowotImplementedErrowor


class ImpowortFailuwure(Exceptiowon):
    pass
