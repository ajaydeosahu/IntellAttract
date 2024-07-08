import json
import boto3
import collections
import datetime

ec = boto3.client('ec2','us-west-2')
def lambda_handler(event, context):
 reservations = ec.describe_snapshots( Filters=[ {'Name': 'tag:Name', 'Values': ['devops-eks-cluster-dynamic-snapshot*']},] )
 print(reservations)
 now = datetime.datetime.today().strftime('%Y%m%d')
 print (now)
 current = int(now)
 retention = 7
 for snapshot in reservations['Snapshots']:
  print ("Checking snapshot %s which was created on %s" % (snapshot['SnapshotId'],snapshot['StartTime']))
  snapshotDate = snapshot['StartTime'].strftime('%Y%m%d')
  print(snapshotDate)
  snaptime = int(snapshotDate)
  print (snaptime)
  delete_date = (current - snaptime)
  print (delete_date)
  if delete_date > retention:
   print ("The snapshot is older than retention days. Deleting Now")
   ec.delete_snapshot(SnapshotId= snapshot['SnapshotId'])
  else:
   print ("Snapshot is newer than configured retention of %d days so we keep it" % (retention))
  
