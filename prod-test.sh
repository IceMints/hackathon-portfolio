#!/bin/bash

# Color Codes
red=`tput setaf 1`
green=`tput setaf 2`
yellow=`tput setaf 3`
purple=`tput setaf 5`
white=`tput setaf 7`
cyan=`tput setaf 6`
reset_color=`tput sgr0`
exitstatus=0

# website data
URL="https://weepingmelon.duckdns.org"
PAGES="/ /blog /health /login /register /profiles/Gigi /projects/Portfolio"
METHODS="GET POST DELETE PUT PATCH"

# Testing endpoints with request methods
echo ${cyan}Testing endpoints with request methods${reset_color}
for PAGE in $PAGES; do
for METHOD in $METHODS; do

GETVAR=$(curl -LI $URL$PAGE -o /dev/null -w '%{http_code}\n' -s -X $METHOD) 
STATCAT=${GETVAR:0:1}
if [[ $STATCAT == 2 ]]; then
echo $PAGE ${white}$METHOD${reset_color} $GETVAR ${green}'SUCCESS'${reset_color}
elif [[ $GETVAR == 418 ]]; then
echo $PAGE ${white}$METHOD${reset_color} $GETVAR ${purple}"I'm a teapot"${reset_color}
elif [[ $GETVAR == 405 ]]; then 
echo $PAGE ${white}$METHOD${reset_color} $GETVAR ${yellow}'METHOD NOT ALLOWED'${reset_color}
else
echo $PAGE ${white}$METHOD${reset_color} $GETVAR ${red}'ERROR'${reset_color}
exitstatus=1
fi
done
done

# Function to post endpoints
testing_endpoint () {
GETVAR=$1
if [[ $GETVAR == $2 ]]; then
echo $GETVAR ${green}'SUCCESS'${reset_color}
else
echo $GETVAR ${red}'ERROR'${reset_color}
exitstatus=2
fi
}

# Testing /register endpoint with post
echo ${cyan}Testing register endpoint ${reset_color}
testing_endpoint "$(curl -sX POST $URL'/register')" "Username is required."

echo ${cyan}Posting to URL with username ${reset_color}
testing_endpoint "$(curl -sX POST -d "username=testing" $URL'/register')" "Password is required."

# Set username to test
USERNAME=test

echo ${cyan}Posting an existing username and password ${reset_color}
testing_endpoint "$(curl -sX POST -d "username=$USERNAME&password=test" $URL'/register')" "User test is already registered."

# Creates a random user to be created
COUNT=$((1 + $RANDOM % 1000000))

echo ${cyan}Posting with new username and password ${reset_color}
testing_endpoint "$(curl -sX POST -d "username=$USERNAME$COUNT&password=test" $URL'/register')" "User $USERNAME$COUNT created successfully"

# Testing /login endpoint with post
echo ${cyan}Posting to /login endpoint ${reset_color}
testing_endpoint "$(curl -sX POST $URL'/login')" "Incorrect username."

echo ${cyan}Posting to /login endpoint with unregister user${reset_color}
testing_endpoint "$(curl -sX POST -d "username=scooby$COUNT" POST $URL'/login')" "Incorrect username."

echo ${cyan}Posting to /login endpoint with register user and empty password${reset_color}
testing_endpoint "$(curl -sX POST -d "username=test" POST $URL'/login')" "Incorrect password."

echo ${cyan}Posting to /login endpoint with registered user and correct password${reset_color}
testing_endpoint "$(curl -sX POST -d "username=test&password=test" POST $URL'/login')" "Login Successful"

exit $exitstatus