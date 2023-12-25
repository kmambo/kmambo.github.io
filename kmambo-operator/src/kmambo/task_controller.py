import logging
import kopf

TASK = "task"


@kopf.on.create(TASK)
def task_on_create(spec, name, namespace, logger: logging.Logger, body, **kwargs):
    logger.info(f"name: {name}, namespace: {namespace}, spec:{spec}")
