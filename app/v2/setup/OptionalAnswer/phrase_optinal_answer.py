import asyncio
import pandas as pd
from prisma import Prisma
from prisma.models import OptionalAnswer, Question
import logging

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_optional_answers_from_csv(csv_file):
    try:
        # Read CSV file into a DataFrame
        df = pd.read_csv(csv_file)

        # Iterate over rows in the DataFrame and create optional answers
        for index, row in df.iterrows():
            question_id = int(row['QuestionID'])
            try:
                # Verify that the question exists
                question_exists = await Question.prisma().find_unique(where={"QuestionID": question_id})
                if not question_exists:
                    logger.error(f"QuestionID {question_id} does not exist in the Question table.")
                    continue

                entry = {
                    "QuestionID": question_id,
                    "Text": row['Text'],
                    "Order": int(row['Order']),
                    "followingQuestionID": int(row['FollowingQuestions']) if pd.notna(row['FollowingQuestions']) else None
                }
                await OptionalAnswer.prisma().create(data=entry)
                logger.info(f"Created optional answer for QuestionID {entry['QuestionID']}")
            except Exception as e:
                logger.error(f"Error creating optional answer for QuestionID {question_id}: {str(e)}")

    except Exception as e:
        logger.error(f"Error creating optional answers from CSV: {str(e)}")
        raise

async def main():
    try:
        db = Prisma(auto_register=True)
        await db.connect()
        await create_optional_answers_from_csv("OptionalAnswers.csv")

    except Exception as e:
        logger.error(f"Error in main process: {str(e)}")
        raise

    finally:
        await db.disconnect()

if __name__ == '__main__':
    asyncio.run(main())
