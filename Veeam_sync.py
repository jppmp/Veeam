
import os
import shutil
import time
import sys


class Sync:
	#
	
	def __init__(self,args):
		
		self.end_string = None
		self.unkownedArg = False
		self.askedHelp = False
		if "--help" in sys.argv:
			self.askedHelp = True
			print("Usage: Veeam_test.py [arguments] [source folder path] [replica folder path] \n\n"
				"Arguments: \n"
				"\t--path \tto see source and replica folder global paths \n"
				"\t--logfile \tto see the created log file absolute path \n"
				"\t--sync \tto see the synchronization periodic interval \n"
				"\t--def_sync <int value> \t define the synchronization periodic interval \n")
		else:
			self.delay = 60
			self.src_path = args[-2]
			self.rep_path = args[-1]
			for i,arg in enumerate(sys.argv):
				if arg == "--path":
					print("global path to source folder is %s" % (os.path.abspath(self.src_path)))
					print("global path to replica folder is %s" % (os.path.abspath(self.rep_path)))
				elif arg == "--logfile":
					print("global path to log file is %s" % (os.path.abspath("%s/log_file.txt" % (self.rep_path))))
				elif arg == "--sync":
					print("Syncrhonization periodic interval is set to %i" % (self.delay))
				elif arg == "--def_sync":
					self.delay = int(sys.argv[i+1])
				elif arg == "--help":
					continue
				elif "--" in arg:
					print("\n%s argument not recognized" % (arg))
					self.unkownedArg = True
			
	def sync(self):
		#
		
		self.log_file = open("%s/log_file.txt" % (self.rep_path),"a")
		
		src = os.listdir(self.src_path)
		rep = os.listdir(self.rep_path)
		
		for obj in src:
			if not obj in rep:
				shutil.copy("%s/%s" % (self.src_path, obj), self.rep_path)
				self.log_file.write("created file %s on %s \n" % (obj, time.ctime(time.time())))
				print("created file %s on %s" % (obj, time.ctime(time.time())))
				
				
				
		for obj in rep:
			if obj == "log_file.txt":
				continue
			if not obj in src:	
				os.remove("%s/%s" % (self.rep_path,obj))
				self.log_file.write("deleated file %s on %s \n" % (obj, time.ctime(time.time())))
				print("deleated file %s on %s" % (obj, time.ctime(time.time())))
		
		self.log_file.close()
				
		return
		
	def doSync(self):
		#
		if self.askedHelp:
			return
			
		if not self.unkownedArg:		
			print("\nBegin Synchronization")
			while True:
				self.sync()
				time.sleep(self.delay)
			
		return
		
	
backup = Sync(sys.argv)
backup.doSync()
		
		

