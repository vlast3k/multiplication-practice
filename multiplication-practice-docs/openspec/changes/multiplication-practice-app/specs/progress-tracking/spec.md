## ADDED Requirements

### Requirement: Display total problems attempted
The system SHALL display the total number of multiplication problems the user has attempted across all sessions.

#### Scenario: Count includes all answered questions
- **WHEN** user views progress dashboard
- **THEN** system SHALL display total count of all questions answered (correct + incorrect)

#### Scenario: Count updates after each answer
- **WHEN** user submits an answer
- **THEN** total problems count SHALL increment by 1

### Requirement: Display accuracy percentage
The system SHALL calculate and display the user's overall accuracy as a percentage of correct answers.

#### Scenario: Accuracy calculated from all attempts
- **WHEN** user views progress dashboard
- **THEN** system SHALL display accuracy as (correctAnswers / totalAnswers) × 100

#### Scenario: Accuracy displayed with one decimal place
- **WHEN** accuracy is calculated
- **THEN** system SHALL display percentage with one decimal (e.g., "87.5%")

#### Scenario: Accuracy shows 0% when no questions answered
- **WHEN** user has not answered any questions
- **THEN** system SHALL display "0.0%" accuracy

### Requirement: Display current points total
The system SHALL display the user's current total points prominently on the progress dashboard.

#### Scenario: Points total shown with large font
- **WHEN** user views dashboard
- **THEN** points total SHALL be displayed in large, readable font (minimum 24pt)

#### Scenario: Points total matches database value
- **WHEN** dashboard loads
- **THEN** displayed points SHALL match user's totalPoints field in database

### Requirement: Display earned badges
The system SHALL display all badges the user has earned with visual indicators and earned dates.

#### Scenario: Earned badges shown in color
- **WHEN** user views dashboard
- **THEN** all earned badges SHALL display with full-color icons

#### Scenario: Badge earned date displayed
- **WHEN** user hovers over or taps earned badge
- **THEN** system SHALL show date badge was earned

#### Scenario: Locked badges shown in grayscale
- **WHEN** user views dashboard
- **THEN** unearned badges SHALL display in grayscale with lock icon

### Requirement: Show visual progress chart
The system SHALL display a visual chart showing accuracy trend over recent practice sessions.

#### Scenario: Chart displays last 10 sessions
- **WHEN** user has completed at least 10 sessions
- **THEN** chart SHALL show accuracy for most recent 10 sessions

#### Scenario: Chart displays all sessions if fewer than 10
- **WHEN** user has completed fewer than 10 sessions
- **THEN** chart SHALL show accuracy for all completed sessions

#### Scenario: Chart uses colorful bars or lines
- **WHEN** chart is rendered
- **THEN** system SHALL use child-friendly colors (bright, high contrast)

### Requirement: Display practice session history
The system SHALL show a list of recent practice sessions with date, duration, and performance summary.

#### Scenario: Session list shows last 5 sessions
- **WHEN** user views dashboard
- **THEN** system SHALL display 5 most recent practice sessions

#### Scenario: Each session shows date and time
- **WHEN** session is displayed
- **THEN** system SHALL show date in child-friendly format (e.g., "Today", "Yesterday", "3 days ago")

#### Scenario: Each session shows questions answered
- **WHEN** session is displayed
- **THEN** system SHALL show total questions and number correct (e.g., "8/10 correct")

#### Scenario: Each session shows star rating
- **WHEN** session is displayed
- **THEN** system SHALL show star rating based on accuracy (3 stars: 90%+, 2 stars: 70-89%, 1 star: <70%)

### Requirement: Update dashboard in real-time
The system SHALL update all dashboard statistics immediately after each practice session ends.

#### Scenario: Stats refresh when returning to dashboard
- **WHEN** user completes quiz and navigates to dashboard
- **THEN** all statistics SHALL reflect the just-completed session

#### Scenario: No manual refresh required
- **WHEN** dashboard data changes
- **THEN** system SHALL automatically update display without user action
