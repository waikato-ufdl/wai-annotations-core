from typing import Iterator

from wai.common.adams.imaging.locateobjects import LocatedObjects, LocatedObject

from ....core.domain import Annotation


class DetectedObjects(LocatedObjects, Annotation):

    # PyCharm doesn't seem to be able to work out the typing for this
    def __iter__(self) -> Iterator[LocatedObject]:
        return super().__iter__()
