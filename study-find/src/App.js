import logo from "./logo.svg";
import "./App.css";
import axios from 'axios';
import { Button, Tab, Tabs } from "react-bootstrap";
import Modal from "react-bootstrap/Modal";
import { useEffect, useState } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
    faUser,
    faEnvelope,
    faBuilding,
    faExternalLinkAlt,
} from "@fortawesome/free-solid-svg-icons";

function App() {
    let [isOpen, setIsOpen] = useState(false);
    let [searchResearcherName, setSearchResearcherName] = useState(String);
    let [researcherList, setResearcherList] = useState({ 
        name: "", 
        organization: "", 
        topics: [], 
        studies: []
    });

    const openModal = () => {
        setIsOpen(true);
    };

    const closeModal = () => {
        setIsOpen(false);
    };

    const learnMore = (url) => {
        window.open(url, "_blank");
    };

    const handleSubmit = (event) => {
        event.preventDefault()
        fetchData()
        openModal()
    }
    
    const fetchData = () => {
        var myParams = {
            'id': searchResearcherName
        }

        axios.post('http://localhost:8080/add', myParams)
            .then(function(response){
                console.log(response.data);
                setResearcherList(prevState => ({
                    name: response.data.name,
                    organization: response.data.organization,
                    topics: response.data.topics,
                    studies: response.data.studies
                }))
        })
        .catch(function(error){
            console.log(error);


        });
    };

    return (
        <div className="App">
            <Modal
                show={isOpen}
                onHide={closeModal}
                animation={true}
                backdropClassName={"modal-backdrop"}
                centered={true}
                size={"lg"}
                dialogClassName={"modal-style"}>
                <Modal.Header closeButton></Modal.Header>
                <Modal.Body>
                    <Tabs defaultActiveKey="researcher" className="tabs">
                        <div>
                            <div>
                                Researcher Name: {researcherList.name}
                            </div>
                            
                            <div>Organization: {researcherList.organization}</div>
                            <div>Topics: {researcherList.topics.map((topic, ind) => (
                                <div>
                                    {topic}
                                </div>
                            ))}
                            </div>
                            <div>Studies: {researcherList.studies.map((study, ind) => (
                                <ul>
                                    {console.log(study)}
                                    <li>
                                        Title: <u>{study.title}</u>{" "}
                                        Publication Date: {study["publication date"]}
                                        PDF link: {study["pdf link"]}
                                        Description: {study.description}
                                    </li>
                                </ul>
                            ))}
                            </div>
                        </div>
                        <Tab
                            eventKey="researcher"
                            title="About the Researcher"
                            tabClassName="tab">
                            <div class="tab-cont">
                                <div class="researcher-contact">
                                    <h3>About the Researcher</h3>
                                    <p>
                                        <FontAwesomeIcon icon={faUser} />{" "}
                                        {researcherList.name}
                                        <br />
                                        <FontAwesomeIcon
                                            icon={faBuilding}
                                        />{" "}
                                        {researcherList.organization}
                                    </p>
                                </div>
                                <div class="content">
                                    <p>Recent Studies From This Researcher:</p>
                                    {researcherList.studies.map((study, ind) => (
                                        <ul>
                                            <li>
                                                Title: <u>{study.title}</u>{" "}
                                            </li>
                                            <li>
                                                Publication Date: {study["publication date"]}
                                            </li>
                                            <li>
                                                PDF link: {study["pdf link"]}
                                            </li>
                                            <li>
                                                Description: {study.description}
                                            </li>
                                        </ul>
                                    ))}
                                </div>
                                <div class="content">
                                    <p>
                                        Common Topics Studied by This
                                        Researcher:
                                    </p>
                                    {researcherList.topics.map((topic, ind) => (
                                        <div>
                                            {topic}
                                        </div>
                                    ))}
                                </div>
                            </div>
                        </Tab>
                    </Tabs>
                </Modal.Body>
                <Modal.Footer>
                    <Button variant="primary" onClick={closeModal}>
                        Close
                    </Button>
                </Modal.Footer>
            </Modal>
            <form onSubmit={handleSubmit}>
                <label>
                    Enter name: 
                </label>
                <input type="text" value={searchResearcherName} onChange={e => setSearchResearcherName(e.target.value)}/>
                <input type="submit" class="button" styyle={{ height: "100%" }}/>
            </form>
        </div>
    );
}

export default App;
