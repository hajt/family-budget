from rest_framework.exceptions import NotAcceptable


class NotOwnerError(NotAcceptable):
    DETAIL = "You are not owner of this wallet."

    def __init__(self, detail=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.detail = detail if detail else self.DETAIL
