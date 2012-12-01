#
#  RSSimpleAppDelegate.py
#  Cocoa-Python
#
#  Created by Moises Aranas on 3/9/12.
#  Copyright __MyCompanyName__ 2012. All rights reserved.
#

from Foundation import *
from AppKit import *
from objc import IBAction, IBOutlet
from PyObjCTools import AppHelper
import threading
import Queue
import time
import webbrowser

from RSStatusItem import RSStatusItem
from RSWindow import RSWindow
from RSSliderCell import RSSliderCell
import player_controls
try:
    import pyNotificationCenter
except:
    pyNotificationCenter = None

REFRESH_INTERVAL = 5 # 5 second ticks

class RSSimpleAppDelegate(NSObject):
    status_item = None
    main_window = None
    arrow_window = None
    
    main_view = IBOutlet()
    arrow_view = IBOutlet()
    about_view = IBOutlet()
    
    play_button = IBOutlet()
    back_button = IBOutlet()
    next_button = IBOutlet()
    progress_bar = IBOutlet()
    
    song_title = IBOutlet()
    song_info = IBOutlet()
    
    mainmenudummy = IBOutlet()
    
    # volume controls
    volume_popup = IBOutlet()
    volume_control = IBOutlet()
    
    def applicationDidFinishLaunching_(self, sender):
        self.is_running = True
        NSLog("Application did finish launching.")
        self.status_image = NSImage.alloc().initWithContentsOfFile_(NSBundle.mainBundle().pathForResource_ofType_("feed", "png"))
        self.status_image_alt = NSImage.alloc().initWithContentsOfFile_(NSBundle.mainBundle().pathForResource_ofType_("feed-alt", "png"))
        
        self.play_img = NSImage.alloc().initWithContentsOfFile_(NSBundle.mainBundle().pathForResource_ofType_("play", "png"))
        self.pause_img = NSImage.alloc().initWithContentsOfFile_(NSBundle.mainBundle().pathForResource_ofType_("pause", "png"))
        
        frame = Foundation.NSMakeRect(0, 0, NSStatusBar.systemStatusBar().thickness(), 18)
        self.status_item = NSStatusBar.systemStatusBar().statusItemWithLength_(24)
        self.status_item.setHighlightMode_(True)
        self._status_item_view = RSStatusItem.alloc().initWithFrame_controller_(frame, self)
        self._status_item_view.setImage_alt_(self.status_image, self.status_image_alt)
        self.status_item.setTarget_(self._status_item_view)
        self.status_item.setView_(self._status_item_view)
        self.volume_popup.animator().setAlphaValue_(0)
        NSApp.setMainMenu_(self.mainmenudummy)
        NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(REFRESH_INTERVAL, self, "refreshThis", None, YES)
        # hackish way to trigger the first cycle. Make sure this method returns first
        # before running.
        NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(0.5, self, "refreshThis", None, NO)
    
    def displayWindowAtPoint_(self, point):
        screen_width = NSScreen.mainScreen().visibleFrame().size.width
        xpos = point.x
        if point.x + self.main_view.bounds().size.width > screen_width:
            xpos -= (point.x + self.main_view.bounds().size.width - screen_width)
        ypos = point.y - self.main_view.bounds().size.height - 7 # so it will overlap a little
        content_rect = Foundation.NSMakeRect(xpos-(self.main_view.bounds().size.width/2)+11, ypos, self.main_view.bounds().size.width, self.main_view.bounds().size.height)
        self.main_window = RSWindow.alloc().initWithContentRect_styleMask_backing_defer_(content_rect, 0, 2, False)
        arrow_content_rect = Foundation.NSMakeRect(point.x, point.y - 22, self.arrow_view.bounds().size.width, self.arrow_view.bounds().size.height)
        self.arrow_window = RSWindow.alloc().initWithContentRect_styleMask_backing_defer_(arrow_content_rect, 0, 2, False)
        self.arrow_window.contentView().addSubview_(self.arrow_view )
        self.main_window.contentView().addSubview_(self.main_view)
        self.main_window.setDelegate_(self)
        NSApplication.sharedApplication().activateIgnoringOtherApps_(True)
        self.main_window.setFrame_display_(content_rect, False)
        self.main_window.display()
        self.main_window.invalidateShadow()
        self.arrow_window.orderFront_(self)
        self.main_window.makeKeyAndOrderFront_(self)

    def hideWindow(self):
        if self.main_window is not None:
            self.main_window.orderOut_(self)
            self.arrow_window.orderOut_(self)
            
    def windowDidResignKey_(self, notification):
        if self._status_item_view.active:
            self._status_item_view.toggleWindow()
    
    def applicationShouldTerminate_(self, sender):
        NSLog("Application is terminating.")
        return NSTerminateNow
    
    @IBAction
    def quit_(self, arg):
        self.is_running = False
        AppHelper.callAfter(NSApp.terminate_, self)

    @IBAction
    def aboutView_(self, arg):
        self.about_view.center()
        self.about_view.makeKeyAndOrderFront_(self)
        NSApp.activateIgnoringOtherApps_(True)

    @IBAction
    def openGSWeb_(self, arg):
        webbrowser.open("http://www.ganglionsoftware.com")

    @IBAction
    def openIconAuthorWeb_(self, arg):
        webbrowser.open("http://www.pixeden.com/")

# Player controls
    @IBAction
    def playPause_(self, arg):
        player_controls.playpause()
        if player_controls.is_playing():
            self.play_button.setImage_(self.pause_img)
        else:
            self.play_button.setImage_(self.play_img)
        player_controls.hide_itunes()

    @IBAction
    def next_(self, arg):
        player_controls.next_track()
        self.refreshThis()

    @IBAction
    def back_(self,arg):
        player_controls.back_track()
        self.refreshThis()

    @IBAction
    def seek_(self, arg):
        player_controls.set_player_position(self.progress_bar.intValue())
        self.refreshThis()
    
# Volume controls
    @IBAction
    def volumePop_(self,arg):
        vol = player_controls.get_volume_percent()
        self.volume_control.setIntValue_(vol)
        alpha = 0
        if self.volume_popup.alphaValue() == 0:
            alpha = 1
        self.volume_popup.animator().setAlphaValue_(alpha)
        self.volume_control.setEnabled_(alpha)
        self.volume_control.setNeedsDisplay()

    @IBAction
    def volumeSet_(self, arg):
        player_controls.set_volume_percent(self.volume_control.intValue())
        self.volume_control.setNeedsDisplay()

# Progress/state updater
    def refreshThis(self):
        if player_controls.is_playing():
            self.play_button.setImage_(self.pause_img)
        else:
            self.play_button.setImage_(self.play_img)
        self.progress_bar.setIntValue_(player_controls.get_player_position())
        curr_track = player_controls.get_current_track()
        song_title = curr_track[1] or '(unknown title)'
        song_artist = curr_track[0] or '(unknown artist)'
        song_album = curr_track[2] or '(unknown album)'
        self.song_title.setStringValue_(song_title)
        self.song_info.setStringValue_("%s - %s" % (song_artist, song_album))
        self.song_title.setNeedsDisplay()
        self.song_info.setNeedsDisplay()
        self.volume_control.setNeedsDisplay()
