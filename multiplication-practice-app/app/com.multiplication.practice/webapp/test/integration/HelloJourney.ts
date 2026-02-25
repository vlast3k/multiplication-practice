import opaTest from "sap/ui/test/opaQunit";
import MainPage from "./pages/MainPage";

const onTheMainPage = new MainPage();

QUnit.module("Sample Data Journey");

opaTest("Should display the data table", function () {
	// Arrangements
	onTheMainPage.iStartMyUIComponent({
		componentConfig: {
			name: "com.multiplication.practice"
		}
	});

	// Assertions
	onTheMainPage.iShouldSeeTheDataTable();
	onTheMainPage.iShouldSeeTheDetailForm();
	onTheMainPage.iShouldSeeTableWithCorrectColumns();

	// Cleanup
	onTheMainPage.iTeardownMyApp();
});

opaTest("Should select table row and populate detail form", function () {
	// Arrangements
	onTheMainPage.iStartMyUIComponent({
		componentConfig: {
			name: "com.multiplication.practice"
		}
	});

	// Actions
	onTheMainPage.iSelectFirstTableRow();

	// Assertions
	onTheMainPage.iShouldSeeTheDetailForm();

	// Cleanup
	onTheMainPage.iTeardownMyApp();
});
