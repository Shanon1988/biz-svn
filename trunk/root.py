# root.py -- Root application


import imp
import time
import os
import os.path


class ApplicationInfo(object):
	__slots__ = "name","path","body","mtime","usage","hotplug"

	def __init__(self, name, path, body, mtime=None, hotplug=False):
		self.name = name
		self.path = path
		self.body = body
		self.mtime = mtime
		self.usage = 0
		self.hotplug = hotplug


class BizRoot:
	def __init__(self):
		self._apps = {}  # cached apps
		self._applist = {}  # all apps
		self._index = None  # index app
		self._error = None
		self.environ = None
		self.start_response = None

	def register_app(self, name, path, hotplug=False):
		if name not in self._applist:
			self._applist[name] = ApplicationInfo(name, path, None, os.stat(path).st_mtime, hotplug)

	def register_index(self, path, hotplug=False):
		self._index = ApplicationInfo(None, path, self._load_body(path), os.stat(path).st_mtime, hotplug)

	def register_error(self, path, hotplug=False):
		self._error = ApplicationInfo(None, path, self._load_body(path), os.stat(path).st_mtime, hotplug)

	def _load_body(self, path):
		path, modname = os.path.split(path)
		modname = modname.split(".py")[0]
		return imp.load_module(modname,
				*imp.find_module(modname, [path])).load(self.environ, self.start_response)

	def _cache_app(self, name):
		app = self._applist[name]
		app.body = self._load_body(app.path)
		self._apps[name] = app

	def _uncache_app(self, name):
		app = self._apps[name]
		app.body = None
		del self._apps[name]

	def _default_index(self):
		try:
			try:
				f = file("doc/welcome.html")
				page = f.read()
			finally:
				f.close()

		except IOError:
			page = "Index method is left out."

		self.start_response("200 Index", [("content-type","text/html")])
		return page

	def _default_error(self):
		code = self.environ["biz.error.code"]
		msg = self.environ["biz.error.message"]

		self.start_response("%s error" % code, [("content-type","text/plain")])
		return msg

	def __call__(self, environ, start_response):
		def tuplize(x):
			l = x.split("=")[:2]
			if len(l) == 1:
				l.append(True)
			return tuple(l)

		self.environ = environ
		self.start_response = start_response

		path = [p for p in environ["PATH_INFO"].split("/") if p] or [""]
		if "QUERY_STRING" in environ:
			params = dict([tuplize(x) for x in environ["QUERY_STRING"].split("&") if x])
		else:
			params = {}

		environ["biz.path"] = path
		environ["biz.params"] = params

		if not path[0]:
			if not self._index:
				return self._default_index()

			app = self._index
				
			in_cache = 1

		else:
			try:
				name = path[0]
				app = self._apps[name]
					
				in_cache = 1
			except KeyError:  # app is not cached
				try:
					self._cache_app(name)
					app = self._apps[name]
					in_cache = 0
				except KeyError:
					environ["biz.error.code"] = "404"
					environ["biz.error.message"] = "Method not found."

					if self._error:
						app = self._error
						in_cache = 1
					else:
						return self._default_error()					

		if app.hotplug:
			# check whether the application is modified
			mt = os.stat(app.path).st_mtime
			if not app.mtime or mt > app.mtime:
				app.body = self._load_body(app.path)

		app.usage += 1
		environ["biz.debug.app.usage"] = str(app.usage)
		environ["biz.debug.app.in_cache"] = str(in_cache)

		app.body.refresh(environ, start_response)
		app.body.run()
		##return app.body.run(environ, start_response)
		return app.body.get_response()


root = BizRoot()
root.register_index("apps/wello.py", hotplug=True)
##root.register_index("apps/vfolder/vfolder_app.py", hotplug=True)
##root.register_error("apps/vfolder/vfolder_app.py", hotplug=True)
root.register_app("sum", "apps/sum/sum_app.py", hotplug=True)
root.register_app("zello", "apps/wello.py", hotplug=True)
##root.register_app("name", "apps/name.py", hotplug=True)
root.register_app("favicon.ico", "apps/favicon.py", hotplug=True)

