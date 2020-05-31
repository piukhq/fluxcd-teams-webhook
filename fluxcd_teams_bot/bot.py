from botbuilder.core import ActivityHandler, TurnContext
from fluxcd_teams_bot.bot_adapter import BOT_ADAPTER
from botbuilder.schema import ChannelAccount, Activity, Attachment
from fluxcd_teams_bot.cards import Card
import traceback

from fluxcd_teams_bot import settings
from fluxcd_teams_bot.conversation_store.base import BaseStore
# TODO make configurable
from fluxcd_teams_bot.conversation_store.file import FileStore


class Bot(ActivityHandler):
    def __init__(self, *args, **kwargs) -> None:
        self._conversation_references = {}

        self._store: BaseStore = FileStore(settings.FILE_STORAGE)

        super(Bot, self).__init__(*args, **kwargs)

    async def on_conversation_update_activity(self, turn_context: TurnContext):
        conversation_reference = TurnContext.get_conversation_reference(turn_context.activity)
        await self._store.add_conversation_ref(conversation_reference)

        return await super().on_conversation_update_activity(turn_context)

    # TODO shouldn't need this
    async def on_message_activity(self, turn_context: TurnContext) -> None:
        conversation_reference = TurnContext.get_conversation_reference(turn_context.activity)
        await self._store.add_conversation_ref(conversation_reference)

    async def send_activity(self, card: Card) -> None:
        async for conversation_reference in self._store.get_conversations():
            try:
                await BOT_ADAPTER.continue_conversation(
                    conversation_reference,
                    lambda turn_context: turn_context.send_activity(card.activity()),
                    settings.APP_ID)
            except Exception as err:
                traceback.print_exc()
                traceback.print_tb(err)
