import BaseController from "./BaseController";
import Text from "sap/m/Text";
import Dialog from "sap/m/Dialog";
import Button from "sap/m/Button";
import Input from "sap/m/Input";
import FlexBox from "sap/m/FlexBox";
import VBox from "sap/m/VBox";
import MessageToast from "sap/m/MessageToast";

/**
 * @namespace com.multiplication.practice.controller
 */
export default class Profile extends BaseController {
	private userId: string = "e8c8e6f0-1234-5678-9abc-def012345678"; // Emma's ID

	public onInit(): void {
		this.loadProfileData();
	}

	public async loadProfileData(): Promise<void> {
		try {
			// Get user data
			const userResponse = await fetch(`/odata/v4/quiz/Users('${this.userId}')`);
			const user = await userResponse.json();
			
			// Get all answers for statistics
			const answersResponse = await fetch(`/odata/v4/quiz/Answers?$filter=session/user_ID eq ${this.userId}`);
			const answersData = await answersResponse.json();
			const answers = answersData.value || [];
			
			const totalQuestions = answers.length;
			const correctAnswers = answers.filter((a: any) => a.isCorrect).length;
			const accuracy = totalQuestions > 0 ? ((correctAnswers / totalQuestions) * 100).toFixed(1) : "0.0";
			
			// Update UI
			(this.byId("avatarDisplay") as Text).setText(user.avatar);
			(this.byId("avatarText") as Text).setText(user.avatar);
			(this.byId("nameDisplay") as Text).setText(user.name);
			(this.byId("profilePoints") as Text).setText(user.totalPoints.toString());
			(this.byId("profileQuestions") as Text).setText(totalQuestions.toString());
			(this.byId("profileAccuracy") as Text).setText(`${accuracy}%`);
			(this.byId("profileCurrentStreak") as Text).setText(user.currentStreak.toString());
			(this.byId("profileBestStreak") as Text).setText(user.bestStreak.toString());
			
			// Format member since date
			const memberSince = new Date(user.createdAt).toLocaleDateString('en-US', { 
				year: 'numeric', 
				month: 'long', 
				day: 'numeric' 
			});
			(this.byId("profileMemberSince") as Text).setText(memberSince);
			
			// Load badges
			await this.loadProfileBadges();
			
		} catch (error) {
			console.error("Failed to load profile data:", error);
		}
	}

	private async loadProfileBadges(): Promise<void> {
		try {
			// Get all badges
			const badgesResponse = await fetch(`/odata/v4/quiz/Badges`);
			const badgesData = await badgesResponse.json();
			const badges = badgesData.value || [];
			
			// Get user's achievements
			const achievementsResponse = await fetch(`/odata/v4/quiz/BadgeAchievements?$filter=user_ID eq ${this.userId}`);
			const achievementsData = await achievementsResponse.json();
			const achievements = achievementsData.value || [];
			const earnedBadgeIds = achievements.map((a: any) => a.badge_id);
			
			// Get answers for progress
			const answersResponse = await fetch(`/odata/v4/quiz/Answers?$filter=session/user_ID eq ${this.userId}`);
			const answersData = await answersResponse.json();
			const answers = answersData.value || [];
			
			const badgesContainer = this.byId("profileBadgesContainer") as FlexBox;
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
							text: badge.description
						}).addStyleClass("badgeDescription"),
						new Text({ 
							text: isEarned ? "✓ Earned" : progress
						}).addStyleClass(isEarned ? "badgeEarned" : "badgeProgress")
					]
				}).addStyleClass("badgeCard");
				
				badgesContainer.addItem(badgeBox);
			}
			
		} catch (error) {
			console.error("Failed to load profile badges:", error);
		}
	}

	private calculateBadgeProgress(badge: any, answers: any[], isEarned: boolean): string {
		if (isEarned) return "Earned!";
		
		const totalAnswered = answers.length;
		const totalCorrect = answers.filter((a: any) => a.isCorrect).length;
		
		switch (badge.requirementType) {
			case 'problems_completed':
				const pct1 = Math.min(100, Math.floor((totalAnswered / badge.requirementValue) * 100));
				return `${pct1}% (${totalAnswered}/${badge.requirementValue})`;
			case 'problems_correct':
				const pct2 = Math.min(100, Math.floor((totalCorrect / badge.requirementValue) * 100));
				return `${pct2}% (${totalCorrect}/${badge.requirementValue})`;
			case 'streak':
				return `Need ${badge.requirementValue} in a row`;
			case 'tables_mastery':
				return "Practice all tables 1-10";
			default:
				return "";
		}
	}

	public onAvatarPress(): void {
		const avatars = ["🦄", "🐶", "🐱", "🦊", "🐻", "🐼", "🦁", "🐸"];
		
		const dialog = new Dialog({
			title: "Choose Your Avatar",
			content: [
				new FlexBox({
					wrap: "Wrap",
					justifyContent: "Center",
					items: avatars.map(avatar => 
						new Button({
							text: avatar,
							press: () => {
								this.updateAvatar(avatar);
								dialog.close();
							}
						}).addStyleClass("avatarOption")
					)
				})
			],
			endButton: new Button({
				text: "Cancel",
				press: () => dialog.close()
			}),
			afterClose: () => dialog.destroy()
		});
		
		dialog.open();
	}

	private async updateAvatar(avatar: string): Promise<void> {
		try {
			await fetch(`/odata/v4/quiz/Users('${this.userId}')`, {
				method: 'PATCH',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ avatar })
			});
			
			(this.byId("avatarDisplay") as Text).setText(avatar);
			(this.byId("avatarText") as Text).setText(avatar);
			MessageToast.show("Avatar updated!");
			
		} catch (error) {
			MessageToast.show("Failed to update avatar");
		}
	}

	public onNamePress(): void {
		const currentName = (this.byId("nameDisplay") as Text).getText();
		
		const input = new Input({
			value: currentName,
			placeholder: "Enter your name"
		});
		
		const dialog = new Dialog({
			title: "Edit Name",
			content: [input],
			beginButton: new Button({
				text: "Save",
				press: async () => {
					const newName = input.getValue();
					if (newName) {
						await this.updateName(newName);
						dialog.close();
					}
				}
			}),
			endButton: new Button({
				text: "Cancel",
				press: () => dialog.close()
			}),
			afterClose: () => dialog.destroy()
		});
		
		dialog.open();
	}

	private async updateName(name: string): Promise<void> {
		try {
			await fetch(`/odata/v4/quiz/Users('${this.userId}')`, {
				method: 'PATCH',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ name })
			});
			
			(this.byId("nameDisplay") as Text).setText(name);
			MessageToast.show("Name updated!");
			
		} catch (error) {
			MessageToast.show("Failed to update name");
		}
	}

	public async onSettingChange(): Promise<void> {
		// Settings are stored locally in browser for now
		// Could be extended to save to backend if needed
		MessageToast.show("Setting saved!");
	}

	public onNavigateToQuiz(): void {
		const navContainer = sap.ui.getCore().byId("app--navContainer") as any;
		const quizPage = sap.ui.getCore().byId("quizView--quizPage");
		if (navContainer && quizPage) {
			navContainer.to(quizPage);
		}
	}

	public onNavigateToDashboard(): void {
		const navContainer = sap.ui.getCore().byId("app--navContainer") as any;
		const dashboardPage = sap.ui.getCore().byId("dashboardView--dashboardPage");
		if (navContainer && dashboardPage) {
			navContainer.to(dashboardPage);
		}
	}

	public onNavigateToProfile(): void {
		// Already on profile
		this.loadProfileData(); // Refresh data
	}
}
