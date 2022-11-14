import React ,{useState} from "react";
import "./ReportForm.css";
import ReportFormFields from "../ReportFormFields/ReportFormFields";

function ReportForm() {
    const [selected,setSelected]=useState("Information");
    const pages = [{name:"Information"},{name:"Location"}];


    return(
        <div>
        <div class="col-md-6 w-auto card px-3 py-5 d-flex justify-content-center  text-secondary">
            <h1>adding report form</h1>
            <p>
                you can add a report here
            </p>
            
            <nav aria-label="Page navigation example dark">
            <ul class="pagination justify-content-center">
                {/* <li class="page-item ">
                  <a class="page-link" href="#" tabindex="-1" aria-disabled="true">Previous</a>
                </li> */}
                {pages.map((page) => {
                    return (
                        <li 
                            className={`page-item ${(selected==page.name)?"active":""}`}
                            onClick ={()=>setSelected(page.name)} 
                        >
                            <a class="page-link" href="#">{page.name}</a>
                        </li>
                    );
                    
                })}
                {/* <li class="page-item">
                <a class="page-link" href="#">Next</a>
                </li> */}
            </ul>
            </nav>
            <ReportFormFields current={selected}/>
        </div>
        </div>
    )
}
export default ReportForm;