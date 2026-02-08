from datetime import datetime, timedelta, timezone
from src.ventio_api.infrastructure.database.conversations_db import ConversationDatabase
from src.ventio_api.infrastructure.database.messages_db import MessageDatabase
from src.ventio_api.infrastructure.database.summaries_db import SummaryDatabase
from src.ventio_api.models.summary_model import Summary
from uuid import uuid4


class CronService:

    def __init__(self):
        self.convo_db = ConversationDatabase()
        self.messages_db = MessageDatabase()
        self.summaries_db = SummaryDatabase()

    async def summarize_stale_conversations(self):
        one_hour = datetime.now(timezone.utc) - timedelta(hours=1)

        try:
            conversations = await self.convo_db.get_stale_conversations(
                time_threshold=one_hour
            )
        except Exception as e:
            print(f"[CRON] Failed to fetch stale conversations: {e}")
            return

        for convo in conversations:
            try:
                messages = await self.messages_db.get_many(
                    conversation_id=convo.conversation_id
                )
                ## mock llm call
                summary = await llm.summarize(
                    "\n".join([message.message for message in messages])
                )

                await self.summaries_db.insert(
                    Summary(
                        summary_id=uuid4(),
                        conversation_id=convo.conversation_id,
                        title=summary.title,
                        content=summary.content,
                        timestamp=datetime.now(timezone.utc),
                    )
                )

                await self.messages_db.delete(conversation_id=convo.conversation_id)
                await self.convo_db.delete(conversation_id=convo.conversation_id)

            except Exception as e:
                print(
                    f"[CRON] Failed to process conversation {convo.conversation_id}: {e}"
                )

            await self.delete_exceeding_summaries(convo.conversation_id)

    async def delete_exceeding_summaries(self, convo_id):
        summaries = await self.summaries_db.get_many(
            conversation_id=convo_id, sort=[("timestamp", -1)]
        )
        if len(summaries) > 3:
            to_delete = summaries[3:]
            for summary in to_delete:
                try:
                    await self.summaries_db.delete(summary_id=summary.summary_id)
                except Exception as e:
                    print(f"[CRON] Failed to delete summary {summary.summary_id}: {e}")
