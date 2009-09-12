#!/usr/bin/env python

import os
import sys

if __name__ == '__main__':
    PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    HURRICANE_ROOT = os.path.abspath(os.path.join(PROJECT_ROOT, '../../hurricane'))

    sys.path.append(PROJECT_ROOT)
    sys.path.append(HURRICANE_ROOT)

    from hurricane.runner import main
        
    import settings

    main(settings)