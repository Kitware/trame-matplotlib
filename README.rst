.. |pypi_download| image:: https://img.shields.io/pypi/dm/trame-matplotlib

Matplotlib widget for trame |pypi_download|
===========================================================================

.. image:: https://github.com/Kitware/trame-matplotlib/actions/workflows/test_and_release.yml/badge.svg
    :target: https://github.com/Kitware/trame-matplotlib/actions/workflows/test_and_release.yml
    :alt: Test and Release

trame-matplotlib extend trame **widgets** with a component that is capable of rendering Matplotlib plots.
This library allow you to create rich visualization by leveraging `Matplotlib <https://matplotlib.org/>`__ within trame.


Installing
-----------------------------------------------------------

trame-matplotlib can be installed with `pip <https://pypi.org/project/trame-matplotlib/>`__:

.. code-block:: bash

    pip install --upgrade trame-matplotlib


Usage
-----------------------------------------------------------

The `Trame Tutorial <https://kitware.github.io/trame/guide/tutorial>`__ is the place to go to learn how to use the library and start building your own application.

The `API Reference <https://trame.readthedocs.io/en/latest/index.html>`__ documentation provides API-level documentation.


License
-----------------------------------------------------------

trame-matplotlib is made available under the BSD-3 License. For more details, see `LICENSE <https://github.com/Kitware/trame-matplotlib/blob/master/LICENSE>`__
This package is under the BSD-3 License as it is compatible with `matplotlib <https://matplotlib.org/stable/users/project/license.html>`__ and `mpld3 <https://github.com/mpld3/mpld3/blob/master/LICENSE>`__ which are used underneath that trame widget.


Community
-----------------------------------------------------------

`Trame <https://kitware.github.io/trame/>`__ | `Discussions <https://github.com/Kitware/trame/discussions>`__ | `Issues <https://github.com/Kitware/trame/issues>`__ | `Contact Us <https://www.kitware.com/contact-us/>`__

.. image:: https://zenodo.org/badge/410108340.svg
    :target: https://zenodo.org/badge/latestdoi/410108340


Enjoying trame?
-----------------------------------------------------------

Share your experience `with a testimonial <https://github.com/Kitware/trame/issues/18>`__ or `with a brand approval <https://github.com/Kitware/trame/issues/19>`__.


Code sample
-----------------------------------------------------------

Using the component method

.. code-block:: python

    import matplotlib.pyplot as plt
    from trame.widgets import matplotlib

    fig, ax = plt.subplots(**figure_size)

    widget = matplotlib.Figure(figure=None) # could pass fig at construction
    widget.update(fig)


JavaScript dependency
-----------------------------------------------------------

This Python package bundle the ``mpld3@0.5.7`` JavaScript library. If you would like us to upgrade it, `please reach out <https://www.kitware.com/trame/>`_.
