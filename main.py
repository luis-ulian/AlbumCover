import asyncio
from winsdk.windows.media.control import \
    GlobalSystemMediaTransportControlsSessionManager as MediaManager
from winsdk.windows.storage.streams import DataReader

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

        cover = bytearray(stream.size)
        reader.read_bytes(cover)

        await print_album_cover(cover)
        print("album cover found.")

async def print_album_cover(cover):
    print(cover)

asyncio.run(get_media_info())