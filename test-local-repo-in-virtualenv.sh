#!/bin/bash -ev

TIMESTAMP=`date +%s`
TEST_DIR="/tmp/test-ado/$TIMESTAMP"

echo "Running test script in $TEST_DIR"
mkdir -p $TEST_DIR
pushd $TEST_DIR

virtualenv testenv
source testenv/bin/activate

git clone ~/dev/ado $TEST_DIR/ado
cd ado
pip install .

cd docs
dexy setup
dexy
cd ..

# go back into timestamp dir
cd ..

dexy gen -plugins 'ado.dexy_plugins' -t adoreport -d testreport

cd testreport
dexy
cd ..

