#!/bin/bash

function email() {
    cd
    cd desktop/projects/EmailLogin
    python3 SignIn.py $1
    cd
}
