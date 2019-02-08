#!/bin/bash
git_repos=$(cat $1 | grep $2 | cut -d',' -f5)
for repo in $git_repos:
do
    git clone $repo
done
