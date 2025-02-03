class MyRuntimeError(RuntimeError):
    def __init__(self,token,message):
        self.token=token
        super().__init__(message)
        
        
        