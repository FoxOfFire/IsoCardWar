pyenv install 3.12.9
pyenv local 3.12.9
echo "Version set to: $(pyenv exec python --version)"

echo "Creating venv"
pyenv exec python -m venv ./.venv

echo "Activating"
source ./.venv/bin/activate

echo "Installing requirements:"
pyenv exec pip install --upgrade pip
if [ ! -f ./requirements.txt ]; then
	echo "./requirements.txt not found, creating a new one"
	touch ./requirements.txt
fi
pyenv exec pip install -r ./requirements.txt

source .venv/bin/activate

exit 0
