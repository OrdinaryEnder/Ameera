

apt update && apt upgrade -y

apt install clang python libjpeg-turbo libpng libsodium libffi openssl git -y
export SODIUM_INSTALL=system 

arch=$(uname -m)

if [[ $arch == aarch64 ]]; then
    echo "64 bit detected"
    export LDFLAGS="-L/system/lib64"
    pip install -r requirements.txt
elif [[ $arch == arm64 ]]; then
   echo "64 Bit Detected"
   export LDFLAGS="-L/system/lib64"
   pip install -r requirements.txt
else
    pip install -r requirements.txt
fi

exit=$(echo $?)

if [[ $exit == 0 ]]; then 
	echo "Installer been running and installation been successful"
else
	echo "Did something kill it?"
fi

