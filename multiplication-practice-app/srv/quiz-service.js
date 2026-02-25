const cds = require('@sap/cds');

module.exports = cds.service.impl(async function() {
  const { Users, PracticeSessions, Answers, Badges, BadgeAchievements } = this.entities;

  // Generate a random multiplication question based on difficulty
  this.on('generateQuestion', async (req) => {
    const { difficulty } = req.data;
    
    // Determine operand range based on difficulty
    let maxOperand = 10; // Medium (default)
    if (difficulty === 'Easy') maxOperand = 5;
    else if (difficulty === 'Hard') maxOperand = 12;
    
    // Generate two random operands
    const operand1 = Math.floor(Math.random() * maxOperand) + 1;
    const operand2 = Math.floor(Math.random() * maxOperand) + 1;
    const correctAnswer = operand1 * operand2;
    
    // Generate 3 distractor options within ±20% of correct answer
    const distractors = new Set();
    const range = Math.max(1, Math.floor(correctAnswer * 0.2));
    
    while (distractors.size < 3) {
      const offset = Math.floor(Math.random() * range * 2) - range;
      const distractor = correctAnswer + offset;
      if (distractor > 0 && distractor !== correctAnswer) {
        distractors.add(distractor);
      }
    }
    
    // Create options array with correct answer and distractors, then shuffle
    const options = [correctAnswer, ...Array.from(distractors)];
    options.sort(() => Math.random() - 0.5);
    
    return {
      operand1,
      operand2,
      correctAnswer,
      options
    };
  });

  // Submit an answer and calculate points, streaks, and badges
  this.on('submitAnswer', async (req) => {
    const { sessionId, operand1, operand2, userAnswer } = req.data;
    const correctAnswer = operand1 * operand2;
    const isCorrect = userAnswer === correctAnswer;
    
    // Get the session to find the user
    const session = await SELECT.one.from(PracticeSessions).where({ ID: sessionId });
    if (!session) {
      req.error(404, 'Session not found');
      return;
    }
    
    const userId = session.user_ID;
    const user = await SELECT.one.from(Users).where({ ID: userId });
    if (!user) {
      req.error(404, 'User not found');
      return;
    }
    
    // Calculate points
    let pointsEarned = isCorrect ? 10 : 0;
    let currentStreak = isCorrect ? user.currentStreak + 1 : 0;
    
    // Check for streak bonuses
    if (isCorrect && currentStreak === 5) {
      pointsEarned += 25; // 5 consecutive bonus
    } else if (isCorrect && currentStreak === 10) {
      pointsEarned += 50; // 10 consecutive bonus
    }
    
    // Update user points and streak
    const totalPoints = user.totalPoints + pointsEarned;
    const bestStreak = Math.max(user.bestStreak, currentStreak);
    
    await UPDATE(Users).set({
      totalPoints,
      currentStreak,
      bestStreak
    }).where({ ID: userId });
    
    // Save answer record
    await INSERT.into(Answers).entries({
      session_ID: sessionId,
      operand1,
      operand2,
      userAnswer,
      correctAnswer,
      isCorrect,
      pointsEarned,
      timestamp: new Date().toISOString()
    });
    
    // Check badge criteria
    const newBadges = await checkBadges(userId, currentStreak, totalPoints);
    
    return {
      isCorrect,
      pointsEarned,
      newBadges,
      totalPoints,
      currentStreak
    };
  });

  // Start a new practice session
  this.on('startSession', async (req) => {
    const { userId, difficulty } = req.data;
    
    // Create new session
    const session = await INSERT.into(PracticeSessions).entries({
      user_ID: userId,
      startTime: new Date().toISOString(),
      difficultyLevel: difficulty,
      totalQuestions: 0,
      correctAnswers: 0
    });
    
    return {
      sessionId: session.ID || session
    };
  });

  // End a practice session and calculate summary
  this.on('endSession', async (req) => {
    const { sessionId } = req.data;
    
    // Get all answers for this session
    const answers = await SELECT.from(Answers).where({ session_ID: sessionId });
    
    const totalQuestions = answers.length;
    const correctAnswers = answers.filter(a => a.isCorrect).length;
    const accuracy = totalQuestions > 0 ? (correctAnswers / totalQuestions) * 100 : 0;
    const pointsEarned = answers.reduce((sum, a) => sum + a.pointsEarned, 0);
    
    // Update session with end time and stats
    await UPDATE(PracticeSessions).set({
      endTime: new Date().toISOString(),
      totalQuestions,
      correctAnswers
    }).where({ ID: sessionId });
    
    return {
      totalQuestions,
      correctAnswers,
      accuracy,
      pointsEarned
    };
  });

  // Helper function to check badge criteria
  async function checkBadges(userId, currentStreak, totalPoints) {
    const newBadges = [];
    
    // Get all badges
    const badges = await SELECT.from(Badges);
    
    // Get user's existing achievements
    const achievements = await SELECT.from(BadgeAchievements).where({ user_ID: userId });
    const earnedBadgeIds = achievements.map(a => a.badge_id);
    
    // Get user's answer statistics
    const allAnswers = await SELECT.from(Answers)
      .where({ session_ID: { in: 
        SELECT.from(PracticeSessions).columns('ID').where({ user_ID: userId })
      }});
    
    const totalAnswered = allAnswers.length;
    const totalCorrect = allAnswers.filter(a => a.isCorrect).length;
    
    for (const badge of badges) {
      // Skip if already earned
      if (earnedBadgeIds.includes(badge.id)) continue;
      
      let earned = false;
      
      switch (badge.requirementType) {
        case 'problems_completed':
          // Getting Started: 10 problems
          earned = totalAnswered >= badge.requirementValue;
          break;
          
        case 'problems_correct':
          // Multiplication Master: 100 correct
          earned = totalCorrect >= badge.requirementValue;
          break;
          
        case 'streak':
          // Perfect Ten: 10 in a row
          earned = currentStreak >= badge.requirementValue;
          break;
          
        case 'tables_mastery':
          // Times Table Champion: 5+ correct for each table 1-10
          earned = await checkTablesMastery(userId);
          break;
      }
      
      if (earned) {
        await INSERT.into(BadgeAchievements).entries({
          user_ID: userId,
          badge_id: badge.id,
          earnedAt: new Date().toISOString()
        });
        newBadges.push(badge.name);
      }
    }
    
    return newBadges;
  }

  // Helper function to check if user has mastered all tables 1-10
  async function checkTablesMastery(userId) {
    const answers = await SELECT.from(Answers)
      .where({ session_ID: { in: 
        SELECT.from(PracticeSessions).columns('ID').where({ user_ID: userId })
      }});
    
    // Count correct answers for each table (1-10)
    const tableCounts = {};
    for (let i = 1; i <= 10; i++) {
      tableCounts[i] = 0;
    }
    
    for (const answer of answers) {
      if (answer.isCorrect) {
        // Check if either operand is in range 1-10
        if (answer.operand1 >= 1 && answer.operand1 <= 10) {
          tableCounts[answer.operand1]++;
        }
        if (answer.operand2 >= 1 && answer.operand2 <= 10) {
          tableCounts[answer.operand2]++;
        }
      }
    }
    
    // Check if all tables have at least 5 correct answers
    for (let i = 1; i <= 10; i++) {
      if (tableCounts[i] < 5) return false;
    }
    
    return true;
  }
});
