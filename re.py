
import re

sent = "He gained numerous awards in recognition of his work, including the Copley Medal of the Royal Society of London in 1925, and the Franklin Medal of the Franklin Institute in 1935. "
sent = sent.encode('ascii', 'ignore')
res = re.search("(the|year|in|In) ([1-3][0-9]{3})",sent)

print res.group(0)