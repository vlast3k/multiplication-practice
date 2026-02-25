## Context

Building a child-friendly multiplication practice application using SAP BTP technologies (CAP + UI5). Target users are elementary school children (grades 1-3) who need engaging, self-directed math practice. The application must work locally during development with mock data, use standard SAP patterns, and prioritize simplicity and fun over complexity.

Current state: New greenfield project with no existing infrastructure.

Constraints:
- Local execution only (no BTP deployment in development phase)
- No external integrations or authentication
- Must use CAP backend with UI5 frontend
- Child-safe, ad-free interface
- Touch-friendly for tablet use

## Goals / Non-Goals

**Goals:**
- Create engaging multiplication quiz with immediate feedback
- Implement gamification (points, badges, streaks) to motivate practice
- Build progress tracking dashboard with visual stats
- Design child-friendly UI with large buttons and colorful animations
- Ensure all data persists across sessions (local SQLite database)
- Support multiple difficulty levels (tables 1-5, 1-10, 1-12)

**Non-Goals:**
- BTP deployment or cloud configuration (development phase only)
- Authentication or multi-user security
- Integration with external systems (school APIs, parent notifications)
- Mobile native apps (web-only for MVP)
- Other math operations beyond multiplication
- Social features or multiplayer modes

## Decisions

### 1. Architecture: CAP Backend + Custom UI5 Frontend

**Decision:** Use CAP for backend services with custom UI5 application (not Fiori Elements).

**Rationale:**
- CAP provides standard OData services with minimal boilerplate
- Custom UI5 gives full control over child-friendly interface design
- Fiori Elements too rigid for gamification animations and custom interactions
- Allows precise control over button sizes, colors, and feedback animations

**Alternatives Considered:**
- Fiori Elements: Rejected due to limited customization for child-specific UX
- Pure JavaScript frontend: Rejected to stay within SAP ecosystem and use UI5 components

### 2. Data Model: Five Core Entities

**Decision:** Implement five entities: Users, PracticeSessions, Answers, Badges, BadgeAchievements.

**Entities:**
```
Users: { id, name, avatar, totalPoints, currentStreak, createdAt }
PracticeSessions: { id, userId, startTime, endTime, totalQuestions, correctAnswers, difficultyLevel }
Answers: { id, sessionId, question, userAnswer, correctAnswer, isCorrect, pointsEarned, timestamp }
Badges: { id, name, description, icon, requirement, points } (static definitions)
BadgeAchievements: { id, userId, badgeId, earnedAt }
```

**Rationale:**
- Separates session-level stats from individual answers for flexible querying
- Badge definitions stored separately from user achievements for easy expansion
- Tracks streaks and points at user level for quick access
- Minimal schema reduces complexity for local development

**Alternatives Considered:**
- Single entity for all data: Rejected due to poor normalization and query performance
- NoSQL document store: Rejected to use standard CAP/HANA patterns

### 3. Quiz Logic: Backend-Generated Questions

**Decision:** Backend generates random multiplication questions on-demand via API call.

**API:** `GET /quiz/question?difficulty=medium` returns `{ operand1, operand2, correctAnswer, options: [a, b, c, d] }`

**Rationale:**
- Centralizes question generation logic (easier to test and modify)
- Frontend stays simple (just displays and submits)
- Options array includes correct answer + 3 plausible distractors
- Difficulty parameter controls operand ranges (easy: 1-5, medium: 1-10, hard: 1-12)

**Alternatives Considered:**
- Frontend-generated questions: Rejected to avoid duplicating logic and ensure consistency
- Pre-generated question bank: Rejected as overkill for simple multiplication

### 4. Points & Badges: Server-Side Calculation

**Decision:** Backend calculates points and checks badge eligibility after each answer submission.

**Flow:**
1. Frontend submits answer: `POST /quiz/submit { sessionId, question, userAnswer }`
2. Backend validates answer, updates points, checks streak, evaluates badges
3. Returns: `{ isCorrect, pointsEarned, newBadges: [], totalPoints, currentStreak }`

**Rationale:**
- Prevents client-side tampering (integrity for child's actual progress)
- Simplifies frontend logic (just display results)
- Badge checking logic stays in one place (easier to add new badges)

**Alternatives Considered:**
- Frontend calculates points: Rejected due to lack of data integrity
- Separate badge-checking endpoint: Rejected to reduce API calls

### 5. UI Structure: Single-Page App with Three Views

**Decision:** One UI5 app with three views accessible via top navigation bar.

**Views:**
- Quiz View: Main practice interface with question, options, submit button
- Dashboard View: Progress stats, badges, accuracy chart
- Profile View: Name, avatar selection, settings

**Navigation:** Custom header bar with three buttons (Quiz, Dashboard, Profile) visible on all pages.

**Rationale:**
- Simple navigation for children (no URL manipulation needed)
- Consistent header across views (always know where you are)
- Single app reduces complexity (one manifest.json, one component.js)

**Alternatives Considered:**
- Separate apps per view: Rejected due to navigation complexity
- Routing without visible nav: Rejected (children need clear visual navigation)

### 6. Visual Feedback: CSS Animations + UI5 MessageToast

**Decision:** Use CSS animations for badge unlocks and UI5 MessageToast for answer feedback.

**Implementation:**
- Correct answer: Green border flash + "Great job!" toast + points animation
- Incorrect answer: Gentle shake + "Try again!" toast (no red/negative visuals)
- Badge earned: Full-screen celebration animation + badge icon zoom-in

**Rationale:**
- CSS animations perform well and don't require heavy libraries
- MessageToast is standard UI5 component (no custom code)
- Positive feedback only (no punishment for mistakes)

**Alternatives Considered:**
- Third-party animation library: Rejected to minimize dependencies
- No animations: Rejected (animations critical for engagement)

### 7. Mock Data Strategy: Hardcoded Initial User

**Decision:** App starts with one pre-created user ("Emma") with sample data.

**Data:**
- 1 user with 50 completed questions, 2 badges earned, 450 points
- 5 practice sessions with varying accuracy
- Badge definitions for 4 achievements

**Rationale:**
- Demonstrates progress tracking immediately (no empty state)
- Simplifies development (no user creation flow needed)
- Child can start practicing right away

**Alternatives Considered:**
- User registration flow: Deferred to post-MVP (adds complexity)
- Completely empty database: Rejected (poor first impression)

## Risks / Trade-offs

**[Risk]** Child loses interest quickly → **Mitigation:** Focus on immediate rewards (points, animations) and test with real children early in development.

**[Risk]** UI too complex for target age → **Mitigation:** Use large buttons (min 44px), high contrast colors, and extensive user testing with 7-9 year olds.

**[Risk]** Performance issues with animations on older tablets → **Mitigation:** Use CSS transforms (GPU-accelerated), test on low-end devices, provide animation disable option.

**[Risk]** Badge requirements unclear to child → **Mitigation:** Show progress bars for each badge ("8/10 problems completed for Getting Started badge").

**[Trade-off]** No authentication means no multi-user support → **Acceptable for MVP:** Single-child household use case, can add later.

**[Trade-off]** Mock data limits realism → **Acceptable for development:** Focus is on functionality and UX, real data comes with BTP deployment.

**[Trade-off]** Custom UI5 requires more code than Fiori Elements → **Worth it:** Child-friendly UX requires customization that Fiori Elements cannot provide.
