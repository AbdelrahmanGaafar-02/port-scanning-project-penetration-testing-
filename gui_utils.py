"""
GUI Utilities Module
"""
from datetime import datetime

class GUILogger:
    """Logger class for GUI output"""
    
    def __init__(self, text_widget):
        """
        Initialize logger
        
        Args:
            text_widget: ScrolledText widget to output to
        """
        self.text_widget = text_widget
        
    def log(self, message, level='info'):
        """Log a message to the GUI"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_msg = f"[{timestamp}] {message}\n"
        
        # Map level to tag
        tag = level
        if level == 'title':
            tag = 'title'
        elif level == 'success':
            tag = 'success'
        elif level == 'warning':
            tag = 'warning'
        elif level == 'error':
            tag = 'error'
        else:
            tag = 'info'
            
        self.text_widget.insert('end', formatted_msg, tag)
        self.text_widget.see('end')


class Colors:
    """Color constants for reference"""
    INFO = 'blue'
    SUCCESS = 'green'
    WARNING = 'orange'
    ERROR = 'red'
    TITLE = 'purple'