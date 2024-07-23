import asyncio
from prisma import Prisma
from prisma.models import Question, Survey
from prisma.enums import enumQtype
import logging

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_question(survey_id, qtype, text, order):
    try:
        # Create a new question
        question_data = {
            "SurveyID": survey_id,
            "Type": qtype,
            "Text": text,
            "Order": order
        }
        question = await Question.prisma().create(data=question_data)
        logger.info(f"Created question with ID: {question.QuestionID}")
        return question

    except Exception as e:
        logger.error(f"Error creating question: {str(e)}")
        raise

async def get_question(question_id):
    try:
        # Retrieve question by ID
        question = await Question.prisma().find_unique(where={"QuestionID": question_id})
        if not question:
            logger.warning(f"Question with ID {question_id} not found.")
        return question

    except Exception as e:
        logger.error(f"Error retrieving question: {str(e)}")
        raise

async def update_question(question_id, new_text):
    try:
        # Update question text
        updated_question = await Question.prisma().update(
            where={"QuestionID": question_id},
            data={"Text": new_text}
        )
        logger.info(f"Updated question with ID {question_id}. New text: {new_text}")
        return updated_question

    except Exception as e:
        logger.error(f"Error updating question: {str(e)}")
        raise

async def delete_question(question_id):
    try:
        # Delete question by ID
        deleted_question = await Question.prisma().delete(where={"QuestionID": question_id})
        logger.info(f"Deleted question with ID: {question_id}")
        return deleted_question

    except Exception as e:
        logger.error(f"Error deleting question: {str(e)}")
        raise

async def delete_all_questions():
    try:
        # Start a transaction using Prisma's transaction method
        async with Question.prisma().database.transaction():
            # Delete all questions
            deleted_count = await Question.prisma().delete_many()
            logger.info(f"Deleted {deleted_count} questions.")

            # Reset the auto-increment sequence for QuestionID column
            await Question.prisma().execute_raw("ALTER SEQUENCE question_questionid_seq RESTART WITH 1;")
            logger.info("QuestionID sequence reset successfully.")

            return deleted_count

    except Exception as e:
        logger.error(f"Error deleting all questions and resetting sequence: {str(e)}")
        raise

async def list_questions():
    try:
        # List all questions
        questions = await Question.prisma().find_many()
        if not questions:
            logger.info("No questions found.")
        else:
            logger.info("List of questions:")
            for question in questions:
                logger.info(f"QuestionID: {question.QuestionID}, SurveyID: {question.SurveyID}, Type: {question.Type}, Text: {question.Text}, Order: {question.Order}")

    except Exception as e:
        logger.error(f"Error listing questions: {str(e)}")
        raise

async def option_selection_menu():
    while True:
        print("\nOptions:")
        print("1. Create a new question")
        print("2. Get question by ID")
        print("3. Update question text")
        print("4. Delete question by ID")
        print("5. Delete all questions")
        print("6. List all questions")
        print("7. Exit")

        choice = input("Enter your choice (1-7): ").strip()

        if choice == '1':
            survey_id = int(input("Enter SurveyID for the new question: ").strip())
            print("Select question type:")
            print("1. Location")
            print("2. OpenQuestion")
            print("3. RadioButton")
            qtype_choice = input("Enter type choice (1, 2, or 3): ").strip()
            
            if qtype_choice == '1':
                qtype = enumQtype.Location.value
            elif qtype_choice == '2':
                qtype = enumQtype.OpenQuestion.value
            elif qtype_choice == '3':
                qtype = enumQtype.RadioButton.value
            else:
                print("Invalid type choice.")
                continue
            
            text = input("Enter Text for the new question: ").strip()
            order = int(input("Enter Order for the new question: ").strip())
            await create_question(survey_id, qtype, text, order)

        elif choice == '2':
            question_id = int(input("Enter QuestionID to retrieve: ").strip())
            await get_question(question_id)

        elif choice == '3':
            question_id = int(input("Enter QuestionID to update: ").strip())
            new_text = input("Enter new Text for the question: ").strip()
            await update_question(question_id, new_text)

        elif choice == '4':
            question_id = int(input("Enter QuestionID to delete: ").strip())
            await delete_question(question_id)

        elif choice == '5':
            await delete_all_questions()

        elif choice == '6':
            await list_questions()

        elif choice == '7':
            print("Exiting program.")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 7.")

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
