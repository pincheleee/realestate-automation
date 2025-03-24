#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Function to print colored messages
print_message() {
    echo -e "${2}${1}${NC}"
}

# Function to check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        print_message "Docker is not running. Please start Docker first." "$RED"
        exit 1
    fi
}

# Function to start the environment
start() {
    print_message "Starting development environment..." "$YELLOW"
    docker-compose up -d
    print_message "Development environment is ready!" "$GREEN"
}

# Function to stop the environment
stop() {
    print_message "Stopping development environment..." "$YELLOW"
    docker-compose down
    print_message "Development environment stopped." "$GREEN"
}

# Function to build and start production environment
prod_up() {
    print_message "Building and starting production environment..." "$YELLOW"
    docker-compose -f docker-compose.prod.yml up --build -d
    print_message "Production environment is ready!" "$GREEN"
}

# Function to stop production environment
prod_down() {
    print_message "Stopping production environment..." "$YELLOW"
    docker-compose -f docker-compose.prod.yml down
    print_message "Production environment stopped." "$GREEN"
}

# Function to show logs
logs() {
    print_message "Showing logs..." "$YELLOW"
    docker-compose logs -f
}

# Function to show logs for a specific service
show_service_logs() {
    if [ -z "$1" ]; then
        print_message "Please specify a service name" "$RED"
        exit 1
    fi
    print_message "Showing logs for $1..." "$YELLOW"
    docker-compose logs -f "$1"
}

# Function to rebuild a specific service
rebuild_service() {
    if [ -z "$1" ]; then
        print_message "Please specify a service name" "$RED"
        exit 1
    fi
    print_message "Rebuilding service $1..." "$YELLOW"
    docker-compose up -d --build "$1"
    print_message "Service $1 rebuilt successfully!" "$GREEN"
}

# Function to show help
show_help() {
    echo "Usage: ./docker.sh [command]"
    echo ""
    echo "Commands:"
    echo "  start    Start the development environment"
    echo "  stop     Stop the development environment"
    echo "  prod-up  Build and start production environment"
    echo "  prod-down Stop production environment"
    echo "  logs     Show logs"
    echo "  logs [service] Show logs for a specific service"
    echo "  rebuild [service] Rebuild a specific service"
    echo "  help     Show this help message"
}

# Main script
check_docker

case "$1" in
    "start")
        start
        ;;
    "stop")
        stop
        ;;
    "prod-up")
        prod_up
        ;;
    "prod-down")
        prod_down
        ;;
    "logs")
        if [ -z "$2" ]; then
            logs
        else
            show_service_logs "$2"
        fi
        ;;
    "rebuild")
        rebuild_service "$2"
        ;;
    "help"|"")
        show_help
        ;;
    *)
        print_message "Unknown command: $1" "$RED"
        show_help
        exit 1
        ;;
esac 