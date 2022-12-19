rm -rf ~/.jim
cp ./* ~/.jim
unlink ~/.local/bin/jim
cd ~/.jim; ln jim.sh ~/.local/bin/jim
chmod +x ~/jim.sh
echo "Done."