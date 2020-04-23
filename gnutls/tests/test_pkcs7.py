#!/usr/bin/env python

import unittest
import sys
import os
import pytest

from gnutls.crypto import X509Certificate, X509PrivateKey, Pkcs7, X509TrustList
from gnutls.library.constants import (
    GNUTLS_PKCS7_INCLUDE_TIME,
    GNUTLS_PKCS7_INCLUDE_CERT,
    GNUTLS_VERIFY_DISABLE_TIME_CHECKS,
    GNUTLS_VERIFY_DISABLE_TRUSTED_TIME_CHECKS,
)
from gnutls.library.errors import GNUTLSError

certs_path = os.path.join("gnutls", "tests", "pkcs7")


class TestPkcs7(unittest.TestCase):
    def test_pkcs7_verify(self):

        with open(os.path.join(certs_path, "LVFS-CA.pem"), "rb") as f:
            cert = X509Certificate(f.read())
            self.assertEqual(cert.issuer, "CN=LVFS CA,O=Linux Vendor Firmware Project")
            self.assertEqual(cert.serial_number, 1)
            self.assertEqual(cert.activation_time, 1501545600)
            self.assertEqual(cert.expiration_time, 2448230400)
            self.assertEqual(cert.version, 3)

        with open(os.path.join(certs_path, "firmware.bin"), "rb") as f:
            data = f.read()

        # verify with a signature from the old LVFS
        with open(os.path.join(certs_path, "firmware.bin.p7b"), "rb") as f:
            data_sig = f.read()
        tl = X509TrustList()
        tl.add_ca(cert)
        pkcs7 = Pkcs7()
        pkcs7.import_signature(data_sig)
        pkcs7.verify(
            tl,
            data,
            flags=GNUTLS_VERIFY_DISABLE_TIME_CHECKS
            | GNUTLS_VERIFY_DISABLE_TRUSTED_TIME_CHECKS,
        )

        # verify will fail with valid signature and different data
        with pytest.raises(GNUTLSError):
            pkcs7.verify(
                tl,
                b"FOO",
                flags=GNUTLS_VERIFY_DISABLE_TIME_CHECKS
                | GNUTLS_VERIFY_DISABLE_TRUSTED_TIME_CHECKS,
            )

    def test_pkcs7_self_sign(self):

        # PCKS7 sign some data then verify it
        with open(os.path.join(certs_path, "test.pem"), "rb") as f:
            cert = X509Certificate(f.read())
        with open(os.path.join(certs_path, "test.key"), "rb") as f:
            privkey = X509PrivateKey(f.read())

        data = b"Hello World!"
        pkcs7 = Pkcs7()
        pkcs7.sign(
            cert,
            privkey,
            data,
            flags=GNUTLS_PKCS7_INCLUDE_TIME | GNUTLS_PKCS7_INCLUDE_CERT,
        )
        data_sig = pkcs7.export()
        pkcs7 = Pkcs7()
        pkcs7.import_signature(data_sig)
        pkcs7.verify_direct(cert, data)
