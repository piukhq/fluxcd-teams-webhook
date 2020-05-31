from typing import Tuple, Dict, Any, Union, cast

from fluxcd_teams_bot.cards import ErrorCard, Card, AutoreleaseCard


def split_workload_id(workload_id: str) -> Tuple[str, str]:
    return cast(Tuple[str, str], workload_id.split(':', 1))


def parse(data: Dict[str, Any]) -> Union[Card, None]:
    card = None

    type_ = data.get('type')
    if type_ == 'sync':
        if 'errors' in data['metadata']:
            # Sync Error Card
            card = ErrorCard()

            for error in data['metadata']['errors']:
                namespace, resource = split_workload_id(error['ID'])
                card.add_error(namespace, resource, error['Path'], error['Error'])

    elif type_ == 'autorelease':
        card = AutoreleaseCard()

        for change in data['metadata']['spec']['Changes']:
            namespace, resource = split_workload_id(change['WorkloadID'])
            card.add_autorelease(
                namespace,
                resource,
                change['Container']['Image'],
                change['ImageID']
            )

    return card
