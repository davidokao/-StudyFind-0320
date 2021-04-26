# StudyFind-0320
Junior Design project

*Release Notes Version 1.0.0*
* New software features for this release:
  * Created PubMed and Google Scholar web scrappers
  * Researcher profile generation from scrapped results
* Known bugs and defects:
  * The information pulled from PubMed and GoogleScholar may not be consistent if there are multiple authors with the same name. However, most information will be pulled from PubMed and fallback to GoogleScholar if needed.

*Install Guide:*
* Pre-requisites:
  * MacOS preferred
* Dependent libraries that must be installed:
  * Axios
  * Bootstrap
  * Chakra-ui
  * Firebase admin
  * Flask
  * Font-awesome
  * Framer-motion
  * Nltk
  * Node.js
  * React
  * React-bootstrap
  * React-dom
  * React-modal
  * React-native-elements
  * React-scripts
  * Requests
  * Selenium
  * Web-vitals
* Download instructions. Run the following commands on the terminal when in the project directory:
  * pip3 install -r requirements.txt
  * brew install node
  * npm install
* Installation of actual application:
  * git clone https://github.com/davidokao/StudyFind-0320.git
* Run instructions (what does the user/customer have to do to get the software to execute?):
  * npm start
* Troubleshooting:
  * I’m having CORS issue on my web browser. What should I do?
    * The app is not production code, so it has some networking hiccups. You can download CORS Unblock from Google Chrome to bypass this temporarily.
