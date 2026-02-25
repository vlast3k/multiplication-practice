import type {SuiteConfiguration} from "sap/ui/test/starter/config";
export default {
	name: "QUnit test suite for the UI5 Application: com.multiplication.practice",
	defaults: {
		page: "ui5://test-resources/com/multiplication/practice/Test.qunit.html?testsuite={suite}&test={name}",
		qunit: {
			version: 2
		},
		sinon: {
			version: 4
		},
		ui5: {
			language: "EN",
			theme: "sap_horizon"
		},
		coverage: {
			only: ["com/multiplication/practice/"],
			never: ["test-resources/com/multiplication/practice/"]
		},
		loader: {
			paths: {
				"com/multiplication/practice": "../"
			}
		}
	},
	tests: {
		"unit/unitTests": {
			title: "Unit tests for com.multiplication.practice"
		},
		"integration/opaTests": {
			title: "Integration tests for com.multiplication.practice"
		}
	}
} satisfies SuiteConfiguration;
