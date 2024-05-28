// Copyright (c) 2024, neha and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Library Transaction", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on('Library Transaction', {

        has_fine: function(frm){
          add_create_fine_button(frm);
    },

    date:function(frm) {
      frm.call("check_fine_status").then(r => {
        frm.set_value("has_fine", r.message)
        frm.refresh_fields()
      })
      add_create_fine_button(frm)
    }


});

function add_create_fine_button(frm) {
  if (frm.doc.has_fine){
     frm.add_custom_button('Create Fine', () => {
        frappe.new_doc('Library Fine', {
            library_transaction: frm.doc.name
        })
    })
  }
  else {
    frm.remove_custom_button('Create Fine')
  }
}
