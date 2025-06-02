:: activate the conda environment
call conda activate aemntc

:: install PyTorch with CUDA 12.6 support
call pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126
pause