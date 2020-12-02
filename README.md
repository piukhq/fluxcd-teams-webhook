# FluxCD Teams Webhook

TODO badges

Simple Python web server which Flux v1 can send events to. Will send updates to an MS Teams webhook URL for any errors when applying GitOps manifests and when deployments are updated when new images are found.

```
docker pull ghcr.io/binkhq/fluxcd-teams-webhook:latest
```

## Setup

Run the Flux Teams webhook container somewhere Flux can call, in theory you could have flux deploy the webhook container via GitOps.

The container has the following environment variables

| Name                | Description                                                                            | Default                                                   |
|---------------------|----------------------------------------------------------------------------------------|-----------------------------------------------------------|
| `LOG_LEVEL`         | Python logging level, can be one of `DEBUG`, `INFO`, `WARNING`, `ERROR` and `CRITICAL` | `INFO`                                                    |
| `LISTEN_ADDR`       | Web server listening address                                                           | `0.0.0.0`                                                 |
| `LISTEN_PORT`       | Web server listening port                                                              | `8080`                                                    |
| `GIT_REPO_PREFIX`   | URL prefix used to generate links to the Git repo in Teams messages                    | `https://github.com/fluxcd/flux-get-started/blob/master/` |
| `TEAMS_WEBHOOK_URL` | MS Teams webhook URL                                                                   |                                                           |

Update the Flux container manifest to add the following args:

```
- --connect=ws://flux-teams-webhook-url
- --token=abc123abc123abc123abc123
```

TODO token currently not checked

The webhook url scheme should be `ws` if running the flux teams bot normally or `wss` if being fronted by SSL.
