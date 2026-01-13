import sys
import codecs

# Windows UTF-8 Fix
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except AttributeError:
        # Fallback for older Python versions
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def safe_print(msg: str = ""):
    """Prints strings safely, handling potential encoding issues."""
    try:
        print(msg)
    except UnicodeEncodeError:
        try:
            print(msg.encode('utf-8', errors='replace').decode('utf-8'))
        except:
            pass # Last resort
