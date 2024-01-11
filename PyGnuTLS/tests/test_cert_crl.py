#!/usr/bin/env python

import unittest
import os
import time

from PyGnuTLS.crypto import X509Certificate, X509CRL

certs_path = os.path.join("PyGnuTLS", "tests", "certs")


class TestCertificates(unittest.TestCase):
    def test_crl_is_revoked(self):

        cert = X509Certificate(open(os.path.join(certs_path, "valid.crt"), "rb").read())
        crl = X509CRL(open(os.path.join(certs_path, "crl.pem"), "rb").read())

        print("CRL certs/crl.pem:")
        print("CRL issuer:")
        print(f"  CN = {crl.issuer.CN}")  # or crl.issuer.common_name
        print(f"  O  = {crl.issuer.O}")  # or crl.issuer.organization
        print(f"  OU = {crl.issuer.OU}")  # or crl.issuer.organization_unit
        print(f"  C  = {crl.issuer.C}")  # or crl.issuer.country
        print(f"  ST = {crl.issuer.ST}")  # or crl.issuer.state
        print(f"  L  = {crl.issuer.L}")  # or crl.issuer.locality
        print(f"  EMAIL = {crl.issuer.EMAIL}")  # or crl.issuer.email
        print("CRL version:", crl.version)
        print("CRL count:  ", crl.count)

        print("Certificate certs/valid.crt:")
        print("Cert subject:")
        print(f"  CN = {cert.subject.CN}")  # or cert.subject.common_name
        print(f"  O  = {cert.subject.O}")  # or cert.subject.organization
        print(f"  OU = {cert.subject.OU}")  # or cert.subject.organization_unit
        print(f"  C  = {cert.subject.C}")  # or cert.subject.country
        print(f"  ST = {cert.subject.ST}")  # or cert.subject.state
        print(f"  L  = {cert.subject.L}")  # or cert.subject.locality
        print(f"  EMAIL = {cert.subject.EMAIL}")  # or cert.subject.email
        print("Cert issuer:")
        print(f"  CN = {cert.issuer.CN}")  # or cert.issuer.common_name
        print(f"  O  = {cert.issuer.O}")  # or cert.issuer.organization
        print(f"  OU = {cert.issuer.OU}")  # or cert.issuer.organization_unit
        print(f"  C  = {cert.issuer.C}")  # or cert.issuer.country
        print(f"  ST = {cert.issuer.ST}")  # or cert.issuer.state
        print(f"  L  = {cert.issuer.L}")  # or cert.issuer.locality
        print(f"  EMAIL = {cert.issuer.EMAIL}")  # or cert.issuer.email
        print("Cert serial:    ", cert.serial_number)
        print("Cert version:   ", cert.version)
        print("Cert activation:", time.ctime(cert.activation_time))
        print("Cert expiration:", time.ctime(cert.expiration_time))
        self.assertFalse(crl.is_revoked(cert))

        cert = X509Certificate(
            open(os.path.join(certs_path, "revoked.crt"), "rb").read()
        )
        print("Certificate certs/revoked.crt:")
        print("Cert subject:")
        print(f"  CN = {cert.subject.common_name}")  # here we use long names
        print(f"  O  = {cert.subject.organization}")
        print(f"  OU = {cert.subject.organization_unit}")
        print(f"  C  = {cert.subject.country}")
        print(f"  ST = {cert.subject.state}")
        print(f"  L  = {cert.subject.locality}")
        print(f"  EMAIL = {cert.subject.email}")
        print("Cert issuer:")
        print(f"  CN = {cert.issuer.common_name}")
        print(f"  O  = {cert.issuer.organization}")
        print(f"  OU = {cert.issuer.organization_unit}")
        print(f"  C  = {cert.issuer.country}")
        print(f"  ST = {cert.issuer.state}")
        print(f"  L  = {cert.issuer.locality}")
        print(f"  EMAIL = {cert.issuer.email}")
        print("Cert serial:    ", cert.serial_number)
        print("Cert version:   ", cert.version)
        print("Cert activation:", time.ctime(cert.activation_time))
        print("Cert expiration:", time.ctime(cert.expiration_time))
        self.assertTrue(crl.is_revoked(cert))


if __name__ == "__main__":
    unittest.main()
