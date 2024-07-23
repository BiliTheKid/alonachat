-- CreateEnum
CREATE TYPE "enumQtype" AS ENUM ('Location', 'OpenQuestion', 'RadioButton', 'yesno');

-- CreateTable
CREATE TABLE "Survey" (
    "SurveyID" SERIAL NOT NULL,
    "PersonID" INTEGER NOT NULL,
    "Timestamp" TIMESTAMP(3) NOT NULL,
    "Title" TEXT NOT NULL,

    CONSTRAINT "Survey_pkey" PRIMARY KEY ("SurveyID")
);

-- CreateTable
CREATE TABLE "Question" (
    "QuestionID" SERIAL NOT NULL,
    "SurveyID" INTEGER NOT NULL,
    "Type" "enumQtype" NOT NULL,
    "Text" TEXT NOT NULL,
    "Order" INTEGER NOT NULL,

    CONSTRAINT "Question_pkey" PRIMARY KEY ("QuestionID")
);

-- CreateTable
CREATE TABLE "OptionalAnswer" (
    "AnswerID" SERIAL NOT NULL,
    "QuestionID" INTEGER NOT NULL,
    "Text" TEXT NOT NULL,
    "Order" INTEGER NOT NULL,

    CONSTRAINT "OptionalAnswer_pkey" PRIMARY KEY ("AnswerID")
);

-- CreateTable
CREATE TABLE "UserAnswer" (
    "PersonID" INTEGER NOT NULL,
    "QuestionID" INTEGER NOT NULL,
    "AnswerID" INTEGER NOT NULL,
    "Text" TEXT,
    "Location" TEXT,
    "Timestamp" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "UserAnswer_pkey" PRIMARY KEY ("PersonID","QuestionID")
);

-- CreateTable
CREATE TABLE "_FollowingQuestions" (
    "A" INTEGER NOT NULL,
    "B" INTEGER NOT NULL
);

-- CreateIndex
CREATE UNIQUE INDEX "_FollowingQuestions_AB_unique" ON "_FollowingQuestions"("A", "B");

-- CreateIndex
CREATE INDEX "_FollowingQuestions_B_index" ON "_FollowingQuestions"("B");

-- AddForeignKey
ALTER TABLE "Question" ADD CONSTRAINT "Question_SurveyID_fkey" FOREIGN KEY ("SurveyID") REFERENCES "Survey"("SurveyID") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "OptionalAnswer" ADD CONSTRAINT "OptionalAnswer_QuestionID_fkey" FOREIGN KEY ("QuestionID") REFERENCES "Question"("QuestionID") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "UserAnswer" ADD CONSTRAINT "UserAnswer_QuestionID_fkey" FOREIGN KEY ("QuestionID") REFERENCES "Question"("QuestionID") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "_FollowingQuestions" ADD CONSTRAINT "_FollowingQuestions_A_fkey" FOREIGN KEY ("A") REFERENCES "OptionalAnswer"("AnswerID") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "_FollowingQuestions" ADD CONSTRAINT "_FollowingQuestions_B_fkey" FOREIGN KEY ("B") REFERENCES "Question"("QuestionID") ON DELETE CASCADE ON UPDATE CASCADE;
