python -m nuitka --onefile \
    --enable-plugin=pyside6 \
    --include-module=pygments.lexers.python \
    --include-module=pygments.formatters.html \
    main.py

mv main.bin pycodeview