import json
import logging
import os
import kopf
from kubernetes.client import V1Namespace
from kubernetes import config, client

TASK = "task"


@kopf.on.startup()
async def startup_func(logger, **kwargs):
    if os.getenv("KUBERNETES_SERVICE_HOST"):
        config.load_incluster_config()
    else:
        # assume running outside cluster AND kubeconfig is available
        config.load_kube_config()


@kopf.on.create(TASK)
def task_on_create(spec: kopf.Spec, name, namespace, logger: logging.Logger, **kwargs):
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
    resp = v1.create_namespaced_pod(namespace="default", body=body, dry_run="All")
    logger.info(f"resp: {resp}")
