import sys
import os
import glob

import sublime
import sublime_plugin


class ExecuteCommand(sublime_plugin.WindowCommand):
    def __init__(self, *args, **kwargs):
        #self.get_commands()
        super(ExecuteCommand, self).__init__(*args, **kwargs)

    def get_commands(self):
        """
        This is a stub for getting the existing commands and adding
        autocomplete
        """
        packages = os.listdir(sublime.packages_path())
        self.packages = sorted(packages, key=lambda s: s.lower())
        self.window_commands = []

        for package in self.packages:
            package_dir = sublime.packages_path() + '/' + package
            sys.path.append(package_dir)
            __all__ = [os.path.basename(f)[:-3] for f in glob.glob(package_dir + "/*.py")]
            for sub_package in __all__:
                module = __import__(sub_package)
                for obj in dir(module):
                    actual_obj = getattr(module, obj)
                    if isinstance(actual_obj,
                                  sublime_plugin.WindowCommand):
                        self.window_commands.append(obj)
                    if isinstance(actual_obj,
                                  sublime_plugin.TextCommand):
                        self.window_commands.append(obj)

        print self.window_commands

    def on_done(self, text):
        command = text

        view = self.window.active_view()

        view.run_command(command)
        self.window.run_command(command)

        #edit = view.begin_edit()
        #view.insert(edit, 0, text)
        #view.end_edit(edit)

    def run(self):
        self.window.show_input_panel(
            "Command:", "", self.on_done, None, None)
