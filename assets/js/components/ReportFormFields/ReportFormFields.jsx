import React, { useState } from "react";
import "./ReportFormFields.css"
import axios from 'axios'


function ReportFormFields({current}) {
    const [ReportInfo,setReportInfo]=useState({})

    const submit = (e) => {
        e.preventDefault();

        axios
            // .post("http://localhost:8000/api/reports/", (ReportInfo))
            .post("/api/reports/", (ReportInfo))
            .then((res => console.log(res)))

        console.log(ReportInfo)
        
    }

    return(
        <form class="align-items-center container mt-2 " onSubmit={submit}>
            <h4>{current}</h4>
            {current== "Information" ? 
            <>
                
                <div class = "form-row">  
                    <div class = "col-md-6 form-group">  
                        <label for = "subject_property"> Subject Property </label>  
                        <input type = "text" class = "form-control" id = "subject_property" placeholder = "Subject Property"
                            onChange={(e)=>setReportInfo({...ReportInfo,subject_property : e.target.value})}
                            value={ReportInfo.subject_property}/>  
                        <div class = "invalid-feedback">  
                            Valid first name is required.  
                        </div>  
                    </div>
                    {/* <div class = "col-md-6 form-group">  
                        <label for = "lastname"> Last Name </label>  
                        <input type = "text" class = "form-control" id = "lastname" placeholder = "Last Name"
                            onChange={(e)=>setReportInfo({...ReportInfo,lastname : e.target.value})}
                            value={ReportInfo.lastname}/>  
                        <div class = "invalid-feedback">  
                             Valid last name is required.  
                        </div>  
                    </div>   */}
                </div>  
                <div class = "form-row">  

                    <div class = "col-md-6 form-group">  
                        <label for = "report_date"> report date  </label>  
                        <input type = "date" class = "form-control" id = "report_date"
                            onChange={(e)=>setReportInfo({...ReportInfo,report_date : e.target.value})} />  
                    </div>
                    <div class = "col-md-6 form-group">  
                        <label for = "effective_date"> effective date</label>  
                        <input type = "date" class = "form-control" id = "effective_date" placeholder = "effective date"
                            onChange={(e)=>setReportInfo({...ReportInfo,effective_date : e.target.value})}/>  
                    </div>  
                </div>
                <div class = "form-row">  
                    <div class = "col-md-6 form-group">  
                        <label for = "client_name"> client name</label>  
                        <input type = "text" class = "form-control" id = "client_name" placeholder = "client name"
                            onChange={(e)=>setReportInfo({...ReportInfo,client_name : e.target.value})}
                            value={ReportInfo.client_name}/>  
                    </div>
                    <div class = "col-md-6 form-group">  
                        <label for = "file_no"> ref code</label>  
                        <input type = "text" class = "form-control" id = "file_no" placeholder = "File No."
                            onChange={(e)=>setReportInfo({...ReportInfo,file_no : e.target.value})}
                            value={ReportInfo.file_no}/>  

                    </div>  
                </div>    
                {/* <div class = "form-row">  
                    <div class = "col-md-6 form-group">  
                        <label for = "email"> email</label>  
                        <input type = "email" class = "form-control" id = "email" placeholder = "email"
                            onChange={(e)=>setReportInfo({...ReportInfo,email : e.target.value})}
                            value={ReportInfo.email}/>  
                    </div>
                    <div class = "col-md-6 form-group">  
                        <label for = "phone_number"> Phone number</label>  
                        <input type = "text" class = "form-control" id = "phone_number" placeholder = "phone number"
                            onChange={(e)=>setReportInfo({...ReportInfo,phone_number: e.target.value})}
                            value={ReportInfo.phone_number}/>  

                    </div>  
                </div> */}
            </>                  
                :<></>
            }
            {
            current == "Location" ?
            <>
                {/* <div class = "form-row">  
                    <div class = "col-md-6 form-group">  
                        <label for = "location"> location</label>  
                        <textarea type = "textarea" class = "form-control" id = "location" placeholder = "location" rows = "4"
                            onChange={(e)=>setReportInfo({...ReportInfo,location : e.target.value})}
                            value={ReportInfo.location}/>  
                    </div>
                
                    <div class = "col-md-6 form-group">  
                        <label for = "municipal_address"> Municipal Address</label>  
                        <input type = "text" class = "form-control" id = "municipal_address" placeholder = "municipal address"
                            onChange={(e)=>setReportInfo({...ReportInfo,minicipal_address : e.target.value})}
                            value={ReportInfo.minicipal_address}/>
                        <label for = "site_area"> Site Area</label> 
                        <input type = "number" class = "form-control" id = "site_area" placeholder = "Site Area(Sqr. Ft.)"
                            onChange={(e)=>setReportInfo({...ReportInfo,site_area : e.target.value})}
                            value={ReportInfo.site_area}/>  

                    </div>  
                </div>     
                <div class = "form-row">  
                    <div class = "col-md-6 form-group">  
                        <label for = "latitude"> Latitude</label>  
                        <input type = "number" class = "form-control" id = "latitude" placeholder = "Latitude"
                            onChange={(e)=>setReportInfo({...ReportInfo,latitude: e.target.value})}
                            value={ReportInfo.latitude}/>  
                    </div>
                    <div class = "col-md-6 form-group">  
                        <label for = "longitude"> Longitude</label>  
                        <input type = "number" class = "form-control" id = "longitude" placeholder = "Longitude"
                            onChange={(e)=>setReportInfo({...ReportInfo,longitude : e.target.value})}
                            value={ReportInfo.longitude}/>  

                    </div>  
                </div> */}
                <button class = "btn btn-primary bt-lg btn-block mb-3" type = "submit"> Create Report </button>
                </>
                :<></>
            }
            
        </form>
        
    )
}
export default ReportFormFields;