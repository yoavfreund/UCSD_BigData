from mrjob.emr import EMRJobRunner
def find_waiting_flow(aws_access_key_id,aws_secret_access_key):
    JobRunner = EMRJobRunner(aws_access_key_id=aws_access_key_id,aws_secret_access_key=aws_secret_access_key)
    emr_conn = JobRunner.make_emr_conn()
    job_flows=emr_conn.describe_jobflows()
    job_id='NONE'
    for flow in job_flows:
        if flow.state=='WAITING':
            print flow,flow.name,flow.jobflowid,flow.state
            job_id=flow.jobflowid
    return job_id