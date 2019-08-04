mkdir cgalinstallation
cd cgalinstallation

# install cmake
wget https://github.com/Kitware/CMake/releases/download/v3.13.3/cmake-3.13.3.tar.gz
tar -xvzf cmake-3.13.3.tar.gz
cd cmake-3.13.3
./bootstrap --prefix=$HOME/.local/
make
make install

# install boost
cd ..
wget https://dl.bintray.com/boostorg/release/1.69.0/source/boost_1_69_0.tar.gz
tar -xvzf boost_1_69_0.tar.gz
cd boost_1_69_0
./bootstrap.sh --prefix=$HOME/.local/
./b2 install

# install gmp
cd ..
wget https://ftp.gnu.org/gnu/gmp/gmp-6.1.2.tar.xz
tar xf gmp-6.1.2.tar.xz
cd gmp-6.1.2
./configure --prefix=$HOME/.local/
make
make install

# install Motif 
cd ..
wget https://sourceforge.net/projects/motif/files/Motif%202.3.8%20Source%20Code/motif-2.3.8.tar.gz
tar xf motif-2.3.8.tar.gz
cd motif-2.3.8
./configure --prefix=$HOME/.local
make
make install

# install Geomview
cd ..
#wget https://osdn.net/projects/sfnet_geomview/downloads/geomview/1.9.5/geomview-1.9.5.tar.gz
tar xf geomview-1.9.5.tar.gz
cd geomview-1.9.5
./configure --prefix=$HOME/.local/ --with-motif=$HOME/.local
make
make install

# install Eigen
cd ..
wget http://bitbucket.org/eigen/eigen/get/3.3.7.tar.bz2
tar -xvf 3.3.7.tar.bz2
mv eigen-eigen-323c052e1731/ eigen-3.3.7
mkdir eigen
cd eigen
cmake -DCMAKE_INSTALL_PREFIX=$HOME/.local/ ../eigen-3.3.7
make
make install


# install mpfr
cd ..
wget https://www.mpfr.org/mpfr-current/mpfr-4.0.1.tar.xz
tar xf mpfr-4.0.1.tar.xz
cd mpfr-4.0.1
./configure --prefix=$HOME/.local/ --with-gmp=$HOME/.local/
make
make install

# install cgal
cd ..
wget https://github.com/CGAL/cgal/releases/download/releases%2FCGAL-4.11.3/CGAL-4.11.3.tar.xz
tar xf CGAL-4.11.3.tar.xz
cd CGAL-4.11.3
cmake -DCMAKE_INSTALL_PREFIX=$HOME/.local/ .
make
make install
