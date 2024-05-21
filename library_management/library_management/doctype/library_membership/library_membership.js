// Copyright (c) 2024, neha and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Library Membership", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on('Library Membership',{
  from_date: function(frm){
    if(frm.doc.from_date &&(frm.doc.to_date  <  frm.doc.from_date)){
      frm.set_value('from_date',"")
      frappe.throw("ToDate is should be lesser than FromDate")
    }
  },
  to_date: function(frm){
    if(frm.doc.to_date &&(frm.doc.to_date < frm.doc.from_date)){
      frm.set_value('to_date',"")
      frappe.throw({
        title: __("Error Message"),
        indication: 'red',
        message: __('ToDate is should be lesser than FromDate')
          });

   }
  }
});
