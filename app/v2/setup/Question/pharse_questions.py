import asyncio
import pandas as pd
from prisma import Prisma
from prisma.models import Question
import logging

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_questions_from_csv(csv_file):
    try:
        # Read CSV file into a DataFrame
        df = pd.read_csv(csv_file)

        # Iterate over rows in the DataFrame and create questions
        for index, row in df.iterrows():
            entry = {
                "SurveyID": int(row['SurveyID']),
                "Type": row['Type'],
                "Text": row['Text'],
                "Order": int(row['Order'])
            }
            await Question.prisma().create(data=entry)
            logger.info(f"Created question for SurveyID {entry['SurveyID']}")

    except Exception as e:
        logger.error(f"Error creating questions from CSV: {str(e)}")
        raise

async def main():
    try:
        db = Prisma(auto_register=True)
        await db.connect()

        csv_file = 'questions.csv'  # Update with your CSV file path for questions
        await create_questions_from_csv(csv_file)

    except Exception as e:
        logger.error(f"Error in main process: {str(e)}")
        raise

    finally:
        await db.disconnect()

if __name__ == '__main__':
    asyncio.run(main())
