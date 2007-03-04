
from biz import *


class FaviconIco(Application):
	def static(self):
		icon = 'GIF87a\x10\x00\x10\x00\x84\x0f\x00fff\xcc\xcc\xcc\xcc\xcc\xffff\x99\x99\xcc\xff33\x9933\xcc\x99\x99\xcc33fff\xcc\xcc\xff\xff\x99\x99\x99f\x99\xcc\x003\xcc\x003\x99\xff\xff\xff\x99ff3f\xcc3\x00\xccff3f3f\x99f\x99f\x99\xff333\x00f\xff\x003f\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff,\x00\x00\x00\x00\x10\x00\x10\x00\x00\x05\x8b\xa0\x10\x88\xe4h\x96\x8a@<\x84\x90\xaeD\x10\xc7g-\x88\x07\x00\xdc\xf2\x98\xca\xac\x00c!\n\x1cdD\x17O\xa0c E\xb1\x12f\x10IT{G\xa5\xac\x01\x18\x0c\x00\x86\x83\x98q\xb0\x18G\r\x08 \x01(8\xba\xba\x02T\xc0\xf5\x82\x0b:\x9d\x81\xb0\x18Itl\x06x_mc\x0c\x06\x15v\x82\x00\x14z\x19\x08\x03\x08\x7fkwpm\x08:\x08u\x8d\x82\x13\x84\x06\x17\x99\x7fTw\x10_\x10\x0e\x98\x13\x9a\x0b\x8a\x0e^^\x05\x08\xa9\x05\x82\x05\x05\t\x06!\x00;'
	
	class Handler(biz.ArgHandler):
		def dynamic(self, r):
			return Response(FaviconIco.icon, content_type="image/gif")
			
			
def load(x):
	return FaviconIco(x)
