# Homework Crawler for ECE568
  This python program is a simple crawler to help automate information collection of students homework submission in ECE568 at Duke University.

# Prerequisites
  To run this program, you need to make sure you have installed python3 and requests library in your environment. If you are grading homework on a new Linux Environment, install the prerequisites by typing the following commands (Assuming you are using Ubuntu Distro.)
  `sudo apt install -y python3 python3-pip && pip3 install requests`

# Configuration
  This program tries to pull submission information from Duke GitLab via the REST APIs provided by GitLab. For instructors or TAs who are trying to generate submission details, you need to first get your private access token from GitLab and paste that token
  after token entry in the configuration file.

  To get your pricate access token, Log into your Duke Gitlab account, go to `User Settings->Access Tokens`
  Name the application `ece568` and carefully choose the expiration date (End of the semester or class). Then check `api` option in `Scopes` section and click `Create personal access token` to generate the private token. The token will only appear once, so you need to remember it and keep it secretly because any third-party application can be granted with complete read/write access to the API, including all projects on your behalf. So please don't share it with anyone.

  Copy and paste the token sequence you've been given into the token entry in the configuration file. The rest of the configuration keywords are straightforward. Notice that TA names should be separated by comma delimeter without whitespaces. The config file in the repository provides a complete usage example.

# Run
  To run and generate submission details, simply type `./crawler.py`. The crawler will search any configuration file named `config` in the current working directory. You could also have the crawler read a specific configuration file to which you provide by typing `./crawler.py --config <path/to/file>`
  If you run with `./crawler.py -g G`, the crawler will retrive submission information and then clone all the assignments which this TA is in charge of grading from GitLab.

  If you already have the CSV file generated, you could simply run `./pull.sh <path/to/csv> <Name>` to clone the repositories

# Notes
  This crawler combined with the bash script in the same repo may help reduce the work for future instructors and TAs teaching this class. Note that this crawler doesn't try to handle every incorrect usage so it may be buggy if not being used correctly. If you found any issue or bug, welcome to bother me.

