# -*- coding: utf-8 -*-
import logging
import sys
from queue import Queue
from typing import Any

import requests
from bs4 import BeautifulSoup, Tag

from .interfaces import ITyping, TypingType, ITypingClass, ITypingLiteral, ITypingFunction
from .parser import Parser
from .writer import TypingWriter


# Some starting points to find the data
BASE_INDEX_URLS: list[str] = [
	"https://docs.wxpython.org/wx.1moduleindex.html",
	"https://docs.wxpython.org/wx.ribbon.1moduleindex.html",
	"https://docs.wxpython.org/wx.lib.buttons.html",
	"https://docs.wxpython.org/wx.lib.calendar.html",
	"https://docs.wxpython.org/wx.lib.scrolledpanel.html",
	"https://docs.wxpython.org/wx.lib.dialogs.html",
	"https://docs.wxpython.org/wx.lib.newevent.html",
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
EXTRA_KNOWN_ITEMS: list[ITyping] = []
lObj: ITypingLiteral = {
	"type": TypingType.LITERAL,
	"name": "GROW",
	"moduleName": "wx",
	"returnType": "int",
	"docstring": "Synonym of wx.EXPAND",
	"source": "",
}
EXTRA_KNOWN_ITEMS.append(lObj)
lObj = {
	"type": TypingType.LITERAL,
	"name": "RA_HORIZONTAL",
	"moduleName": "wx",
	"returnType": "int",
	"docstring": "Synonym of wx.HORIZONTAL",
	"source": "",
}
EXTRA_KNOWN_ITEMS.append(lObj)
lObj = {
	"type": TypingType.LITERAL,
	"name": "RA_VERTICAL",
	"moduleName": "wx",
	"returnType": "int",
	"docstring": "Synonym of wx.VERTICAL",
	"source": "",
}
EXTRA_KNOWN_ITEMS.append(lObj)
lObj = {
	"type": TypingType.LITERAL,
	"name": "NORMAL",
	"moduleName": "wx",
	"returnType": "int",
	"docstring": "",
	"source": "",
}
EXTRA_KNOWN_ITEMS.append(lObj)
lObj = {
	"type": TypingType.LITERAL,
	"name": "DEFAULT",
	"moduleName": "wx",
	"returnType": "int",
	"docstring": "",
	"source": "",
}
EXTRA_KNOWN_ITEMS.append(lObj)
lObj = {
	"type": TypingType.LITERAL,
	"name": "wxEVT_COMMAND_BUTTON_CLICKED",
	"moduleName": "wx",
	"returnType": "int",
	"docstring": "",
	"source": "",
}
EXTRA_KNOWN_ITEMS.append(lObj)
lObj = {
	"type": TypingType.LITERAL,
	"name": "RED",
	"moduleName": "wx",
	"returnType": "int",
	"docstring": "",
	"source": "",
}
EXTRA_KNOWN_ITEMS.append(lObj)
lObj = {
	"type": TypingType.LITERAL,
	"name": "YELLOW",
	"moduleName": "wx",
	"returnType": "int",
	"docstring": "",
	"source": "",
}
EXTRA_KNOWN_ITEMS.append(lObj)
lObj = {
	"type": TypingType.LITERAL,
	"name": "BLACK",
	"moduleName": "wx",
	"returnType": "int",
	"docstring": "",
	"source": "",
}
EXTRA_KNOWN_ITEMS.append(lObj)
lObj = {
	"type": TypingType.LITERAL,
	"name": "WHITE",
	"moduleName": "wx",
	"returnType": "int",
	"docstring": "",
	"source": "",
}
EXTRA_KNOWN_ITEMS.append(lObj)
lObj = {
	"type": TypingType.LITERAL,
	"name": "BLUE",
	"moduleName": "wx",
	"returnType": "int",
	"docstring": "",
	"source": "",
}
EXTRA_KNOWN_ITEMS.append(lObj)
lObj = {
	"type": TypingType.LITERAL,
	"name": "GREEN",
	"moduleName": "wx",
	"returnType": "int",
	"docstring": "",
	"source": "",
}
EXTRA_KNOWN_ITEMS.append(lObj)
lObj = {
	"type": TypingType.LITERAL,
	"name": "CYAN",
	"moduleName": "wx",
	"returnType": "int",
	"docstring": "",
	"source": "",
}
EXTRA_KNOWN_ITEMS.append(lObj)
lObj = {
	"type": TypingType.LITERAL,
	"name": "OPEN",
	"moduleName": "wx",
	"returnType": "int",
	"docstring": "",
	"source": "",
}
EXTRA_KNOWN_ITEMS.append(lObj)
lObj = {
	"type": TypingType.LITERAL,
	"name": "EVT_TIMER",
	"moduleName": "wx",
	"returnType": "int",
	"docstring": "",
	"source": "",
}
EXTRA_KNOWN_ITEMS.append(lObj)
cObj: ITypingClass = {
	"type": TypingType.CLASS,
	"name": "FrozenWindow",
	"moduleName": "wx",
	"source": "",
	"superClass": ["ContextManager"],
	"docstring": "Freeze the window and all its children.",
	"functions": [
		{
			"type": TypingType.FUNCTION,
			"name": "__init__",
			"moduleName": "wx.FrozenWindow",
			"returnType": "None",
			"methodType": "normal",
			"source": "",
			"docstring": "Constructor",
			"params": {
				"window": "'Window'",
			},
			"paramStr": "self, window: 'Window'",
		}, {
			"type": TypingType.FUNCTION,
			"name": "__enter__",
			"moduleName": "wx.FrozenWindow",
			"returnType": "None",
			"methodType": "normal",
			"source": "",
			"docstring": "Enter the context manager.",
			"params": {},
			"paramStr": "self",
		}, {
			"type": TypingType.FUNCTION,
			"name": "__exit__",
			"moduleName": "wx.FrozenWindow",
			"returnType": "None",
			"methodType": "normal",
			"source": "",
			"docstring": "Exit the context manager.",
			"params": {},
			"paramStr": "self, *args, **kwargs",
		}
	],
}
EXTRA_KNOWN_ITEMS.append(cObj)
lObj = {
	"type": TypingType.LITERAL,
	"name": "NullCursor",
	"moduleName": "wx",
	"returnType": "'Cursor'",
	"docstring": "",
	"source": "",
}
EXTRA_KNOWN_ITEMS.append(lObj)
lObj = {
	"type": TypingType.LITERAL,
	"name": "LIST_AUTOSIZE",
	"moduleName": "wx",
	"returnType": "int",
	"docstring": "",
	"source": "",
}
EXTRA_KNOWN_ITEMS.append(lObj)
fObj: ITypingFunction = {
	"type": TypingType.FUNCTION,
	"name": "NewCommandEvent",
	"methodType": "normal",
	"moduleName": "wx.lib.newevent",
	"returnType": "tuple['Event', int]",
	"params": {},
	"paramStr": "",
	"docstring": "Generates a new (command_event, binder) tuple.",
	"source": "https://docs.wxpython.org/wx.lib.newevent.html",
}
EXTRA_KNOWN_ITEMS.append(fObj)
fObj = {
	"type": TypingType.FUNCTION,
	"name": "NewEvent",
	"methodType": "normal",
	"moduleName": "wx.lib.newevent",
	"returnType": "tuple['Event', int]",
	"params": {},
	"paramStr": "",
	"docstring": "Generates a new (event, binder) tuple.",
	"source": "https://docs.wxpython.org/wx.lib.newevent.html",
}
EXTRA_KNOWN_ITEMS.append(fObj)
OVERRIDES: dict[str, dict[str, Any]] = {
	"wx.ListCtrl.GetFirstSelected": {
		"returnType": "int",
	},
	"wx.ListCtrl.GetFocusedItem": {
		"returnType": "int",
	},
	"wx.NewIdRef": {
		"returnType": "int",
	},
	"wx.ListCtrl.OnGetItemAttr": {
		"returnType": "Optional['ItemAttr']",
	},
	"wx.TreeCtrl.GetItemData": {
		"returnType": "Any",
	},
	"wx.TreeCtrl.GetFirstChild": {
		"returnType": "tuple['TreeItemId', str]",
	},
	"wx.TreeCtrl.GetNextChild": {
		"returnType": "tuple['TreeItemId', str]",
	},
	"wx.GetApp": {
		"returnType": "'App'",
	},
	"wx.App": {
		"superClass": ["PyApp", "AppConsole"],
	},
	"wx.App.Get": {
		"returnType": "'App'",
	}
}


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
				self.parser.processClassApi(classUrl)

		# Retrieve the parse data and put it in the queue
		typingDict = self.parser.retrieveFoundClasses()
		for typing in typingDict.values():
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
		if indexTable is None:
			return
		if not isinstance(indexTable, Tag):
			return

		# Check each row
		for aTag in indexTable.find_all("a", class_="reference"):
			aHref: str = aTag["href"]
			if "#" in aHref:
				aHref = aHref[:aHref.find("#")]
			self.classQueue.put(aHref)
