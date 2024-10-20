# Makefile

# Variables
FRONTEND_DIR = frontend
BACKEND_DIR = backend
PYTHON_ENV = backend/venv/bin/activate

# Setup commands
install:
	# Set up frontend and backend dependencies
	cd $(FRONTEND_DIR) && npm install
	cd $(BACKEND_DIR) && pip install -r requirements.txt

run-backend:
	# Run the Flask API and the socket server concurrently
	# Activates Python environment in the same command to avoid subshell issues
	. $(PYTHON_ENV) && cd $(BACKEND_DIR) && flask run --host=0.0.0.0 --port=5000 &
	. $(PYTHON_ENV) && cd $(BACKEND_DIR) && python socket_server.py

run-frontend:
	# Run the React app
	cd $(FRONTEND_DIR) && npm start

build-frontend:
	# Build the React app for production
	cd $(FRONTEND_DIR) && npm run build

clean:
	# Clean up node modules and Python cache
	rm -rf $(FRONTEND_DIR)/node_modules
	rm -rf $(BACKEND_DIR)/__pycache__

.PHONY: install run-backend run-frontend build-frontend clean