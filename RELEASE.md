Pypi
====


Preparation:
* new domain added?

  * add `to-void-DOMAIN` dummy writer
  * add simple reader/writer `from-FILE-DOMAIN`/`to-FILE-DOMAIN` (like `from-images-ic`/`to-images-ic`)
  * add source/isp/sink (and simple test classes) to `wai.annotations.generic` to provide support for new domain  
    
* increment version in `setup.py`
* add new changelog section in `CHANGES.rst`
* update plugin section in `README.md`
* commit/push all changes

Commands for releasing on pypi (requires twine >= 1.8.0):

```
  rm -r dist src/wai.annotations.core.egg-info
  python setup.py clean sdist
  twine upload dist/*
```


Github
======

Steps:
* start new release (version: `vX.Y.Z`)
* enter release notes, i.e., significant changes since last release
* upload `wai.annotations.core-X.Y.Z.tar.gz` previously generated with `setup.py`
* publish
