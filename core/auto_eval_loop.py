from apscheduler.schedulers.blocking import BlockingScheduler
from evaluation_engine import evaluate

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=30)
def run_eval():
    print("AUTO EVALUATION RUNNING")
    evaluate()

print("NARAYA AUTO-EVAL ACTIVE")

sched.start()
