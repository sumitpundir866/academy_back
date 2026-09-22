from pwdlib import PasswordHash
password_hash = PasswordHash.recommended()



def get_password_hash(password):
    return password_hash.hash(password)



def verify_password(plain_password, hashed_password):
    try:
        return password_hash.verify(plain_password, hashed_password)
    except Exception as e:
        # logger.warning("Password verification failed: %s", e)
        return False

hashed = get_password_hash("Army@123")
verified = verify_password("Army@123", hashed)
print("verified : ", hashed, verified)