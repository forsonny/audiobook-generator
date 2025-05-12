#!/bin/bash

# ANSI color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Function to print error messages
print_error() {
    echo -e "${RED}${BOLD}ERROR:${NC} $1"
}

# Function to print success messages
print_success() {
    echo -e "${GREEN}${BOLD}SUCCESS:${NC} $1"
}

# Print header
echo -e "${BLUE}${BOLD}==================================================="
echo -e "   Audiobook Generator - Application Launcher"
echo -e "===================================================${NC}"
echo ""
echo "Starting the application..."
echo "This will launch both the backend and frontend services."
echo ""

# Check for Python
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed or not in the PATH."
    print_error "Please install Python 3.8 or newer and try again."
    exit 1
fi

# Check for Node.js
if ! command -v node &> /dev/null; then
    print_error "Node.js is not installed or not in the PATH."
    print_error "Please install Node.js v16+ and try again."
    exit 1
fi

# Check for npm
if ! command -v npm &> /dev/null; then
    print_error "npm is not installed or not in the PATH."
    print_error "Please install Node.js with npm and try again."
    exit 1
fi

print_success "All dependencies found! Starting application..."
echo ""
echo "Press Ctrl+C to stop all services."
echo ""

# Start the application
npm run start:all

# If it fails, offer troubleshooting
if [ $? -ne 0 ]; then
    echo ""
    echo "Application failed to start properly."
    echo ""
    echo "Troubleshooting options:"
    echo "1. Start backend only (for debugging)"
    echo "2. Start frontend only (if backend is already running)"
    echo "3. Exit"
    echo ""
    read -p "Choose an option (1-3): " option
    
    case $option in
        1)
            echo "Starting backend only..."
            npm run start:backend-only
            ;;
        2)
            echo "Starting frontend only..."
            npm run start:frontend-only
            ;;
        3)
            ;;
        *)
            echo "Invalid option. Exiting."
            ;;
    esac
fi

echo ""
echo "Thank you for using Audiobook Generator!"
echo "" 