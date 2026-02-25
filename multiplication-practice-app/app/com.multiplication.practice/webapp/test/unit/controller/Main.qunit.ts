import Main from "com/multiplication/practice/controller/Main.controller";

QUnit.module("Sample Main controller test");

QUnit.test("The Main controller class has a onRowSelectionChange method", function (assert) {
	// as a very basic test example just check the presence of the "onRowSelectionChange" method
	assert.strictEqual(typeof Main.prototype.onRowSelectionChange, "function");
});
