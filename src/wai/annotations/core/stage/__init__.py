"""
A "stage" in wai.annotations is a set of components where the input and outputs
sides are each instances of some domain i.e. The components within a stage may
convert the instances to any other type, but the first component should expect
instances, and the last component produce instances (except for source/sink stages,
where the first/last component doesn't consume/produce anything).

The bounds package provides a mechanism for generically describing what domains
a stage can operate in. Source/sink stages provide an instance-type bound-union,
which is the union of all the instance-types the stage can produce/consume. Each
individual bound within the union can be either a specific instance-type for a
domain (e.g. an image-classification instance) or a pair of (data-type, annotation-type)
to indicate that any domain whose instances match that data/annotation-type can
be used. Processor stages instead provide an instance-type bound-relationship,
which indicates how the input and output domains must relate to one-another,
in addition to their bound-unions. The relationship can be set between the input
and output instance-types, or separately between the input/output data- and
annotation-types. The relationship can be set such that:
 - there is no enforced relationship between the input and output types, or,
 - the input and output types must be the same, or,
 - the input type must be a sub-type of the output type, or,
 - the output type must be a sub-type of the input type.

New stages are added to wai.annotations via the plugin system.
"""
