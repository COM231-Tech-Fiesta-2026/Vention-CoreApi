import asyncio
from src.ventio_api.infrastructure.cron.cron_service import CronService


async def cron_runner():
    cron_service = CronService()

    while True:
        print("[CRON] Checking for stale conversations...")
        try:
            await cron_service.summarize_stale_conversations()
        except Exception as e:
            print(f"[CRON] Unexpected rror cron job: {e}")

        await asyncio.sleep(60)


if __name__ == "___main__":
    asyncio.run(cron_runner())
