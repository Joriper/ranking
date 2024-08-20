import bs4

def Parser(data):
    return bs4.BeautifulSoup(data,features="lxml")


