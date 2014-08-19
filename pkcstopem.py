#!/usr/bin/env python2.7

import os
import sys
from OpenSSL import crypto
from getpass import getpass

usage = """
usage: %s <p12 cert pack>
       this utility will output a pem bundle in the same directory
        """ % os.path.basename(sys.argv[0])

if len(sys.argv) <= 1:
    print usage
    sys.exit(1)

p12Filename = sys.argv[1]
p12Passphrase = getpass('passphrase[%s]: ' % p12Filename) or ''
pemFilename = os.path.splitext(p12Filename)[0][0:].strip() + '.pem'

try:
    with open(p12Filename, 'rb') as p12File:
        p12 = crypto.load_pkcs12(p12File.read(), p12Passphrase)
        p12_certificate = p12.get_certificate()
        p12_privatekey = p12.get_privatekey()

        certificate = crypto.dump_certificate(crypto.FILETYPE_PEM, p12_certificate)
        private_key = crypto.dump_privatekey(crypto.FILETYPE_PEM, p12_privatekey)
except Exception, e:
    if any(s in "mac verify failure" for s in e.message[0]):
        print "please provide a passphrase"
        sys.exit(1)
    else:
        print "uncaught exception"
        print e
        sys.exit(1)

try:
    with open(pemFilename, 'wb') as pemFile:
        pemFile.write(certificate + private_key)
except Exception, e:
    print e
    sys.exit(1)
