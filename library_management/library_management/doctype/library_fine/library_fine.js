// Copyright (c) 2024, neha and contributors
// For license information, please see license.txt

frappe.ui.form.on("Library Fine",{
  refresh(frm){
    frm.set_query('library_transaction', () => {
      return {
         filters: {
             docstatus: 0
         }
       }
    })

  },
});
