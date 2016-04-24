import rocket
import freeablo

class TradeMenu(object):
    """
    Class for representing rml menus, which are lists of entries that can be selected with the keyboard,
    or clicked with the mouse. For an example of usage, see resources/gui/pausemenu.rml.
    """

    def __init__(self, doc, selfName, containerId, entries, onSelect=None):
        """
        Arguments:
        doc -- The rocket.Document instance to operate on.
        selfName -- The name by which this instance can be referred to from rml.
            Needed to access members from rml callbacks, eg: <span id="..." onclick="selfName.setSelected(...
        containerId -- The id of the element within which to place the menu rml
        entries -- A list of dicts, each one containing the following fields:
            text -- Mandatory. The text for this entry
            func -- Optional. The function to be called when a user presses return with this entry hilighted
            textFunc -- Optional. The function to be called (without () at the end) when a user clicks on 
                the entry. Must be accessible from within the scope of rml callbacks. 
                Required for similar reasons to the selfName field above
        fmtSelected -- The format for rml for entries when they are selected. Must contain %s somewhere, which
            will be replaced with entry.text for each entry.
        fmtNotSelected -- Same as above, but for unselected entries.
        onSelect -- Callback function when user selects menu entry
        """

        self.doc = doc
        self.entries = entries
        self.containerId = containerId
        self.selfName = selfName
        self.onSelect = onSelect
        self.maximumVisible = 4
        self.visibleIndexStart = 0;
        self.visibleIndexStop = len(self.entries) - 1
        if self.visibleIndexStop > self.maximumVisible - 1:
            self.visibleIndexStop = self.maximumVisible - 1

        self.initMenu()
        self.current = -1
        self.setSelected(0, False)

    def initMenu(self):

        i = -1
        menuHtmlStr = ""
        for id, val in enumerate(self.entries):
            i = i + 1
            if i < self.visibleIndexStart or i > self.visibleIndexStop:
                continue

            args = val["args"] if "args" in val else ""
            onclick = (val["strFunc"]+"({0})").format(args) if "strFunc" in val else ""
            entryStr = '<span class="trade-menu-entry" id="tradeMenuEntry%05d" onmouseover="%s.mouseover(%05d)" onclick="%s.activate()" style="display:block;">' % (id, self.selfName, id, self.selfName)
            entryStr +=     '<span class="empty-pentagon-left" id="pentagon-left-%05d"></span>' % id
            entryStr +=     '<span class="trade-menu-item-name">%s</span><span class="trade-menu-item-price">%d</span>' % (val["text"], val["price"])
            entryStr +=     '<span class="empty-pentagon-right" id="pentagon-right-%05d"></span>' % id
            entryStr +=     '<span class="trade-menu-item-description">'
            entryStr +=         'armor: 2 dur: 15/15, no required attributes'
            entryStr +=     '</span>'
            entryStr += '</span>'
            entryStr += '<span id="tradeMenuEntrySeparator%05d"></span>' % id
            menuHtmlStr += entryStr

        container = self.doc.GetElementById(self.containerId)
        container.inner_rml = menuHtmlStr

    def mouseover(self, num):
        print "mouse over %d" % num
        self.setSelected(num)


    def deleteEntry(self, num):
        if num < len(self.entries):
            del self.entries[num]
            self.initMenu()
            if self.onSelect != None:
                self.onSelect(self.doc, 0)

            self.onDeleteEntrySetSelected(num)

    def getEntryElement(self, num):
        return self.doc.GetElementById('tradeMenuEntry%05d' % num)

    def getLeftPentagon(self, num):
        return self.doc.GetElementById('pentagon-left-%05d' % num)

    def getRightPentagon(self, num):
        return self.doc.GetElementById('pentagon-right-%05d' % num)

    def onDeleteEntrySetSelected(self, num):
        elem = self.getLeftPentagon(num)

        if elem != None:
            elem.SetClass('pentagon-left', True)
            elem.SetClass('empty-pentagon-left', False)

            elem = self.getRightPentagon(num)
            elem.SetClass('pentagon-right', True)
            elem.SetClass('empty-pentagon-right', False)

            self.current = num

    def setSelected(self, num, playSound=True):
        if self.current != num:
            if playSound:
                freeablo.playSound("sfx/items/titlemov.wav")

            if self.current != -1:
                self.setNotSelected(self.current)
                if self.onSelect != None:
                    self.onSelect(self.doc, num)

            elem = self.getLeftPentagon(num)
            elem.SetClass('pentagon-left', True)
            elem.SetClass('empty-pentagon-left', False)

            elem = self.getRightPentagon(num)
            elem.SetClass('pentagon-right', True)
            elem.SetClass('empty-pentagon-right', False)

            self.current = num

    
    def setNotSelected(self, num):

        elem = self.getLeftPentagon(num)
        if elem != None:
            elem.SetClass('pentagon-left', False)
            elem.SetClass('empty-pentagon-left', True)

            elem = self.getRightPentagon(num)
            elem.SetClass('pentagon-right', False)
            elem.SetClass('empty-pentagon-right', True)

    def activate(self):
        freeablo.playClickButtonSound()
        currentEntry = self.entries[self.current]

        self.deleteEntry(self.current)

        #if("func" in currentEntry):
        #    currentEntry["func"](*currentEntry["args"]) if "args" in currentEntry \
        #        else currentEntry["func"]()

    def moveDown(self):
        if self.current + 1 > self.visibleIndexStop and self.visibleIndexStop + 1 < len(self.entries):
            self.visibleIndexStart = self.visibleIndexStart + 1
            self.visibleIndexStop = self.visibleIndexStop + 1
            self.initMenu()

        if self.current + 1 < len(self.entries):
            self.setSelected(self.current + 1)

    def moveUp(self):
        if self.current - 1 < self.visibleIndexStart and self.visibleIndexStart - 1 >= 0:
            self.visibleIndexStart = self.visibleIndexStart - 1
            self.visibleIndexStop = self.visibleIndexStop - 1
            self.initMenu()

        if self.current - 1 >= 0:
            self.setSelected(self.current - 1)


    def onKeyDown(self, event):
        if event.parameters['key_identifier'] == rocket.key_identifier.DOWN:
            self.moveDown()
            return True

        elif event.parameters['key_identifier'] == rocket.key_identifier.UP:
            self.moveUp()
            return True

        elif event.parameters['key_identifier'] == rocket.key_identifier.RETURN:
            self.activate()
            return True

        return False
