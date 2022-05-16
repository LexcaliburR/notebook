
起因：conda自动自动推送的都为gpu版本，但实际上在anaconda.org中查找，是有对应gpu版本的

pytorch 1.9.1 cudatoolkit 11.1 py3.8
conda install -c "pytorch" -c "nvidia" python=3.8 pytorch=1.9.1