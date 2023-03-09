import itertools
from typing import Callable

from ..._AbstractConversionTest import AbstractConversionTest
from wai.annotations.core.store import DictStore
from wai.annotations.core.stream import Pipeline
from wai.annotations.core.util.path import PathKey
from wai.annotations.domain.image.classification import ImageClassificationInstance

from wai.test.decorators import Test

class ToData(AbstractConversionTest):
    @Test
    @AbstractConversionTest.SubjectArgs(
        ["to-data-ic", "-s", "dict-store", "-o", "results", "--split-names", "A", "B", "C", "--split-ratios", "1", "1", "1"],
        source=itertools.repeat(ImageClassificationInstance(PathKey("test"), AbstractConversionTest.get_test_image(), None), 100)
    )
    def test_to_data(self, subject: Callable[[], Pipeline]):
        pipeline = subject()
        store = pipeline.sink.store
        self.assertIsInstance(store, DictStore)
        self.assertIn(store.ensure_key(PathKey("results/A/test")), store)
        self.assertIn(store.ensure_key(PathKey("results/B/test")), store)
        self.assertIn(store.ensure_key(PathKey("results/C/test")), store)
