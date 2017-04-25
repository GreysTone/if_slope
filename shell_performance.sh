#!/bin/bash

begin=`date +%s.%N`

count=1000
for ((i=0;i<count;i++))
do
  cat /proc/net/dev | grep eth0 > /dev/null
done

end=`date +%s.%N`

echo $end
echo $begin
