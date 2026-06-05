import asyncio
from winsdk.windows.media.control import \
    GlobalSystemMediaTransportControlsSessionManager as MediaManager
from winsdk.windows.storage.streams import DataReader
from PIL import Image
import io

light_to_dark = ["$","@","B","%","8","&","W","M","#","*","o","a","h","k","b","d","p","q","w","m","Z","O","0","Q","L","C","J","U","Y","X","z","c","v","u","n","x","r","j","f","t","/","\\","|","(",")","1","{","}","[","]","?","-","_","+","~","<",">","i","!","l","I",";",":",",",'"',"^","`","'","."," "]
light_to_dark.reverse()

x_size = 160
y_size = 80

async def get_media_info():
    sessions = await MediaManager.request_async()
    current = sessions.get_current_session()

    if not current:
        print("No media found.")
        return

    info = await current.try_get_media_properties_async()

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

async def print_album_cover(cover):
    image = Image.open(cover)
    image = image.resize([x_size,y_size])
    px = image.load()

    for y in range(y_size - 1):
        line = ""
        for x in range(x_size - 1):
            pixel = px[x,y]
            colorgray = rgb_to_grayscale(pixel[0],pixel[1],pixel[2])
            line = line + "\x1b[" + "38;2;" + str(pixel[0]) + ";" + str(pixel[1]) + ";" + str(pixel[2]) + "m" +  light_to_dark[round(colorgray/3.7)] + "\x1b[0m"
        print(line)
            
def rgb_to_grayscale(R,G,B):
    return (0.299 * R) + (0.587 * G) + (0.114 * B)

asyncio.run(get_media_info())
