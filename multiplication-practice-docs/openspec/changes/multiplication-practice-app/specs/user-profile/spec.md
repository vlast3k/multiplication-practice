## ADDED Requirements

### Requirement: Display user name
The system SHALL display the user's name prominently in the profile view.

#### Scenario: Name displayed at top of profile
- **WHEN** user navigates to profile view
- **THEN** system SHALL display user's name in large, friendly font

#### Scenario: Name editable by user
- **WHEN** user clicks on their name
- **THEN** system SHALL allow editing name with text input field

#### Scenario: Name persists after edit
- **WHEN** user changes name and saves
- **THEN** system SHALL update name in database and display new name everywhere

### Requirement: Provide avatar selection
The system SHALL allow the user to select an avatar from a predefined set of child-friendly icons.

#### Scenario: Avatar gallery shows options
- **WHEN** user opens avatar selector
- **THEN** system SHALL display at least 8 avatar options (animals, emojis, characters)

#### Scenario: Selected avatar displayed in profile
- **WHEN** user selects an avatar
- **THEN** system SHALL display selected avatar as profile picture

#### Scenario: Avatar persists across sessions
- **WHEN** user selects avatar and closes app
- **THEN** system SHALL display same avatar when app reopens

#### Scenario: Avatar shown in navigation header
- **WHEN** user navigates any view
- **THEN** system SHALL display user's avatar in top-right corner of header

### Requirement: Display personal statistics summary
The system SHALL display a summary of the user's key statistics in the profile view.

#### Scenario: Total points displayed
- **WHEN** user views profile
- **THEN** system SHALL display total points earned

#### Scenario: Total questions answered displayed
- **WHEN** user views profile
- **THEN** system SHALL display total number of questions answered

#### Scenario: Overall accuracy displayed
- **WHEN** user views profile
- **THEN** system SHALL display overall accuracy percentage

#### Scenario: Current streak displayed
- **WHEN** user views profile
- **THEN** system SHALL display current streak count (if streak > 0)

#### Scenario: Best streak displayed
- **WHEN** user views profile
- **THEN** system SHALL display highest streak ever achieved

### Requirement: Display all badges with progress
The system SHALL display all available badges with visual indicators of earned status and progress toward locked badges.

#### Scenario: Earned badges shown in color
- **WHEN** user views profile badges section
- **THEN** earned badges SHALL display in full color with checkmark

#### Scenario: Locked badges shown with progress bar
- **WHEN** user views profile badges section
- **THEN** locked badges SHALL display progress bar (e.g., "8/10 completed")

#### Scenario: Badge descriptions visible
- **WHEN** user taps or hovers over badge
- **THEN** system SHALL display badge name and requirement description

### Requirement: Provide settings access
The system SHALL provide access to user settings from the profile view.

#### Scenario: Settings button visible
- **WHEN** user views profile
- **THEN** system SHALL display "Settings" button

#### Scenario: Timer toggle in settings
- **WHEN** user opens settings
- **THEN** system SHALL provide toggle to enable/disable quiz timer

#### Scenario: Sound effects toggle in settings
- **WHEN** user opens settings
- **THEN** system SHALL provide toggle to enable/disable sound effects

#### Scenario: Settings persist across sessions
- **WHEN** user changes settings
- **THEN** system SHALL save preferences to database and apply on next session

### Requirement: Display account creation date
The system SHALL display the date when the user's account was created.

#### Scenario: Creation date shown in profile
- **WHEN** user views profile
- **THEN** system SHALL display "Member since [date]" in friendly format

#### Scenario: Date format is child-friendly
- **WHEN** creation date is displayed
- **THEN** system SHALL use format like "January 15, 2024" (not technical format)
