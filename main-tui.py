#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
terminal user-interface
"""

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.widgets import Header, Footer, TabbedContent, TabPane, Static, MarkdownViewer, Rule
from pathlib import Path
from my_babel_py.core.cste import SYS_INFO, MODIFIED_BOURGES_QUOTE


class Tab_Find(TabPane):
	def compose(self) -> ComposeResult:
		with Horizontal():
			with Vertical():
				yield Static("1")
				yield Static("2")
			with Vertical():
				yield Static("3")
				yield Static("4")


class Tab_Browse(TabPane):
	def compose(self) -> ComposeResult:
		with Horizontal():
			with Vertical():
				yield Static("1")
				yield Static("2")
			with Vertical():
				yield Static("3")
				yield Static("4")


class Tab_Help(TabPane):
	def compose(self) -> ComposeResult:
		with TabbedContent():
			with TabPane("System info"):
				yield Static("The extended “Library of Babel” in terminal: search for a book or browse books")
				yield Rule(line_style="dashed")
				yield Static(SYS_INFO)
				yield Rule(line_style="dashed")
				yield Static(MODIFIED_BOURGES_QUOTE)
			with TabPane("About"):
				yield MarkdownViewer(Path("docs", "1-ABOUT.md").read_text(encoding="utf-8"))
			with TabPane("Details"):
				yield MarkdownViewer(Path("docs", "2-DETAILS.md").read_text(encoding="utf-8"))


class MyApp(App):
	CSS_PATH = "assets/style.tcss"
	TITLE = "LIBRARY OF BABEL"
	BINDINGS = [
		Binding(key="q", action="quit", description="Quit"), # built-in: no need to define a function
		Binding(key="d", action="toggle_dark", description="Toggle dark mode"), # built-in: no need to define a function
	]

	def compose(self) -> ComposeResult:
		yield Header(show_clock=True)
		yield Footer()
		with TabbedContent():
			yield Tab_Help("Help", id="tab-help")
			yield Tab_Find("Find")
			yield Tab_Browse("Browse")


MyApp().run()
