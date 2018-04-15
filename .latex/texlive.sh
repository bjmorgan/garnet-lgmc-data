# Obtain TeX Live
wget http://mirror.ctan.org/systems/\
texlive/tlnet/install-tl-unx.tar.gz
tar -xzf install-tl-unx.tar.gz
cd install-tl-20*

# Install a minimal system
./install-tl \
  --profile=../.latex/texlive.profile

# Add the TL system to the PATH
PATH=/tmp/texlive/bin/x86_64-linux:$PATH
export PATH
cd ..

# Core requirements for the test system
tlmgr install babel babel-english \
  latex latex-bin latex-fonts \
  latexconfig xetex 
tlmgr install ptex uptex 
tlmgr install collection-latex
tlmgr install type1cm dvipng
