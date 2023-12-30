import json
import logging
import os
import kopf
from kubernetes import config, client

TASK = "task"


@kopf.on.startup()
async def startup_func(settings, **_):
    if os.getenv("KUBERNETES_SERVICE_HOST"):
        settings.admission.server = kopf.WebhookServer(addr='0.0.0.0', port=8080)
        config.load_incluster_config()
    else:
        # assume running outside cluster AND kubeconfig is available
        settings.admission.server = kopf.WebhookAutoServer(port=8080)
        settings.admission.managed = 'auto.kopf.dev'
        config.load_kube_config()


@kopf.on.validate(TASK)
async def task_on_create(spec: kopf.Spec, name, namespace, logger: logging.Logger, **kwargs):
    logger.info(f"name: {name}, namespace: {namespace}, spec:{spec}")
    logger.info(f"type(spec): {type(spec)}")
    # logger.info(f"kwargs:{kwargs}")
    v1 = client.CoreV1Api()
    body = {
        'apiVersion': 'v1',
        'kind': 'Pod',
        'metadata': {
            'name': name
        },
        'spec': eval(f"{spec['template']}")
    }
    try:
        resp = v1.create_namespaced_pod(namespace="default", body=body, dry_run="All")
    except Exception as e:
        raise kopf.AdmissionError(f"Unable to create Task {e}")
    logger.info(f"resp: {resp}")
