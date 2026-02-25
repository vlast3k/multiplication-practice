using multiplication.practice from '../db/schema';

service QuizService {
  entity Users as projection on practice.Users;
  entity PracticeSessions as projection on practice.PracticeSessions;
  entity Answers as projection on practice.Answers;
  entity Badges as projection on practice.Badges;
  entity BadgeAchievements as projection on practice.BadgeAchievements;

  type QuestionResult {
    operand1      : Integer;
    operand2      : Integer;
    correctAnswer : Integer;
    options       : array of Integer;
  }

  type SubmitAnswerResult {
    isCorrect     : Boolean;
    pointsEarned  : Integer;
    newBadges     : array of String;
    totalPoints   : Integer;
    currentStreak : Integer;
  }

  type SessionStartResult {
    sessionId : UUID;
  }

  type SessionSummary {
    totalQuestions : Integer;
    correctAnswers : Integer;
    accuracy       : Decimal;
    pointsEarned   : Integer;
  }

  action generateQuestion(difficulty : String) returns QuestionResult;
  action submitAnswer(sessionId : UUID, operand1 : Integer, operand2 : Integer, userAnswer : Integer) returns SubmitAnswerResult;
  action startSession(userId : UUID, difficulty : String) returns SessionStartResult;
  action endSession(sessionId : UUID) returns SessionSummary;
}
