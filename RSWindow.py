from Foundation import *
from AppKit import *

class RSWindow(NSWindow):
    def initWithContentRect_styleMask_backing_defer_(self, rect, mask, backing, defer):
        self = super(RSWindow, self).initWithContentRect_styleMask_backing_defer_(rect, mask, backing, False)
        self.setMovableByWindowBackground_(False)
        self.setBackgroundColor_(NSColor.clearColor())
        self.setLevel_(NSMainMenuWindowLevel+1)
        self.setOpaque_(False)
        self.setHasShadow_(True)
        self.setExcludedFromWindowsMenu_(True)
        self.setAlphaValue_(1.0)
        self.useOptimizedDrawing_(True)
        return self
    
    def canBecomeKeyWindow(self):
        return True