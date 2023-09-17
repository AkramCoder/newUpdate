import React, { useState, useEffect, useContext } from 'react';

import AuthContext from "../../context/AuthContext"
import { useNavigate, useParams } from 'react-router-dom';
import axios from 'axios';

import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';

import Navbar from "../../components/navbar/Navbar"
import Sidebar from "../../components/sidebar/Sidebar"
import CvViewer from '../../components/CvViewer';
import PDFViewer from '../../components/PDFViewer';
import "../update/update.scss";



const NewCv = () => {


    const statusOptions = [
        { value: '', text: '--Choisir une option--' },
        { value: 'treaty', text: 'Traite' },
        { value: 'untreated', text: 'Non traite' },

    ];


    let { user, authTokens, logoutUser } = useContext(AuthContext)
    let [manager, setManager] = useState([])

    let getManager = async () => {
        console.log(user.user_id)
        console.log("token in fetch", String(authTokens.access))
        let response = await fetch(`http://127.0.0.1:8000/user/managercurrent/${user.user_id}/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + String(authTokens.access)
            }
        })
        let data = await response.json()

        if (response.status === 200) {
            setManager(data)

        } else if (response.statusText === 'Unauthorized') {
            console.log(" ERROR ")
        }

    }

    const navigate = useNavigate();

    const [cv_file, setCv_file] = useState("")
    const [tags, setTags] = useState("")
    const [status, setStatus] = useState(statusOptions[1].value)
    const [candidate, setCandidate] = useState("")

    useEffect(() => {
        getManager()
    }, [])

    const cvTreated = () => {

    }


    const addCv = async () => {
        let formField = new FormData();

        formField.append('cv_file', cv_file);
        formField.append('tags', tags);
        formField.append('status', status);
        formField.append('candidate', candidate);



        await axios({
            method: 'POST',
            url: `http://127.0.0.1:8000/user/interview/`,
            data: formField,
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + String(authTokens.access)
            },
        }).then(response => {
            setCv_file("")
            setTags("")
            setStatus(statusOptions[1].value)
            
            console.log(response.data);
            alert("status", response.status)
        })
    }
    return (
        <div className="new">
            <Sidebar />
            <div className="newContainer">
                <Navbar />
                {/* <div>
                    {successMessage &&
                        <Alert className="alert" variant="success" onClose={() => setShow(false)} dismissible>
                            <Alert.Heading><h6>{successMessage}</h6></Alert.Heading>

                        </Alert>}
                </div> */}
                <div className='newtop_list'>
                    <div className="newtop right-padding">
                        <div className='newtop back' style={{'margin': '0px'}}>
                            <button onClick={cvTreated}>Marquer comme traite</button>
                        </div>
                        <div className='block'>
                            <div>Modifier</div>
                            <h2>CV</h2>
                        </div>
                        <div className='block'>
                            {/* <CvViewer/> */}
                            <PDFViewer />
                        </div>
                    </div>
                    <div className="newtop left-padding">
                        <div>
                            <h1 className="newtitle">Ajouter Poste </h1>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        // <div className="single">
        //     <Sidebar />
        //     <div className="singleContainer">
        //         <Navbar />
        //         <form >
        //             <Container>

        //                 <Row>
        //                     <h3>Ajouter CV</h3>
        //                 </Row>
        //                 <Row>
        //                 <div className="newtop">gfsgf</div>
        //                 <div className="newtop">gfsgf</div>
        //                     <Form.Group className="mb-3" controlId="exampleForm.ControlInput1">
        //                         <Form.Label>CV</Form.Label>
        //                         <Form.Control type="file" name="cv_file" size="lg"
        //                             value={cv_file}
        //                             onChange={(e) => setCv_file(e.target.value)} />
        //                     </Form.Group>
        //                 </Row> 
        //                 <Row>
        //                     <Col>
        //                         <Form.Group className="mb-3" controlId="exampleForm.ControlInput1">
        //                             <Form.Label>Tags</Form.Label>
        //                             <Form.Control type="text" name="tags"
        //                                 value={tags}
        //                                 onChange={(e) => setTags(e.target.value)} />
        //                         </Form.Group>
        //                     </Col>
        //                     <Col>
        //                         <Form.Group className="mb-3" controlId="exampleForm.ControlInput1">
        //                             <Form.Label>Candidate</Form.Label>
        //                             <Form.Control type="text" name="candidate"
        //                                 value={candidate}
        //                                 onChange={(e) => setCandidate(e.target.value)} />
        //                         </Form.Group>
        //                     </Col>
        //                     <Col>
        //                         <Form.Group className="mb-3" controlId="exampleForm.ControlInput1">
        //                             <Form.Label>Status</Form.Label>
        //                             <Form.Select value={status} name="etat" onChange={(e) => setStatus(e.target.value)}>
        //                                 {statusOptions.map(option => (
        //                                 <option key={option.value} value={option.value}>
        //                                     {option.text}
        //                                 </option>
        //                             ))}
        //                             </Form.Select>
        //                         </Form.Group>
        //                     </Col>
        //                 </Row>
                        
        //                 <Row>
        //                     <Col>
        //                         <Button variant="outline-primary" type="submit" onClick={addCv}>Ajouter</Button>
        //                     </Col>
        //                 </Row>
        //             </Container>
        //         </form>
        //     </div>
        // </div>


    )
}

export default NewCv;