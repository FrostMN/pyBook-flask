import bcrypt, hashlib
from sqlCalls import getSalt, getHash, Execute


## generates a random salt to use for password hashing
def genSalt():
    salt = bcrypt.gensalt()
    return hashlib.sha256(str(salt).encode('utf-8')).hexdigest()


## hashes password with salt
def hashPword(salt, pword):
    return hashlib.sha256((salt + pword).encode('utf-8')).hexdigest()


## pulls salt from db hashes pw with salt compares new hash to old hash also creates a new salt and updates salt/hash
def testPWORD(uname, pword, db_loc="pyBook.db"):
    salt = getSalt(uname, db_loc)
    if hashPword(salt, pword) == getHash(uname, db_loc):
        updateHash(uname, pword, db_loc)
        return True
    else:
        return False


## updates hash and salr in db
def updateHash(uname, pword, db_loc="pyBook.db"):
    salt = genSalt()
    params = (salt, hashPword(salt, pword), uname)
    call = """
UPDATE users 
  SET salt = ?, hash = ?
  WHERE uname = ?;"""
    Execute(call, db_loc, params)