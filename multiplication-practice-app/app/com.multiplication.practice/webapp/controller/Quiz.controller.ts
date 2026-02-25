import BaseController from "./BaseController";
import MessageToast from "sap/m/MessageToast";
import Dialog from "sap/m/Dialog";
import Text from "sap/m/Text";
import Button from "sap/m/Button";
import HBox from "sap/m/HBox";
import { Button$PressEvent } from "sap/m/Button";

/**
 * @namespace com.multiplication.practice.controller
 */
export default class Quiz extends BaseController {
	private currentQuestion: any;
	private currentSessionId: string | null = null;
	private userId: string = "e8c8e6f0-1234-5678-9abc-def012345678"; // Emma's ID

	public onInit(): void {
		// Load initial question
		this.loadQuestion();
	}

	public async loadQuestion(): Promise<void> {
		const difficulty = this.getDifficulty();
		
		try {
			// Call generateQuestion action
			const response = await fetch(`/odata/v4/quiz/generateQuestion(difficulty='${difficulty}')`);
			const data = await response.json();
			
			this.currentQuestion = data;
			
			// Update UI
			const questionText = this.byId("questionText") as Text;
			questionText.setText(`${data.operand1} × ${data.operand2} = ?`);
			
			// Update answer buttons
			const buttons = [
				this.byId("answer1") as Button,
				this.byId("answer2") as Button,
				this.byId("answer3") as Button,
				this.byId("answer4") as Button
			];
			
			data.options.forEach((option: number, index: number) => {
				buttons[index].setText(option.toString());
				buttons[index].setEnabled(true);
				buttons[index].removeStyleClass("correct-answer");
				buttons[index].removeStyleClass("incorrect-answer");
			});
		} catch (error) {
			MessageToast.show("Failed to load question");
		}
	}

	public async onAnswerSelected(event: Button$PressEvent): Promise<void> {
		const button = event.getSource() as Button;
		const userAnswer = parseInt(button.getText());
		
		// Disable all buttons
		const buttons = [
			this.byId("answer1") as Button,
			this.byId("answer2") as Button,
			this.byId("answer3") as Button,
			this.byId("answer4") as Button
		];
		buttons.forEach(btn => btn.setEnabled(false));
		
		// Start session if needed
		if (!this.currentSessionId) {
			await this.startSession();
		}
		
		try {
			// Submit answer
			const response = await fetch(`/odata/v4/quiz/submitAnswer`, {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({
					sessionId: this.currentSessionId,
					operand1: this.currentQuestion.operand1,
					operand2: this.currentQuestion.operand2,
					userAnswer: userAnswer
				})
			});
			
			const result = await response.json();
			
			// Show feedback
			if (result.isCorrect) {
				button.addStyleClass("correct-answer");
				MessageToast.show(`Great job! +${result.pointsEarned} points`);
			} else {
				button.addStyleClass("incorrect-answer");
				MessageToast.show("Almost! Try again!");
			}
			
			// Update points display
			const pointsText = this.byId("pointsText") as Text;
			pointsText.setText(`${result.totalPoints} points`);
			
			// Update streak display
			const streakBox = this.byId("streakBox") as HBox;
			if (result.currentStreak >= 2) {
				streakBox.setVisible(true);
				const streakText = this.byId("streakText") as Text;
				streakText.setText(`${result.currentStreak} in a row!`);
			} else {
				streakBox.setVisible(false);
			}
			
			// Show badge celebration if earned
			if (result.newBadges && result.newBadges.length > 0) {
				this.showBadgeCelebration(result.newBadges[0]);
			}
			
			// Load next question after 2 seconds
			setTimeout(() => {
				this.loadQuestion();
			}, 2000);
			
		} catch (error) {
			MessageToast.show("Failed to submit answer");
		}
	}

	public onDifficultyChange(): void {
		// Load new question with new difficulty
		this.loadQuestion();
	}

	private getDifficulty(): string {
		const segmentedButton = this.byId("difficultySelector");
		const selectedKey = (segmentedButton as any).getSelectedKey();
		return selectedKey || "Medium";
	}

	private async startSession(): Promise<void> {
		const difficulty = this.getDifficulty();
		
		try {
			const response = await fetch(`/odata/v4/quiz/startSession`, {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({
					userId: this.userId,
					difficulty: difficulty
				})
			});
			
			const result = await response.json();
			this.currentSessionId = result.sessionId;
		} catch (error) {
			MessageToast.show("Failed to start session");
		}
	}

	private showBadgeCelebration(badgeName: string): void {
		const dialog = new Dialog({
			title: "🎉 Badge Unlocked!",
			content: [
				new Text({ text: `You earned: ${badgeName}!` }).addStyleClass("celebrationText")
			],
			beginButton: new Button({
				text: "Awesome!",
				press: () => dialog.close()
			}),
			afterClose: () => dialog.destroy()
		}).addStyleClass("celebrationDialog");
		
		dialog.open();
	}

	public onNavigateToQuiz(): void {
		const navContainer = this.getView()?.getParent()?.getParent() as any;
		navContainer.to(this.byId("quizPage"));
	}

	public onNavigateToDashboard(): void {
		const app = this.getOwnerComponent()?.getRootControl() as any;
		const navContainer = app.byId("navContainer");
		const dashboardPage = sap.ui.getCore().byId("__xmlview1--dashboardPage");
		if (dashboardPage) {
			navContainer.to(dashboardPage);
		}
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
