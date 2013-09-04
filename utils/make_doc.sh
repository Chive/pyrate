#!/bin/bash
deactivate
pip uninstall pyrate -y
cd ..
python setup.py sdist install
cd utils/
python generate_modules_func.py --suffix=rst --dest-dir=../docs/source/modules ../pyrate
cd ../docs/
make clean
make html