import BaseController from "./BaseController";

/**
 * @namespace com.multiplication.practice.controller
 */
export default class App extends BaseController {
	public onInit(): void {
		// Initialize navigation container with Quiz view
		const navContainer = this.byId("navContainer") as any;
		
		// Create and add Quiz view
		sap.ui.require(["sap/ui/core/mvc/XMLView"], (XMLView: any) => {
			XMLView.create({
				id: "quizView",
				viewName: "com.multiplication.practice.view.Quiz"
			}).then((quizView: any) => {
				const quizPage = quizView.byId("quizPage");
				navContainer.addPage(quizPage);
				navContainer.to(quizPage);
			});
			
			// Create and add Dashboard view
			XMLView.create({
				id: "dashboardView",
				viewName: "com.multiplication.practice.view.Dashboard"
			}).then((dashboardView: any) => {
				const dashboardPage = dashboardView.byId("dashboardPage");
				navContainer.addPage(dashboardPage);
			});
			
			// Create and add Profile view
			XMLView.create({
				id: "profileView",
				viewName: "com.multiplication.practice.view.Profile"
			}).then((profileView: any) => {
				const profilePage = profileView.byId("profilePage");
				navContainer.addPage(profilePage);
			});
		});
	}
}
