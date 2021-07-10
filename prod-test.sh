#!/bin/bash

# Color Codes
# red=`tput setaf 1`
# green=`tput setaf 2`
# yellow=`tput setaf 3`
# purple=`tput setaf 5`
# white=`tput setaf 7`
# cyan=`tput setaf 6`
# reset_color=`tput sgr0`
exitstatus=0

# website data
URL="https://weepingmelon.duckdns.org"
PAGES="/ /blog /health /login /register /profiles/Gigi /projects/Portfolio"
METHODS="GET POST DELETE PUT PATCH"

# Testing endpoints with request methods
echo Testing endpoints with request methods
for PAGE in $PAGES; do
for METHOD in $METHODS; do

GETVAR=$(curl -LI $URL$PAGE -o /dev/null -w '%{http_code}\n' -s -X $METHOD) 
if [ $GETVAR == 2.* ]; then
echo $PAGE $METHOD $GETVAR'SUCCESS'
elif [ $GETVAR == 418 ]; then
echo $PAGE $METHOD $GETVAR "I'm a teapot"
elif [ $GETVAR == 405 ]; then 
echo $PAGE $METHOD $GETVAR 'METHOD NOT ALLOWED'
else
echo $PAGE $METHOD $GETVAR 'ERROR'
exitstatus=1
fi
done
done

# Function to post endpoints
testing_endpoint () {
GETVAR=$1
if [ $GETVAR == $2 ]; then
echo $GETVAR 'SUCCESS'
else
echo $GETVAR 'ERROR'
exitstatus=2
fi
}

# Testing /register endpoint with post
echo Testing register endpoint 
testing_endpoint "$(curl -sX POST $URL'/register')" "Username is required."

echo Posting to URL with username 
testing_endpoint "$(curl -sX POST -d "username=testing" $URL'/register')" "Password is required."

# Set username to test
USERNAME=test

echo Posting an existing username and password 
testing_endpoint "$(curl -sX POST -d "username=$USERNAME&password=test" $URL'/register')" "User test is already registered."

# Creates a random user to be created
COUNT=$((1 + $RANDOM % 1000000))

echo Posting with new username and password 
testing_endpoint "$(curl -sX POST -d "username=$USERNAME$COUNT&password=test" $URL'/register')" "User $USERNAME$COUNT created successfully"

# Testing /login endpoint with post
echo Posting to /login endpoint 
testing_endpoint "$(curl -sX POST $URL'/login')" "Incorrect username."

echo Posting to /login endpoint with unregister user
testing_endpoint "$(curl -sX POST -d "username=scooby$COUNT" POST $URL'/login')" "Incorrect username."

echo Posting to /login endpoint with register user and empty password
testing_endpoint "$(curl -sX POST -d "username=test" POST $URL'/login')" "Incorrect password."

echo Posting to /login endpoint with registered user and correct password
testing_endpoint "$(curl -sX POST -d "username=test&password=test" POST $URL'/login')" "Login Successful"

exit $exitstatus