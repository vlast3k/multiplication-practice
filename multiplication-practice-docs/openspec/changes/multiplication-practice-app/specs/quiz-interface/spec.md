## ADDED Requirements

### Requirement: Display multiplication question with multiple-choice options
The system SHALL present a multiplication question with four multiple-choice answer options, where exactly one option is correct and three are plausible distractors.

#### Scenario: Question displayed with correct answer among options
- **WHEN** user navigates to quiz view
- **THEN** system displays a multiplication question (e.g., "7 × 8 = ?") with four answer buttons

#### Scenario: Options include correct answer
- **WHEN** system generates question options
- **THEN** one option MUST be the mathematically correct answer

#### Scenario: Distractors are plausible
- **WHEN** system generates incorrect options
- **THEN** distractors MUST be within ±20% of correct answer to avoid obvious wrong answers

### Requirement: Accept and validate user answer
The system SHALL allow the user to select one answer option and SHALL validate whether the selected answer is correct.

#### Scenario: User selects correct answer
- **WHEN** user clicks the button with the correct answer
- **THEN** system indicates the answer is correct with positive feedback

#### Scenario: User selects incorrect answer
- **WHEN** user clicks a button with an incorrect answer
- **THEN** system indicates the answer is incorrect with supportive feedback

#### Scenario: Only one answer can be selected per question
- **WHEN** user clicks an answer button
- **THEN** system SHALL disable all answer buttons until next question loads

### Requirement: Provide immediate visual feedback
The system SHALL provide immediate visual feedback after answer submission, indicating whether the answer was correct or incorrect.

#### Scenario: Correct answer shows positive feedback
- **WHEN** user submits correct answer
- **THEN** system displays green border flash and success message (e.g., "Great job!")

#### Scenario: Incorrect answer shows supportive feedback
- **WHEN** user submits incorrect answer
- **THEN** system displays gentle animation and encouraging message (e.g., "Almost! Try again!")

#### Scenario: Feedback appears within 200ms
- **WHEN** user submits any answer
- **THEN** visual feedback MUST appear within 200 milliseconds

### Requirement: Load next question automatically
The system SHALL automatically load the next question after a brief delay following answer submission.

#### Scenario: Next question loads after feedback
- **WHEN** user submits an answer and feedback is displayed
- **THEN** system SHALL load a new question within 2 seconds

#### Scenario: Each question is unique within session
- **WHEN** system generates a new question
- **THEN** question MUST be different from all previous questions in the current session

### Requirement: Display optional countdown timer
The system SHALL provide an optional countdown timer that can be enabled or disabled by the user.

#### Scenario: Timer displays remaining seconds
- **WHEN** timer is enabled and question is displayed
- **THEN** system shows countdown in seconds (default 30 seconds per question)

#### Scenario: Timer can be disabled
- **WHEN** user disables timer in settings
- **THEN** no countdown is displayed during quiz

#### Scenario: Question auto-submits when timer expires
- **WHEN** timer reaches zero and user has not submitted answer
- **THEN** system treats question as unanswered and loads next question

### Requirement: Support touch-friendly interaction
The system SHALL ensure all interactive elements are large enough for touch interaction on tablets.

#### Scenario: Answer buttons meet minimum touch target size
- **WHEN** quiz view is rendered
- **THEN** each answer button MUST be at least 44×44 pixels

#### Scenario: Buttons have adequate spacing
- **WHEN** answer options are displayed
- **THEN** buttons MUST have at least 8 pixels spacing between them

### Requirement: Track answer in practice session
The system SHALL record each answer with question details, user response, correctness, and timestamp.

#### Scenario: Correct answer recorded
- **WHEN** user submits correct answer
- **THEN** system SHALL save record with question, userAnswer, isCorrect=true, and timestamp

#### Scenario: Incorrect answer recorded
- **WHEN** user submits incorrect answer
- **THEN** system SHALL save record with question, userAnswer, isCorrect=false, and timestamp
