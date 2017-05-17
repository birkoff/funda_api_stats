#!/usr/bin/env bash


# Create build Directory and copy files
mkdir ./build
cp -v *.py ./build/
cd build;

# Install dependencies
pip install requests -t ./
pip install pymysql -t ./

# Generate buildfile and copy to parent directory
zip -r buildfile.zip data_collector.py requests pymysql
cd ..
rm buildfile.zip
cp ./build/buildfile.zip ./

# Cleanup
rm -rf ./build/

# Copy to s3
aws s3 cp buildfile.zip s3://<LambdaFunctionS3Bucket>/<LambdaFunctionS3Key>