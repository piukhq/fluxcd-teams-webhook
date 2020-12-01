from typing import Any, Dict, Tuple, Union, cast

from fluxcd_teams_bot.cards import AutoreleaseCard, Card, ErrorCard


def split_workload_id(workload_id: str) -> Tuple[str, str]:
    return cast(Tuple[str, str], workload_id.split(":", 1))


def parse(data: Dict[str, Any]) -> Union[Card, None]:
    type_ = data.get("type")
    if type_ == "sync":
        if "errors" in data["metadata"]:
            # Sync Error Card
            e_card = ErrorCard()

            for error in data["metadata"]["errors"]:
                namespace, resource = split_workload_id(error["ID"])
                e_card.add_error(namespace, resource, error["Path"], error["Error"])
            return e_card

    elif type_ == "autorelease":
        a_card = AutoreleaseCard()

        for change in data["metadata"]["spec"]["Changes"]:
            namespace, resource = split_workload_id(change["WorkloadID"])
            a_card.add_autorelease(namespace, resource, change["Container"]["Image"], change["ImageID"])

        return a_card

    return None
