Remote PHPUnit commands
=======================

Originally forked from https://github.com/paza/RemotePHPUnit-for-Sublime-Text


This plugin allows you the run the PHPUnit on a remote server tests using the Sublime Text interface, without having to open and use the command line.

### Available commands:

- `Remote PHPUnit: Run all`
- `Remote PHPUnit: Run unit tests`
- `Remote PHPUnit: Run functional tests`
- `Remote PHPUnit: Run tests in current file`

### Coloring output

![Coloring output](https://raw.github.com/m0nah/SimplePHPUnit-for-Sublime-Text/master/Screen%20Shot.png)

### Installation:
Use Package Controller or create a the directory `RemotePHPUnit` in your Sublime Text Packages directory, and you're ready to go.

### Configuration:

The server_address configuration is mandatory.

An example for a Vagrant setup looks as follows:

Find out your key file with `vagrant ssh-config`
```
{
	"phpunit_path": "/usr/bin/phpunit",
    "phpunit_xml_path": "phpunit-dev.xml",
    "root_folder": "vagrant",
    "server_user": "vagrant",
    "server_address": "127.0.0.1",
    "server_port": "2222",
    "ssh_key": "/path/to/vagrant_key"

}
```
* The shared folder on vagrant is /vagrant
* The phpunit_xml is the relative path to the project root

### Usage:
Press Cmd + Shift + P for the dropdown command list, search for `Remote PHPUnit: `, and pick your command. Also you can use `Tools/Remote PHPUnit` menu item

### Notes:
- You need insert in Sublime Text user settings `"show_panel_on_build": true` or use `Tools/Build Results/Show Build Results` menu item for view results.

Special thanks to [@evgeny-golubev](https://www.github.com/evgeny-golubev) and [@paza](https://www.github.com/paza)
