from rsa import key

(public_key, private_key) = key.newkeys(1024)

with open("public_key.pem" , "a") as pb_file:
	pb_file.write(public_key.save_pkcs1().decode("utf-8"))
	
with open("private_key.pem" , "a") as pv_file:
	pv_file.write(private_key.save_pkcs1().decode("utf-8"))
	

print("hat geklappt")