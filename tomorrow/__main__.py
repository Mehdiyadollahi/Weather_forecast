import logging
import asyncio
import schedule
import time
from . import config
# import config
from .scraper import fetch_all_weather, store_weather_data_batch
# from scraper import fetch_all_weather, store_weather_data_batch
from dbt.cli.main import dbtRunner, dbtRunnerResult


# configure logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')
logger = logging.getLogger(__name__)

# Main entry point for the asynchronous fetching


async def main():
    weather_data = await fetch_all_weather()
    weather_data = [x for xs in weather_data for x in xs]
    await store_weather_data_batch(weather_data)
    
# Function to programmatically invoke dbt run with specified project directory
def dbt_run():
    try:
        # Initialize the dbtRunner
        runner = dbtRunner()
        
        # Set up the dbt run arguments, pointing to the project directory
        args = ["run", "--project-dir", config.DBT_PROJECT_DIR, "--profiles-dir", config.DBT_PROJECT_DIR]
        
        # This invokes dbt's run command programmatically within the specified directory
        result = runner.invoke(args)

        # inspect the results   
        for r in result.result:
            print(f"{r.node.name}: {r.status}")
            
    except Exception as e:
        print("dbt run failed:", e)


def schedule_calling_api():
    # Run the asynchronous main function
    asyncio.run(main())
    
    logger.info("Weather data fetching completed successfully.")
        
    # Run dbt programmatically after successful completion
    dbt_run()

# Schedule the wrapper function to run every hour
schedule.every().hour.do(schedule_calling_api)

# Run immediately, then enter the scheduled loop
schedule_calling_api()  # Run the function immediately upon script start

while True:
    schedule.run_pending()
    time.sleep(1)

