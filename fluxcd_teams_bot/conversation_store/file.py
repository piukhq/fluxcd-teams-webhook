from typing import AsyncIterator
import shelve
from fluxcd_teams_bot.conversation_store.base import BaseStore

from botbuilder.schema import ConversationReference


class FileStore(BaseStore):
    def __init__(self, filepath: str):
        self._path = filepath

        super(FileStore, self).__init__()

        self._store = shelve.open(self._path)

    async def add_conversation_ref(self, ref: ConversationReference) -> None:
        self._store[ref.user.id] = ref
        self._store.sync()

    async def get_conversations(self) -> AsyncIterator[ConversationReference]:
        result = list(self._store.values())
        for val in result:
            yield val
