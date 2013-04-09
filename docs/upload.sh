cp output-site/ado-index.html output-ado-root/index.html
cp ../noting-much-about-ado.pdf output-ado-root/noting-much-about-ado.pdf
rsync -rv --partial --progress output-site/ anaslist@ananelson.com:~/sites/dexy.it/ado/guide
rsync -rv --partial --progress output-ado-root/ anaslist@ananelson.com:~/sites/dexy.it/ado/
