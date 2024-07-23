/*
  Warnings:

  - The values [yesno] on the enum `enumQtype` will be removed. If these variants are still used in the database, this will fail.
  - You are about to drop the `_FollowingQuestions` table. If the table is not empty, all the data it contains will be lost.

*/
-- AlterEnum
BEGIN;
CREATE TYPE "enumQtype_new" AS ENUM ('Location', 'OpenQuestion', 'RadioButton');
ALTER TABLE "Question" ALTER COLUMN "Type" TYPE "enumQtype_new" USING ("Type"::text::"enumQtype_new");
ALTER TYPE "enumQtype" RENAME TO "enumQtype_old";
ALTER TYPE "enumQtype_new" RENAME TO "enumQtype";
DROP TYPE "enumQtype_old";
COMMIT;

-- DropForeignKey
ALTER TABLE "_FollowingQuestions" DROP CONSTRAINT "_FollowingQuestions_A_fkey";

-- DropForeignKey
ALTER TABLE "_FollowingQuestions" DROP CONSTRAINT "_FollowingQuestions_B_fkey";

-- AlterTable
ALTER TABLE "OptionalAnswer" ADD COLUMN     "followingQuestionID" INTEGER;

-- DropTable
DROP TABLE "_FollowingQuestions";

-- AddForeignKey
ALTER TABLE "OptionalAnswer" ADD CONSTRAINT "OptionalAnswer_followingQuestionID_fkey" FOREIGN KEY ("followingQuestionID") REFERENCES "Question"("QuestionID") ON DELETE SET NULL ON UPDATE CASCADE;
