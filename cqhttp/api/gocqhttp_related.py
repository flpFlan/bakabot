from cqhttp.api.base import ApiAction, register_to_api


@register_to_api
class GetCookies(ApiAction):
    class Response(ApiAction.Response):
        class Data:
            cookies: str

        data: Data

    action = "get_cookies"

    def __init__(self, domain: str, *, echo: str = ""):
        self.domain = domain
        self.echo = echo


@register_to_api
class GetCsrfToken(ApiAction):
    class Response(ApiAction.Response):
        class Data:
            token: int

        data: Data

    action = "get_csrf_token"

    def __init__(self, *, echo: str = ""):
        self.echo = echo


@register_to_api
class GetCredentials(ApiAction):
    class Response(ApiAction.Response):
        class Data:
            cookies: str
            csrf_token: int

        data: Data

    action = "get_credentials"

    def __init__(self, domain: str, *, echo: str = ""):
        self.domain = domain
        self.echo = echo


@register_to_api
class GetVersionInfo(ApiAction):
    class Response(ApiAction.Response):
        class Data:
            app_name: str
            app_version: str
            app_full_name: str
            protocol_version: str
            coolq_edition: str
            coolq_directory: str
            go_cqhttp: bool = True  # 响应字段为go-cqhttp，但是规定值true
            plugin_version: str
            plugin_build_number: int
            plugin_build_configuration: str
            runtime_version: str
            runtime_os: str
            version: str
            protocol: str

        data: Data

    action = "get_version_info"

    def __init__(self, *, echo: str = ""):
        self.echo = echo


@register_to_api
class GetStatus(ApiAction):
    class Response(ApiAction.Response):
        class Data:
            class Statistics:
                PacketReceived: int
                PacketSent: int
                PacketLost: int
                MessageReceived: int
                MessageSent: int
                DisconnectTimes: int
                LostTimes: int
                LastMessageTime: int

            app_initialized: bool
            app_enabled: bool
            plugins_good: bool
            app_good: bool
            online: bool
            good: bool
            stat: Statistics

        data: Data

    action = "get_status"

    def __init__(self, *, echo: str = ""):
        self.echo = echo


@register_to_api
class SetRestart(ApiAction):
    action = "set_restart"

    def __init__(self, delay: int = 0, *, echo: str = ""):
        self.delay = delay
        self.echo = echo


@register_to_api
class CleanCache(ApiAction):
    action = "clean_cache"

    def __init__(self, *, echo: str = ""):
        self.echo = echo


@register_to_api
class ReloadEventFilter(ApiAction):
    action = "reload_event_filter"

    def __init__(self, file: str, *, echo: str = ""):
        self.file = file
        self.echo = echo


@register_to_api
class DownloadFile(ApiAction):
    class Response(ApiAction.Response):
        class Data:
            file: str

        data: Data

    action = "download_file"

    def __init__(
        self, url: str, thread_count: int, headers: str | list, *, echo: str = ""
    ):
        self.url = url
        self.thread_count = thread_count
        self.headers = headers
        self.echo = echo


@register_to_api
class CheckUrlSafely(ApiAction):
    class Response(ApiAction.Response):
        class Data:
            level: int

        data: Data

    action = "check_url_safely"

    def __init__(self, url: str, *, echo: str = ""):
        self.url = url
        self.echo = echo


@register_to_api
class GetWordSlices(ApiAction):
    class Response(ApiAction.Response):
        class Data:
            slices: list[str]

        data: Data

    action = ".get_word_slices"

    def __init__(self, content: str, *, echo: str = ""):
        self.content = content
        self.echo = echo


@register_to_api
class HandleQuickOperation(ApiAction):
    action = ".handle_quick_operation"

    def __init__(self, context: object, operation: object, *, echo: str = ""):
        self.context = context
        self.operation = operation
        self.echo = echo
