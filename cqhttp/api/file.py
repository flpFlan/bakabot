from cqhttp.api.base import ApiAction, register_to_api


@register_to_api
class UploadGroupFile(ApiAction):
    action = "upload_group_file"

    def __init__(
        self, group_id: int, file: str, name: str, folder: str = "", *, echo: str = ""
    ):
        self.group_id = group_id
        self.file = file
        self.name = name
        if folder:
            self.folder = folder
        self.echo = echo


@register_to_api
class DeleteGroupFile(ApiAction):
    action = "delete_group_file"

    def __init__(self, group_id: int, file_id: str, busid: int, *, echo: str = ""):
        self.group_id = group_id
        self.file_id = file_id
        self.busid = busid
        self.echo = echo


@register_to_api
class CreateGroupFileFolder(ApiAction):
    action = "create_group_file_folder"

    def __init__(
        self, group_id: int, name: str, parent_id: str = "/", *, echo: str = ""
    ):
        self.group_id = group_id
        self.name = name
        self.parent_id = parent_id
        self.echo = echo


@register_to_api
class DeleteGroupFolder(ApiAction):
    action = "delete_group_folder"

    def __init__(self, group_id: int, folder_id: str, *, echo: str = ""):
        self.group_id = group_id
        self.folder_id = folder_id
        self.echo = echo


@register_to_api
class GetGroupFileSystemInfo(ApiAction):
    class Response(ApiAction.Response):
        class Data:
            file_count: int
            limit_count: int
            used_space: int
            total_space: int

        data: Data

    action = "get_group_file_system_info"

    def __init__(self, group_id: int, *, echo: str = ""):
        self.group_id = group_id
        self.echo = echo


@register_to_api
class GetGroupRootFiles(ApiAction):
    class Response(ApiAction.Response):
        class Data:
            files: list
            folders: list

        data: Data

    action = "get_group_root_files"

    def __init__(self, group_id: int, echo: str = ""):
        self.group_id = group_id
        self.echo = echo


@register_to_api
class GetGroupFilesByFolder(ApiAction):
    class Response(ApiAction.Response):
        class Data:
            files: list
            folders: list

        data: Data

    action = "get_group_files_by_folder"

    def __init__(self, group_id: int, folder_id: str, echo: str = ""):
        self.group_id = group_id
        self.folder_id = folder_id
        self.echo = echo


@register_to_api
class GetGroupFileUrl(ApiAction):
    class Response(ApiAction.Response):
        class Data:
            url: str

        data: Data

    action = "get_group_file_url"

    def __init__(self, group_id: int, file_id: str, busid: int, *, echo: str = ""):
        self.group_id = group_id
        self.file_id = file_id
        self.busid = busid
        self.echo = echo


@register_to_api
class UploadPrivateFile(ApiAction):
    action = "upload_private_file"

    def __init__(self, user_id: int, file: str, name: str, *, echo: str = ""):
        self.user_id = user_id
        self.file = file
        self.name = name
        self.echo = echo
