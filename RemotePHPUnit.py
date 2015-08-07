import os
import sys
import shlex
import subprocess
import sublime
import sublime_plugin

if sys.version_info < (3, 3):
    raise RuntimeError('RemotePHPUnit works with Sublime Text 3 only')

SPU_THEME = 'Packages/RemotePHPUnit/RemotePHPUnit.hidden-tmTheme'
SPU_SYNTAX = 'Packages/RemotePHPUnit/RemotePHPUnit.hidden-tmLanguage'

class ShowInPanel:
    def __init__(self, window):
        self.window = window

    def display_results(self):
        self.panel = self.window.get_output_panel("exec")
        self.window.run_command("show_panel", {"panel": "output.exec"})

        self.panel.settings().set("color_scheme", SPU_THEME)
        self.panel.set_syntax_file(SPU_SYNTAX)

class RemotePhpUnitCommand(sublime_plugin.WindowCommand):
    def __init__(self, *args, **kwargs):
        super(RemotePhpUnitCommand, self).__init__(*args, **kwargs)
        self.settings         = sublime.load_settings('RemotePHPUnit.sublime-settings')
        self.phpunit_path     = self.settings.get('phpunit_path')
        self.root_folder      = self.settings.get('root_folder')
        self.ssh_key          = self.settings.get('ssh_key')
        self.server_user      = self.settings.get('server_user')
        self.server_address   = self.settings.get('server_address')
        self.server_port      = self.settings.get('server_port')
        self.phpunit_xml      = self.settings.get('phpunit_xml')

        if (str(self.phpunit_path) == ""):
            sublime.status_message("You have to set the phpunit_path in the RemotePHPUnit configuration")

        if (str(self.server_address) == ""):
            sublime.status_message("You have to set the server_address in the RemotePHPUnit configuration")

    def run(self, *args, **kwargs):
        try:
            self.PROJECT_PATH = self.window.folders()[0] + "/"

            self.params = kwargs.get('params', False)
            self.type = kwargs.get('type', False)
            self.group = ""
            self.filename = ""

            if self.type == "unit":
                self.group = " --exclude-group functional_test"
            elif self.type == "functional":
                self.group = " --group functional_test"
            elif self.type == "current_file":
                self.filename = self.file_name()
                if not os.path.isfile(self.filename):
                    sublime.status_message("file " + self.filename + " not found")
                    return False
                else:
                    self.filename = self.filename[len(self.PROJECT_PATH):]

            self.on_done()
        except IndexError:
            sublime.status_message("Please open a project with PHPUnit")

    def file_name(self):
        return self.window.active_view().file_name()

    def on_done(self):
        try:
            self.run_shell_command(self.PROJECT_PATH)
        except IOError:
            sublime.status_message('IOError - command aborted')

    def run_shell_command(self, working_dir):
            self.window.run_command("exec", {
                "cmd": self.build_command(),
                "shell": True,
                "working_dir": working_dir
            })
            self.display_results()
            return True

    def build_command(self):
        command = "ssh "

        # add ssh key if configured
        if (self.ssh_key):
            command += " -i " + self.ssh_key + " "

        # add server user if configured
        if (self.server_user):
            command += self.server_user + "@"

        # add server address
        command += self.server_address

        command += " "

        if (self.server_port):
            command += "-p " + self.server_port

        if (self.root_folder):
            command += " ' cd /" + self.root_folder + "; "

        # set the php_unit path and group
        command += self.phpunit_path + self.group

        # set the xml configuration path if configured
        if (self.phpunit_xml):
            command += " -c " + self.phpunit_xml

        # set file name if set
        if (self.filename):
            command += " " + self.filename

        command += "'"

        return command;

    def display_results(self):
        display = ShowInPanel(self.window)
        display.display_results()

    def window(self):
        return self.view.window()
