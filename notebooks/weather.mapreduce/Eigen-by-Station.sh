#!/bin/bash
# compute weather statistics as a function of station's latitude.

source $CSD181/hadoop/hadoop_shared/hadoop_bashrc.sh

code_dir=$CSD181/yfreund/weather/processing
in_hdfs=/user/arapat/weather
out_hdfs=/user/$USER/weather_eigen_2

hdfs -rmr $out_hdfs

time had jar /opt/hadoop/contrib/streaming/hadoop-*streaming*.jar -Dmapred.map.tasks=20 -Dmapred.reduce.tasks=20 -mapper $code_dir/map-year-temp.py -reducer $code_dir/reduce-year-temp.py -input $in_hdfs/* -output $out_hdfs


#Instead of plain text files, you can generate gzip files as your generated output. 
# Pass '-D mapred.output.compress=true -D mapred.output.compression.codec=org.apache.hadoop.io.compress.GzipCodec' as option to your streaming job.
