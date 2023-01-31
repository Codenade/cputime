# CPU process tracker

A tool to track the top processes running on the system.

## Usage

Install Python

Install required dependencies:

* psutil
* keyboard

`pip install psutil keyboard`

Use python to execute `toptasks.py`.

### Arguments

`python toptasks.py [file] [<additional arguments>] `

##### `[file]` :  The path where the resulting csv file will be saved to (e.g. ~/example.csv)
##### `-i`, `--interval` : Set a sampling interval in seconds (default = 0.5)
##### `--hotkey` : Set a hotkey to mark a section of the output. Format according to [boppreh/keyboard](https://github.com/boppreh/keyboard#keyboardadd_hotkeyhotkey-callback-args-suppressfalse-timeout1-trigger_on_releasefalse)
##### ~~`-f`, `--format`~~ : unused

### Supported output formats (at the time):

* csv

## Dependencies

* Python
* psutil
* keyboard