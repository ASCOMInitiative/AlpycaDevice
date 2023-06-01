Version 0.1.0 Experimental (2023-02-03)
=======================================

Getting ready for limited private test and evaluation. Logic is complete,
ConformU passes, docs are extensive, and there are templates for all
ASCOM device types. No end to documentation though ha ha.

Version 0.2.0 Experimental (2023-05-30)
=======================================
Incomplete release caused by premature merge of development branch with
master. Oops.

Version 0.3.0 Experimental (2023-06-01)
=======================================

* Refactoring for multi-device types, mainly movement of the common endpoints
  into the individual device modules, so they can be implemented separately
  for each device *types*. Same with metadata. This covers
  `GitHub Issue #1 <https://github.com/BobDenny/AlpycaDevice/issues/1>`_
  and
  `GitHub Issue #3 <https://github.com/BobDenny/AlpycaDevice/issues/3>`_.
* Enhancment of templates to add explicit names and procesing of PUT parameters
  and for proper exception reporting. This includes
  `GitHub Issue #2 <https://github.com/BobDenny/AlpycaDevice/issues/2>`_.
* Passes the new Alpaca Protocol checker (this required numerous changes!)
