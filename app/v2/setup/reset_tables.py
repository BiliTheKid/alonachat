import asyncio
from prisma import Prisma
import prisma
from prisma.models import OptionalAnswer, Survey, Question, UserAnswer
import logging

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def reset_tables():
    try:
        db = Prisma(auto_register=True)
        await db.connect()

        # Delete all UserAnswers
        deleted_user_answers = await UserAnswer.prisma().delete_many()
        logger.info(f"Deleted {deleted_user_answers} UserAnswers.")

        # Delete all OptionalAnswers
        deleted_optional_answers = await OptionalAnswer.prisma().delete_many()
        logger.info(f"Deleted {deleted_optional_answers} OptionalAnswers.")

        # Delete all Questions
        deleted_questions = await Question.prisma().delete_many()
        logger.info(f"Deleted {deleted_questions} Questions.")

        # Delete all Surveys
        deleted_surveys = await Survey.prisma().delete_many()
        logger.info(f"Deleted {deleted_surveys} Surveys.")

        # Reset auto-increment sequences
        await db.execute_raw('ALTER SEQUENCE "Survey_SurveyID_seq" RESTART WITH 1')
        await db.execute_raw('ALTER SEQUENCE "Question_QuestionID_seq" RESTART WITH 1')
        await db.execute_raw('ALTER SEQUENCE "OptionalAnswer_AnswerID_seq" RESTART WITH 1')

        logger.info("Reset auto-increment sequences.")

    except Exception as e:
        logger.error(f"Error resetting tables: {str(e)}")
        raise
    finally:
        await db.disconnect()

async def main():
    try:
        await reset_tables()
    except Exception as e:
        logger.error(f"Error in main process: {str(e)}")
        raise

if __name__ == '__main__':
    asyncio.run(main())
