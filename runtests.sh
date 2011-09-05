#!/bin/bash

find . -name '*.pyc' -delete

args=("$@")
num_args=${#args[@]}
index=0

django=12
reuse_env=true
disable_coverage=true
update_requirements=false

python="python" # to ensure this script works if no python option is specified
while [ "$index" -lt "$num_args" ]
do
case "${args[$index]}" in
        "-f"|"--failfast")
            failfast="--failfast"
            ;;

        "-r"|"--rebuild-env")
            reuse_env=false
            ;;
        
        "-u"|"--update-requirements")
            update_requirements=true
            ;;
        
        "-d"|"--django")
            let "index = $index + 1"
            django="${args[$index]}"
            ;;
        
        "-p"|"--python")
            let "index = $index + 1"
            python="${args[$index]}"
            ;;
            
        "-c"|"--with-coverage")
            disable_coverage=false
            ;;
        
        "-h"|"--help")
            echo ""
            echo "usage:"
            echo " runtests.sh"
            echo ""
            echo "flags:"
            echo " -r, --rebuild-env - delete virtualenv and rebuild virtualenv before the tests"
            echo " -u, --update-requirements - update requirements before the tests"
            echo " -d, --django <version> - run tests against a django version, options: 12, 13 or trunk"
            echo " -c, --with-coverage - enables coverage"
            echo " -p, --python /path/to/python - python version to use to run the tests"
            echo " -h, --help - display this help"
            exit 1
            ;;
    esac
let "index = $index + 1"
done

python_executeable=`which $python`

echo "using python at: $python_executeable"

venv="venv-$python-$django"

if [ $reuse_env == false ]; then
    rm -rf $venv
    echo "deleted virtualenv: $venv"
fi

if [ ! -d $venv ]; then
    echo "building virtualenv"
    virtualenv $venv --distribute -p $python_executeable
    update_requirements=true
else
    echo "reusing current virualenv: $venv"
fi

if [ $update_requirements == true ]; then
    echo "updating requirements"
    $venv/bin/pip install -r requirements-$django.txt
    $venv/bin/pip install -r requirements.txt
fi

if [ $disable_coverage == false ]; then
    $venv/bin/coverage run --rcfile=coveragerc setup.py test
    retcode=$?
    echo "build coverage reports"

    $venv/bin/coverage xml --rcfile=coveragerc
    $venv/bin/coverage html --rcfile=coveragerc
    $venv/bin/coverage report -m --rcfile=coveragerc
else
    $venv/bin/python setup.py test
    retcode=$?
fi
exit $retcode