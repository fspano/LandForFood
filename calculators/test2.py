from functools import partial
from random import randint

for roll in iter(partial(randint, 1, 8), 1):
    print 'you rolled: {}'.format(roll)
    if roll == 1:
	print 'oops you rolled a 1!'
#	raise SystemExit
#oops you rolled a 1!
