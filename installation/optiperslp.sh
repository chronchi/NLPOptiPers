# steps to install optisperslp in a cluster

# install cgal
bash cgal.sh

# install glpk
wget https://ftp.gnu.org/gnu/glpk/glpk-4.65.tar.gz
tar xf glpk-4.65.tar.gz
cd glpk-4.65
./configure --prefix=$HOME/.local/
make
make install

# install optiperslp
wget https://bitbucket.org/remere/optiperslp/downloads/optiperslp-1.2.1.tar.gz
tar xf optiperslp-1.2.1.tar.gz
cd optiperslp-1.2.1
export LD_LIBRARY_PATH=$HOME/.local/lib64/
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$HOME/.local/lib/
export LD_LIBRARY=$HOME/.local/lib64/
export LD_LIBRARY=$LD_LIBRARY:$HOME/.local/lib/
export CPATH=$HOME/.local/include/
./configure --prefix=$HOME/.local/
make
make check
make install
