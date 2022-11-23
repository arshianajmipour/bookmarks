//import React ,{useState} from "react";
//import "./ReportForm.css";
//import ReportFormFields from "../ReportFormFields/ReportFormFields";

function ReportForm() {
    const [selected,setSelected]=useState("Information");
    const pages = [{name:"Information"},{name:"Location"}];
    const Next =  ()=>{
        if(selected=="Information"){
            setSelected ("Location")
        }
    }
    const Prev = ()=>{
        if(selected=="Location"){
            setSelected("Information")
        }
    }

    return(
        <>
        <div class="col-md-6 w-auto card px-3 py-5 d-flex justify-content-center  text-secondary">
            <h1>adding report form</h1>
            <p>
                you can add a report here
            </p>
            
            <nav aria-label="Page navigation example dark">
            <ul class="pagination justify-content-center">

                <li className="page-item">
                   <button className={`page-link ${(selected=="Information")?"text-white":"text-dark"}`} onClick={Prev}> {"<"} </button>
                </li>
                {pages.map((page) => {
                    return <li className={`page-item ${(selected==page.name)?"active":""}`}
                        onClick ={()=>setSelected(page.name)} >
                        <a class="page-link" href="#">{page.name}</a>
                    </li>
                })}
                <li className="page-item">
                    <button className={`page-link ${(selected=="Location")?"text-white":"text-dark"}`} onClick={Next}> {">"} </button>
                </li>
            </ul>
            </nav>
            <ReportFormFields current={selected}/>
            
            <div className="page-item">
                <button className={`page-link text-light bg-secondary ${(selected=="Information")?"d-none":""}`}
                 onClick={Prev}> {"< Prev "} </button>
            </div>
            <div className="page-item d-flex justify-content-end">
                    <button className={`page-link text-light text-end bg-secondary ${(selected=="Location")?"d-none":""}`}
                     onClick={Next}> {" Next > "} </button>
            </div>
            
        </div>
        </>
    )
}
//export default ReportForm;

const domContainer = document.querySelector('#report-form');
const root = ReactDOM.createRoot(domContainer);
root.render(<ReportForm/>);