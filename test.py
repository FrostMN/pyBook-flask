import bcrypt
from sqlCalls import PrintDB, isbnExist, getLibrary, Execute

PrintDB()

salt = bcrypt.gensalt() + bcrypt.gensalt() + bcrypt.gensalt() + bcrypt.gensalt()
salt = str(salt)

digits = 54

print(salt[digits:-1])
print(len(salt[digits:-1]))