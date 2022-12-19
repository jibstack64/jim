rm -rf ~/.jim
mkdir ~/.jim
mv ./* ~/.jim
cd ~/.jim
echo "python ~/.jim/jim.py \"\"\$@'\"\"" >> ./jim.sh
chmod +x jim.sh
unlink ~/.local/bin/jim
ln jim.sh ~/.local/bin/jim # change if you want
echo "Installed. Run 'jim -h'."