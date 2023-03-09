from setuptools import setup, find_namespace_packages


def _read(filename: str) -> str:
    """
    Reads in the content of the file.

    :param filename:    The file to read.
    :return:            The file content.
    """
    with open(filename, "r") as file:
        return file.read()


setup(
    name="wai.annotations.core",
    description="Python library for converting between deep-learning annotation formats.",
    long_description=f"{_read('DESCRIPTION.rst')}\n"
                     f"{_read('CHANGES.rst')}",
    url="https://github.com/waikato-datamining/wai-annotations-core",
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Programming Language :: Python :: 3',
    ],
    license='Apache License Version 2.0',
    package_dir={
        '': 'src'
    },
    packages=find_namespace_packages(where='src'),
    namespace_packages=[
        "wai",
        "wai.annotations"
    ],
    version="0.3.0",
    author='Corey Sterling',
    author_email='coreytsterling@gmail.com',
    install_requires=[
        "wai.common>=0.0.41",
        "wai.json>=0.0.4,<0.1",
        "wai.bynning>=0.0.2,<0.1",
        "Pillow",
        "contextlib2",
        "numpy>=1.16",
        "planar",
        "scikit-image",
        "wai.pycocotools",
        "opencv-python",
        "librosa",
        "Shapely",
        "soundfile",
    ],
    tests_require=[
        "wai.test"
    ],
    entry_points={
        "console_scripts": ["wai-annotations=wai.annotations.main:sys_main"],
        "wai.annotations.plugins": [
            # Domains
            "ac=wai.annotations.domain.audio.classification:AudioClassificationDomainSpecifier",
            "sp=wai.annotations.domain.audio.speech:SpeechDomainSpecifier",
            "ic=wai.annotations.domain.image.classification:ImageClassificationDomainSpecifier",
            "od=wai.annotations.domain.image.object_detection:ImageObjectDetectionDomainSpecifier",
            "is=wai.annotations.domain.image.segmentation:ImageSegmentationDomainSpecifier",
            "sc=wai.annotations.domain.spectra.classification:SpectrumClassificationDomainSpecifier",

            # Stores
            "dict-store=wai.annotations.core.store.specifier.specifiers:DictStoreSpecifier",
            "local-file-store=wai.annotations.core.store.specifier.specifiers:LocalFileStoreSpecifier",

            # Formats
            "from-data=wai.annotations.format.data.specifier:FromDataSpecifier",
            "to-data=wai.annotations.format.data.specifier:ToDataSpecifier",
            "to-void=wai.annotations.format.void.specifier:ToVoidSpecifier",
            "from-audio-files-ac=wai.annotations.format.data.specifier:FromDataSpecifier",
            "from-audio-files-sp=wai.annotations.format.data.specifier:FromDataSpecifier",
            "from-images-ic=wai.annotations.format.data.specifier:FromDataSpecifier",
            "from-images-is=wai.annotations.format.data.specifier:FromDataSpecifier",
            "from-images-od=wai.annotations.format.data.specifier:FromDataSpecifier",
            "from-spectra-sc=wai.annotations.format.data.specifier:FromDataSpecifier",
            "to-audio-files-ac=wai.annotations.format.data.specifier:ToDataSpecifier",
            "to-audio-files-sp=wai.annotations.format.data.specifier:ToDataSpecifier",
            "to-images-ic=wai.annotations.format.data.specifier:ToDataSpecifier",
            "to-images-is=wai.annotations.format.data.specifier:ToDataSpecifier",
            "to-images-od=wai.annotations.format.data.specifier:ToDataSpecifier",
            "to-spectra-sc=wai.annotations.format.data.specifier:ToDataSpecifier",

            # ISPs
            "check-duplicate-filenames=wai.annotations.isp.check_duplicate_keys.specifier:CheckDuplicateKeysISPSpecifier",
            "check-duplicate-keys=wai.annotations.isp.check_duplicate_keys.specifier:CheckDuplicateKeysISPSpecifier",
            "clean-transcript=wai.annotations.isp.clean_transcript.specifier:CleanTranscriptISPSpecifier",
            "coerce-box=wai.annotations.isp.coercions.specifier:BoxBoundsCoercionISPSpecifier",
            "coerce-mask=wai.annotations.isp.coercions.specifier:MaskBoundsCoercionISPSpecifier",
            "convert-image-format=wai.annotations.isp.convert_image_format.specifier:ConvertImageFormatISPSpecifier",
            "dimension-discarder=wai.annotations.isp.dimension_discarder.specifier:DimensionDiscarderISPSpecifier",
            "discard-invalid-images=wai.annotations.isp.discard_invalid_images.specifier:DiscardInvalidImagesISPSpecifier",
            "discard-negatives=wai.annotations.isp.discard_negatives.specifier:DiscardNegativesISPSpecifier",
            "filter-labels=wai.annotations.isp.filter_labels.specifier:FilterLabelsISPSpecifier",
            "filter-metadata=wai.annotations.isp.filter_metadata.specifier:FilterMetadataISPSpecifier",
            "label-present=wai.annotations.isp.label_present.specifier:LabelPresentISPSpecifier",
            "map-labels=wai.annotations.isp.map_labels.specifier:MapLabelsISPSpecifier",
            "passthrough=wai.annotations.isp.passthrough.specifier:PassThroughISPSpecifier",
            "polygon-discarder=wai.annotations.isp.polygon_discarder.specifier:PolygonDiscarderISPSpecifier",
            "remove-classes=wai.annotations.isp.remove_classes.specifier:RemoveClassesISPSpecifier",
            "rename=wai.annotations.isp.rename.specifier:RenameISPSpecifier",
            "sample=wai.annotations.isp.sample.specifier:SampleISPSpecifier",
            "strip-annotations=wai.annotations.isp.strip_annotations.specifier:StripAnnotationsISPSpecifier",
            "write-labels=wai.annotations.isp.write_labels.specifier:WriteLabelsISPSpecifier",

            # XDCs
            "od-into-ic=wai.annotations.xdc.od_to_ic.specifier:OD2ICXDCSpecifier",
            "od-into-is=wai.annotations.xdc.od_to_is.specifier:OD2ISXDCSpecifier",
        ]
    }
)
