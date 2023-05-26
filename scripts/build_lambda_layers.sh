#!/bin/sh


###############################
# Python lambda build
###############################

MY_PYTHON_FUNCTION=my_python_function
BUILD_MY_PYTHON_FUNCTION=build_$MY_PYTHON_FUNCTION

# Clean up local folders
echo "Cleaning up local env..."
rm -rf $BUILD_MY_PYTHON_FUNCTION


# Map local folder with docker to "simulate" lambda layers and include external python packages in the lambda runtime
echo "Creating docker volumes for lambda layers"
docker run --rm --volume=$(pwd):/lambda-build -w=/lambda-build lambci/lambda:build-python3.8 pip install -r ./functions/$MY_PYTHON_FUNCTION/requirements.txt --target $BUILD_MY_PYTHON_FUNCTION/python

# Change ownership of lambda layers folder
if [ "$CI" = "true" ]; then
    # Github actions
    echo "Detected env: CI"
    echo "Changing ownership to lambda layers folder"
    sudo chown -R runner:docker $BUILD_MY_PYTHON_FUNCTION 
elif [  -n "$(uname -a | grep Ubuntu)" ]; then
    echo "Detected env: Ubuntu"
    sudo chown -R $USER:docker $BUILD_MY_PYTHON_FUNCTION 
else 
    echo "Detected env: Local"
fi

###############################
# TypeScript lambda build
###############################
cd functions/my_typescript_function
npm install