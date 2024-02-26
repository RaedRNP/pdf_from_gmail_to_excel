import string

def decodeAtIndex(s: str, k: int) -> str:
        """
        :type s: str
        :type k: int
        :rtype: str
        """
        s = s.lower()
        
        if not 2 <= len(s) <= 100:
            print("Not valid quantity of characters")
            return
        
        if not s[0] in string.ascii_letters:
            print("First character is not a letter")
            return
        
        if not 1 <= k <= 10**9:
            print("Not a valid number")
            return
        
        tape = ""
        num = ""
        
        for letter in s:
            if letter in "23456789":
                num = int(letter)
                tape = tape * num
                if len(tape) >= k:
                    break
                continue
            tape += letter
                    
        print(tape[k-1])
        

decodeAtIndex("leet2code3", 10)
decodeAtIndex("y959q969u3hb22odq595", 222280369)
decodeAtIndex("a2345678999999999999999", 1)