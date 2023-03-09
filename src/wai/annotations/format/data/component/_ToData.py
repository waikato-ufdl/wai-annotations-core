import os.path

from ....core.component.util.output import WritableStoreSink, ExpectsDirectory
from ....core.component.util.output.splitting import SplitSink, RequiresNoSplitFinalisation
from ....core.domain import Annotation, Data, Instance


class ToData(
    RequiresNoSplitFinalisation,
    SplitSink[Instance[Data, Annotation]],
    ExpectsDirectory,
    WritableStoreSink[Instance[Data, Annotation]]
):
    """
    Writes data-files to the specified output directory.
    """
    def consume_element_for_split(self, element: Instance[Data, Annotation]):
        data = element.data
        if data is not None:
            path = element.key
            if self.is_splitting:
                path = os.path.join(self.split_label, path)
            self.write(data.data, path)
