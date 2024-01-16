class Register:
    def __init__(self, size:int, startVal=0):
        self.__size=size
        self.__val=startVal

    def __str__(self):
        
        ans=bin(self.__val)[2:]
        
        while (len(ans)>self.__size):
            self.__val-=2**self.__size
            print("overflow")
            ans=bin(self.__val)[2:]
            
        while (self.__size-len(ans)):
            ans='0'+ans
            
        return ans

    def inc(self):
        self.__val+=1
        ans=bin(self.__val)[2:]
        while (len(ans)>self.__size):
            self.__val-=2**self__size
        print("overflow happend")

    def read(self, start=0, end=None):
        if end==None:
            end=self.__size
        return int((str(self))[start:end],2)

    def write(self, val, start=0, end=None):

        if end==None:
            end=self.__size

        req=bin(val)[2::]
        if (len(req)>(end-start)) or (end-start > self.__size):
            printErrorAndExit("Invalid size of input to write")

        curr=bin(self.__val)[2::]
        
        self.__val=int((curr[:start]+req+curr[end:]),2)

if __name__ == __main__:
    IR=Register(8,3)
    IBR=Register(20,837762)
    MAR=Register(12)
    print(IR,IBR,MAR,end='\n\n',sep='\n')
    print(Register.read(IR))
    print(IBR.read())
    print(IR.read())
    IBR.write(15,0,4)
    print(IBR.read())
        
        
