#!/bin/bash

# Installs parsedatetime and asana python modules.  Copies toysana.py to executable path.


die() { echo "$@" 1>&2 ; exit 1; }


TOY_LOC="/usr/local/bin"
TMP_DIR="/tmp/toysanainstall"
echo "==> If prompted, enter your user password or computer login password here."
echo "===> Why? Some of the libraries required have to be installed at the system level."
sudo rm -rf ${TMP_DIR}

sudo cp -f toysana.py ${TOY_LOC}
sudo chmod +x ${TOY_LOC}/toysana.py

[ -e /usr/bin/git ] || die "You need to install git first." 
mkdir ${TMP_DIR} 2>/dev/null
[ -d ${TMP_DIR} ] || die "Error creating ${TMP_DIR}" 

cd ${TMP_DIR}
git clone https://github.com/bear/parsedatetime.git

cd ${TMP_DIR}/parsedatetime
sudo python setup.py install
python -c "import parsedatetime" || die "Unable to install parsedatetime module"

cd ${TMP_DIR}
git clone https://github.com/pandemicsyn/asana.git
cd ${TMP_DIR}/asana
sudo python setup.py install
python -c "import asana" || die "Unable to install parsedatetime module"

echo "---"
echo "DONE! Toysana is now installed in ${TOY_LOC}"
echo "Next, open the asana-alfred.workflow file in the alfred/ subdirectory if you want to use Alfred."
echo "Configure Alfred first by typing the following as an Alfred command:"
echo "    askey  <YOUR_API_KEY>  ${TOY_LOC}/toysana.py"
echo "    You can get the API key for Asana from the Asana web site in your profile section."
echo "    More information in README.alfred"
echo ""
echo "If you want to use Toysana directly from the terminal, have a look at the README file for info on how to configure your environment with the Asana API KEY."
