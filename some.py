import string

def decodeAtIndex(s: str, k: int):
    """
    :type s: str
    :type k: int
    :rtype: str
    """
    
    lenS = 0
    n = 0
    
    for char in s:
        if char in string.digits:
            n = int(char)
            lenS *= n
            continue
        lenS += len(char)
    
    lenS = lenS / int(s[-1])
        
    print(k % lenS)
    
        

decodeAtIndex("leet2code3", 10) #o
decodeAtIndex("a2345678999999999999999", 1) #a
decodeAtIndex("y959q969u3hb22odq595", 222280369) #y