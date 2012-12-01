from Foundation import *
from AppKit import *

class RSSliderCell(NSSliderCell):
    knobImage = NSImage.alloc().initWithContentsOfFile_(NSBundle.mainBundle().pathForResource_ofType_("volumeadjust", "png"))
    barImage =  NSImage.alloc().initWithContentsOfFile_(NSBundle.mainBundle().pathForResource_ofType_("volumebar", "png"))

    def drawKnob_(self, rect):
        knobRect = self.knobImage.size()
        # DEPRECATED
        # point = Foundation.NSMakePoint(rect.origin.x + ((rect.size.width - knobRect.width)/2), rect.origin.y + ((rect.size.height - knobRect.height)/2))
        # self.knobImage.compositeToPoint_operation_(point, 2)
        rect.origin.x = rect.origin.x + ((rect.size.width - knobRect.width)/2)
        rect.origin.y = rect.origin.y + ((rect.size.height - knobRect.height)/2)
        rect.size.width = knobRect.width
        rect.size.height = knobRect.height
        self.knobImage.drawInRect_fromRect_operation_fraction_(rect, Foundation.NSZeroRect, 2, 1)

    def setNeedsDisplayInRect_(self, rect):
        super.setNeedsDisplayInRect_(self.bounds())

    def drawBarInside_flipped_(self, rect, flipped):
        knobRect = self.knobRectFlipped_(0)
        rect.size.height = knobRect.origin.y
        if rect.size.height < 0:
            # First run; knob position not init'd yet.
            rect.size.height = 72
        rect.origin.y = 82 - rect.size.height
        self.barImage.drawInRect_fromRect_operation_fraction_(rect, Foundation.NSZeroRect, 2, 1)

    def drawWithFrame_inView_(self, frame, view):
        self.drawBarInside_flipped_(frame, 0)
        self.drawKnob()
