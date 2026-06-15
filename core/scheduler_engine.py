from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=60)
def berita_job():
    print("RUN BERITA")

sched.start()
