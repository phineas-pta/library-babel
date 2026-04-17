#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
terminal user-interface
"""

from typing import final, Final
from pathlib import Path

from .core import config

if not config.CAPABILITIES["tui"]:
	raise RuntimeError("TUI is not supported on this system.")

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.screen import Screen
from textual.widget import Widget
from textual import containers as c, widgets as w

_project_dir: Final = Path(__file__).parents[1]

###############################################################################

@final
class BookSaving(Widget):
	def compose(self) -> ComposeResult:
		yield w.Checkbox("save book content")
		yield w.Checkbox("save png image")
		yield w.Checkbox("save pdf document")
		yield w.Static("choose directory to save files")
		yield w.DirectoryTree("~/")


@final
class ScreenHome(Screen):
	SUB_TITLE = "Home"

	def compose(self) -> ComposeResult:
		yield w.Header(show_clock=True)
		yield w.Footer()
		yield w.Static("The extended “Library of Babel” in terminal", markup=False)
		yield w.Static(config.MODIFIED_BOURGES_QUOTE, markup=False)
		yield w.Rule(line_style="dashed") # shameless copy from @zwyx
		yield w.Static("[b]Welcome, visitor[/b]")
		yield w.Static("The “Library of Babel” contains [i]all the books[/i].")
		yield w.Static("Every book [i]that has [b]ever been[/b] written[/i].")
		yield w.Static("Every book [i]that will [b]ever be[/b] written[/i].")
		yield w.Static("And the vast majority of books [i]that will [b]never be[/b] written[/i].")
		yield w.Button("Search for text", variant="success", action="app.switch_mode('search')")
		yield w.Button("Browse a book", variant="primary", action="app.switch_mode('browse')")
		yield w.Rule(line_style="dashed")
		yield w.Static(config.SRC_URL, markup=False)


@final
class ScreenHelp(Screen):
	SUB_TITLE = "Help"

	def compose(self) -> ComposeResult:
		yield w.Header(show_clock=True)
		yield w.Footer()
		with w.TabbedContent():
			with w.TabPane("System info"):
				yield w.Static(config.SYS_INFO, markup=False)
			with w.TabPane("About"):
				yield w.MarkdownViewer(Path(_project_dir, "docs", "1-ABOUT.md").read_text(encoding="utf-8"))
			with w.TabPane("Details"):
				yield w.MarkdownViewer(Path(_project_dir, "docs", "2-DETAILS.md").read_text(encoding="utf-8"))


###############################################################################

@final
class ScreenSearch(Screen):
	SUB_TITLE = "Search"

	def compose(self) -> ComposeResult:
		yield w.Header(show_clock=True)
		yield w.Footer()
		with c.Horizontal():
			with c.Vertical():
				yield w.Static("enter text to search for a book", markup=False)
				yield w.TextArea(show_line_numbers=True)
				yield w.Button("Search", variant="primary")
			with c.VerticalScroll():
				for i in range(config.PAGES_PER_BOOK):
					yield w.Static(f"Page {i}", markup=False)
			with c.Vertical(classes="sidebar"):
				with w.RadioSet():
					yield w.Static("Fill option", markup=False)
					yield w.RadioButton("empty", value=True)
					yield w.RadioButton("random")
				yield w.Checkbox("save book position", True)
				yield BookSaving()


###############################################################################

@final
class ScreenBrowse(Screen):
	SUB_TITLE = "Browse"

	def compose(self) -> ComposeResult:
		yield w.Header(show_clock=True)
		yield w.Footer()
		with c.Horizontal():
			with c.Vertical(classes="sidebar"):
				yield w.Static("choose book position file", markup=False)
				yield w.DirectoryTree("./")
				yield w.Button("Browse", variant="primary")
			with c.VerticalScroll():
				for i in range(config.PAGES_PER_BOOK):
					yield w.Static(f"Page {i}", markup=False)
			with c.Vertical(classes="sidebar"):
				yield BookSaving()


###############################################################################

@final
class MyApp(App):
	TITLE = "LIBRARY of BABEL"
	CSS_PATH = Path(_project_dir, "assets", "style.tcss")
	MODES = {"home": ScreenHome, "search": ScreenSearch, "browse": ScreenBrowse, "help": ScreenHelp}
	DEFAULT_MODE = "home"
	BINDINGS = [
		Binding(key="q", action="quit", description="Quit"), # built-in action: no need to define a function
		Binding(key="d", action="toggle_dark", description="Toggle dark mode"), # idem
		Binding(key="escape", action="switch_mode('home')", description="Home"), # idem
		Binding(key="s", action="switch_mode('search')", description="Search"),
		Binding(key="b", action="switch_mode('browse')", description="Browse"),
		Binding(key="f1", action="switch_mode('help')", description="Help"),
	]
	AUTO_FOCUS = "" # to disable
	ENABLE_COMMAND_PALETTE = False

	def on_mount(self) -> None:
		self.theme = "tokyo-night"


if __name__ == "__main__":
	MyApp().run()
