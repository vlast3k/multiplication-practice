namespace multiplication.practice;

using { cuid, managed } from '@sap/cds/common';

entity Users : cuid {
  name            : String;
  avatar          : String;
  totalPoints     : Integer default 0;
  currentStreak   : Integer default 0;
  bestStreak      : Integer default 0;
  lastDifficulty  : String default 'Medium';
  createdAt       : Timestamp;
}

entity PracticeSessions : cuid {
  user            : Association to Users;
  startTime       : Timestamp;
  endTime         : Timestamp;
  totalQuestions  : Integer default 0;
  correctAnswers  : Integer default 0;
  difficultyLevel : String;
}

entity Answers : cuid {
  session         : Association to PracticeSessions;
  operand1        : Integer;
  operand2        : Integer;
  userAnswer      : Integer;
  correctAnswer   : Integer;
  isCorrect       : Boolean;
  pointsEarned    : Integer default 0;
  timestamp       : Timestamp;
}

entity Badges {
  key id              : String;
  name                : String;
  description         : String;
  icon                : String;
  requirementType     : String;
  requirementValue    : Integer;
}

entity BadgeAchievements : cuid {
  user            : Association to Users;
  badge           : Association to Badges;
  earnedAt        : Timestamp;
}
