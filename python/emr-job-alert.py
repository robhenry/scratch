#!/usr/bin/python

"""
Connect via boto to check last 24 hours of jobs. Notify to SNS arn if a job has failed and it hasn't already been notified. Requires boto
"""
import sys
import boto.emr
from datetime import datetime, timedelta

notification_arn = sys.argv[1]
jobs_to_monitor_file = sys.argv[2]
notified_jobs_file = sys.argv[3]

jobs_to_monitor = set(line.strip() for line in open(jobs_to_monitor_file, 'r'))
notified_jobid = set(line.strip() for line in open(notified_jobs_file, 'r'))

d=datetime.utcnow()-timedelta(hours=24)
emr_conn = boto.emr.EmrConnection()
failed_jobs = emr_conn.describe_jobflows(created_after=d,states=['FAILED'])

for job in failed_jobs:
    for mjob in jobs_to_monitor:
        if job.jobflowid not in notified_jobid:
            if job.name.find(mjob) > -1:
                nf = open(notified_jobid, 'a')
                nf.write(str(job.jobflowid) + '\n')
                nf.flush()
                conn = boto.sns.connect_to_region('us-east-1')
                conn.publish(notification_arn, "EMR Failure" + job.name + ' - ' + job.jobflowid + ' - ' + job.creationdatetime)
