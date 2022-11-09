import React from "react";
import "./ReportFormFields.css"
function ReportFormFields({current}) {
    return(
        <form class="align-items-center container mt-2">
            {current==1 ? 
            <>
                <div class = "form-row">  
                    <div class = "col-md-6 form-group">  
                        <label for = "firstname"> First Name </label>  
                        <input type = "text" class = "form-control" id = "firstname" placeholder = "First Name"/>  
                        <div class = "invalid-feedback">  
                            Valid first name is required.  
                        </div>  
                    </div>
                    <div class = "col-md-6 form-group">  
                        <label for = "lastname"> Last Name </label>  
                        <input type = "text" class = "form-control" id = "lastname" placeholder = "Last Name"/>  
                        <div class = "invalid-feedback">  
                             Valid last name is required.  
                        </div>  
                    </div>  
                </div>  
                <div class = "form-row">  
                <div class = "col-md-6 form-group">  
                    <label for = "report_date"> report date  </label>  
                    <input type = "date" class = "form-control" id = "report_date" />  
                </div>
                <div class = "col-md-6 form-group">  
                    <label for = "effective_date"> effective date</label>  
                    <input type = "date" class = "form-control" id = "effective_date" placeholder = "Last Name"/>  
                    <div class = "invalid-feedback">  
                         Valid last name is required.  
                    </div>  
                </div>  
            </div>
                <div class = "form-row">  
                    <div class = "col-md-6 form-group">  
                        <label for = "client_name"> client name</label>  
                        <input type = "text" class = "form-control" id = "client_name" placeholder = "client name"/>  
                    </div>
                    <div class = "col-md-6 form-group">  
                        <label for = "ref_code"> ref code</label>  
                        <input type = "text" class = "form-control" id = "ref_code" placeholder = "ref code"/>  
                        <div class = "invalid-feedback">  
                             Valid last name is required.  
                        </div>  
                    </div>  
                </div>              
            </>                  
                :<></>
            }
            <div>here should be form number {current}</div>
        </form>
        
    )
}
export default ReportFormFields;