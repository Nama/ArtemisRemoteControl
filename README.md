# ArtemisRemoteControl
Library and script loader to control LEDs over the WebAPI of Artemis with [this plugin](https://gist.github.com/SpoinkyNL/fb7d03b22ddfb19ddc150de1b99053e2).
## Usage
### Download exe
Go to [Actions](https://github.com/Nama/ArtemisRemoteControl/actions) or [Releases](https://github.com/Nama/ArtemisRemoteControl/releases) and download ArtemisRemoteControl
### Using the source
If you already have python installed and know how to venv and pip, use this method:

1. Create a new virtualenv
2. `pip install https://github.com/Nama/ArtemisRemoteControl/archive/refs/heads/main.zip`

### Config
Edit `config.json` to your needs or use `config.add()` (read below). Put the [example](https://github.com/Nama/ArtemisRemoteControl/tree/main/scripts) or your own scripts into your `scripts` folder.
If you've downloaded the exe, run it. Else, run `run.py`.

## Scripting
- Put your own scripts in to the folder `scripts`
- Always use `from threading import Thread`, the plugin loader is blocking
- Do `from artemisremotecontrol import getleds, setleds`
    - Use `getleds` to get a json file with all available LEDs
    - To set LEDs: `setleds(devices, leds, '#AA00FF)`
        - `devices` and `leds` need to be lists. So you can define a whole set of LEDs with the same conditions
- You can use the `Config()` class for your own scripts  
  Use these to initialize, so all scripts have their own "namespace" in the config:
```py
from artemisremotecontrol.config import Config
try:
    # Get the filename and use it for the config
    config_name = __name__.split('.')[1]
except IndexError:
    # Script was started directly, not with run.py, exit
    # Read scripts/tasmota.py for a full example
    exit()

config = Config()
config.load(config_name)
...
config.add(config_name, [url, key, value, devices, leds, color1, color2, color3])
```

## venv
My idea was to have `run.py` in PATH of the venv and just do `run.py` to run it.  
`run.py` gets set to the path in the venv, also the shebang gets correctly set, but I couldn't run it. Windows complains, that there is no program defined to run that file.  
So, we (or only I?) have to get the `run.py` from this repo and run it in the cwd.