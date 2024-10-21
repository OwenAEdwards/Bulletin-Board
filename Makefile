# Makefile

# Variables
FRONTEND_DIR = frontend
BACKEND_DIR = backend
PYTHON_ENV = backend/venv/bin/activate

# Setup commands
install:
	@echo "Setting up frontend and backend dependencies"
	cd $(FRONTEND_DIR) && npm install
	cd $(BACKEND_DIR) && pip install -r requirements.txt

run-backend:
	@echo "Running the Flask API and the socket server concurrently"
	. $(PYTHON_ENV) && cd $(BACKEND_DIR) && flask run --host=0.0.0.0 --port=5000 &
	. $(PYTHON_ENV) && cd $(BACKEND_DIR) && python socket_server.py

run-frontend:
	@echo "Running the React app"
	cd $(FRONTEND_DIR) && npm start

build-frontend:
	@echo "Building the React app for production"
	cd $(FRONTEND_DIR) && npm run build

clean:
	@echo "Cleaning up node modules and Python cache"
	rm -rf $(FRONTEND_DIR)/node_modules
	rm -rf $(BACKEND_DIR)/__pycache__

.PHONY: install run-backend run-frontend build-frontend clean