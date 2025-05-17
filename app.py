from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import logging
from datetime import datetime

db = SQLAlchemy()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('metadata_service.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cMetadata = db.Column(db.JSON, nullable=False)

    def __repr__(self):
        return f"File('{self.id}')"

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app) 

    @app.route('/metadata/<int:fileID>', methods=['POST', 'GET'])
    def metadataFunc(fileID):
        #post
        if request.method == 'POST':
            logger.info(f"Received POST request for file ID: {fileID}")
            data = request.get_json()
            if not data or 'metadata' not in data:
                logger.error(f"Invalid POST request - missing data or metadata for file ID: {fileID}")
                return jsonify({"error": "Data or metadata Missing"}), 400
            
            file = File.query.get(fileID)
            if file:
                logger.info(f"Updating metadata for existing file ID: {fileID}")
                file.cMetadata = data['metadata']
                db.session.commit()
                return jsonify({"message": "Metadata updated successfully", "id": fileID}), 200
            else:
                logger.info(f"Creating new file entry with ID: {fileID}")
                new_file = File(id=fileID, cMetadata=data['metadata'])
                db.session.add(new_file)
                db.session.commit()
                return jsonify({"message": "Metadata added successfully", "id": fileID}), 201

        #Get
        elif request.method == 'GET':
            logger.info(f"Received GET request for file ID: {fileID}")
            file = File.query.get(fileID)
            if file:
                logger.info(f"Successfully retrieved metadata for file ID: {fileID}")
                return jsonify(file.cMetadata)
            else:
                logger.warning(f"File not found for ID: {fileID}")
                return jsonify({"error": "File not found"}), 404
        else:
            logger.error(f"Invalid method {request.method} received for file ID: {fileID}")
            return jsonify({"error": "Method not allowed"}), 405

    with app.app_context():
        db.create_all() # Create tables if they don't exist

    return app

if __name__ == '__main__':
    app_instance = create_app() 
    app_instance.run(debug=True, port=5004)