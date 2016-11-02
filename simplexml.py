class XmlWriter:
	def __init__(self, path, link, config):
		self.path = path
		self.link = link
		self.config = config
		self.pastedObjects = []
		self.pastedLinks = []

	def log(self, msg):
		print "log", msg
	
	def buildMenuLink(self, menuObject, mediathek, objectCount):
		print "buildMenuLink", menuObject, objectCount
		self.pastedObjects.append(menuObject)

	def closeMenuContext(self):
		pass

	def buildVideoLink(self, displayObject, mediathek, objectCount):
		print "buildVideoLink", displayObject, objectCount
		#if not displayObject.isPlayable:
		#	self.pastedLinks.append(displayObject)
		
