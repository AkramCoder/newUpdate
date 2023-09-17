import React, { useEffect, useState } from "react"
import { Viewer, Worker, PdfJs } from "@react-pdf-viewer/core"
import { defaultLayoutPlugin } from "@react-pdf-viewer/default-layout"

import "@react-pdf-viewer/core/lib/styles/index.css"
import "@react-pdf-viewer/default-layout/lib/styles/index.css"

import TextSelectionListener from "../pages/update/TextSelectionListener"
import { pdfjs } from "react-pdf"
import { API_URL } from "../constants"
import axios from "axios"

const PDFViewer = () => {
// Create new plugin instance
const defaultLayoutPluginInstance = defaultLayoutPlugin();
  
// for onchange event
const [pdfFile, setPdfFile]=useState(null);
const [pdfFileError, setPdfFileError]=useState('');

// for submit event
const [viewPdf, setViewPdf]=useState(null);
const [text, setText] = useState("");

// onchange event
const fileType=['application/pdf'];
const handlePdfFileChange=(e)=>{
  let selectedFile=e.target.files[0];
  if(selectedFile){
    if(selectedFile&&fileType.includes(selectedFile.type)){
      let reader = new FileReader();
          reader.readAsDataURL(selectedFile);
          reader.onloadend = (e) =>{
            setPdfFile(e.target.result);
            setPdfFileError('');
          }
    }
    else{
      setPdfFile(null);
      setPdfFileError('Please select valid pdf file');
    }
  }
  else{
    console.log('select your file');
  }
}

// form submit
const handlePdfFileSubmit=(e)=>{
  e.preventDefault();
  if(pdfFile!==null){
    setViewPdf(pdfFile);
  }
  else{
    setViewPdf(null);
  }
}

const getData = async (text) => {
  await axios({
    method: 'POST',
    url: `${API_URL}user/process-text/`, 
    data: {input_text: text},
    headers: {
      'Content-Type': 'application/json'
    },
  }).then(response => {
      console.log(response)
  }).catch(error => {
      console.log(error)
  })
} 

const extractTextFromPdf = async () => {
  if (viewPdf) {
    // Initialize the PDFJS worker
    pdfjs.GlobalWorkerOptions.workerSrc =
      `https://cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.min.js`;

    try {
      // Load the PDF
      const loadingTask = pdfjs.getDocument(viewPdf);
      const pdfDocument = await loadingTask.promise;

      let extractedText = "";

      // Extract text from each page
      for (let i = 1; i <= pdfDocument.numPages; i++) {
        const page = await pdfDocument.getPage(i);
        const textContent = await page.getTextContent();
        textContent.items.forEach((item) => {
          extractedText += item.str + " ";
        });
      }

      // Set the extracted text
      setText(extractedText);
      getData(extractedText)
    } catch (error) {
      console.error("Error extracting text from PDF:", error);
    }
  }
};
useEffect(() => {
  extractTextFromPdf()
}, [viewPdf])


return (
  <div className='container'>

  <br></br>
  
    <form className='form-group' onSubmit={handlePdfFileSubmit}>
      <input type="file" className='form-control'
        required onChange={handlePdfFileChange}
      />
      {pdfFileError&&<div className='error-msg'>{pdfFileError}</div>}
      <br></br>
      <button type="submit" className='btn btn-success btn-lg'>
        UPLOAD
      </button>
    </form>
    <br></br>
    <h4>View PDF</h4>
    <div className='pdf-container'>
      {/* show pdf conditionally (if we have one)  */}
      {viewPdf&&<><Worker workerUrl="https://unpkg.com/pdfjs-dist@3.4.120/build/pdf.worker.min.js">
        <Viewer fileUrl={viewPdf}
          plugins={[defaultLayoutPluginInstance]} />
    </Worker></>}

    {/* if we dont have pdf or viewPdf state is null */}
    {!viewPdf&&<>No pdf file selected</>}
    </div>

    <TextSelectionListener />
  </div>
)
}

export default PDFViewer