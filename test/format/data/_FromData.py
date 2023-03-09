from typing import Callable

from ..._AbstractConversionTest import AbstractConversionTest
from wai.annotations.core.store import DictStore
from wai.annotations.core.stream import Pipeline

from wai.test.decorators import Test

class FromData(AbstractConversionTest):
    @Test
    @AbstractConversionTest.SubjectArgs(
        ["from-data-ac", "-i", "test", "-s", "dict-store", "-S=-m", f"-S=test>{AbstractConversionTest.TEST_DICT_STORE_AUDIO}", "to-void"]
    )
    def test_to_data(self, subject: Callable[[], Pipeline]):
        pipeline = subject()
        store = pipeline.source.store
        self.assertIsInstance(store, DictStore)
        self.assertIn(
            store.ensure_key("test"),
            store
        )
