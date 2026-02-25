import BaseController from "./BaseController";
import {Table$RowSelectionChangeEvent} from "sap/ui/table/Table";

/**
 * @namespace com.multiplication.practice.controller
 */
export default class Main extends BaseController {

	onRowSelectionChange(oEvent: Table$RowSelectionChangeEvent): void {
		const selectedContext = oEvent.getParameter("rowContext");
		this.byId("detailForm").setBindingContext(selectedContext);
	}
}
