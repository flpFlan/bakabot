# -- stdlib --

# -- third party --

# -- own --

# -- code --


class revProcessor:
    def __init__(self, bot):
        self.bot = bot

    def process_by_type(self, post_type, rev):
        if post_type == "message":
            return self.process_message(rev)
        if post_type == "notice":
            return self.process_notice(rev)
        if post_type == "request":
            return self.process_request(rev)
        if post_type == "redbag":
            return self.process_redbag(rev)

    def process_message(self, rev):
        self.bot._["qq"] = rev["user_id"]
        is_group = rev["message_type"] == "group"

        if is_group:
            self.bot._["group_id"] = rev["group_id"]

        return process_raw_message(rev)

    def process_notice(self, rev):
        return None

    def process_request(self, rev):
        return None

    def process_redbag(self, rev):
        return None


def process_raw_message(rev):
    message = rev["raw_message"]
    message = message.replace("&amp;", "&")
    message = message.replace("&#91;", "[")
    message = message.replace("&#93;", "]")
    message = message.replace("&#44;", ",")
    return message
