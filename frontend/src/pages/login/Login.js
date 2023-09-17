import React, { useContext } from 'react'
import AuthContext from '../../context/AuthContext'
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import { useNavigate } from 'react-router-dom';

import "./login.css";

const Login = () => {
    let { loginUser, user } = useContext(AuthContext)

    const navigate = useNavigate()
    if(user) {
        navigate('/')
        return
    }
    return (
        <div className="loginbg">
            <form onSubmit={loginUser}>
                <Container style={{ backgroundColor: "lightblue", marginTop: 50, maxWidth:500, padding:20}}>
                    <Row>
                        <Col md={{ span: 6, offset: 3 }}>
                        <div className="mb-3">
                            <label>Email address</label>
                            <input
                                type="email"
                                name="email"
                                className="form-control"
                                placeholder="Enter email"
                            />
                            </div>
                        </Col>
                    </Row>
                    <Row>
                        <Col md={{ span: 6, offset: 3 }}>
                        <div className="mb-3">
                            <label>Password</label>
                            <input
                                type="password"
                                name="password"
                                className="form-control"
                                placeholder="Enter password"
                            />
                        </div>
                        <button type="submit" className="btn btn-primary">
                            Submit
                            </button>
                        </Col>

                    </Row>
                </Container>
            </form>
        </div>
    )
}

export default Login