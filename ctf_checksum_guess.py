import itertools
import hashlib

# Warning!
# python2! For unknown reasons python3 seems to be a random generator.

# define all possible components of the checksum here
# (might be all strings you have)
items = {"window", "more", "random", "8cd4eb8d79", "4029", "some", "random", "junk"}
checksum = "b3b740d455c027f9865998cfa531cac3818b49017a03ec17e6d0a58ff91c2d73"

# if needed, define a salt:
salt = "8917591"

# seperators when building the text from the items
seperator = ["", "-", ".", "_", " "]

# define the hash functions to test
hashs = [("md5", hashlib.md5), 
	("SHA1", hashlib.sha1), 
	("SHA224", hashlib.sha224),
	("SHA256", hashlib.sha256),
	("SHA384", hashlib.sha384),
	("SHA512", hashlib.sha512)]

# ------------------ lets guess! ------------------------
def all_sorts(s):
	if s == None:
		return []
	s = list(s)
	r = []

	for i in s:
		s_rest = s[:]
		s_rest.remove(i)
		r_loop = [i] + (all_sorts(s_rest))
		r.append(r_loop)
	return r

def folder(lists):
	result = []
	if type(lists) is list and len(lists) > 1:
		result.append(lists[0])
		result += folder(lists[1])
	if type(lists) is list and len(lists) == 1:
		result.append(lists[0])
	return result

def get_all_combinations(inputs):
	# get the powerset
	powerset = set((x 
		for length in range(len(items)+1) 
		for x in itertools.combinations(items, length )
		if len(x) is not 0))
	result = []
	for liste in powerset:
		r_loop = all_sorts(liste)
		for l in r_loop:
			result.append(folder(l))

	return result


def list_to_string(liste, seperator):
	result = ""
	i = 0
	for item in liste:
		if i is not 0:
			result += seperator
		result += item
		i += 1
	return result

def try_hash(text):
	global items
	global hashs
	global salt
	global checksum

	for h in hashs:
		has = h[1]()
		has.update(text.encode("utf-8"))
		if salt is not None:
			has.update(salt.encode("utf-8"))
		result = has.hexdigest()
		if result == checksum:
			return h[0]
	return None

print("CTF Checksum Guess Tool")
print("\nTries to guess a checksum by brute forcing all given\ntext combinations and implemented hashs.\n")


for combination in get_all_combinations(items):
	for sep in seperator:
		text = list_to_string(combination, sep)
		if try_hash(text) is not None:
			print("Found it!\n\n" + 
				try_hash(text) + 
				"(message=" + 
				text + 
				", salt="+ 
				salt +")\n= " + checksum)
			break

print("\nFor improvements mail me at cguess(at)f5w.de")
print("\nby Mark Schneemann")





