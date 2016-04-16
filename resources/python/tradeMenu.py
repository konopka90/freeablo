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

        self.initMenu()

    def initMenu(self):

        menuHtmlStr = ""
        for i, val in enumerate(self.entries):
            args = val["args"] if "args" in val else ""
            onclick = (val["strFunc"]+"({0})").format(args) if "strFunc" in val else ""
            entryStr = '<span class="trade-menu-entry" id="tradeMenuEntry%05d" onmouseover="%s.setSelected(%05d)" onclick="%s.activate()" style="display:block;">' % (i, self.selfName, i, self.selfName)
            entryStr +=     '<span class="empty-pentagon-left" id="pentagon-left-%05d"></span>' % i
            entryStr +=     '<span class="trade-menu-item-name">%s</span><span class="trade-menu-item-price">%d</span>' % (val["text"], val["price"])
            entryStr +=     '<span class="empty-pentagon-right" id="pentagon-right-%05d"></span>' % i
            entryStr +=     '<span class="trade-menu-item-description">'
            entryStr +=         'armor: 2 dur: 15/15, no required attributes'
            entryStr +=     '</span>'
            entryStr += '</span>'
            entryStr += '<span id="tradeMenuEntrySeparator%05d"></span>' % i
            menuHtmlStr += entryStr

        container = self.doc.GetElementById(self.containerId)
        container.inner_rml = menuHtmlStr

        self.current = -1
        self.setSelected(0, False)

    def deleteEntry(self, num):
        if len(self.entries) > 1 and num != len(self.entries) - 1:
            del self.entries[num]
            self.initMenu()
            if self.onSelect != None:
                self.onSelect(self.doc, 0)


    def getEntryElement(self, num):
        return self.doc.GetElementById('tradeMenuEntry%05d' % num)

    def getLeftPentagon(self, num):
        return self.doc.GetElementById('pentagon-left-%05d' % num)

    def getRightPentagon(self, num):
        return self.doc.GetElementById('pentagon-right-%05d' % num)

    

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
        elem.SetClass('pentagon-left', False)
        elem.SetClass('empty-pentagon-left', True)

        elem = self.getRightPentagon(num)
        elem.SetClass('pentagon-right', False)
        elem.SetClass('empty-pentagon-right', True)

    def activate(self):
        freeablo.playClickButtonSound()
        currentEntry = self.entries[self.current]
        if("func" in currentEntry):
            currentEntry["func"](*currentEntry["args"]) if "args" in currentEntry \
                else currentEntry["func"]()

    def onKeyDown(self, event):
        if event.parameters['key_identifier'] == rocket.key_identifier.DOWN:
            self.setSelected((self.current + 1) % len(self.entries))
            return True
        elif event.parameters['key_identifier'] == rocket.key_identifier.UP:
            self.setSelected((self.current - 1) % len(self.entries))
            return True
        elif event.parameters['key_identifier'] == rocket.key_identifier.RETURN:
            self.activate()
            return True

        return False
