import asyncio
from job_pipeline import JobPipeline


if __name__ == "__main__":
    app = JobPipeline()
    asyncio.run(app.run())
