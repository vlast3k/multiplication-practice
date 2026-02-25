import BaseController from "./BaseController";
import Text from "sap/m/Text";
import FlexBox from "sap/m/FlexBox";
import VBox from "sap/m/VBox";
import JSONModel from "sap/ui/model/json/JSONModel";

/**
 * @namespace com.multiplication.practice.controller
 */
export default class Dashboard extends BaseController {
	private userId: string = "e8c8e6f0-1234-5678-9abc-def012345678"; // Emma's ID

	public onInit(): void {
		this.loadDashboardData();
	}

	public async loadDashboardData(): Promise<void> {
		await this.loadUserStats();
		await this.loadBadges();
		await this.loadRecentSessions();
	}

	private async loadUserStats(): Promise<void> {
		try {
			// Get user data
			const userResponse = await fetch(`/odata/v4/quiz/Users('${this.userId}')`);
			const user = await userResponse.json();
			
			// Get all answers for accuracy calculation
			const answersResponse = await fetch(`/odata/v4/quiz/Answers?$filter=session/user_ID eq ${this.userId}`);
			const answersData = await answersResponse.json();
			const answers = answersData.value || [];
			
			const totalQuestions = answers.length;
			const correctAnswers = answers.filter((a: any) => a.isCorrect).length;
			const accuracy = totalQuestions > 0 ? ((correctAnswers / totalQuestions) * 100).toFixed(1) : "0.0";
			
			// Update UI
			(this.byId("totalPointsText") as Text).setText(user.totalPoints.toString());
			(this.byId("accuracyText") as Text).setText(`${accuracy}%`);
			(this.byId("totalQuestionsText") as Text).setText(totalQuestions.toString());
			
		} catch (error) {
			console.error("Failed to load user stats:", error);
		}
	}

	private async loadBadges(): Promise<void> {
		try {
			// Get all badges
			const badgesResponse = await fetch(`/odata/v4/quiz/Badges`);
			const badgesData = await badgesResponse.json();
			const badges = badgesData.value || [];
			
			// Get user's achievements
			const achievementsResponse = await fetch(`/odata/v4/quiz/BadgeAchievements?$filter=user_ID eq ${this.userId}&$expand=badge`);
			const achievementsData = await achievementsResponse.json();
			const achievements = achievementsData.value || [];
			const earnedBadgeIds = achievements.map((a: any) => a.badge_id);
			
			// Get answers for progress calculation
			const answersResponse = await fetch(`/odata/v4/quiz/Answers?$filter=session/user_ID eq ${this.userId}`);
			const answersData = await answersResponse.json();
			const answers = answersData.value || [];
			
			const badgesContainer = this.byId("badgesContainer") as FlexBox;
			badgesContainer.removeAllItems();
			
			for (const badge of badges) {
				const isEarned = earnedBadgeIds.includes(badge.id);
				const progress = this.calculateBadgeProgress(badge, answers, isEarned);
				
				const badgeBox = new VBox({
					alignItems: "Center",
					items: [
						new Text({ 
							text: badge.icon
						}).addStyleClass(isEarned ? "badgeIconEarned" : "badgeIconLocked"),
						new Text({ 
							text: badge.name
						}).addStyleClass("badgeName"),
						new Text({ 
							text: isEarned ? "✓ Earned" : progress
						}).addStyleClass(isEarned ? "badgeEarned" : "badgeProgress")
					]
				}).addStyleClass("badgeCard");
				
				badgesContainer.addItem(badgeBox);
			}
			
		} catch (error) {
			console.error("Failed to load badges:", error);
		}
	}

	private calculateBadgeProgress(badge: any, answers: any[], isEarned: boolean): string {
		if (isEarned) return "Earned!";
		
		const totalAnswered = answers.length;
		const totalCorrect = answers.filter((a: any) => a.isCorrect).length;
		
		switch (badge.requirementType) {
			case 'problems_completed':
				return `${totalAnswered}/${badge.requirementValue}`;
			case 'problems_correct':
				return `${totalCorrect}/${badge.requirementValue}`;
			case 'streak':
				return `Reach ${badge.requirementValue} streak`;
			case 'tables_mastery':
				return "Master all tables";
			default:
				return "";
		}
	}

	private async loadRecentSessions(): Promise<void> {
		try {
			const response = await fetch(`/odata/v4/quiz/PracticeSessions?$filter=user_ID eq ${this.userId}&$orderby=startTime desc&$top=5`);
			const data = await response.json();
			const sessions = data.value || [];
			
			const sessionsList = this.byId("sessionsList") as any;
			const model = new JSONModel();
			
			const formattedSessions = sessions.map((session: any) => {
				const date = this.formatDate(session.startTime);
				const accuracy = session.totalQuestions > 0 
					? (session.correctAnswers / session.totalQuestions) * 100 
					: 0;
				const stars = this.getStarRating(accuracy);
				const questions = `${session.correctAnswers}/${session.totalQuestions} correct`;
				
				return { date, questions, stars };
			});
			
			model.setData({ sessions: formattedSessions });
			sessionsList.setModel(model);
			
		} catch (error) {
			console.error("Failed to load recent sessions:", error);
		}
	}

	private formatDate(timestamp: string): string {
		const date = new Date(timestamp);
		const now = new Date();
		const diffDays = Math.floor((now.getTime() - date.getTime()) / (1000 * 60 * 60 * 24));
		
		if (diffDays === 0) return "Today";
		if (diffDays === 1) return "Yesterday";
		if (diffDays < 7) return `${diffDays} days ago`;
		
		return date.toLocaleDateString();
	}

	private getStarRating(accuracy: number): string {
		if (accuracy >= 90) return "⭐⭐⭐";
		if (accuracy >= 70) return "⭐⭐";
		return "⭐";
	}

	public onNavigateToQuiz(): void {
		const app = this.getOwnerComponent()?.getRootControl() as any;
		const navContainer = app.byId("navContainer");
		const quizPage = sap.ui.getCore().byId("__xmlview0--quizPage");
		if (quizPage) {
			navContainer.to(quizPage);
		}
	}

	public onNavigateToDashboard(): void {
		// Already on dashboard
		this.loadDashboardData(); // Refresh data
	}

	public onNavigateToProfile(): void {
		const app = this.getOwnerComponent()?.getRootControl() as any;
		const navContainer = app.byId("navContainer");
		const profilePage = sap.ui.getCore().byId("__xmlview2--profilePage");
		if (profilePage) {
			navContainer.to(profilePage);
		}
	}
}
