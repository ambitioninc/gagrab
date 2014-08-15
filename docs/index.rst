gagrab Documentation
=============================

The official Google Analytics API is very powerfull and
extensive. Sometimes, though, you just want to grab some data and have
it returned in a clean format.

Using ``gagrab`` is as simple as

.. code-block:: python

    from service_account_auth import AuthorizedService
    from gagrab import Grabber

    my_ga_service = AuthorizedService('my-project-555', 'analytics', 'v3')
    grabber = Grabber(my_ga_service)

    data = grabber.query(
        view='UA-000000-1',
        metrics=['sessions', 'pageviews'],
        dimensions=['browser', 'userAgeBracket']
        start_date='2014-07-01',
        end_date='2014-08-15',
    )


.. toctree::
   :maxdepth: 2

   installation
   ref/gagrab
   contributing
   release_notes
