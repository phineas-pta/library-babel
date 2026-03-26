#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
terminal user-interface
"""

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Header, Footer, TabbedContent, TabPane, Label, Markdown, Placeholder
from pathlib import Path
from my_babel_py.core.cste import SYS_INFO


with (Path(__file__).parent / "docs" / "1-ABOUT.md").open(mode="r", encoding="utf-8") as f:
	about_page = f.read()
with (Path(__file__).parent / "docs" / "2-DETAILS.md").open(mode="r", encoding="utf-8") as f:
	details_page = f.read()


class MyApp(App):
	TITLE = "LIBRARY OF BABEL"
	BINDINGS = [
		Binding(key="q", action="quit", description="Quit the app"),
		Binding(key="question_mark", action="help", description="Show help screen", key_display="?"),
	]

	def compose(self) -> ComposeResult:
		yield Header(show_clock=True)
		yield Footer()
		with TabbedContent():
			with TabPane("Search"):
				yield Placeholder()
			with TabPane("Find"):
				yield Placeholder()
			with TabPane("System info"):
				yield Label(SYS_INFO)
			with TabPane("About"):
				yield Markdown(about_page)
			with TabPane("Details"):
				yield Markdown(details_page)


MyApp().run()
