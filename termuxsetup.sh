apt update && apt upgrade -y
apt install clang python libjpeg-turbo libpng libsodium libffi openssl git python-pillow -y
export SODIUM_INSTALL=system 

pip install -r requirements.txt

exit=$(echo $?)

if [[ $exit == 0 ]]; then 
	echo "Installer been running and installation been successful"
else
	echo "Did something kill it?"
fi

