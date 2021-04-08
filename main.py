# Required Imports
import os
import sys
from flask import Flask, request, jsonify
from firebase_admin import credentials, firestore, initialize_app
from research import generate_researcher, generate_article_and_tags
from googleScholar import getResearcherURL, getResearcherProfile

# Initialize Flask App
app = Flask(__name__)

# Initialize Firestore DB
cred = credentials.Certificate('key.json')
default_app = initialize_app(cred)
db = firestore.client()
todo_ref = db.collection('Researchers')


@app.route('/add', methods=['POST'])
def create():
    """
        create() : Add document to Firestore collection with request body
        Ensure you pass a custom ID as part of json body in post request
        e.g. json={'id': '1', 'title': 'Write a blog post'}
    """
    print('hi')
    try:
        researcher_name = request.json['name']
        researcher_email = request.json['email'] if request.json['email'] != "" else None
        researcher_organization = request.json['organization'] if request.json['organization'] != "" else None
        # attempt to get researcher profile by name
        doc = todo_ref.document(researcher_name).get().to_dict()
        if doc is None:
            print('Scraped')
            print(researcher_name, researcher_email, researcher_organization)
            profile = generate_researcher(name=researcher_name, email=researcher_email, org=researcher_organization)
            # profile['topics'] == "None"
            # profile['studies'] == "None"
            print(profile)
            print(profile['studies'])
            print(profile['studies'] == "None")
            if profile['studies'] == "None":
                print('scholar')
                link = getResearcherURL(researcher_name)
                print(link)
                if link != 'no valid researcher found':
                    profile = getResearcherProfile(link)
                else:
                    return jsonify(profile), 200
            # only add to firebase if valid response
            print("before firebase")
            todo_ref.document(researcher_name).set(profile)
            print("updated firebase")
            return jsonify(profile), 200
        else:
            print('Didn\'t scrape')
            return jsonify(doc), 200

    except Exception as e:
        return f"An Error Occured: {e}"


@app.route('/list', methods=['GET'])
def read():
    """
        read() : Fetches documents from Firestore collection as JSON
        todo : Return document that matches query ID
        all_todos : Return all documents
    """
    try:
        todo_id = request.args.get('id')    
        if todo_id:
            todo = todo_ref.document(todo_id).get()
            return jsonify(todo.to_dict()), 200
        else:
            all_todos = [doc.to_dict() for doc in todo_ref.stream()]
            return jsonify(all_todos), 200
    except Exception as e:
        return f"An Error Occured: {e}"


@app.route('/update', methods=['POST', 'PUT'])
def update():
    """
        update() : Update document in Firestore collection with request body
        Ensure you pass a custom ID as part of json body in post request
        e.g. json={'id': '1', 'title': 'Write a blog post today'}
    """
    try:
        id = request.json['id']
        todo_ref.document(id).update(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"


@app.route('/delete', methods=['GET', 'DELETE'])
def delete():
    """
        delete() : Delete a document from Firestore collection
    """
    try:
        todo_id = request.args.get('id')
        todo_ref.document(todo_id).delete()
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"


port = int(os.environ.get('PORT', 8080))
if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=port)