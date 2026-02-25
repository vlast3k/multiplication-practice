## ADDED Requirements

### Requirement: Provide three difficulty levels
The system SHALL provide three difficulty levels: Easy (tables 1-5), Medium (tables 1-10), and Hard (tables 1-12).

#### Scenario: Easy level uses tables 1-5
- **WHEN** user selects Easy difficulty
- **THEN** all questions SHALL use operands between 1 and 5

#### Scenario: Medium level uses tables 1-10
- **WHEN** user selects Medium difficulty
- **THEN** all questions SHALL use operands between 1 and 10

#### Scenario: Hard level uses tables 1-12
- **WHEN** user selects Hard difficulty
- **THEN** all questions SHALL use operands between 1 and 12

### Requirement: Allow difficulty selection before quiz
The system SHALL allow the user to select difficulty level before starting a quiz session.

#### Scenario: Difficulty selector shown on quiz start
- **WHEN** user navigates to quiz view without active session
- **THEN** system SHALL display three difficulty buttons (Easy, Medium, Hard)

#### Scenario: Selected difficulty starts quiz
- **WHEN** user clicks a difficulty button
- **THEN** system SHALL start quiz with that difficulty level

#### Scenario: Default difficulty is Medium
- **WHEN** user has never selected difficulty
- **THEN** system SHALL default to Medium level

### Requirement: Allow difficulty change during quiz
The system SHALL allow the user to change difficulty level at any time during a quiz session.

#### Scenario: Difficulty selector accessible during quiz
- **WHEN** user is answering questions
- **THEN** system SHALL display difficulty selector in quiz header

#### Scenario: Changing difficulty loads new question
- **WHEN** user changes difficulty during quiz
- **THEN** system SHALL immediately load a new question matching new difficulty

#### Scenario: Difficulty change recorded in session
- **WHEN** user changes difficulty during session
- **THEN** system SHALL record difficulty change in practice session data

### Requirement: Display current difficulty level
The system SHALL clearly indicate the current difficulty level to the user.

#### Scenario: Difficulty badge shown in quiz view
- **WHEN** user is answering questions
- **THEN** system SHALL display current difficulty as a colored badge (Easy: green, Medium: yellow, Hard: red)

#### Scenario: Difficulty shown in session history
- **WHEN** user views past sessions in dashboard
- **THEN** each session SHALL show difficulty level used

### Requirement: Track difficulty-specific statistics
The system SHALL track separate statistics for each difficulty level.

#### Scenario: Accuracy tracked per difficulty
- **WHEN** user views dashboard
- **THEN** system SHALL show accuracy percentage for each difficulty level separately

#### Scenario: Questions count tracked per difficulty
- **WHEN** user views dashboard
- **THEN** system SHALL show number of questions answered at each difficulty level

### Requirement: Generate appropriate questions for difficulty
The system SHALL generate questions that match the selected difficulty level's operand range.

#### Scenario: Easy questions use small numbers
- **WHEN** difficulty is Easy
- **THEN** both operands in question SHALL be between 1 and 5

#### Scenario: Medium questions use medium numbers
- **WHEN** difficulty is Medium
- **THEN** both operands in question SHALL be between 1 and 10

#### Scenario: Hard questions use larger numbers
- **WHEN** difficulty is Hard
- **THEN** both operands in question SHALL be between 1 and 12

#### Scenario: Questions evenly distributed across range
- **WHEN** system generates questions
- **THEN** all valid operand combinations SHALL have equal probability of appearing

### Requirement: Persist difficulty preference
The system SHALL remember the user's last selected difficulty level.

#### Scenario: Last difficulty saved after session
- **WHEN** user completes quiz session
- **THEN** system SHALL save difficulty level to user preferences

#### Scenario: Last difficulty used as default
- **WHEN** user starts new quiz session
- **THEN** system SHALL default to last used difficulty level
