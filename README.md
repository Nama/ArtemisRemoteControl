# ArtemisRemoteControl
Library and script loader to control LEDs over the WebAPI of Artemis with [Cheerpipes plugin](https://github.com/Cheerpipe/Artemis.Plugins.Public/tree/master/src/Modules/Artemis.Plugins.Modules.Json).
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
- check `tasmota.py` for a full working example
- Always use `from threading import Thread`, the plugin loader is blocking
- Do `from artemisremotecontrol import setleds`
    - To set LEDs: `setleds({'scriptname': {key, value}, url)`
        - This appears in Artemis as a DataModel
        - Set in Artemis what you want to do with the data
- `setleds()` returns the endpoint URL, just send it again as the second parameter, so the URL doesn't need to be looked up again
- You can use the `Config()` class for your own scripts  
  Use these to initialize, so all scripts have their own "namespace" in the config:
```py
from artemisremotecontrol.config import Config
from artemisremotecontrol import setleds
from threading import Thread
from time import sleep
endpoint_url = None
try:
    # Get the filename and use it for the config
    config_name = __name__.split('.')[1]
except IndexError:
    # Script was started directly, not with run.py, exit
    # Read scripts/tasmota.py for a full example
    exit()

def loop():
    while True:
        global endpoint_url
        data = {config_name: {'key', 'value'}}
        endpoint_url = setleds(data, endpoint_url)
        sleep(5)

config = Config()
config.load(config_name)
#Config.add(config_name, device)

tloop = Thread(target=loop)
tloop.start()
```

## venv
My idea was to have `run.py` in PATH of the venv and just do `run.py` to run it.  
`run.py` gets set to the path in the venv, also the shebang gets correctly set, but I couldn't run it. Windows complains, that there is no program defined to run that file.  
So, we (or only I?) have to get the `run.py` from this repo and run it in the cwd.