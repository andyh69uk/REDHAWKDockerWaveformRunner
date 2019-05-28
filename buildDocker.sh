#!/bin/bash
usage()
{
	
	printf "\nusage: buildDocker.sh [[[-w waveform]]|[-h]]\n\n"
	printf "Script will prepare and build a REDHAWK docker image containing the waveform and dependencies passed using -w <waveform name>\n\n"
	printf "Any rpms that need making available to the docker build should be placed in localrepo, if any rpms exists createrepo will be run and folder tar'd up\n\n"
	printf "The rpms will be made available with local.repo\n\n"
	printf "Any other repo files should be placed in repofiles, any .repo files will be added to /etc/yum.repos.d/ at the beginning of the docker build\n\n"
}

WAVEFORM=''
TAG=''
while [ "$1" != "" ]; do
	case $1 in
		-w | --waveform )	shift
							WAVEFORM=$1
							TAG="redhawk_${WAVEFORM,,}"
							;;
		-h | --help )		usage
							exit
							;;
		* )					usage
							exit 1
	esac
	shift
done

if [ -z "$WAVEFORM" ]
then 
	printf "\n#### Must pass target waveform name ####\n\n"; 
	usage
	exit 1
fi

if [ $(find ./localrepo/ -name '*.rpm' | wc -l) -gt 0 ]
then 
	createrepo ./localrepo/
	tar -cvzf localrepo.tar.gz ./localrepo/
fi
docker build -t $TAG --build-arg WAVEFORM=$WAVEFORM -f dockerbuild .
