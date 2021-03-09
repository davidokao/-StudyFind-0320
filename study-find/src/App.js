import logo from "./logo.svg";
import "./App.css";
import axios from "axios";
import { Accordion, Button, Card, Tab, Tabs } from "react-bootstrap";
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
        studies: [],
    });
    let [isCompact, setIsCompact] = useState(false);

    // modal events
    const openModal = () => {
        setIsOpen(true);
    };
    const closeModal = () => {
        setIsOpen(false);
    };

    // // open link in new tab
    // const learnMore = (url) => {
    //     window.open(url, "_blank");
    // };

    // web scraping methods
    const handleSubmit = (event) => {
        event.preventDefault();
        fetchData();
        openModal();
    };
    const fetchData = () => {
        var myParams = {
            id: searchResearcherName,
        };

        axios
            .post("http://localhost:8080/add", myParams)
            .then(function (response) {
                console.log(response.data);
                setResearcherList((prevState) => ({
                    name: response.data.name,
                    organization: response.data.organization,
                    topics: response.data.topics,
                    studies: response.data.studies,
                }));
            })
            .catch(function (error) {
                console.log(error);
            });
    };

    //window size handling
    const handleWindowSizeChange = () => {
        if (window.innerWidth < 992) {
            setIsCompact(true);
        } else {
            setIsCompact(false);
        }
    };
    useEffect(() => {
        window.addEventListener("resize", handleWindowSizeChange);
        return () => {
            window.removeEventListener("resize", handleWindowSizeChange);
        };
    });
    useEffect(() => {
        handleWindowSizeChange();
    }, []);

    // modal content
    let modalContent = [
        {
            title: "Full Description",
            content: (
                <div class="tab-cont">
                    <h3>Full Description</h3>
                </div>
            ),
            tabEventKey: "description",
        },
        {
            title: "Additional Criteria",
            content: (
                <div class="tab-cont">
                    <h3>Additional Criteria</h3>
                </div>
            ),
            tabEventKey: "criteria",
        },
        {
            title: "All Locations",
            content: (
                <div class="tab-cont">
                    <h3>All Locations</h3>
                    <ul>
                        <li></li>
                    </ul>
                </div>
            ),
            tabEventKey: "locations",
        },
        ...(researcherList.name === ""
            ? []
            : {
                  title: "About the Researcher",
                  content: (
                      <div class="tab-cont">
                          <div class="researcher-contact">
                              <h3>About the Researcher</h3>
                              <p>
                                  <FontAwesomeIcon icon={faUser} />{" "}
                                  {researcherList.name}
                                  <br />
                                  <FontAwesomeIcon icon={faBuilding} />{" "}
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
                                          Publication Date:{" "}
                                          {study["publication date"]}
                                      </li>
                                      <li>PDF link: {study["pdf link"]}</li>
                                      <li>Description: {study.description}</li>
                                  </ul>
                              ))}
                          </div>
                          <div class="content">
                              <p>Common Topics Studied by This Researcher:</p>
                              {researcherList.topics.map((topic, ind) => (
                                  <div>{topic}</div>
                              ))}
                          </div>
                      </div>
                  ),
                  tabEventKey: "researcher",
              }),
        {
            title: "Learn More",
            content: (
                <div class="tab-cont">
                    <a href="" target="_blank">
                        Learn more at ClinicalTrials.gov{" "}
                        <FontAwesomeIcon icon={faExternalLinkAlt} />
                    </a>
                </div>
            ),
            tabEventKey: "more",
        },
    ];

    return (
        <div className="App">
            <Modal
                show={isOpen}
                onHide={closeModal}
                animation={true}
                backdropClassName={"modal-backdrop"}
                centered={true}
                size={"lg"}
                dialogClassName={"modal-style"}
            >
                <Modal.Header closeButton></Modal.Header>
                <Modal.Body>
                    {!isCompact && (
                        <Tabs defaultActiveKey="description" className="tabs">
                            {modalContent.map((section, i) => (
                                <Tab
                                    eventKey={section.tabEventKey}
                                    title={section.title}
                                    tabClassName="tab"
                                >
                                    {section.content}
                                </Tab>
                            ))}
                        </Tabs>
                    )}
                    {isCompact && (
                        <Accordion>
                            {modalContent.map((section, i) => (
                                <Card>
                                    <Card.Header>
                                        <Accordion.Toggle
                                            as={Button}
                                            variant="link"
                                            eventKey={i + 1}
                                        >
                                            {section.title}
                                        </Accordion.Toggle>
                                    </Card.Header>
                                    <Accordion.Collapse eventKey={i + 1}>
                                        <Card.Body>{section.content}</Card.Body>
                                    </Accordion.Collapse>
                                </Card>
                            ))}
                        </Accordion>
                    )}
                </Modal.Body>
                <Modal.Footer>
                    <Button variant="primary" onClick={closeModal}>
                        Close
                    </Button>
                </Modal.Footer>
            </Modal>
            <form onSubmit={handleSubmit}>
                <label>Enter name:</label>
                <input
                    type="text"
                    value={searchResearcherName}
                    onChange={(e) => setSearchResearcherName(e.target.value)}
                />
                <input
                    type="submit"
                    class="button"
                    styyle={{ height: "100%" }}
                />
            </form>
        </div>
    );
}

export default App;
