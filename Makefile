.PHONY: clean build up down bake build-bake

# Task to clean up unnecessary files
clean:
	@echo "Cleaning up unnecessary files..."
	find . -name ".DS_Store" -delete
	find . -name "__pycache__" -type d -exec rm -rf {} +
	@echo "Cleanup completed."

# Task to build Docker images
build: clean
	@echo "Building Docker images..."
	docker-compose build

# Task to bring up Docker Compose services in detached mode
up: build
	@echo "Starting Docker Compose services..."
	docker-compose up --build -d

# Task to stop and remove Docker Compose services
down:
	@echo "Stopping Docker Compose services..."
	docker-compose down

# Task to run Docker Compose Bake
bake:
	@echo "Running Docker Compose Bake..."
	docker compose bake

# Combined task to build and bake
build-bake: build bake
	@echo "Build and Bake completed."
