import asyncio
from datetime import datetime
from prisma import Prisma
from prisma.models import Survey, Question
from prisma.enums import enumQtype
import logging

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_survey(person_id, title):
    try:
        # Create a new survey
        survey_data = {
            "PersonID": person_id,
            "Timestamp": datetime.now(),
            "Title": title
        }
        survey = await Survey.prisma().create(data=survey_data)
        logger.info(f"Created survey with ID: {survey.SurveyID}")
        return survey

    except Exception as e:
        logger.error(f"Error creating survey: {str(e)}")
        raise

async def list_surveys():
    try:
        # List all surveys
        surveys = await Survey.prisma().find_many()
        if not surveys:
            logger.info("No surveys found.")
        else:
            logger.info("List of surveys:")
            for survey in surveys:
                logger.info(f"SurveyID: {survey.SurveyID}, Title: {survey.Title}, Timestamp: {survey.Timestamp}")

    except Exception as e:
        logger.error(f"Error listing surveys: {str(e)}")
        raise

async def delete_all_surveys():
    try:
        # Delete all surveys
        deleted_count = await Survey.prisma().delete_many()
        logger.info(f"Deleted {deleted_count} surveys.")
        return deleted_count

    except Exception as e:
        logger.error(f"Error deleting all surveys: {str(e)}")
        raise

async def option_selection_menu():
    while True:
        print("\nOptions:")
        print("1. Create a new survey")
        print("2. List all surveys")
        print("3. Delete all surveys")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ").strip()

        if choice == '1':
            person_id = int(input("Enter PersonID for the new survey: ").strip())
            title = input("Enter Title for the new survey: ").strip()
            await create_survey(person_id, title)

        elif choice == '2':
            await list_surveys()

        elif choice == '3':
            await delete_all_surveys()

        elif choice == '4':
            print("Exiting program.")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

async def main():
    try:
        db = Prisma(auto_register=True)
        await db.connect()

        await option_selection_menu()

    except Exception as e:
        logger.error(f"Error in main process: {str(e)}")
        raise

    finally:
        await db.disconnect()

if __name__ == '__main__':
    asyncio.run(main())
