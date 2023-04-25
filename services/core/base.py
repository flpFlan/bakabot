core_services = []


def core_service(cls):
    core_services.append(cls)
    if not cls.__dict__.get("priority", None):
        cls.priority = 0
    return cls
