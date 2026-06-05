import asyncio
from winsdk.windows.media.control import \
    GlobalSystemMediaTransportControlsSessionManager as MediaManager
from winsdk.windows.storage.streams import DataReader
from PIL import Image
import io
import os
import keyboard

light_to_dark = ["$","@","B","%","8","&","W","M","#","*","o","a","h","k","b","d","p","q","w","m","Z","O","0","Q","L","C","J","U","Y","X","z","c","v","u","n","x","r","j","f","t","/","\\","|","(",")","1","{","}","[","]","?","-","_","+","~","<",">","i","!","l","I",";",":",",",'"',"^","`","'","."," "]
light_to_dark.reverse()

x_size = 80
y_size = int(x_size/2)

previous = None

async def get_media_info(previous):
    while True:
        sessions = await MediaManager.request_async()
        current = sessions.get_current_session()
        
        if not current:
            print("no media found.")
            return

        info = await current.try_get_media_properties_async()

        if previous == None or (info.title != previous.title or info.artist != previous.artist):
            os.system('cls')
            print("title:", info.title)
            print("artist:", info.artist)

            if info.thumbnail:
                stream = await info.thumbnail.open_read_async()

                reader = DataReader(stream)
                await reader.load_async(stream.size)

                data = bytearray(stream.size)
                reader.read_bytes(data)
                
                cover = io.BytesIO(data)

                await print_album_cover(cover)
        previous = info
        if keyboard.is_pressed('esc'):
            break

            
            

async def print_album_cover(cover):
    image = Image.open(cover)
    image = image.resize([x_size,y_size])
    px = image.load()

    for y in range(y_size - 1):
        line = ""
        for x in range(x_size - 1):
            pixel = px[x,y]
            colorgray = rgb_to_grayscale(pixel[0],pixel[1],pixel[2])
            line = line + painted_char(pixel[0], pixel[1], pixel[2], light_to_dark[round(colorgray/3.7)])
        print(line)
            
def rgb_to_grayscale(R,G,B):
    return (0.299 * R) + (0.587 * G) + (0.114 * B)

def painted_char(R,G,B,char):
    return("\x1b[" + "38;2;" + str(R) + ";" + str(G) + ";" + str(B) + "m" + char + "\x1b[0m")

asyncio.run(get_media_info(previous))

    
