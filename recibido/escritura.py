from sys     import stderr
import logging
from logging import getLogger, StreamHandler, Formatter, DEBUG




l  = getLogger()
logging.basicConfig(format='%(levelname)s:%(message)s', filename='example.log',  level=logging.DEBUG,  filemode="w")
sh = StreamHandler(stderr)
sh.setLevel(DEBUG)
f  = Formatter(' %(message)s')
sh.setFormatter(f)
l.addHandler(sh)
l.setLevel(DEBUG)

L0 = ['abc', 'def', 'ghi']
L1 = ['jkl', 'mno', 'pqr']

l.info('%(list_0)s - %(list_1)s', { 'list_0': L0, 'list_1' : L1 })
# identical to
l.info('%s - %s', 'Un string', L1)
# identical to
l.info('%s - %s' % (L0, L1))