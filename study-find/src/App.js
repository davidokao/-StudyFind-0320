import logo from "./logo.svg";
import "./App.css";
import axios from "axios";
// import { Accordion, Card, Tab, Tabs, Button } from "react-bootstrap";
import { Accordion, Card, Button } from "react-bootstrap";
import Modal from "react-bootstrap/Modal";
import { useEffect, useState } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
    faUser,
    faEnvelope,
    faBuilding,
    faExternalLinkAlt,
} from "@fortawesome/free-solid-svg-icons";
import Placeholder from "./assets/Placeholder.png";
import {
    ChakraProvider,
    ThemeProvider,
    theme,
    UnorderedList,
    ListItem,
    Tabs,
    TabList,
    TabPanel,
    Tab,
    TabPanels,
} from "@chakra-ui/react";

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
    // const placeholderImage = require("./assets/Placeholder.png");

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

    const submitSearch = (topic) => {
        return true;
    };

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
                    <UnorderedList>
                        <ListItem></ListItem>
                    </UnorderedList>
                </div>
            ),
            tabEventKey: "locations",
        },
        researcherList.name === ""
            ? []
            : {
                  title: "About the Researcher",
                  content: (
                      <div class="tab-cont">
                          {!isCompact && (
                              <img src={Placeholder} className="float-right" />
                          )}
                          <h3>About the Researcher</h3>
                          <div class="researcher-contact tab-section">
                              <p>
                                  <FontAwesomeIcon icon={faUser} />{" "}
                                  {researcherList.name}
                                  <br />
                                  <FontAwesomeIcon icon={faBuilding} />{" "}
                                  {researcherList.organization}
                              </p>
                          </div>
                          {isCompact && (
                              <img src={Placeholder} className="center-img" />
                          )}
                          <div class="content tab-section">
                              <h4>Recent Studies From This Researcher:</h4>
                              {researcherList.studies.map((study, ind) => (
                                  <div className="bottom-padding">
                                      <u>
                                          <a
                                              href={study["pdf link"]}
                                              target="_blank"
                                          >
                                              {study.title}
                                          </a>
                                      </u>
                                      <p className="insert-indent">
                                          <strong>Publication Date:</strong>{" "}
                                          {study["publication date"]}
                                      </p>
                                      <p className="insert-indent">
                                          <strong>Description:</strong>{" "}
                                          {study.description}
                                      </p>
                                  </div>
                              ))}
                          </div>
                          <div class="content tab-section">
                              <h4>Common Topics Studied by This Researcher:</h4>
                              {researcherList.topics.map((topic, ind) => (
                                  <Button
                                      type="button"
                                      className="topic"
                                      variant="secondary"
                                      onClick={submitSearch(topic)}
                                  >
                                      {topic}
                                  </Button>
                              ))}
                          </div>
                      </div>
                  ),
                  tabEventKey: "researcher",
              },
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
        <ChakraProvider>
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
                            <Tabs variant="enclosed" colorScheme="green">
                                <TabList>
                                    <Tab
                                        _selected={{
                                            color: "white",
                                            bg: "#387DFF",
                                        }}
                                    >
                                        Full Description
                                    </Tab>
                                    <Tab
                                        _selected={{
                                            color: "white",
                                            bg: "#387DFF",
                                        }}
                                    >
                                        Additional Criteria
                                    </Tab>
                                    <Tab
                                        _selected={{
                                            color: "white",
                                            bg: "#387DFF",
                                        }}
                                    >
                                        All Locations
                                    </Tab>
                                    <Tab
                                        _selected={{
                                            color: "white",
                                            bg: "#387DFF",
                                        }}
                                    >
                                        About the Researcher
                                    </Tab>
                                    <Tab
                                        _selected={{
                                            color: "white",
                                            bg: "#387DFF",
                                        }}
                                    >
                                        Learn More
                                    </Tab>
                                </TabList>
                                <TabPanels>
                                    {modalContent.map((section, i) => (
                                        <TabPanel>{section.content}</TabPanel>
                                    ))}
                                </TabPanels>
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
                                            <Card.Body>
                                                {section.content}
                                            </Card.Body>
                                        </Accordion.Collapse>
                                    </Card>
                                ))}
                            </Accordion>
                        )}
                    </Modal.Body>
                    <Modal.Footer>
                        <Button
                            variant="primary"
                            onClick={closeModal}
                            className="blueBackground"
                        >
                            Close
                        </Button>
                    </Modal.Footer>
                </Modal>
                <form onSubmit={handleSubmit}>
                    <label>Enter name:</label>
                    <input
                        type="text"
                        value={searchResearcherName}
                        onChange={(e) =>
                            setSearchResearcherName(e.target.value)
                        }
                    />
                    <input
                        type="submit"
                        class="button"
                        styyle={{ height: "100%" }}
                    />
                </form>
            </div>
        </ChakraProvider>
    );
}

export default App;
