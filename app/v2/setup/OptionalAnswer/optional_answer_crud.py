import asyncio
from prisma import Prisma
from prisma.models import OptionalAnswer, Question
import logging

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_optional_answer(question_id, text, order):
    try:
        # Create a new optional answer
        optional_answer_data = {
            "QuestionID": question_id,
            "Text": text,
            "Order": order
        }
        optional_answer = await OptionalAnswer.prisma().create(data=optional_answer_data)
        logger.info(f"Created optional answer with ID: {optional_answer.AnswerID}")
        return optional_answer

    except Exception as e:
        logger.error(f"Error creating optional answer: {str(e)}")
        raise

async def get_optional_answer(answer_id):
    try:
        # Retrieve optional answer by ID
        optional_answer = await OptionalAnswer.prisma().find_unique(where={"AnswerID": answer_id})
        if not optional_answer:
            logger.warning(f"Optional answer with ID {answer_id} not found.")
        return optional_answer

    except Exception as e:
        logger.error(f"Error retrieving optional answer: {str(e)}")
        raise

async def update_optional_answer(answer_id, new_text):
    try:
        # Update optional answer text
        updated_optional_answer = await OptionalAnswer.prisma().update(
            where={"AnswerID": answer_id},
            data={"Text": new_text}
        )
        logger.info(f"Updated optional answer with ID {answer_id}. New text: {new_text}")
        return updated_optional_answer

    except Exception as e:
        logger.error(f"Error updating optional answer: {str(e)}")
        raise

async def delete_optional_answer(answer_id):
    try:
        # Delete optional answer by ID
        deleted_optional_answer = await OptionalAnswer.prisma().delete(where={"AnswerID": answer_id})
        logger.info(f"Deleted optional answer with ID: {answer_id}")
        return deleted_optional_answer

    except Exception as e:
        logger.error(f"Error deleting optional answer: {str(e)}")
        raise

async def delete_all_optional_answers():
    try:
        # Delete all optional answers
        deleted_count = await OptionalAnswer.prisma().delete_many()
        logger.info(f"Deleted {deleted_count} optional answers.")
        return deleted_count

    except Exception as e:
        logger.error(f"Error deleting all optional answers: {str(e)}")
        raise

async def list_optional_answers():
    try:
        # List all optional answers
        optional_answers = await OptionalAnswer.prisma().find_many()
        if not optional_answers:
            logger.info("No optional answers found.")
        else:
            logger.info("List of optional answers:")
            for answer in optional_answers:
                logger.info(f"AnswerID: {answer.AnswerID}, QuestionID: {answer.QuestionID}, Text: {answer.Text}, Order: {answer.Order}, Following Question ID: {answer.followingQuestionID}")

    except Exception as e:
        logger.error(f"Error listing optional answers: {str(e)}")
        raise

async def option_selection_menu():
    while True:
        print("\nOptions:")
        print("1. Create a new optional answer")
        print("2. Get optional answer by ID")
        print("3. Update optional answer text")
        print("4. Delete optional answer by ID")
        print("5. Delete all optional answers")
        print("6. List all optional answers")
        print("7. Exit")

        choice = input("Enter your choice (1-7): ").strip()

        if choice == '1':
            question_id = int(input("Enter QuestionID for the new optional answer: ").strip())
            text = input("Enter Text for the new optional answer: ").strip()
            order = int(input("Enter Order for the new optional answer: ").strip())
            await create_optional_answer(question_id, text, order)

        elif choice == '2':
            answer_id = int(input("Enter AnswerID to retrieve: ").strip())
            await get_optional_answer(answer_id)

        elif choice == '3':
            answer_id = int(input("Enter AnswerID to update: ").strip())
            new_text = input("Enter new Text for the optional answer: ").strip()
            await update_optional_answer(answer_id, new_text)

        elif choice == '4':
            answer_id = int(input("Enter AnswerID to delete: ").strip())
            await delete_optional_answer(answer_id)

        elif choice == '5':
            await delete_all_optional_answers()

        elif choice == '6':
            await list_optional_answers()

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
