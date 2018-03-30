# The nmpccodegen requires the GNU toolchain to compile the generated C code if you want to simulate.

## Tips for windows users
- Install the correct mingw/mingw-64
- [MSYS](http://www.mingw.org/wiki/MSYS) offers an easy way to install mingw/mingw64

## Tips for mac users

## Tips for Linux users
1. When using some Matlab versions the following error appears:
cmake: /usr/local/MATLAB/R2016a/bin/glnxa64/libcurl.so.4: no version information available (required by cmake)
cmake: /usr/local/MATLAB/R2016a/sys/os/glnxa64/libstdc++.so.6: version `GLIBCXX_3.4.18' not found (required by cmake)
cmake: /usr/local/MATLAB/R2016a/sys/os/glnxa64/libstdc++.so.6: version `CXXABI_1.3.9' not found (required by cmake)
cmake: /usr/local/MATLAB/R2016a/sys/os/glnxa64/libstdc++.so.6: version `GLIBCXX_3.4.20' not found (required by cmake)
cmake: /usr/local/MATLAB/R2016a/sys/os/glnxa64/libstdc++.so.6: version `GLIBCXX_3.4.21' not found (required by cmake)
cmake: /usr/local/MATLAB/R2016a/sys/os/glnxa64/libstdc++.so.6: version `GLIBCXX_3.4.21' not found (required by /usr/lib/x86_64-linux-gnu/libjsoncpp.so.1)
cmake: /usr/local/MATLAB/R2016a/sys/os/glnxa64/libstdc++.so.6: version `CXXABI_1.3.8' not found (required by /usr/lib/x86_64-linux-gnu/libicuuc.so.57)

This is due to Matlab using some old version from gcc. 

solution: start matlab as following: "LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libstdc++.so.6 matlab" 