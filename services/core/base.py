from services.base import Service

class CoreService(Service):
    classes=set()
    priority=Service.Priority.Highest

def core_service(cls):
    CoreService.classes.add(cls)
    return cls
