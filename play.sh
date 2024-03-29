# added by Anaconda2 2018.12 installer
# >>> conda init >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$(CONDA_REPORT_ERRORS=false '/home/jelix/anaconda2/bin/conda' shell.bash hook 2> /dev/null)"
if [ $? -eq 0 ]; then
    \eval "$__conda_setup"
else
    if [ -f "/home/jelix/anaconda2/etc/profile.d/conda.sh" ]; then
        . "/home/jelix/anaconda2/etc/profile.d/conda.sh"
        CONDA_CHANGEPS1=false conda activate base
    else
        \export PATH="/home/jelix/anaconda2/bin:$PATH"
    fi
fi
unset __conda_setup
# <<< conda init <<<

conda deactivate
conda activate py35
python test_record.py
