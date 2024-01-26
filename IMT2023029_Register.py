from IMT2023029_Utilities import printErrorAndExit

class Register:
    """
        This class simulates a register holding integers in sign-magnitude form
    """
    
    def __init__(self, size:int, startVal=0):
        """
            A Register is created of the required size and starting value.
        """

        
        self.__size=size
        if startVal<0:
            if (((2**(size-1))-1) < (-startVal)):
                printErrorAndExit("Invalid input into register")
            self.__val= -startVal
            self.__sign = 1
        else:
            if ((2**(size-1)-1) < startVal):
                if (startVal<2**size):
                    self.__sign = 1
                    self.__val = startVal - 2**(size-1)
                else:
                    printErrorAndExit("Invalid input into register")
            else:
                self.__val= startVal
                self.__sign = 0

    
    def getVal(self):
        """
            This gives the value required
        """
        return self.__val


    def getSign(self):
        """
            This gives the sign required
        """
        return self.__sign


    def getSV(self):
        """
            This gives the signed-value required
        """
        return (1-2*self.__sign)*self.__val        

    
    def __str__(self):

        """
            It returns the stored value in its binary form
        """
        
        ans=str(self.__sign)+bin(self.__val)[2:]
        while (len(ans)>self.__size):
            printErrorAndExit("overflow")
        while (self.__size-len(ans)):
            ans=ans[0]+'0'+ans[1::]
        return ans

    def inc(self):

        """
            It incriments the stored value by 1
        """
                
        if self.__sign:
            self.__val-=1
            if self.__val<0:
                printErrorAndExit("underflow")
        else:
            self.__val+=1
        while (len(bin(self.__val))>self.__size+1):
            printErrorAndExit("overflow happend while incrimenting")

    def read(self, start=0, end=None):
        
        """
            It returns a slice of the stored value in decimal form.
        """
        
        if end==None:
            end=self.__size
            
        return int((str(self))[start:end],2)

    def negate(self):

        """
            It returns the negative of the stored value in decimal form.
        """
        return ((-1)*self.getSV())

    def abs(self):
        
        """
            It returns the absolute value of the stored value in decimal form.
        """
                
        return (self.getSV())

    def write(self, val, start=0, end=None):
        
        """
            It takes in a decimal value and overwrites the given register from [start, end).
        """
        val = int(val)
        
        if end==None:
            end=self.__size

        if (end-start > self.__size):
            printErrorAndExit("Invalid size of input to write")
            
        if start==0:
            if val < 0:
                val = - val
                self.__sign = 1
                if val >= 2**(self.__size-1):
                    printErrorAndExit("Invalid value to write")
                else:
                    req=bin(val)[2::]
                    while len(req)<(end):
                        req='0'+req
                    curr=str(self)[1::]
                    self.__val=int((req+curr[len(req):]),2)
            else:
                if val >= 2**(self.__size):
                    printErrorAndExit("Invalid value to write")
                else:
                    if val >= 2**(self.__size-1):
                        self.__sign = 1
                        val=val-2**(self.__size-1)
                    else:
                        self.__sign = 0
                    
                    req = bin(val)[2::]
                    while len(req)<end:
                        req='0'+req
                    curr=str(self)[1::]
                    self.__val=int((req+curr[len(req):]),2)
        else:
            if val < 0:
                val = -val
            elif val > 2**(self.__size - 1):
                val=val-2**(self.__size-1)

            if val>2**(self.__size):
                printErrorAndExit("Writer Error")

            req = bin(val)[2::]
            while len(req)<(end-start):
                req='0'+req
            curr=str(self)[1::]
            self.__val=int((curr[:start-1:] + req + curr[start-1+len(req)::]),2)
                

if __name__ == "__main__":
    IR=Register(8,3)
    IBR=Register(20,837762)
    MAR=Register(12)
    print(IR,IBR,MAR,end='\n\n',sep='\n')
    print(Register.read(IR))
    print(IBR.read())
    print(IR.read())
    IBR.write(15,0,4)
    print(IBR.read())
    print(IBR.negate())
        
        
