python-import-analyzer
======================

Analyzes a python project and produces a count of all the root imports used.

eg: 
```python
import os
import re
import re
from datetime import date
```

Will return
```
os, 1
re, 1
datetime, 1
```
