import rsa

def load_private_key(file_path):
    # Read the private key from a file
    with open(file_path, "rb") as pri_file:
        private_key_data = pri_file.read()
    return rsa.PrivateKey.load_pkcs1(private_key_data)

def load_public_key(file_path):
    # Read the public key from a file
    with open(file_path, "rb") as pub_file:
        public_key_data = pub_file.read()

    return rsa.PublicKey.load_pkcs1(public_key_data)


