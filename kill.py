#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Plugin to kill a rogue process."""

import psutil
import sublime
import sublime_plugin


class KillCommand(sublime_plugin.WindowCommand):
    """
    Kill a rogue process.
    """
    def run(self):
        """
        Iterates through all currently active processes looking
        for one associated with the file to kill, then attempts
        to kill that process.
        """
        path = self.window.extract_variables()['file']
        sublime.status_message("Looking for the rogue process...")
        for process in map(psutil.Process, psutil.pids()):
            try:
                if path in process.cmdline():
                    process.kill()
                    sublime.status_message("Killed process with "
                                           "pid {0}!".format(process.pid))
                    break
            except psutil.AccessDenied:
                pass
        else:
            sublime.status_message('Found no process to kill!')

    def description(self):
        """Returns a description for the command."""
        return self.__doc__
