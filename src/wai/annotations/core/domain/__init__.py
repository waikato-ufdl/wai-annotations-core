"""
A domain is an area of machine learning where datasets consist of data
of some form annotated in some way. An example of this is image classification,
where the data is images and the annotations are classification labels. Sub-classes
of the Data and Annotation base-classes specify the properties of data/annotations
in any domain that uses them, and specific domains are specified by sub-classing
the Instance class. The Instance class specifies which type of Data and Annotation
the domain works in, but also the invariants of the domain.

E.g. The image-segmentation domain uses images as its data-type, and an array of
labels for each pixel as its annotation-type. The instance-type for this domain
ensures that the size of the annotation arrays is equal to the dimensions of the
image data i.e. there is a label for each pixel in the image.
"""
from ._Annotation import Annotation
from ._Data import Data
from ._Instance import Instance
