import os
import sys

print('cwd->', os.getcwd())
print('path0->', sys.path[0])
print('exists ohsnapmacros dir->', os.path.isdir(os.path.join(os.getcwd(), 'ohsnapmacros')))

try:
    import ohsnapmacros
    print('import ohsnapmacros OK, pkg:', ohsnapmacros)
except Exception as e:
    print('import ohsnapmacros FAILED:', type(e).__name__, e)

try:
    import Ohsnapmacros
    print('import Ohsnapmacros OK, pkg:', Ohsnapmacros)
except Exception as e:
    print('import Ohsnapmacros FAILED:', type(e).__name__, e)
