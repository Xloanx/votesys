# Python program to demonstrate 
# RIPEMD 


import hashlib 


#>>> h = hashlib.new('ripemd160')
#>>> h.update("Nobody inspects the spammish repetition")
#>>> h.hexdigest()


# Passing the required algorithm 
# as string to the new constructor 
x = hashlib.new('ripemd160') 
#x = hashlib.md5()
#hashlib.sha256(str(random.getrandbits(256)).encode('utf-8'))
# passing GeeksforGeeks 
# to x() which uses 
# ripemd 160 algorithm for 
# hashing 
word = "GeeksForGeeks"

print("The value of word:") 
print(word) 

x.update(word.encode('utf-8')) 
#x.update(b"GeeksForGeeks") 

# printing the equivalent hexadecimal 
# value. 
print("The hexadecimal equivalent of hash is :") 
print(x.hexdigest()) 
