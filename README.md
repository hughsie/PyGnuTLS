# PyGnuTLS

This package provides a high level object oriented wrapper around libgnutls,
as well as low level bindings to the GnuTLS types and functions via ctypes.
The high level wrapper hides the details of accessing the GnuTLS library via
ctypes behind a set of classes that encapsulate GnuTLS sessions, certificates
and credentials and expose them to python applications using a simple API.

# Release Process

These notes are probably only for the maintainer of this module!

    # set version in setup.py
    make pkg
    ./env/bin/twine upload dist/*
    git commit -a -m "New version for PyPI" && git push
