import io
from typing import Optional, Tuple

from PIL import Image as PILImage

from ...core.domain import Data
from ...core.util import InstanceState
from .util import convert_image_format
from ._ImageFormat import ImageFormat


class Image(Data):
    """
    Contains the information about an image in a data-set.
    """
    def __init__(
            self,
            filename: str,
            data: Optional[bytes] = None,
            format: Optional[ImageFormat] = None,
            size: Optional[Tuple[int, int]] = None
    ):
        super().__init__(filename, data)

        self._format: ImageFormat = (
            format if format is not None
            else ImageFormat.for_filename(filename)
        )

        self._size: Optional[Tuple[int, int]] = (
            size if size is not None
            else (self.pil_image.width, self.pil_image.height) if self.pil_image is not None
            else None
        )

    # The PIL image representation of this image data
    pil_image: Optional[PILImage.Image] = InstanceState(
        lambda self: (
            PILImage.open(io.BytesIO(self.data)) if self.data is not None
            else None
        )
    )

    @classmethod
    def from_file_data(cls, file_name: str, file_data: bytes) -> 'Image':
        return cls(file_name, file_data)

    def convert(self, to_format: ImageFormat) -> 'Image':
        """
        Converts this image into another format.

        :param to_format:   The image format to convert to.
        :return:            The converted image-info object.
        """
        # If it's the same format, just make a copy
        if to_format is self._format:
            return Image(
                self.filename,
                self.data,
                self.format,
                self.size
            )

        return Image(
            to_format.replace_extension(self.filename),
            convert_image_format(self.data, to_format.pil_format_string) if self.data is not None else None,
            to_format,
            self.size
        )

    @property
    def format(self) -> ImageFormat:
        """
        Gets the format of this image.
        """
        return self._format

    @property
    def size(self) -> Tuple[int, int]:
        """
        Gets the (width, height) dimensions of the image.
        """
        return self._size if self._size is not None else (-1, -1)

    @property
    def width(self) -> int:
        """
        Gets the width of the image.

        :return:    The image width.
        """
        return self.size[0]

    @property
    def height(self) -> int:
        """
        Gets the height of the image.

        :return:    The image height.
        """
        return self.size[1]

    def __getattribute__(self, item):
        # Dynamically defines '_repr_png_' or '_repr_jpeg_'
        # based on image data availability
        if (
                item == '_repr_png_'
                and self.data is not None
                and self.format is ImageFormat.PNG
        ):
            return lambda: self.data

        elif (
                item == '_repr_jpeg_'
                and self.data is not None
                and self.format is ImageFormat.JPG
        ):
            return lambda: self.data

        return super().__getattribute__(item)
