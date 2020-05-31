import os
import json
from typing import Dict, Any, List
from dataclasses import dataclass
from copy import deepcopy

from botbuilder.schema import Activity, Attachment

from fluxcd_teams_bot import settings


class Card(object):
    CARD_FILE = ''
    CARD_DATA: dict = None

    def __init__(self) -> None:
        self.load_content()

    def load_content(self) -> None:
        if self.CARD_FILE and not self.CARD_DATA:
            path = os.path.join(settings.CARD_TEMPLATE_DIR, self.CARD_FILE)
            with open(path, 'r') as fp:
                self.CARD_DATA = json.load(fp)

    def render(self) -> Dict[str, Any]:
        raise NotImplementedError()

    def activity(self) -> Activity:
        attachment = Attachment(
            content_type='application/vnd.microsoft.card.adaptive',
            content=self.render()
        )
        return Activity(type='message', attachments=[attachment])


@dataclass
class ErrorItem:
    namespace: str
    resource: str
    file: str
    error: str


class ErrorCard(Card):
    CARD_FILE = 'sync_error.json'

    def __init__(self) -> None:
        super(ErrorCard, self).__init__()

        self.errors: List[ErrorItem] = []
        self.container = deepcopy(self.CARD_DATA['sections'])
        self.CARD_DATA['sections'].clear()

    def add_error(self, namespace: str, resource: str, file: str, error: str) -> None:
        self.errors.append(ErrorItem(namespace, resource, file, error))

    def render(self) -> Dict[str, Any]:
        result = deepcopy(self.CARD_DATA)

        for index, item in enumerate(self.errors):
            container = deepcopy(self.container)
            container[0]['facts'][0]['value'] = item.namespace
            container[0]['facts'][1]['value'] = item.resource
            container[0]['facts'][2]['value'] = item.file

            url = settings.GIT_REPO_URL_PREFIX + item.file
            container[1]['text'] = f'Error:<br>```{item.error}```<br>[File]({url})'
            result['sections'].extend(container)

        return result


@dataclass
class AutoreleaseItem:
    namespace: str
    resource: str
    src_image: str
    dst_image: str


class AutoreleaseCard(Card):
    CARD_FILE = 'autorelease.json'

    def __init__(self) -> None:
        super(AutoreleaseCard, self).__init__()

        self.releases: List[AutoreleaseItem] = []
        self.container = self.CARD_DATA['sections'].pop()

    def add_autorelease(self, namespace: str, resource: str, src_image: str, dst_image: str) -> None:
        self.releases.append(AutoreleaseItem(namespace, resource, src_image, dst_image))

    def render(self) -> Dict[str, Any]:
        result = deepcopy(self.CARD_DATA)

        for index, item in enumerate(self.releases):
            container = deepcopy(self.container)
            container['facts'][0]['value'] = item.namespace
            container['facts'][1]['value'] = item.resource
            container['facts'][2]['value'] = item.src_image
            container['facts'][3]['value'] = item.dst_image

            container['separator'] = index != 0  # Only use separators after first item

            result['sections'].append(container)

        return result
