from string import ascii_letters,digits
d={}
def initializare(d):
    data = open( './modules/MachineLearning/probabil.txt' ).read().split('\n')
    for i in range(len(data)):
        try:
            data[i]=data[i].split(':')
            d[data[i][0]]=data[i][1]
        except:
            pass
    return d


def initializare_ads(d):
    data = open( './modules/MachineLearning/ads_prob.txt' ).read().split('\n')
    for i in range(len(data)):
        try:
            data[i]=data[i].split(':')
            d[data[i][0]]=data[i][1]
        except:
            pass
    return d


def verify_encoding(word,d):
	suma=0
	nr=0
	for i in range(len(word)-1):
		try:
			nr+=1
			grup=word[i]+word[i+1]
			if d[grup]:
				suma+=int(d[grup])
		except:
			pass
	try:
		return suma/nr
	except:
		pass


def count_lower_probabilities(word):
    letters = ['W','G','P','B','V','K','X','Q','J','Z']
    nr = 0
    for i in word:
        if i.upper() in letters:
            nr += 1
    return nr


def count_litere_mari(word):
    return sum(i.isupper() for i in word)
    


def count_litere_mici(word):
    return sum(i.islower() for i in word)

def count_litere_mai_mari_de_f(word):
    nr = 0
    for i in word:
        if (i in ascii_letters):
            if(i>'f') and (i<='z'):
                nr+=1
            if(i>'F') and (i<='Z'):
                nr+=1
    return nr
    
def count_cifre(word):
    nr = 0
    for i in word:
        if (i in digits):
            nr+=1
    return nr

def count_dots(word):
    return word.count('.')

def count_lines(word):
    return word.count('-')

def get_every_len(word):
    word = word.split('.')
    array = []
    for i in word:
        array.append(float(len(i)))
    for i in range(len(array),100):
        array.append(float(0))
    return array


def get_len(word):
    return len(word)

def read_file(name):
    lst=[]
    f=open(name,"r", encoding="utf8").read().strip().split('\n')
    for i in f:
        new=i.split(' ,')
        lst.append(new)
    return lst