core_services = []


def core_service(cls):
    core_services.append(cls)
    return cls
