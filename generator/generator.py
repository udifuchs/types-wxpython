# -*- coding: utf-8 -*-
import logging
import sys
from queue import Queue

import requests
from bs4 import BeautifulSoup

from .interfaces import ITyping
from .parser import Parser
from .writer import TypingWriter


# Some starting points to find the data
BASE_INDEX_URLS: list[str] = [
	"https://docs.wxpython.org/wx.1moduleindex.html",
	"https://docs.wxpython.org/wx.ribbon.1moduleindex.html",
	"https://docs.wxpython.org/wx.lib.buttons.html",
]
EXTRA_CLASS_URLS: list[str] = [
	"wx.FontFamily.enumeration.html",
	"wx.FontWeight.enumeration.html",
	"wx.StockCursor.enumeration.html",
	"wx.StandardID.enumeration.html",
	"wx.FontEncoding.enumeration.html",
	"wx.FontStyle.enumeration.html",
	"wx.functions.html",
]
EXTRA_KNOWN_ITEMS: list[ITyping] = [
	{
		"type": "literal",
		"name": "GROW",
		"moduleName": "wx",
		"returnType": "int",
		"docstring": "Synonym of wx.EXPAND"
	}, {
		"type": "literal",
		"name": "RA_HORIZONTAL",
		"moduleName": "wx",
		"returnType": "int",
		"docstring": "Synonym of wx.HORIZONTAL"
	}, {
		"type": "literal",
		"name": "RA_VERTICAL",
		"moduleName": "wx",
		"returnType": "int",
		"docstring": "Synonym of wx.VERTICAL"
	}, {
		"type": "literal",
		"name": "NORMAL",
		"moduleName": "wx",
		"returnType": "int",
	}, {
		"type": "literal",
		"name": "DEFAULT",
		"moduleName": "wx",
		"returnType": "int",
	}, {
		"type": "literal",
		"name": "wxEVT_COMMAND_BUTTON_CLICKED",
		"moduleName": "wx",
		"returnType": "int",
	}
]


class DocumentationGenerator:
	""" Generate the documentation
	"""
	def __init__(self) -> None:
		""" Constructor
		"""
		# Create a Queue with classes
		self.classQueue: Queue[str] = Queue()

		# Remember the whole file
		self.typings: Queue[ITyping] = Queue()

		# Create a logger
		self.logger = logging.Logger("WXPythonTypingGenerator")
		handler = logging.StreamHandler(sys.stdout)
		handler.setLevel(logging.DEBUG)
		formatter = logging.Formatter("%(levelname)s: %(message)s")
		handler.setFormatter(formatter)
		self.logger.addHandler(handler)

		# Create a parser
		self.parser = Parser(self.classQueue, self.logger)

	def generate(self) -> None:
		""" Generate
		"""
		# Add the extra classes to the queue
		# This classes are not found by default
		# So we add them manually
		#
		for classUrl in EXTRA_CLASS_URLS:
			self.classQueue.put(classUrl)

		# Check each index
		for url in BASE_INDEX_URLS:
			self.logger.info("Fetching Index: " + url)
			self._processIndex(url)

			# Process all the classes
			while not self.classQueue.empty():
				# Retrieve the next item
				classUrl = self.classQueue.get()
				self.logger.info("Fetching documentation: " + classUrl)

				# Process the data
				typingList = self.parser.processClassApi(classUrl)
				if typingList is None:
					continue

				# Put the items in the queue
				for typing in typingList:
					self.typings.put(typing)

		# Add the extra typing to the list
		for typing in EXTRA_KNOWN_ITEMS:
			self.typings.put(typing)

		# Write to files
		TypingWriter(self.logger).write(self.typings)

	def _processIndex(self, url: str) -> None:
		""" Process the index file with all the classes
		"""
		# Retrieve the page
		r = requests.get(url)
		if r.status_code != 200:
			self.logger.error("This index '%s' doesnt work!" % url)
			return

		# Process the HTML
		soup = BeautifulSoup(r.text, 'html.parser')
		indexTable = soup.find(id="class-summary")
		if indexTable is None:
			indexTable = soup.find(id="class-summary-classes-summary")

		# Check each row
		for aTag in indexTable.find_all("a", class_="reference"):
			aHref: str = aTag["href"]
			if "#" in aHref:
				aHref = aHref[:aHref.find("#")]
			self.classQueue.put(aHref)
