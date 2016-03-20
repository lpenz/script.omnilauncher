[![Build Status](https://travis-ci.org/lpenz/script.omnilauncher.svg?branch=master)](https://travis-ci.org/lpenz/script.omnilauncher)
[![Coverage Status](https://coveralls.io/repos/lpenz/script.omnilauncher/badge.svg)](https://coveralls.io/r/lpenz/script.omnilauncher)


# script.omnilauncher

Omni launcher add-on for kodi

This is a program addon that interprets *nfo* XML files with the usual
information and artwork file reference, and builds a menu tree in kodi, where
the leafs are allowed to run arbitrary commands. The example below clarifies
how it works.

I've been using this addon since Advanced Laucher went belly up.


## Examples

An example menu file, placed in `c:\Program Files` could be the following:
```
<?xml version='1.0' encoding='UTF-8'?>
<omniitem>
  <title>Programs</title>
  <info>
      <plot>Generic programs</plot>
  </info>
  <art>
      <thumb>thumb.png</thumb>
      <fanart>fanart.jpg</fanart>
  </art>
  <target type="glob">*/omniitem.nfo</target>
</omniitem>
```

You could then have a `c:\Program Files\Internet Explorer\omniitem.nfo` file
with the following contents:
```
<?xml version='1.0' encoding='UTF-8'?>
<omniitem>
  <title>Internet Explorer</title>
  <info>
      <plot>An obsolete browser that is not good at all</plot>
  </info>
  <art>
      <thumb>thumb.png</thumb>
      <fanart>fanart.jpg</fanart>
  </art>
  <target type="command">iexplore.exe</target>
</omniitem>
```

