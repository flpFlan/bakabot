from typing import ClassVar, Type


class Event:
    classes:ClassVar[set[Type["Event"]]]=set() # events that can be actually instantiated

    @classmethod
    def get_real_types(cls)->list[Type["Event"]]:
        """get sub_events that can be actually delivered by go-cqhttp"""
        return [c for c in Event.classes if issubclass(c,cls) or c is cls]
