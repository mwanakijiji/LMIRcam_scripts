# LMIRcam_scripts

To rsync the .py files only, run
rsync -vr --include="*/" --include="*.py" --exclude="*" observer@lbti-lmircam:~/Scripts/* .
