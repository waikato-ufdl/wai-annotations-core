# Plugins
## Processor stage
### CHECK-DUPLICATE-FILENAMES
Causes the conversion stream to halt when multiple dataset items have the same filename

#### Domain(s):


#### Options:
```
usage: check-duplicate-filenames
```

### COERCE-BOX
Converts all annotation bounds into box regions

#### Domain(s):


#### Options:
```
usage: coerce-box
```

### COERCE-MASK
Converts all annotation bounds into polygon regions

#### Domain(s):


#### Options:
```
usage: coerce-mask
```

### CONVERT-IMAGE-FORMAT
Converts images from one format to another

#### Domain(s):


#### Options:
```
usage: convert-image-format -f FORMAT

optional arguments:
  -f FORMAT, --format FORMAT
                        format to convert images to
```

### DIMENSION-DISCARDER
Removes annotations which fall outside certain size constraints

#### Domain(s):


#### Options:
```
usage: dimension-discarder [--max-area MAX_AREA] [--max-height MAX_HEIGHT] [--max-width MAX_WIDTH] [--min-area MIN_AREA] [--min-height MIN_HEIGHT] [--min-width MIN_WIDTH]

optional arguments:
  --max-area MAX_AREA   the maximum area of annotations to convert
  --max-height MAX_HEIGHT
                        the maximum height of annotations to convert
  --max-width MAX_WIDTH
                        the maximum width of annotations to convert
  --min-area MIN_AREA   the minimum area of annotations to convert
  --min-height MIN_HEIGHT
                        the minimum height of annotations to convert
  --min-width MIN_WIDTH
                        the minimum width of annotations to convert
```

### DISCARD-NEGATIVES
Discards negative examples (those without annotations) from the stream

#### Domain(s):


#### Options:
```
usage: discard-negatives
```

### FILTER-LABELS
Filters detected objects down to those with specified labels.

#### Domain(s):


#### Options:
```
usage: filter-labels [-l LABELS [LABELS ...]] [-r regexp]

optional arguments:
  -l LABELS [LABELS ...], --labels LABELS [LABELS ...]
                        labels to use
  -r regexp, --regexp regexp
                        regular expression for using only a subset of labels
```

### MAP-LABELS
Maps object-detection labels from one set to another

#### Domain(s):


#### Options:
```
usage: map-labels [-m old=new]

optional arguments:
  -m old=new, --mapping old=new
                        mapping for labels, for replacing one label string with another (eg when fixing/collapsing labels)
```

### OD-TO-IS
Converts image object-detection instances into image segmentation instances

#### Domain(s):


#### Options:
```
usage: od-to-is [--label-error] --labels LABEL [LABEL ...]

optional arguments:
  --label-error         whether to raise errors when an unspecified label is encountered (default is to ignore)
  --labels LABEL [LABEL ...]
                        specifies the labels for each index
```

### PASSTHROUGH
Dummy ISP which has no effect on the conversion stream

#### Domain(s):


#### Options:
```
usage: passthrough
```

### REMOVE-CLASSES
Removes classes from classification/image-segmentation instances

#### Domain(s):


#### Options:
```
usage: remove-classes -c CLASS [CLASS ...]

optional arguments:
  -c CLASS [CLASS ...], --classes CLASS [CLASS ...]
                        the classes to remove
```

### STRIP-ANNOTATIONS
ISP which removes annotations from instances

#### Domain(s):


#### Options:
```
usage: strip-annotations
```


