# Changelog [forever_proc]



## [Version 1.0.0 ~stable] - 02.05.2020

This is the **first** stable release of the *forever_proc* script!



### Added

- "*about*" section in the **settings.json** file
- function "*startJob*"; it tries to spin up a new **forever** instance
- many **Job** <class> parameters



### Changed

- "*log*" is now "*log_path*" in **settings.json**
- "*start*" workflow and behaviour; outsourced most of it's functionallity
- "*jobControl*" workflow 



### Removed

- "*err_log*", "*out_log*" got removed from **settings.json**