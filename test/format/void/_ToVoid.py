import itertools

from ..._AbstractConversionTest import AbstractConversionTest
from wai.annotations.core.util.path import PathKey
from wai.annotations.domain.image.classification import ImageClassificationInstance

from wai.test.decorators import Test

class ToVoid(AbstractConversionTest):
    @Test
    @AbstractConversionTest.SubjectArgs(
        ["to-void-ic"],
        source=itertools.repeat(ImageClassificationInstance(PathKey("test"), None, None), 100)
    )
    def test_to_void(self, subject):
        subject()
