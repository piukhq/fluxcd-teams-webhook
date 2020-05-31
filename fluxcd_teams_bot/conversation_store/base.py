from typing import AsyncIterator

from botbuilder.schema import ConversationReference


class BaseStore(object):
    def __init__(self):
        pass

    async def add_conversation_ref(self, ref: ConversationReference) -> None:
        raise NotImplementedError()

    async def get_conversations(self) -> AsyncIterator[ConversationReference]:
        raise NotImplementedError()
