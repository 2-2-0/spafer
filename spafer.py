#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  spafer.py, by 220
#  
#  Copyright 2015 220 <220@WKH>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import os

class SPAFer ():
	contents = list ()
	
	model_tags = list ()
	unlisted_tags = list ()
	missing_tags = list ()
	
	current_path = ""
	current_model = ""
	
	
	def clear (self):
		self.current_path = ""
		
		del self.contents[:]
		del self.unlisted_tags[:]
		del self.missing_tags[:]
	
	def model (self, filename):
		fstream = open (filename, 'r')
		model_tags = fstream.readlines ()
		fstream.close ()
		
		for model_tag in model_tags:
			model_tag = model_tag.rstrip ()
			self.model_tags.append (model_tag)
		
		model_id = filename.split (".")[0]
		self.current_model = str (model_id.replace ("_", "."))
		
		print "model "+filename+" ("+str (self.current_model)+") loaded. valid tags:"
		print self.model_tags
		
	def set (self, path):
		self.clear ()
		
		if os.access (path, os.W_OK):
			self.current_path = path
			filename = path+"/profile.info"
		
			if os.access (filename, os.R_OK):
				fstream = open (filename, 'r')
				entries = fstream.readlines ()
				fstream.close ()
				
				for entry in entries:
					new_entry = self.parse (entry)
					if (new_entry [0]!=-1):
						self.contents.append (new_entry)
					else:
						self.unlisted_tags.append ((new_entry [1], new_entry [2]))
			
			else:
				print "no profile.info file"
				return
		else:
			print ("invalid path!")
	def write (self, inclusive_write=False):
		if self.current_path=="":
			print "no current SPAF selected."
			return
			
		if len (self.contents)==0:
			print "no SPAF contents created."
			return
			
		filename = self.current_path+"/profile.info"
		
		if os.access (self.current_path, os.W_OK):
			fstream = open (filename, 'w')
			for content in self.contents:
				line = content [0]+":"+content [1]+"\n"
				fstream.write (line)
				print line
				
			if inclusive_write:
				for content in self.unlisted_tags:
					line = 	content [0]+":"+content [1]+"\n"
					fstream.write (line)
					print line
				
			fstream.close ()
			
			print "wrote "+filename+" to disk"
			if not inclusive_write:
				print "left out the following sets:"
				for entry in self.unlisted_tags:
					print entry
		else:
			print "can't write to disk! need permissions?"
			return
		
	def view (self):
		print str (len (self.contents))+" total content entries"
		print
		
		print "[VALID contents]"
		for content in self.contents:
			print content
		
		print
		print "[UNLISTED contents]"
		for content in self.unlisted_tags:
			print content
		


	def parse (self, entry):
		entry = entry.rstrip ()
		line = entry.split (":", 1)
		
		token = line [0]
		value = line [1]
		
		try:
			x = self.model_tags.index (token)
			
		except ValueError:
			print "tag doesn't exist in model: "+token
			return (-1, token, value)
		
		return (token, value)
		
	def add (self, tag, data):
		#let's see if this is a valid model tag...
		try:
			x = self.model_tags.index (tag)
		
		except ValueError:
			print "tag doesn't exist in model: "+tag
			return
			
		#done! now, let's see if it already exists, if it does, overwrite it...
		for content in self.contents:
			if content [0]==tag:
				print "tag already exists!"
				return

		#it doesn't! append it!
		print "adding!"
		self.contents.append ((tag, data))
		return
		
	def remove (self, tag):
		for content in self.contents:
			if content [0]==tag:
				self.contents.remove (content)
				print "removed "+tag+"!"
				return
				
		for content in self.unlisted_tags:
			if content [0]==tag:
				self.unlisted_tags.remove (content)
				print "removed "+tag+" from unlisted!"
				return
		print "no such content exists!"
		
	def removeUnlisted (self):
		del self.unlisted_tags[:]
	
	def edit (self, tag, value):
		for content in self.contents:
			if content [0]==tag:
				self.contents.remove (content)
				self.contents.append ((tag, value))
				print "edited "+tag+" with "+value
				return
				
		print "no "+tag+" tag found!"
		
	def wizard (self):
		new_contents = list ()
		self.removeUnlisted ()
		
		for tag in self.model_tags:
			question = tag
			found = False
			for content in self.contents:
				if content [0]==tag:
					answer = content [1]
					question = question+" ("+content [1]+")"
					found = True
					
			question = question+":"
			value = raw_input (question)
			
			if value=="":
				if found:
					value = answer
					new_contents.append ((tag, value))
			else:
				new_contents.append ((tag, value))
				
		self.contents = new_contents
		
	def readCmd (self):
		cmd = raw_input ("cmd:"+self.current_path+":>")
		
		line = cmd.rstrip ()
		line = line.split (" ", 2)
		
		token = value = data = ""
		
		token = line [0]
		if len (line)>1: value = line [1]
		if len (line)>2: data = line [2]
		if len (line)>3:
			 print "more parameters than needed!"
			 return
		
		if token=="q" or token=="quit":
			return -1
		elif  token=="model":
			if value=="view":
				#model view
				for tag in self.model_tags:
					print tag
			if value=="sview":
				#model view
				print self.model_tags
			elif value=="set":
				#model set from file
				if data!="": self.model (data)
				else: print "Third parameter needed!"
			elif value=="clear":
				#model clear
				del self.model_tags[:]
			else:
				print "model view/sview/clear/set <model_filename>"
		
		elif token=="set" or token=="s":
			if value!="": self.set (value)
			else:
				print "not enough parameters! path missing"
				
		elif token=="view":
			self.view ()
		elif token=="clear":
			self.clear ()
		elif token=="write":
			self.write ()
		elif token=="iwrite":
			self.write (True)
			
		elif token=="add":
			if value!="" and data!="":
				self.add (value, data)
			else:
				print "incomplete syntax! tag and/or data missing!"
		elif token=="edit":
			if value!="" and data!="":
				self.edit (value, data)
			else:
				print "incomplete syntax! tag and/or data missing!"
		elif token=="rem":
			if value!="":
				if value=="unlisted":
					self.removeUnlisted ()
				else:
					self.remove (value)
			else:
				print "incomplete syntax! existing tag missing!"
		
		elif token=="wiz":
			self.wizard ()

		elif token=="h" or token=="help" or token=="?":
			self.displayHelp ()

		elif token!="":
			print "unrecognized command!"
		
	def displayHelp (self):
		print "SPAFer, by 220\n"
		print "q/quit"


def main():
	print "SPAFer, by 220"
	
	spafer = SPAFer ()
	spafer.model ("1_0.model")
		
	active = True
	while (active):
		if spafer.readCmd ()==-1: active=False
	return 0

if __name__ == '__main__':
	main()
