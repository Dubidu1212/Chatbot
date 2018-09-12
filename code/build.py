from cx_Freeze import setup, Executable

base = None

executables = [Executable("bot.py", base=base)]

packages = ["idna"]
options = {
    'build_exe': {
        'packages':packages,
    },
}

setup(
    name = "<Werewolf>",
    options = options,
    version = "<0.0>",
    description = '<Bot>',
    executables = executables
)
