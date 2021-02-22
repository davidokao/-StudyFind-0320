import logo from "./logo.svg";
import "./App.css";
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
    let [isOpen, setIsOpen, researcherList, setResearcherList] = useState(false);

    const openModal = () => {
        setIsOpen(true);
    };

    const closeModal = () => {
        setIsOpen(false);
    };

    const learnMore = (url) => {
        window.open(url, "_blank");
    };

    const fetchData = () => {
        const requestOptions = {
            method: 'GET',
            headers: {'id': 'Hi'}
        }
        fetch("http://0.0.0.0:8080/list", requestOptions)
        .then(res => res.json())
        .then((result) => {
            // setResearcherList({researcher: result})
            console.log(result)
        })
        .catch((error) => {
            console.log("Error", error)
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
                dialogClassName={"modal-style"}
            >
                <Modal.Header closeButton></Modal.Header>
                <Modal.Body>
                    <Tabs defaultActiveKey="description" className="tabs">
                        <Tab
                            eventKey="description"
                            title="Full Description"
                            tabClassName="tab"
                        >
                            <div class="tab-cont">
                                <h3>Full Description</h3>
                                <p>
                                    Infection with SARS-CoV-2 or severe acute
                                    respiratory syndrome coronarvirus type 2 was
                                    highlighted in December 2019 in the city of
                                    Wuhan in China, responsible for an pandemic
                                    evolution since March 11, 2020. The
                                    infection affects all ages of life, although
                                    affecting children in a very small
                                    proportion of cases. The typical
                                    presentation of the disease combines fever
                                    (98%), cough (76%), myalgia and asthenia
                                    (18%) as well as leukopenia (25%) and
                                    lymphopenia (63%). Upper airway involvement
                                    rare. The main clinical presentation
                                    requiring hospitalization of infected
                                    patients is that of atypical pneumonia which
                                    may require critical care management (27%),
                                    and progress to an acute respiratory
                                    distress syndrome (67%) involving
                                    life-threatening conditions in almost 25% of
                                    patients diagnosed with SARS-CoV-2
                                    infection. Other organ damage have been
                                    reported, mainly concerning kidney damage
                                    (29%) which may require renal replacement
                                    therapy in approximately 17% of patients.
                                    Neurological damage has been very rarely
                                    studied, yet reported in 36% of cases in a
                                    study including patients of varying
                                    severity. Finally, the mortality associated
                                    with this emerging virus is high in patients
                                    for whom critical care management is
                                    necessary, reported in 62% of patients. We
                                    therefore propose a prospective
                                    observational study which aim at reporting
                                    the prevalence of acute encephalopathy at
                                    initial management in Critical/Intensive
                                    care or Neurocritical care , to report its
                                    morbidity and mortality and to identify
                                    prognostic factors.
                                </p>
                            </div>
                        </Tab>
                        <Tab
                            eventKey="criteria"
                            title="Additional Criteria"
                            tabClassName="tab"
                        >
                            <div class="tab-cont">
                                <h3>Additional Criteria</h3>
                                <p>
                                    Inclusion Criteria: Critical/Intensive care
                                    or Neurocritical care admission Admission
                                    for/with acute encephalopathy defined as a
                                    rapidly developing (over less than 4 weeks,
                                    but usually within hours to a few days)
                                    pathobiological process in the brain;
                                    including delirium or subsyndromal (DSM V
                                    definition) or coma (Glasgow coma scale
                                    score &#60; 9) SARS-COV-2 infection
                                    (respiratory or other PCR specimen) Age
                                    &#62;= 18 years Exclusion Criteria: -
                                    Opposition to study participation from the
                                    patient itself or patient surrogate
                                </p>
                            </div>
                        </Tab>
                        <Tab
                            eventKey="Locations"
                            title="All Locations"
                            tabClassName="tab"
                        >
                            <div class="tab-cont">
                                <h3>All Locations</h3>
                                <ul>
                                    <li>
                                        Jackson Memorial Health System;
                                        University of Miami, Miller School of
                                        Medicine, Miami, Florida, United States,
                                        33136 
                                    </li>
                                    <li>
                                        Wellstar Atlanta Medical Center,
                                        Atlanta, Georgia, United States, 30312 
                                    </li>
                                    <li>
                                        Universidade Federal de São Paulo, São
                                        Paulo, Brazil
                                    </li>
                                    <li>
                                        Fundación Valle del Lili, University
                                        Hospital, Cali, Colombia 
                                    </li>
                                    <li>
                                        Cairo University Hospitals, Cairo,
                                        Egypt 
                                    </li>
                                    <li>
                                        Centre Hospitalier d'Argenteuil,
                                        Argenteuil, France 
                                    </li>
                                    <li>
                                        Centre Hospitalier de Beauvais,
                                        Beauvais, France 
                                    </li>
                                    <li>
                                        Centre Hospitalier Universitaire
                                        Ambroise Paré, Boulogne, France 
                                    </li>
                                    <li>
                                        Centre Hospitalier de Bourg en Bresse,
                                        Bourg-en-Bresse, France 
                                    </li>
                                    <li>
                                        Centre Hospitalier Régional
                                        Universitaire de Brest, Brest, France 
                                    </li>
                                    <li>
                                        Centre Hospitalier de Brives,
                                        Brive-la-Gaillarde, France 
                                    </li>
                                    <li>
                                        Centre Hospitalier Universitaire
                                        Beaujon, Clichy, France 
                                    </li>
                                    <li>
                                        Centre Hospitalier Universitaire Louis
                                        Mourier, Colombes, France 
                                    </li>
                                    <li>
                                        Centre Hospitalier Universitaire Henri
                                        Mondor, Créteil, France 
                                    </li>
                                    <li>
                                        Centre hospitalier de Dieppe, Dieppe,
                                        France 
                                    </li>
                                    <li>
                                        Centre Hospitalier Universitaire de
                                        Dijon, Dijon, France 
                                    </li>
                                    <li>
                                        Centre Hospitalier d'Etampes, Etampes,
                                        France 
                                    </li>
                                    <li>
                                        Grand Hôpital de l'Est Francilien - Site
                                        de Marne-la-Vallée, Jossigny, France 
                                    </li>
                                    <li>
                                        Centre Hospitalier de la Roche-sur-Yon,
                                        La Roche-sur-Yon, France 
                                    </li>
                                    <li>
                                        Centre Hospitalier de La Rochelle, La
                                        Rochelle, France 
                                    </li>
                                    <li>
                                        Centre Hospitalier de Versailles, Le
                                        Chesnay, France, 78150
                                    </li>
                                </ul>
                            </div>
                        </Tab>
                        <Tab
                            eventKey="researcher"
                            title="About the Researcher"
                            tabClassName="tab"
                        >
                            <div class="tab-cont">
                                <img
                                    src="https://pbs.twimg.com/profile_images/788793925708423168/UDXKAIsT.jpg"
                                    class="researcher-image"
                                />
                                <div class="researcher-contact">
                                    <h3>About the Researcher</h3>
                                    <p>
                                        <FontAwesomeIcon icon={faUser} />{" "}
                                        Stephane Legriel
                                        <br />
                                        <FontAwesomeIcon
                                            icon={faEnvelope}
                                        />{" "}
                                        neurocovid19study@ictalgroup.org
                                        <br />
                                        <FontAwesomeIcon
                                            icon={faBuilding}
                                        />{" "}
                                        Ictal Group
                                    </p>
                                </div>
                                <div class="content">
                                    <p>Recent Studies From This Researcher:</p>
                                    <ul>
                                        <li>
                                            <u>
                                                Psychological Impact of the
                                                COVID-19 Pandemic on Student
                                                Nurses (StudentCov):
                                            </u>{" "}
                                            SARS-CoV-2 coronavirus has been
                                            spreading rapidly throughout the
                                            world and has put a big strain on
                                            hospitals. Identifying risk factors
                                            of post traumatic stress disorder in
                                            student nurses would allow for the
                                            improvement of training and access
                                            to better psychological care.
                                        </li>
                                        <li>
                                            <u>
                                                Comparison of Scores for Early
                                                Brain Damage Assessment at
                                                Intensive Care Unit Admission
                                                After Out of Hospital Cardiac
                                                Arrest (AfterROSC1):
                                            </u>{" "}
                                            There are many models to determine
                                            the risk of unfavorable outcome
                                            following cardiac arrest, but many
                                            lack external validation. Therefore,
                                            the best model needs to be
                                            determined for appropriate
                                            treatment.
                                        </li>
                                        <li>
                                            <u>
                                                Versailles Hospital Cardiac
                                                Arrest Registry:
                                            </u>{" "}
                                            A registry of patients that
                                            experience cardiac arrest requiring
                                            intensive care unit management.
                                        </li>
                                        <li>
                                            <u>
                                                Posterior Reversible
                                                Encephalopathy Syndrome in the
                                                Critically Ill Patients:
                                            </u>{" "}
                                            A registry of individuals that are
                                            prospective Posterior Reversible
                                            Encephalopathy Syndrome patients.
                                        </li>
                                        <li>
                                            <u>
                                                Status Epilepticus in the
                                                Critically Ill Patients:
                                            </u>{" "}
                                            A registry for individuals that are
                                            prospective Convulsive and
                                            Non-Convulsive Status Epilepticus
                                            and Pseudo Status Epilepticus
                                            patients.
                                        </li>
                                    </ul>
                                </div>
                                <div class="content">
                                    <p>
                                        Common Topics Studied by This
                                        Researcher:
                                    </p>
                                    <Button
                                        type="button"
                                        className="topic"
                                        variant="secondary"
                                    >
                                        Neurological Manifestations Brain
                                        Diseases
                                    </Button>
                                    <Button
                                        type="button"
                                        className="topic"
                                        variant="secondary"
                                    >
                                        Cardiovascular Diseases
                                    </Button>
                                    <Button
                                        type="button"
                                        className="topic"
                                        variant="secondary"
                                    >
                                        Seizures
                                    </Button>
                                    <Button
                                        type="button"
                                        className="topic"
                                        variant="secondary"
                                    >
                                        Status Epilepticus
                                    </Button>
                                    <Button
                                        type="button"
                                        className="topic"
                                        variant="secondary"
                                    >
                                        Nervous System Diseases
                                    </Button>
                                    <Button
                                        type="button"
                                        className="topic"
                                        variant="secondary"
                                    >
                                        Central Nervous System Diseases
                                    </Button>
                                    <Button
                                        type="button"
                                        className="topic"
                                        variant="secondary"
                                    >
                                        Heart Diseases
                                    </Button>
                                    <Button
                                        type="button"
                                        className="topic"
                                        variant="secondary"
                                    >
                                        Pathologic Processes
                                    </Button>
                                </div>
                            </div>
                        </Tab>
                        <Tab
                            eventKey="more"
                            title="Learn More"
                            tabClassName="tab"
                            onClick={closeModal}
                        >
                            <div class="tab-cont">
                                <a
                                    href="https://www.clinicaltrials.gov/ct2/show/NCT04320472"
                                    target="_blank"
                                >
                                    Learn more at ClinicalTrials.gov{" "}
                                    <FontAwesomeIcon icon={faExternalLinkAlt} />
                                </a>
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
            <button
                type="button"
                class="button"
                style={{ height: "100%" }}
                onClick={() => {
                    openModal();
                }}
            >
                Details
            </button>
            <button
                onClick={() => {
                    fetchData()
                }}>
                Fetch Data
            </button>
            {researcherList? researcherList : "None"}
        </div>
    );
}

export default App;
