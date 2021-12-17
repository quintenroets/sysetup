# tutorial: https://medium.com/@anarmammadli/how-to-install-cuda-11-4-on-ubuntu-18-04-or-20-04-63f3dee2099

# setup driver
sudo rm /etc/apt/sources.list.d/cuda*
sudo apt remove -y --autoremove nvidia-cuda-toolkit
sudo apt remove -y --autoremove nvidia-*

# remove previous cuda and config
sudo rm -rf /usr/local/cuda*
sudo apt-get -y purge nvidia*

# update deps
sudo apt-get update
sudo apt-get autoremove
sudo apt-get autoclean

# install cuda11.4
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-ubuntu2004.pin
sudo mv cuda-ubuntu2004.pin /etc/apt/preferences.d/cuda-repository-pin-600
wget https://developer.download.nvidia.com/compute/cuda/11.4.0/local_installers/cuda-repo-ubuntu2004-11-4-local_11.4.0-470.42.01-1_amd64.deb
sudo dpkg -i cuda-repo-ubuntu2004-11-4-local_11.4.0-470.42.01-1_amd64.deb
sudo apt-key add /var/cuda-repo-ubuntu2004-11-4-local/7fa2af80.pub
sudo apt-get update
sudo apt-get -y install cuda
rm $(ls | grep cuda-repo)

# already in bashrc setup
# echo "# set PATH for cuda 11.4 installation \
# if [ -d "/usr/local/cuda-11.4/bin/" ]; then \
#    export PATH=/usr/local/cuda-11.4/bin${PATH:+:${PATH}} \
#    export LD_LIBRARY_PATH=/usr/local/cuda-11.4/lib64:$LD_LIBRARY_PATH \
#    export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH \
# fi
# source ~/.bashrc

# tutorial: https://towardsdatascience.com/installing-tensorflow-gpu-in-ubuntu-20-04-4ee3ca4cb75d?gi=133dc8daf50 

# setup driver
#sudo apt remove -y --purge '^nvidia-.*'
#install nvidia-driver-460
#sudo ubuntu-drivers install
#install nvidia-cuda-toolkit

yes | pip uninstall tensorflow

echo please select most recent version of cuda11.4: cuDNN Library for Linux x86
echo press Enter when ready
# download from https://developer.nvidia.com/rdp/form/cudnn-download-survey
chromium https://developer.nvidia.com/rdp/cudnn-download
read

tar -xvzf $docs/$(ls $docs | grep cudnn)

sudo cp cuda/include/cudnn.h /usr/local/cuda/include/
sudo cp cuda/lib64/libcudnn* /usr/local/cuda/lib64/
sudo chmod a+r /usr/local/cuda/include/cudnn.h /usr/local/cuda/lib64/libcudnn*
rm $docs/$(ls $docs | grep cudnn) # must be in docs and not pwd
rm -r cuda

pip install tensorflow
python3 -c "import tensorflow as tf;print(tf.config.list_physical_devices('GPU'))"
