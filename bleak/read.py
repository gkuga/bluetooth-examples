import asyncio
from bleak import BleakClient


async def run(address):
    client = BleakClient(address)
    try:
        await client.connect()
        print(f"Connected: {client.is_connected}")

    finally:
        if client.is_connected:
            await client.disconnect()
            print("Disconnected")

# メイン関数
if __name__ == "__main__":
    device_address = "12345678-XXXX-YYYY-ZZZZ-123456789012"
    asyncio.run(run(device_address))
