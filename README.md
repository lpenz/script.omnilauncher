[![Build Status](https://travis-ci.com/lpenz/script.omnilauncher.svg?branch=master)](https://travis-ci.com/lpenz/script.omnilauncher)
[![Coverage Status](https://coveralls.io/repos/lpenz/script.omnilauncher/badge.svg)](https://coveralls.io/r/lpenz/script.omnilauncher)


# script.omnilauncher

Omnilauncher is an addon for kodi that interprets XML files in a
directory and builds a menu tree that can also launch programs.

This addon doesn't do any scrapping, it just uses what is in the XML
files. It should be used as a glue between a third-party program that
actually does the scrapping and creates the XML and kodi.


## Examples

The only configuration in this addon is the root directory, where all XML
files will be read, and a menu item is created for each one of them.

One could have, for instance, the following file in the root directory:
```
<?xml version='1.0' encoding='UTF-8'?>
<omnilauncher>
  <title>Google chrome</title>
  <info>
      <plot>Web browser developed by Google</plot>
  </info>
  <art>
      <thumb>thumb.png</thumb>
      <fanart>fanart.jpg</fanart>
  </art>
  <target type="shell">google-chrome</target>
</omnilauncher>
```

Another entry could point to a *Games* directory:
```
<?xml version='1.0' encoding='UTF-8'?>
<omnilauncher>
  <title>Games</title>
  <art>
      <thumb>thumb.png</thumb>
      <fanart>fanart.jpg</fanart>
  </art>
  <target type="directory">games</target>
</omnilauncher>
```

Selecting this entry would make omnilauncher parse all XML files in
the `Games` directory and build another menu tree.
