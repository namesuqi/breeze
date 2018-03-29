#!/bin/bash
mysqldump -h 192.168.1.61 -uppc -pyunshang2014 user_experience | gzip > /root/mysql_backup/ue_$(date +%Y%m%d_%H%M%S).sql.gz
