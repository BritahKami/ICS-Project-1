# Modules
import traceback
from datetime import datetime


# Terminal Messaging Formatting
def message(text):

    #Error Types
    if text == 'err':
        message = f"\n***\n[CRITICAL ERROR]...Try again later\n***\n"
    elif text == 'x':
        message = f"\n***\n[SYSTEM IS CLOSING]...Goodbye\n***\n"
    else:
        message = f"\n***\n{text}\n***\n"

    print(message)

# Logging Timestamp
def timestp():
    now = datetime.now()
    return now.strftime("%d-%m-%Y %H:%M:%S")

# Error Details Extractor
def error(e):

    # Extracting Error Type
    err_type = type(e).__name__

    # Extracting Error Message
    err_msg = str(e)

    # Extracting Last Traceback Entry
    tb = traceback.extract_tb(e.__traceback__)[-1]

    # Extracting Error Source File
    filename = tb.filename

    # Extracting Error Line of Origin
    line_no = tb.lineno

    # Formatting Error Details
    error_details = (
        f"Type:\n{err_type}\n\n"
        f'Error Message:\n{err_msg}\n\n'
        f"Origin:\n{filename}\n\n"
        f"Line:\n{line_no}"
    )

    # Return Error Details
    return error_details

# Error Handler
def errhandler(e, logger):

    # Capturing Time of Occurence
    time_str = timestp()

    # Capturing Error Details
    error_details = error(e)

    # Logging Errors
    with open(f'logs/errors/{logger}.txt', 'a') as f:
        f.write(f'***\n--------------------------------------------------\nTIME OF OCCURENCE:---\n{time_str}\n\nERROR DETAILS:---\n{error_details}\n---\n--------------------------------------------------\n\n')

    # Output
    message('err')

# Logging System Messages
def syshandler(msg, logger):

    # Capturing Time of Occurence
    time_str = timestp()

    # Logging Message
    with open(f'logs/system/{logger}.txt', 'a') as f:
        f.write(f'***\n--------------------------------------------------\nTIME OF ENTRY:---\n{time_str}\n\nMESSAGE:---\n{msg}\n---\n--------------------------------------------------\n\n')