# async def get_optional_answer(answer_id: int):
#     try:
#         # Retrieve optional answer by ID
#         optional_answer = await OptionalAnswer.prisma().find_unique(where={"AnswerID": answer_id})
#         if not optional_answer:
#             logger.warning(f"Optional answer with ID {answer_id} not found.")
#             return None
#         return optional_answer

#     except Exception as e:
#         logger.error(f"Error retrieving optional answer: {str(e)}")
#         raise

# @app.get("/optional-answer/{answer_id}")
# async def read_optional_answer(answer_id: int):
#     optional_answer = await get_optional_answer(answer_id)
#     if not optional_answer:
#         raise HTTPException(status_code=404, detail="Optional answer not found")
#     return optional_answer

