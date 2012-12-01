#
#  RSStatusItem.py
#  Cocoa-Python
#
#  Created by Moises Aranas on 3/9/12.
#  Copyright __MyCompanyName__ 2012. All rights reserved.
#

from Foundation import *
from AppKit import *

class RSStatusItem(NSView):
    image = None
    alt_image = None
    controller = None
    active = False

    def initWithFrame_controller_(self, frame, controller):
        ret = RSStatusItem.alloc().initWithFrame_(frame)
        ret.controller = controller
        return ret

    def setImage_alt_(self, image, alt_image=None):
        self.image = image
        self.alt_image = alt_image

    def drawRect_(self, rect):
        if self.image != None:
            zero_point = Foundation.NSPoint()
            zero_point.y = (NSStatusBar.systemStatusBar().thickness() - self.image.size().height)/2 + 1
            zero_point.x = 3
            image_to_draw = self.image
            if self.active:
                NSColor.selectedMenuItemColor().set()
                NSRectFill(rect)
                if self.alt_image is not None:
                    image_to_draw = self.alt_image
            image_to_draw.drawAtPoint_fromRect_operation_fraction_(zero_point, Foundation.NSZeroRect,NSCompositeSourceOver, 1)
    
    def toggleWindow(self):
        self.active = not self.active
        if self.active:
            frame = self.window().frame()
            point = Foundation.NSMakePoint(Foundation.NSMinX(frame), Foundation.NSMinY(frame))
            self.controller.displayWindowAtPoint_(point)
        else:
            self.controller.hideWindow()
        self.setNeedsDisplay_(True)
            
    def mouseDown_(self, event):
        self.toggleWindow()
            
    def rightMouseDown_(self, event):
        self.toggleWindow()

    def isActive(self):
        return self.active

