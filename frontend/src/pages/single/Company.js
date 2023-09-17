import React, { useState, useEffect, useContext } from 'react';

import AuthContext from "../../context/AuthContext"
import Navbar from "../../components/navbar/Navbar"
import Sidebar from "../../components/sidebar/Sidebar"
import axios from 'axios';
import { Link, useParams } from 'react-router-dom';
import { API_URL } from '../../constants';
import "./single.scss";


const Company = () => {

    let { user, authTokens, logoutUser, companyID } = useContext(AuthContext)
    let [customuser, setCustomuser] = useState([])
    let [manager, setManager] = useState([])
    let [companyId, setCompanyId] = useState("")

    let [company, setCompany] = useState([]);
    let [jobs, setJobs] = useState([]);
    let [managers, setManagers] = useState([]);
    let [address, setadress] = useState([]);
    let [wilaya, setWilaya] = useState([]);
    let [commune, setCommune] = useState([]);
    

   
    let getManager = async () => {
        console.log("user", user.user_id)
        console.log("token in fetch", String(authTokens.access))
        let response = await fetch(`${API_URL}user/managercurrent/${user.user_id}/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + String(authTokens.access)
            }
        })
        let data = await response.json()
        console.log('managerData', data)
        if (response.status === 200) {
            setCustomuser(data)
            setManager(data.manager)
            setCompanyId(data.manager.company)

        } else if (response.statusText === 'Unauthorized') {
            console.log(" ERROR ")
        }

    }

    useEffect(() => {
        console.log(" company id from contexts",companyId)
        getManager()
        console.log("we will get the compan")
        fetch(`${API_URL}company/company/${companyId}`)
            .then((data) => data.json())
            .then((data) => {
                console.log("company", data)
                setCompany(data);
                setJobs(data.jobs)
                console.log("jobs", data.jobs)
                setManagers(data.managers)
                setadress(data.address)
                console.log("address", data.address)
                fetch(`${API_URL}company/get-wilaya-commune-names/${data.address.wilaya}/${data.address.commune}`)
                    .then((data) => data.json())
                    .then((data) => {
                        setWilaya(data.wilaya_name)
                        setCommune(data.commune_name)
                    })
            })
    }, [companyId])


    return (
        <div className="single">
            <Sidebar />
            <div className="singleContainer">
                <Navbar />
                <div className="top">
                    <div className="left">
                        <Link to={`/company/update/${companyId}`} style={{ textDecoration: "none" }}>
                            <div className="editButton">Modifier</div>
                        </Link>
                        <h1 className="title">{company.name}</h1>
                        <div className="item">
                            
                            <div className="details">
                                <div className="detailItem">
                                    <span className="itemKey">Type:</span>
                                    <span className="itemValue">{company.company_type}</span>
                                </div>
                                <div className="detailItem">
                                    <span className="itemKey">Niveau:</span>
                                    <span className="itemValue">{company.level}</span>
                                </div>
                                <div className="detailItem">
                                    <span className="itemKey">Site web:</span>
                                    <span className="itemValue">{company.website}</span>
                                </div>
                                <div className="detailItem">
                                    <span className="itemKey">Address:</span>
                                    <span className="itemValue">{wilaya} {commune} {address.complet_adress}</span>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div className="right">
                        <div className="details">
                           
                            <div className="detailItem">
                                <span className="itemKey">OFFRES D'EMPLOI:</span>
                                {/*<span className="itemValue">{jobs.length}</span>*/}
                            </div>
                            <div className="detailItem">
                                <span className="itemKey">MANAGERS:</span>
                                {/*<span className="itemValue">{managers.length}</span>*/}
                            </div>
                            <div className="detailItem">
                                <span className="itemKey">Candidats:</span>
                                {/*<span className="itemValue">{company.website}</span>*/}
                            </div>
                            <div className="detailItem">
                                <span className="itemKey">CVs:</span>
                                {/*<span className="itemValue"></span>*/}
                            </div>
                        </div>
                    </div>
                </div>
                <div className="bottom">
                    <h1 className="title">Modifier</h1>


                </div>
            </div>
        </div>
    )
}
export default Company;
