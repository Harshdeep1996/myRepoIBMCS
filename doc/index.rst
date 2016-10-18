Welcome to cloudant-compliance-checks's documentation!
======================================================

`Check status`_

Tests to run against Cloudant as part of verifying compliance standing

Tests run in the Whitewater `Travis CI system`_ using `nose`_. Each check, including checks that require manual interventions, should be written as a nose test.

Running locally
---------------

For running it on your machine::

  $ virtualenv --no-site-packages venv
  $ source venv/bin/activate
  $ pip install -r requirements.txt
  $ pip install -r local_requirements.txt
  $ python compliance --with-ControlValidation

Manual check
------------

There are some checks that require human intervention (either because the check is not automated yet or cannot be automated). These checks must still be validated here.

Manual checks should have the following workflow:

* Person collects evidence for the check, and writes it into controlled location

    * Second person may validate that data, writing their validation into the same location. This would be verified in a separate check.
* Compliance test pulls in the manually created file from the controlled location and verifies last update time and who last edited the file

Manual checks should inherit from ``compliance.checks.ManualCheck``. For a simple check it pulls in a url or git repo and records the last update for the file and by whom.


.. _Check Status: https://travis.innovate.ibm.com/CloudDataServices/cloudant-compliance-checks.svg?token=t57QjqTUQ8rv6Xvy4sDm
.. _Travis CI system: https://travis.innovate.ibm.com/CloudDataServices/cloudant-compliance-checks
.. _nose: http://nose.readthedocs.io/en/latest/


Source code
-----------

.. toctree::
   :maxdepth: 2

   modules


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
