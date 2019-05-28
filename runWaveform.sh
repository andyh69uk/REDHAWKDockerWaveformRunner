#!/bin/bash
echo $@
source /etc/profile.d/redhawk.sh
if [ "$SDRROOT" == "" ]; then
    export SDRROOT=/var/redhawk/sdr
fi
/usr/local/bin/runWaveform.py $@
