#!/bin/bash

pyinstaller \
  --hidden-import packaging.version \
  --hidden-import packaging.specifiers \
  --hidden-import packaging.requirements \
  --onefile \
  run.py
