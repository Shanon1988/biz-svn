# runbiz.py

import biz.server
from biz.root import Root

root = Root()
root.configure("biz.ini")
biz.server.run(root)

