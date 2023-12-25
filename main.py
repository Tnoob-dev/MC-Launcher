from minecraft_launcher_lib.utils import get_minecraft_directory
from minecraft_launcher_lib.command import get_minecraft_command
import subprocess
import uuid
import os
from configparser import ConfigParser

settings = ConfigParser()

def checkSettings():

    if not os.path.exists('./Settings.ini'):

        optsUserCfg_file: dict = {}
        optsMineCfg_file: dict = {}
        print("No existe aun\nSe creara un archivo config.ini")


        # Take Username from user or from user PC
        username: str = input("Introduzca su nombre de usuario (Tambien puede dejarlo en blanco y presionar enter, en ese caso se utilizara el nombre de usuario de la PC): ")
        optsUserCfg_file['username'] = username
        
        if username == '':
            optsUserCfg_file['username'] = os.getenv('USERNAME')
        
        # Take Minecraft path from the user or from the MC module automatically
        minecraftPath: str = input("Introduzca la ubicacion de su Minecraft, en caso de dejarlo en blanco se utilizara la ruta por defecto: ")
        optsMineCfg_file['mc_path'] = minecraftPath
        
        if minecraftPath == '':
            optsMineCfg_file['mc_path'] = get_minecraft_directory()

        # Take last version of MC from ur PC
        # optsMineCfg_file['mc_version'] = get_latest_version()['release']
        optsMineCfg_file['mc_version'] = '1.20.4' # Use the version that you have in ur PC

        # UUID and token Things (for offline purposes don't care)
        namespace = uuid.NAMESPACE_URL
        optsUserCfg_file['uuid'] = str(uuid.uuid5(namespace, username))

        optsUserCfg_file['token'] = ''

        # Now all things to create the settings.ini
        settings['USER'] = optsUserCfg_file
        settings['MINECRAFT'] = optsMineCfg_file

        with open("Settings.ini", "w") as settingsFile:
            settings.write(settingsFile)

def openMC():
    settings.read('./Settings.ini')
    version = settings['MINECRAFT']['mc_version']
    path = settings['MINECRAFT']['mc_path']

    options = {
        'username': settings['USER']['username'],
        'uuid': settings['USER']['uuid'],
        'token': settings['USER']['token'],
    }
    
    mineCommands = get_minecraft_command(version=version, minecraft_directory=path, options=options)

    subprocess.run(mineCommands)

def main():
    checkSettings()
    openMC()
    
if __name__ == "__main__":
    main()
