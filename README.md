## Python script that scrapes the raw data of listed websites into a single spreadsheet cell

## Commit Style

- **feat**: A new feature is introduced with the changes
- **fix**: A bug fix has occurred
- **chore**: Changes that do not relate to a fix or feature and don't modify src or test files (for example updating dependencies)
- **refactor**: Refactored code that neither fixes a bug nor adds a feature
- **docs**: Updates to documentation such as the README or other markdown files
- **style**: Changes that do not affect the meaning of the code, likely related to code formatting such as white-space, missing semi-colons, and so on.
- **test**: Including new or correcting previous tests
- **perf**: Performance improvements
- **ci**: Continuous integration related
- **build**: Changes that affect the build system or external dependencies
- **revert**: Reverts a previous commit

https://cloudbytes.dev/snippets/run-selenium-and-chrome-on-wsl2#step-1-install-wsl2
```shell
#!/usr/bin/bash

echo "Changing to home directory..."
pushd "$HOME"

echo "Update the repository and any packages..."
sudo apt update && sudo apt upgrade -y

echo "Install prerequisite system packages..."
sudo apt install wget curl unzip jq -y

# Set metadata for Google Chrome repository...
meta_data=$(curl 'https://googlechromelabs.github.io/chrome-for-testing/'\
'last-known-good-versions-with-downloads.json')


echo "Download the latest Chrome binary..."
wget $(echo "$meta_data" | jq -r '.channels.Stable.downloads.chrome[0].url')

echo "Install Chrome dependencies..."
sudo apt install ca-certificates fonts-liberation \
    libappindicator3-1 libasound2 libatk-bridge2.0-0 libatk1.0-0 libc6 \
    libcairo2 libcups2 libdbus-1-3 libexpat1 libfontconfig1 libgbm1 \
    libgcc1 libglib2.0-0 libgtk-3-0 libnspr4 libnss3 libpango-1.0-0 \
    libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 libxcb1 \
    libxcomposite1 libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 \
    libxrandr2 libxrender1 libxss1 libxtst6 lsb-release wget xdg-utils -y


echo "Unzip the binary file..."
unzip chrome-linux64.zip


echo "Downloading latest Chromedriver..."
wget $(echo "$meta_data" | jq -r '.channels.Stable.downloads.chromedriver[0].url')

echo "Unzip the binary file and make it executable..."
unzip chromedriver-linux64.zip

echo "Install Selenium..."
python3 -m pip install selenium

echo "Removing archive files"
rm chrome-linux64.zip  chromedriver-linux64.zip

popd
```
