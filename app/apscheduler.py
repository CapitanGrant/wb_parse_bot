from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler



scheduler = AsyncIOScheduler()
jobstores = {'default': MemoryJobStore()}
scheduler.configure(jobstores=jobstores)
scheduler.start()