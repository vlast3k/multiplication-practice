## ADDED Requirements

### Requirement: Award points for correct answers
The system SHALL award 10 points for each correct answer and SHALL display the points earned immediately after submission.

#### Scenario: Correct answer awards 10 points
- **WHEN** user submits a correct answer
- **THEN** system SHALL add 10 points to user's total points

#### Scenario: Points displayed after answer
- **WHEN** points are awarded
- **THEN** system SHALL display "+10 points" animation on screen

#### Scenario: Incorrect answer awards zero points
- **WHEN** user submits an incorrect answer
- **THEN** system SHALL NOT award any points

### Requirement: Award bonus points for answer streaks
The system SHALL track consecutive correct answers and SHALL award bonus points for maintaining streaks.

#### Scenario: Streak bonus at 5 consecutive correct
- **WHEN** user answers 5 questions correctly in a row
- **THEN** system SHALL award 25 bonus points (5 × 5)

#### Scenario: Streak bonus at 10 consecutive correct
- **WHEN** user answers 10 questions correctly in a row
- **THEN** system SHALL award 50 bonus points (10 × 5)

#### Scenario: Streak resets on incorrect answer
- **WHEN** user submits an incorrect answer
- **THEN** system SHALL reset current streak to zero

#### Scenario: Streak counter visible during quiz
- **WHEN** user has active streak of 2 or more
- **THEN** system SHALL display current streak count (e.g., "🔥 5 in a row!")

### Requirement: Define achievement badges
The system SHALL provide predefined achievement badges that users can unlock by meeting specific criteria.

#### Scenario: Getting Started badge definition
- **WHEN** system initializes badges
- **THEN** "Getting Started" badge SHALL require 10 problems completed

#### Scenario: Multiplication Master badge definition
- **WHEN** system initializes badges
- **THEN** "Multiplication Master" badge SHALL require 100 problems correct

#### Scenario: Perfect Ten badge definition
- **WHEN** system initializes badges
- **THEN** "Perfect Ten" badge SHALL require 10 correct answers in a row

#### Scenario: Times Table Champion badge definition
- **WHEN** system initializes badges
- **THEN** "Times Table Champion" badge SHALL require mastery of all tables 1-10 (at least 5 correct per table)

### Requirement: Unlock badges when criteria met
The system SHALL automatically check badge criteria after each answer and SHALL unlock badges when requirements are satisfied.

#### Scenario: Badge unlocked on criteria completion
- **WHEN** user completes the requirement for an unearned badge
- **THEN** system SHALL mark badge as earned and save achievement record

#### Scenario: Badge unlock triggers celebration
- **WHEN** badge is unlocked
- **THEN** system SHALL display full-screen celebration animation with badge icon

#### Scenario: Previously earned badges not re-awarded
- **WHEN** user meets criteria for already-earned badge
- **THEN** system SHALL NOT trigger celebration or duplicate achievement

### Requirement: Display earned badges in profile
The system SHALL display all earned badges in the user's profile with visual indicators for locked and unlocked states.

#### Scenario: Earned badges shown with color icon
- **WHEN** user views profile
- **THEN** all earned badges SHALL display in full color with earned date

#### Scenario: Locked badges shown in grayscale
- **WHEN** user views profile
- **THEN** unearned badges SHALL display in grayscale with progress indicator

#### Scenario: Badge progress shown for locked badges
- **WHEN** user views locked badge
- **THEN** system SHALL display progress (e.g., "8/10 problems completed")

### Requirement: Persist points and badges across sessions
The system SHALL save all points and badge achievements to the database so they persist when the user returns.

#### Scenario: Points saved after each answer
- **WHEN** user earns points
- **THEN** system SHALL update user's totalPoints in database immediately

#### Scenario: Badges saved when earned
- **WHEN** badge is unlocked
- **THEN** system SHALL create BadgeAchievement record with userId, badgeId, and earnedAt timestamp

#### Scenario: Points and badges restored on app reload
- **WHEN** user opens app after closing
- **THEN** system SHALL display current totalPoints and all earned badges from database
