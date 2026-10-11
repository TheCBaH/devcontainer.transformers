import os
import sys


if __name__ == '__main__':
    if os.environ.get('PYTHONHASHSEED') != '0':
        os.execve(sys.executable, [sys.executable, *sys.argv],
                  {**os.environ, 'PYTHONHASHSEED': '0'})
    from hf_pt2_tools.cli import main
    main()
