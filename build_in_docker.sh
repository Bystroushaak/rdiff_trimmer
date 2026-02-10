#! /usr/bin/env bash

cp -r /code /tmp
cd /tmp/code
#dh $@ --python /usr/bin/python3

export DEB_BUILD_OPTIONS="nocheck"
debuild -b -us -uc

mkdir -p /code/deb_build

find /tmp -maxdepth 1 -name "*.deb" -exec cp {} /code/deb_build \;

chmod -R 777 /code/deb_build
chown 1000:1000 -R /code/deb_build
